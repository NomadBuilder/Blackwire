# BlackWire Intelligence

**Mapping sextortion and extortion infrastructure to protect victims and expose organized abuse.**

BlackWire traces the infrastructure behind sextortion and extortion attempts — mapping phone numbers, domains, VOIP providers, messaging handles, and crypto wallets to reveal hidden networks of abuse.

## Features

- **Phone/VOIP Tracing**: Identify VOIP providers, carriers, and geographic location
- **Domain Analysis**: Track shortlinks, redirect chains, and hosting infrastructure
- **Messaging Platform Mapping**: Link handles across WhatsApp, Telegram, Instagram
- **Crypto Wallet Tracking**: Trace Bitcoin, Ethereum, and other cryptocurrency wallets
- **Cluster Detection**: Identify coordinated abuse patterns and repeat offenders
- **Graph Visualization**: Interactive network graph showing relationships
- **Export Tools**: JSON, GraphML, and law enforcement packet generation

## Project Structure

```
Extort/
├── app.py                    # Flask web server
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Database containers
├── ARCHITECTURE.md           # Detailed architecture doc
├── Index.html                # Landing page
├── support.html              # Support & reporting page
│
├── src/
│   ├── database/
│   │   ├── neo4j_client.py  # Neo4j graph database
│   │   └── postgres_client.py # PostgreSQL client
│   │
│   ├── enrichment/
│   │   ├── phone_enrichment.py      # Phone/VOIP lookup
│   │   ├── domain_enrichment.py     # Domain analysis
│   │   ├── wallet_enrichment.py     # Crypto wallet analysis
│   │   ├── messaging_enrichment.py  # Messaging platform lookup
│   │   └── enrichment_pipeline.py   # Main pipeline
│   │
│   └── clustering/
│       └── cluster_detection.py     # Pattern matching
│
├── scripts/
│   ├── enrich_data.py        # Bulk enrichment script
│   └── export_data.py        # Export tools
│
├── templates/
│   ├── index.html            # Main tracing interface
│   ├── dashboard.html        # Graph visualization
│   └── clusters.html         # Cluster detection UI
│
├── static/
│   ├── css/
│   │   └── style.css         # Styling
│   └── js/
│       └── visualization.js  # Graph visualization (D3.js/vis.js)
│
└── data/
    ├── input/                # Input CSV files
    └── output/               # Exported data
```

## Quick Start

### Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Free API keys (optional, see ARCHITECTURE.md)

### Setup

1. **Clone and install**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Start databases**:
```bash
docker-compose up -d
```

3. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your API keys if needed
```

4. **Start web server**:
```bash
python app.py
```

Visit `http://localhost:5000` to access the tracing tool.

## Usage

### Trace a Phone Number

```
POST /api/trace
{
  "type": "phone",
  "value": "+1234567890"
}
```

### Trace a Domain

```
POST /api/trace
{
  "type": "domain",
  "value": "example.com"
}
```

### Trace a Crypto Wallet

```
POST /api/trace
{
  "type": "wallet",
  "value": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
}
```

## Learnings from AIPornTracker

This project adapts patterns from the AIPornTracker project:

- ✅ **Flask-based web application** with API endpoints
- ✅ **PostgreSQL + Neo4j** dual database architecture
- ✅ **Modular enrichment pipeline** with error handling
- ✅ **Graph visualization** for relationship mapping
- ✅ **Export tools** for data sharing

**Key Adaptations for BlackWire**:
- Added phone/VOIP enrichment (not in AIPornTracker)
- Added crypto wallet tracking (not in AIPornTracker)
- Added messaging platform integration
- Focus on cluster detection for coordinated abuse
- Victim support workflow integration

## Ethics & Safety

- ✅ **No content collection**: Only metadata (phone numbers, domains, wallets)
- ✅ **Privacy protection**: Secure data storage and handling
- ✅ **Victim support**: Integrated support resources and reporting tools
- ✅ **Compliance**: Designed to comply with data privacy laws

## License

This project is intended for legitimate victim support, NGO, and law enforcement use only.

## Status

🚧 **In Development** - Phase 1: Core Infrastructure

