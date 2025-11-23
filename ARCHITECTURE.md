# BlackWire Tool Architecture

## Overview

BlackWire maps sextortion and extortion infrastructure by tracing phone numbers, VOIP providers, domains, messaging handles, and crypto wallets. It builds on patterns from AIPornTracker while adding specialized enrichment for communications and financial tracking.

## Key Differences from AIPornTracker

### Data Types
- **AIPornTracker**: Focuses on domains, hosting, CMS, payment processors
- **BlackWire**: Focuses on:
  - Phone numbers & VOIP providers
  - Messaging platform handles (WhatsApp, Telegram, Instagram, SMS)
  - Crypto wallets (Bitcoin, Ethereum, etc.)
  - Domains (shortlinks, fake login pages)
  - Relationships between all of the above

### Use Cases
- **AIPornTracker**: NGO/law enforcement tracking of NCII sites
- **BlackWire**: Victim support + investigator tools for sextortion/extortion

## Architecture

### Components

1. **Data Input**
   - Phone numbers (with country code)
   - Messaging handles (WhatsApp, Telegram, Instagram)
   - Domains/URLs (shortlinks, fake pages)
   - Crypto wallet addresses
   - CSV import for bulk data

2. **Enrichment Pipeline** (`src/enrichment/`)
   - **Phone/VOIP Enrichment** (`phone_enrichment.py`):
     - Phone number validation and formatting
     - VOIP provider lookup (Twilio, Bandwidth, etc.)
     - Carrier detection
     - Geographic location (country/region)
     - Reverse phone lookup (free APIs)
   
   - **Domain Enrichment** (`domain_enrichment.py`):
     - WHOIS/DNS (from AIPornTracker)
     - IP location and hosting
     - Shortlink expansion (bit.ly, t.co, etc.)
     - Redirect chain tracking
     - SSL certificate analysis
   
   - **Messaging Platform Enrichment** (`messaging_enrichment.py`):
     - Platform detection (WhatsApp, Telegram, Instagram)
     - Handle validation
     - Profile metadata (if public)
     - Associated phone numbers
   
   - **Crypto Wallet Enrichment** (`wallet_enrichment.py`):
     - Wallet address validation (Bitcoin, Ethereum, etc.)
     - Blockchain explorer lookups
     - Transaction history analysis
     - Associated addresses and clusters
   
   - **Pipeline** (`enrichment_pipeline.py`):
     - Orchestrates all enrichment steps
     - Handles rate limiting and errors
     - Caches results

3. **Data Storage**
   - **Neo4j** (`src/database/neo4j_client.py`): Graph database for relationships
     - Nodes: PhoneNumber, VOIPProvider, Domain, Wallet, MessagingHandle, Cluster
     - Relationships: CONTACTS, USES_VOIP, REDIRECTS_TO, ASSOCIATED_WITH, PART_OF_CLUSTER
   
   - **PostgreSQL** (`src/database/postgres_client.py`): Relational storage for metadata
     - Tables: phone_numbers, domains, wallets, messaging_handles, enrichment_cache, clusters

4. **Web Application** (`app.py`)
   - Flask web server
   - Tracing interface: input phone/domain/wallet → enrich → visualize
   - Graph visualization (D3.js or vis.js)
   - Cluster detection UI
   - Export tools

5. **Cluster Detection** (`src/clustering/`)
   - Pattern matching algorithm
   - Identifies repeat VOIP blocks
   - Overlapping wallets
   - Associated domains/handles
   - Time-based clustering

6. **Export Tools** (`scripts/export_data.py`)
   - JSON export for APIs
   - GraphML export for network analysis tools
   - CSV export for spreadsheets
   - Law enforcement packet generation

## Data Flow

```
User Input (phone/domain/wallet)
    ↓
Enrichment Pipeline
    ├── Phone/VOIP Lookup
    ├── Domain Analysis
    ├── Messaging Platform Check
    └── Wallet Analysis
    ↓
Neo4j (Graph Relationships)
    ↓
PostgreSQL (Metadata Storage)
    ↓
Cluster Detection
    ↓
Visualization / Export
```

