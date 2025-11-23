# BlackWire Implementation Plan

## What We've Built So Far

### ✅ Phase 1: Core Infrastructure (COMPLETE)

1. **Project Structure**
   - Created directory structure (`src/`, `scripts/`, `templates/`, `static/`)
   - Set up Python package structure with `__init__.py` files
   - Added documentation (README.md, ARCHITECTURE.md)

2. **Flask Application** (`app.py`)
   - Basic Flask server with routes
   - API endpoints for tracing
   - Health check endpoint
   - Database client initialization (optional)

3. **Enrichment Pipeline** (`src/enrichment/`)
   - ✅ `enrichment_pipeline.py` - Main orchestrator
   - ✅ `phone_enrichment.py` - Phone/VOIP lookup using phonenumbers library
   - ✅ `domain_enrichment.py` - Basic domain/DNS lookup (adapt from AIPornTracker)
   - ✅ `wallet_enrichment.py` - Crypto wallet validation and detection
   - ✅ `messaging_enrichment.py` - Messaging platform handle detection

4. **Database Setup**
   - ✅ `docker-compose.yml` - Neo4j and PostgreSQL containers
   - ✅ `.env.example` - Environment variable template
   - ⏳ Database clients (`src/database/`) - TODO

5. **Dependencies** (`requirements.txt`)
   - Flask, PostgreSQL, Neo4j clients
   - Phone number parsing (phonenumbers)
   - DNS lookup (dnspython)
   - Domain/WHOIS (python-whois)

## What's Next

### ⏳ Phase 2: Database Clients & Storage

1. **PostgreSQL Client** (`src/database/postgres_client.py`)
   - Adapt from AIPornTracker pattern
   - Tables: `phone_numbers`, `domains`, `wallets`, `messaging_handles`, `clusters`
   - Enrichment cache table
   - Create tables on initialization

2. **Neo4j Client** (`src/database/neo4j_client.py`)
   - Adapt from AIPornTracker pattern
   - Create nodes: PhoneNumber, VOIPProvider, Domain, Wallet, MessagingHandle, Cluster
   - Create relationships: USES_VOIP, CONTACTS, LINKED_TO, REDIRECTS_TO, ASSOCIATED_WITH, PART_OF_CLUSTER

3. **Integration**
   - Update `enrichment_pipeline.py` to store results
   - Update `app.py` API endpoints to query databases

### ⏳ Phase 3: Enhanced Enrichment

1. **Phone Enrichment**
   - Add VOIP provider API lookups (numlookupapi.com, Twilio)
   - Reverse phone lookup
   - Carrier detection improvements

2. **Domain Enrichment**
   - Adapt full AIPornTracker domain enrichment:
     - WHOIS lookup
     - IP location (IPLocate.io, ip-api.com)
     - Hosting provider detection
     - CMS detection
     - SSL certificate analysis
   - Shortlink expansion (follow redirect chains)
   - Redirect chain tracking

3. **Wallet Enrichment**
   - Blockchain API integration:
     - blockchain.info (Bitcoin)
     - etherscan.io (Ethereum)
     - blockchair.com (multi-currency)
   - Transaction history
   - Balance lookup
   - Associated address detection

4. **Messaging Enrichment**
   - Platform-specific API lookups (if available)
   - Profile metadata extraction
   - Cross-platform linking

### ⏳ Phase 4: Web Interface

1. **Tracing UI** (`templates/trace.html`)
   - Input form for phone/domain/wallet/handle
   - Results display
   - Integration with existing dark theme

2. **Graph Visualization** (`templates/dashboard.html`)
   - D3.js or vis.js network graph
   - Node types: PhoneNumber, Domain, Wallet, Handle
   - Interactive exploration
   - Filtering and search

3. **Cluster Detection UI** (`templates/clusters.html`)
   - Display detected clusters
   - Cluster details view
   - Export options

### ⏳ Phase 5: Cluster Detection

1. **Algorithm** (`src/clustering/cluster_detection.py`)
   - Pattern matching for repeat VOIP blocks
   - Overlapping wallet addresses
   - Associated domains/handles
   - Time-based clustering
   - Confidence scoring

2. **Integration**
   - Background job to detect clusters
   - API endpoint for cluster queries
   - Visualization of clusters in graph

### ⏳ Phase 6: Export & Tools

1. **Export Tools** (`scripts/export_data.py`)
   - JSON export
   - GraphML export (for network analysis tools)
   - CSV export
   - Law enforcement packet generator

2. **Escalation Packet Generator**
   - Generate ready-to-send abuse reports
   - Include all relevant data (domain, IP, wallet, etc.)
   - Template for different provider types

## Key Learnings from AIPornTracker

### ✅ What We're Adapting

1. **Architecture Pattern**
   - Flask web app with API endpoints
   - PostgreSQL for relational data + Neo4j for graph relationships
   - Modular enrichment pipeline
   - Docker Compose for local development

2. **Domain Enrichment**
   - WHOIS/DNS lookup patterns
   - IP location and hosting detection
   - CMS/tech stack detection
   - Error handling and caching

3. **Database Patterns**
   - PostgreSQL schema for metadata
   - Neo4j graph structure for relationships
   - Connection pooling and error handling

### 🆕 What's New for BlackWire

1. **Phone/VOIP Enrichment** - Not in AIPornTracker
2. **Crypto Wallet Tracking** - Not in AIPornTracker
3. **Messaging Platform Integration** - Not in AIPornTracker
4. **Cluster Detection Focus** - More emphasis on pattern matching
5. **Victim Support Integration** - Direct link to support resources

## Current Status

✅ **Phase 1 Complete**: Basic infrastructure, enrichment modules, Flask app skeleton
⏳ **Phase 2 Next**: Database clients and storage
⏳ **Phase 3**: Enhanced enrichment with APIs
⏳ **Phase 4**: Web interface
⏳ **Phase 5**: Cluster detection
⏳ **Phase 6**: Export tools

## Next Steps

1. **Adapt database clients from AIPornTracker**
   - Copy and modify `postgres_client.py`
   - Copy and modify `neo4j_client.py`
   - Update schema for BlackWire entities

2. **Test enrichment pipeline**
   - Test phone number parsing
   - Test domain lookup
   - Test wallet validation
   - Test messaging handle detection

3. **Build basic tracing UI**
   - Create `templates/trace.html`
   - Connect to API endpoints
   - Display enrichment results

4. **Integrate with databases**
   - Store enrichment results
   - Create graph relationships
   - Query for visualization

