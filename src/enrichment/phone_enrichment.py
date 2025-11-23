"""Phone number and VOIP provider enrichment."""

import os
import re
import requests
import phonenumbers
from typing import Dict, Optional
from phonenumbers import geocoder, carrier, timezone
from dotenv import load_dotenv

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.rate_limiter import check_rate_limit, record_api_request, get_api_remaining
from src.utils.retry import retry_with_backoff
from src.utils.logger import logger
from src.utils.config import Config

load_dotenv()


def enrich_phone(phone_number: str) -> Dict:
    """
    Enrich a phone number with VOIP provider, carrier, and location data.
    
    Args:
        phone_number: Phone number in E.164 format or any format
        
    Returns:
        Dictionary containing enrichment data
    """
    result = {
        "phone_number": phone_number,
        "formatted": None,
        "country_code": None,
        "country": None,
        "carrier": None,
        "voip_provider": None,
        "is_voip": False,
        "timezone": None,
        "is_valid": False,
        "number_type": None,
        "raw_data": {},
        "errors": []
    }
    
    try:
        # Clean up phone number
        phone_clean = re.sub(r'[\s\-\(\)\.]', '', phone_number.strip())
        
        # Try parsing with different approaches
        parsed = None
        default_regions = ["US", "CA", "GB", "AU", "MX"]  # Common regions to try
        
        # First, try parsing without region (if it has country code)
        try:
            parsed = phonenumbers.parse(phone_number, None)
            if phonenumbers.is_valid_number(parsed):
                # Success!
                pass
            else:
                parsed = None  # Invalid, try other methods
        except phonenumbers.NumberParseException as e:
            # Just try other methods, don't add error yet
            parsed = None
        
        # If parsing failed, try with common default regions
        if not parsed or not phonenumbers.is_valid_number(parsed):
            for region in default_regions:
                try:
                    test_parsed = phonenumbers.parse(phone_number, region)
                    if phonenumbers.is_valid_number(test_parsed):
                        parsed = test_parsed
                        logger.debug(f"Parsed {phone_number} using default region: {region}")
                        break
                except phonenumbers.NumberParseException:
                    continue
        
        # If still not parsed, try with phone number starting with 1 (US/Canada)
        if (not parsed or not phonenumbers.is_valid_number(parsed)) and phone_clean.startswith("1") and len(phone_clean) == 11:
            try:
                # Try as US number
                parsed_us = phonenumbers.parse(phone_number, "US")
                if phonenumbers.is_valid_number(parsed_us):
                    parsed = parsed_us
                else:
                    # Try as Canadian number
                    parsed_ca = phonenumbers.parse(phone_number, "CA")
                    if phonenumbers.is_valid_number(parsed_ca):
                        parsed = parsed_ca
            except phonenumbers.NumberParseException:
                pass
        
        # If still not parsed and starts with common patterns, try adding country code
        if (not parsed or not phonenumbers.is_valid_number(parsed)) and not phone_clean.startswith("+"):
            # Try adding US/Canada country code (1) for 10-digit numbers
            if len(phone_clean) == 10:
                try:
                    test_number = "+1" + phone_clean
                    parsed = phonenumbers.parse(test_number, None)
                    if phonenumbers.is_valid_number(parsed):
                        logger.debug(f"Parsed {phone_number} by adding +1 country code")
                except phonenumbers.NumberParseException:
                    pass
        
        # If number starts with 1 and is 11 digits, it might already have country code
        if (not parsed or not phonenumbers.is_valid_number(parsed)) and phone_clean.startswith("1") and len(phone_clean) == 11:
            try:
                # Try parsing with explicit +1
                test_number = "+" + phone_clean
                parsed = phonenumbers.parse(test_number, None)
                if phonenumbers.is_valid_number(parsed):
                    logger.debug(f"Parsed {phone_number} by adding + to 1-prefixed number")
            except phonenumbers.NumberParseException:
                pass
        
        if parsed and phonenumbers.is_valid_number(parsed):
            result["is_valid"] = True
            result["formatted"] = phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
            result["country_code"] = parsed.country_code
            result["country"] = geocoder.description_for_number(parsed, "en")
            result["carrier"] = carrier.name_for_number(parsed, "en")
            result["timezone"] = timezone.time_zones_for_number(parsed)
            
            # Detect if it's a VOIP number
            number_type = phonenumbers.number_type(parsed)
            result["number_type"] = str(number_type)
            
            # Common VOIP indicators
            voip_indicators = [
                phonenumbers.PhoneNumberType.VOIP,
                phonenumbers.PhoneNumberType.VOICEMAIL
            ]
            
            if number_type in voip_indicators:
                result["is_voip"] = True
                result["voip_provider"] = carrier.name_for_number(parsed, "en") or "Unknown VOIP"
            
            # Try to identify VOIP provider from carrier
            carrier_name = carrier.name_for_number(parsed, "en") or ""
            known_voip_providers = ["Twilio", "Bandwidth", "Vonage", "RingCentral", "Google Voice"]
            
            for provider in known_voip_providers:
                if provider.lower() in carrier_name.lower():
                    result["voip_provider"] = provider
                    result["is_voip"] = True
                    break
        # Only add errors if we couldn't parse successfully
        if not parsed or not phonenumbers.is_valid_number(parsed):
            if not parsed:
                result["errors"].append("Could not parse phone number. Try including country code (e.g., +1 for US/Canada)")
            elif not phonenumbers.is_valid_number(parsed):
                result["errors"].append("Phone number format is invalid")
            else:
                result["errors"].append("Phone number validation failed")
        
        # Enhanced lookup with free APIs
        if result["is_valid"] and result["formatted"]:
            # Try numlookupapi.com (free tier: 100 requests/month)
            api_key = os.getenv("NUMLOOKUP_API_KEY", "")
            if api_key:
                try:
                    numlookup_data = lookup_numlookupapi(result["formatted"], api_key)
                    if numlookup_data:
                        result.update(numlookup_data)
                except:
                    pass  # API lookup failed, continue with basic data
            
            # Try ipapi.com phone lookup FIRST (free tier: 1000 requests/month)
            # Use provided key (default) or check environment variable
            ipapi_key = Config.IPAPI_KEY
            
            if ipapi_key and check_rate_limit("ipapi.com"):
                try:
                    ipapi_data = lookup_ipapi(result["formatted"], ipapi_key)
                    record_api_request("ipapi.com")  # Record successful request
                    if ipapi_data:
                        # Merge data, prefer API results over library results
                        if ipapi_data.get("carrier"):
                            result["carrier"] = ipapi_data["carrier"]
                        if ipapi_data.get("line_type"):
                            line_type = ipapi_data["line_type"].upper()
                            if "VOIP" in line_type:
                                result["is_voip"] = True
                                result["voip_provider"] = ipapi_data.get("carrier") or result.get("voip_provider")
                            result["line_type"] = line_type
                        if ipapi_data.get("country_code"):
                            result["country_code"] = ipapi_data["country_code"]
                        if ipapi_data.get("country_name"):
                            result["country"] = ipapi_data["country_name"]
                        if ipapi_data.get("location"):
                            result["location"] = ipapi_data["location"]
                        if ipapi_data.get("timezone"):
                            result["timezone"] = ipapi_data["timezone"]
                    else:
                        # If ipapi returned None (rate limit, error, etc.), we already have fallback data from phonenumbers
                        remaining = get_api_remaining("ipapi.com")
                        if remaining is not None:
                            logger.debug(f"ipapi.com returned no data, {remaining} requests remaining")
                except Exception as e:
                    # API lookup failed (rate limit, network error, etc.)
                    # Continue with library-based data - this is fine, we have fallback
                    error_msg = str(e)
                    if "rate limit" in error_msg.lower() or "429" in error_msg or "quota" in error_msg.lower():
                        logger.warning(f"ipapi.com rate limit/quota reached for the month, using phonenumbers library fallback")
                    else:
                        logger.debug(f"ipapi.com lookup failed, using fallback: {error_msg}")
                    # Continue with phonenumbers library data (already populated above)
            elif ipapi_key:
                # Rate limited - skip API call
                remaining = get_api_remaining("ipapi.com")
                if remaining is not None and remaining == 0:
                    logger.debug(f"ipapi.com rate limited (0 remaining), using phonenumbers library fallback")
        
    except phonenumbers.NumberParseException as e:
        result["errors"] = [str(e)]
    except phonenumbers.NumberParseException as e:
        error_msg = str(e)
        if "INVALID_COUNTRY_CODE" in error_msg or "Missing or invalid default region" in error_msg:
            result["errors"].append("Invalid or missing country code. Try: +1 for US/Canada, +44 for UK, etc.")
        elif "NOT_A_NUMBER" in error_msg:
            result["errors"].append("Not a valid phone number format")
        else:
            result["errors"].append(f"Phone parsing error: {error_msg}")
        logger.warning(f"Phone parsing failed for {phone_number}: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        result["errors"] = [error_msg]
        logger.error(f"Unexpected error enriching phone {phone_number}: {error_msg}", exc_info=True)
    
    # If we have errors but no formatted number, try to provide helpful guidance
    if result["errors"] and not result["formatted"]:
        # Check if it looks like it might need a country code
        phone_clean = re.sub(r'[\s\-\(\)\.]', '', phone_number.strip())
        if len(phone_clean) == 10 or (len(phone_clean) == 11 and phone_clean.startswith("1")):
            result["errors"].append("💡 Tip: For US/Canada numbers, try adding +1 at the start (e.g., +15198000997)")
    
    return result


def lookup_numlookupapi(phone: str, api_key: str) -> Optional[Dict]:
    """Lookup phone using numlookupapi.com (FREE tier: 100/month)."""
    try:
        url = f"https://api.numlookupapi.com/v1/validate/{phone}"
        params = {"apikey": api_key}
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("valid"):
                return {
                    "carrier": data.get("carrier"),
                    "line_type": data.get("line_type"),  # mobile, landline, voip
                    "country_code": data.get("country_code"),
                    "country_name": data.get("country_name"),
                    "location": data.get("location")
                }
    except Exception as e:
        print(f"NumLookupAPI lookup failed: {e}")
    
    return None


@retry_with_backoff(max_retries=2, base_delay=1.0)
def lookup_ipapi(phone: str, api_key: str) -> Optional[Dict]:
    """
    Lookup phone using ipapi.com (FREE tier: 1000/month).
    Falls back gracefully if rate limited or API fails.
    Includes retry logic for transient failures.
    """
    try:
        url = f"https://ipapi.co/phone/{phone}/json/"
        params = {"key": api_key}
        response = requests.get(url, params=params, timeout=Config.API_TIMEOUT_SECONDS)
        
        # Check for rate limiting (HTTP 429 = Too Many Requests)
        if response.status_code == 429:
            raise Exception(f"ipapi.com rate limit reached (HTTP 429) - monthly quota exhausted")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check for API errors (including rate limits in error response)
            if data.get("error"):
                error_info = data.get("error", {})
                error_msg = error_info.get("info", "Unknown API error")
                # Check for various rate limit indicators
                if any(keyword in error_msg.lower() for keyword in ["rate limit", "quota", "exceeded", "limit reached"]):
                    raise Exception(f"ipapi.com monthly quota exhausted: {error_msg}")
                # Other API errors, return None to use fallback (phonenumbers library)
                return None
            
            # Success - return enriched data
            return {
                "carrier": data.get("carrier"),
                "line_type": data.get("type"),  # mobile, landline, voip
                "country_code": data.get("country_code"),
                "country_name": data.get("country_name"),
                "location": data.get("location"),
                "timezone": data.get("timezone")
            }
        
        # Non-200 status code
        if response.status_code >= 500:
            # Server error - use fallback, don't raise
            return None
            
    except requests.exceptions.Timeout:
        logger.warning(f"ipapi.com timeout for {phone[:10]}..., using fallback data")
        return None
    except requests.exceptions.RequestException as e:
        # Network errors - use fallback
        logger.warning(f"ipapi.com network error for {phone[:10]}..., using fallback data: {e}")
        return None
    except Exception as e:
        # Re-raise rate limit/quota errors so we can log them properly
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in ["rate limit", "quota", "exceeded", "429"]):
            raise e  # This will be caught above and logged
        # Other errors - use phonenumbers library fallback silently
        return None
    
    return None

