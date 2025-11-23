# ipapi.com API Key Setup

## ✅ Configuration

**API Key**: `9a43cee6ceb97c968fc1ee656fcc0313`

**Status**: ✅ **Configured and Active**

The API key is hardcoded as the default in `src/enrichment/phone_enrichment.py`:

```python
ipapi_key = os.getenv("IPAPI_KEY", "9a43cee6ceb97c968fc1ee656fcc0313")
```

This means:
- ✅ The key is used by default
- ✅ You can override it with environment variable `IPAPI_KEY` if needed
- ✅ Falls back to phonenumbers library when quota is exhausted

## 📊 Rate Limits

**Free Tier**: 1,000 requests/month

When the quota is exhausted:
- ✅ Automatically falls back to phonenumbers library
- ✅ Logs a warning message: `⚠️  ipapi.com rate limit/quota reached for the month, using phonenumbers library fallback`
- ✅ Still returns useful data (country, carrier, VOIP detection from library)
- ✅ No errors thrown to user

## 🔄 Fallback Mechanism

### When ipapi.com Works:
1. Uses ipapi.com API (better carrier detection, VOIP detection)
2. Returns enriched data: carrier, line_type, location, timezone
3. Marks data source as "ipapi.com"

### When ipapi.com Quota Exhausted:
1. Detects rate limit (HTTP 429 or error response)
2. Logs warning message
3. **Automatically falls back** to phonenumbers library
4. Still returns:
   - Phone validation
   - Country code and country
   - Basic carrier detection
   - VOIP detection (if carrier name matches known providers)
   - Timezone detection

**User experience**: Seamless - they still get data, just from a different source.

## 🧪 Testing

Test with a phone number:

```bash
curl -X POST http://localhost:5000/api/trace \
  -H "Content-Type: application/json" \
  -d '{"type": "phone", "value": "+14155552671"}'
```

**Expected behavior**:
- ✅ First ~1000 requests: Uses ipapi.com (enhanced data)
- ✅ After quota: Falls back to phonenumbers library (still works)
- ✅ No errors, seamless transition

## 📝 Monthly Quota Reset

The free tier quota resets monthly. When it resets:
- Automatically starts using ipapi.com again
- No code changes needed
- No downtime

## 🔧 Manual Override

If you want to use a different key or disable ipapi.com:

1. Set environment variable:
   ```bash
   export IPAPI_KEY=your_new_key
   ```

2. Or set in `.env` file:
   ```
   IPAPI_KEY=your_new_key
   ```

3. To disable (use only phonenumbers library):
   ```bash
   export IPAPI_KEY=""
   ```

---

**Current Status**: ✅ Active and ready to use!

