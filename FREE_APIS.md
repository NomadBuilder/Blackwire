# Free APIs for BlackWire

## ✅ Currently Integrated (Working Now)

### Domain Enrichment
1. **python-whois library** - ✅ FREE, no API key needed
   - WHOIS data (registrar, creation date, expiration)
   - Already integrated

2. **ip-api.com** - ✅ FREE, no API key needed
   - 45 requests/minute
   - IP location, ISP, ASN, country, city
   - Already integrated

3. **IPLocate.io** - ✅ FREE, no API key needed (basic)
   - IP location and ISP data
   - Fallback if ip-api.com fails
   - Already integrated

4. **DNS lookups (dnspython)** - ✅ FREE, no API key needed
   - A records, MX records, NS records
   - Already integrated

### Phone Enrichment
1. **phonenumbers library** - ✅ FREE, no API key needed
   - Phone parsing, validation, country code
   - Carrier detection (limited)
   - Already integrated

2. **numlookupapi.com** - ✅ FREE tier: 100 requests/month
   - Requires API key (free signup)
   - VOIP detection, carrier, line type
   - Already integrated (optional)

3. **ipapi.com** - ✅ FREE tier: 1000 requests/month
   - Requires API key (free signup)
   - Carrier, line type, location
   - Already integrated (optional)

### Wallet Enrichment
1. **blockchain.info API** - ✅ FREE, no API key needed
   - Bitcoin wallet balance, transaction count
   - Transaction history
   - Already integrated

2. **blockchair.com API** - ✅ FREE tier: 100 requests/hour
   - Multi-currency support (Bitcoin, Ethereum, Litecoin, etc.)
   - No API key required for basic queries
   - Already integrated

3. **etherscan.io API** - ✅ FREE tier: 5 calls/second
   - Ethereum wallet balance and transactions
   - Requires free API key
   - Already integrated (optional)

## 📝 Setup Instructions

### Optional API Keys (Enhance Functionality)

Add these to your `.env` file for enhanced enrichment:

```bash
# Phone Lookup (Optional - enhances phone enrichment)
NUMLOOKUP_API_KEY=your_key_here  # Sign up at numlookupapi.com (free tier: 100/month)
IPAPI_KEY=your_key_here          # Sign up at ipapi.com (free tier: 1000/month)

# Ethereum Lookup (Optional - enhances wallet enrichment)
ETHERSCAN_API_KEY=your_key_here  # Sign up at etherscan.io (free tier: 5 calls/sec)
```

**Note**: All APIs work without keys, but with keys you get:
- More detailed phone carrier/VOIP detection
- Ethereum wallet balance lookups
- Higher rate limits

### Getting Free API Keys

1. **numlookupapi.com**:
   - Visit: https://numlookupapi.com/
   - Sign up (free)
   - Get 100 requests/month free

2. **ipapi.com**:
   - Visit: https://ipapi.com/
   - Sign up (free)
   - Get 1000 requests/month free

3. **etherscan.io**:
   - Visit: https://etherscan.io/apis
   - Sign up (free)
   - Get 5 calls/second free

## 🔍 What Works Right Now (No Setup Required)

### ✅ Fully Functional Without Any API Keys:

1. **Phone Numbers**:
   - ✅ Parse and validate phone numbers
   - ✅ Detect country code and country
   - ✅ Basic carrier detection
   - ✅ VOIP detection (if carrier name matches known providers)

2. **Domains**:
   - ✅ DNS lookups (A, MX, NS records)
   - ✅ IP address resolution
   - ✅ WHOIS lookup (registrar, dates)
   - ✅ IP location and ISP (via ip-api.com)
   - ✅ Shortlink detection

3. **Wallets**:
   - ✅ Bitcoin wallet format validation
   - ✅ Ethereum wallet format validation
   - ✅ **Bitcoin balance and transaction count** (via blockchain.info)
   - ✅ **Multi-currency support** (via blockchair.com)

4. **Messaging Handles**:
   - ✅ Platform detection (WhatsApp, Telegram, Instagram)
   - ✅ Phone number format detection
   - ✅ Username validation

## 📊 API Rate Limits Summary

| API | Rate Limit | Requires Key | Status |
|-----|------------|--------------|--------|
| python-whois | Unlimited | ❌ No | ✅ Working |
| ip-api.com | 45/min | ❌ No | ✅ Working |
| IPLocate.io | Unlimited (basic) | ❌ No | ✅ Working |
| blockchain.info | ~1/sec | ❌ No | ✅ Working |
| blockchair.com | 100/hour | ❌ No | ✅ Working |
| phonenumbers lib | Unlimited | ❌ No | ✅ Working |
| numlookupapi.com | 100/month | ✅ Yes | ⚙️ Optional |
| ipapi.com | 1000/month | ✅ Yes | ⚙️ Optional |
| etherscan.io | 5/sec | ✅ Yes | ⚙️ Optional |

## 🚀 Testing What Works

Try these right now (no API keys needed):

**Phone Number**:
```
+14155552671
+442071838750
```

**Domain**:
```
example.com
google.com
github.com
```

**Bitcoin Wallet**:
```
1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa  # Genesis block
1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2  # Example
```

**Ethereum Wallet**:
```
0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
0xde0B295669a9FD93d5F28D9Ec85E40f4cb697BAe
```

All of these will work with real data right now!

