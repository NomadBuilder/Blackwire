# Graph Not Showing - Debug Checklist

## 1. Check Neo4j Connection Status

**In Render Logs (on startup):**
- Look for: `✅ Neo4j connection established to neo4j+s://...`
- If you see: `⚠️ Could not connect to Neo4j` → Connection issue

**Quick Test:**
- Go to Render Dashboard → `blackwire` service → "Logs" tab
- Look at the very first logs when the app starts
- Should see Neo4j connection message

## 2. Verify Environment Variables in Render

**In Render Dashboard → `blackwire` service → "Environment" tab:**

Check these are set correctly:
- ✅ `NEO4J_URI` = `neo4j+s://e4e27046.databases.neo4j.io`
- ✅ `NEO4J_USERNAME` = `neo4j` (NOT `NEO4J_USER`)
- ✅ `NEO4J_PASSWORD` = `Zrw9-8lRlOILYEJb8nTaGkYYNiBL-g2VrWEufgOweWM`

**Common Issues:**
- Wrong variable name (`NEO4J_USER` instead of `NEO4J_USERNAME`)
- Extra spaces in values
- Password mismatch (check Neo4j Aura dashboard)

## 3. Check if Entities Are Being Stored

**After tracing a phone number, check Render Logs for:**
- `📞 Storing phone in Neo4j: value=..., formatted=...`
- `✅ Successfully stored phone ... in Neo4j`
- `⚠️ Failed to store phone ... in Neo4j` (if error)

**If you see storage errors:**
- Check the error message
- Could be connection timeout
- Could be authentication failure
- Could be query syntax error

## 4. Check Neo4j Aura Instance Status

**In Neo4j Aura Dashboard:**
- Go to https://console.neo4j.io
- Check if `blackwire` instance is **RUNNING** (green dot)
- If paused/stopped, start it

**Check Instance Limits:**
- Free tier: 0.5 GB storage
- If storage is full, nodes won't be created

## 5. Verify Phone Format Matching

**The Issue:**
- Phones are stored as: `+15192346539` (E.164 format)
- Search might be using: `5192346539` (10-digit) or `15192346539` (11-digit)

**Check Render Logs for:**
- `🔍 Searching for phones with formats: [...]`
- `📋 Sample phones in database: [...]`
- Compare stored format vs search formats

## 6. Check for Timing Issues

**Possible Issue:**
- Graph is queried immediately after trace
- But Neo4j storage might take a moment
- Retry mechanism should handle this (3 retries, 2s apart)

**Check:**
- Are retries happening? (Look for "Retrying graph fetch" in console)
- Do retries eventually find nodes?

## 7. Test Neo4j Connection Manually

**If you can access Render Shell:**
```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "neo4j+s://e4e27046.databases.neo4j.io",
    auth=("neo4j", "Zrw9-8lRlOILYEJb8nTaGkYYNiBL-g2VrWEufgOweWM")
)

with driver.session() as session:
    # Test connection
    result = session.run("RETURN 1 as test")
    print(list(result))
    
    # Check if any phones exist
    result = session.run("MATCH (n:PhoneNumber) RETURN n.phone, n.formatted LIMIT 5")
    for record in result:
        print(f"Phone: {record['phone']}, Formatted: {record['formatted']}")
```

## 8. Check Neo4j Aura Network Access

**Neo4j Aura Settings:**
- Some Aura instances have IP allowlisting
- Check if your Render IP needs to be allowlisted
- Free tier usually allows all IPs, but check settings

## 9. Check for Query Errors

**In Render Logs, look for:**
- Cypher query syntax errors
- Neo4j timeout errors
- Connection pool errors

## 10. Most Likely Issues (in order):

1. **Neo4j not connected** - Check startup logs for connection message
2. **Wrong environment variable name** - Should be `NEO4J_USERNAME` not `NEO4J_USER`
3. **Password mismatch** - Verify password in Neo4j Aura dashboard
4. **Format mismatch** - Stored format doesn't match search format
5. **Entities not being stored** - Check for storage errors in logs
6. **Neo4j Aura instance paused** - Check Aura dashboard

## Quick Fixes to Try:

1. **Restart Render service** - Sometimes fixes connection issues
2. **Verify environment variables** - Double-check all 3 Neo4j vars
3. **Check Neo4j Aura dashboard** - Ensure instance is running
4. **Clear browser cache** - Sometimes helps with frontend issues