## Database Schema

### Neo4j Nodes

- **PhoneNumber**: `{number, country_code, format, first_seen, last_seen}`
- **VOIPProvider**: `{name, asn, country, known_abuse}`
- **Domain**: `{domain, registrar, ip, hosting, redirects_to}`
- **Wallet**: `{address, currency, first_seen, transactions}`
- **MessagingHandle**: `{handle, platform, phone_linked, profile_data}`
- **Cluster**: `{cluster_id, description, confidence, entities}`

### Neo4j Relationships

- `(PhoneNumber)-[:USES_VOIP]->(VOIPProvider)`
- `(PhoneNumber)-[:CONTACTS]->(MessagingHandle)`
- `(PhoneNumber)-[:LINKED_TO]->(Domain)`
- `(Domain)-[:REDIRECTS_TO]->(Domain)`
- `(Domain)-[:ASSOCIATED_WITH]->(Wallet)`
- `(Wallet)-[:TRANSACTED_WITH]->(Wallet)`
- `(MessagingHandle)-[:LINKED_TO]->(PhoneNumber)`
- `(PhoneNumber)-[:PART_OF_CLUSTER]->(Cluster)`
- `(Domain)-[:PART_OF_CLUSTER]->(Cluster)`
- `(Wallet)-[:PART_OF_CLUSTER]->(Cluster)`

### PostgreSQL Tables

- `phone_numbers`: phone, voip_provider, carrier, country, first_seen, last_seen
- `domains`: domain, registrar, ip, hosting, cms, first_seen, last_seen
- `wallets`: address, currency, first_seen, last_seen, transaction_count
- `messaging_handles`: handle, platform, phone_linked, first_seen, last_seen
- `enrichment_cache`: entity_type, entity_id, enrichment_data, cached_at
- `clusters`: cluster_id, entity_types, confidence, created_at
- `relationships`: source_type, source_id, target_type, target_id, relationship_type

## API Endpoints

### Tracing
- `POST /api/trace` - Trace a phone number, domain, or wallet
- `GET /api/trace/<id>` - Get trace results

### Visualization
- `GET /api/graph` - Get graph data for visualization
- `GET /api/clusters` - Get detected clusters

### Export
- `GET /api/export/json` - Export as JSON
- `GET /api/export/graphml` - Export as GraphML
- `GET /api/export/escalation-packet` - Generate escalation packet

## Free APIs for Enrichment

1. **Phone/VOIP**:
   - `numlookupapi.com` (free tier: 100/month)
   - `phonenumbervalidation.com` API
   - `twilio` lookup API (free tier)
   - Carrier lookup APIs

2. **Domain** (from AIPornTracker):
   - IPLocate.io (1,000/day free)
   - ip-api.com (45/min free)
   - python-whois (no API key)

3. **Crypto**:
   - `blockchain.info` API (Bitcoin)
   - `etherscan.io` API (Ethereum, free tier)
   - `blockchair.com` API (multi-currency, free tier)

4. **Messaging Platforms**:
   - Platform-specific APIs (limited public access)
   - Manual enrichment through pattern matching

## Implementation Phases

### Phase 1: Core Infrastructure (Current)
- ✅ Project structure
- ✅ Flask app skeleton
- ✅ Database setup (PostgreSQL + Neo4j)
- ✅ Basic enrichment modules

### Phase 2: Enrichment Modules
- Phone/VOIP enrichment
- Domain enrichment (adapt from AIPornTracker)
- Wallet enrichment
- Messaging handle enrichment

### Phase 3: Web Interface
- Tracing UI
- Graph visualization
- Cluster detection UI

### Phase 4: Advanced Features
- Cluster detection algorithm
- Export tools
- Escalation packet generator
- API endpoints

## Ethics & Safety

- ✅ No content storage (metadata only)
- ✅ Victim privacy protection
- ✅ Secure credential management
- ✅ Rate limiting on APIs
- ✅ Compliance with data privacy laws

