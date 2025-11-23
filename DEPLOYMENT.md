# Deployment Guide for Render

This guide will help you deploy the BlackWire Sextortion Infrastructure Mapping application to Render.

## Prerequisites

1. **GitHub Account** - Your code is already in: https://github.com/NomadBuilder/Blackwire.git
2. **Render Account** - Sign up at [render.com](https://render.com) (free tier available)

**Note**: Neo4j is optional! The app works with PostgreSQL only, but graph visualization features require Neo4j. You can add Neo4j later if needed.

## Step 1: Deploy PostgreSQL Database on Render

1. Log into [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `blackwire-postgres`
   - **Database**: `blackwire`
   - **User**: `blackwire_user`
   - **Plan**: **Free** (768 MB RAM, 256 MB disk)
   - **Region**: Choose closest to you
4. Click **"Create Database"**
5. Wait for it to be ready (2-3 minutes)
6. Copy the **Internal Database URL** - you'll need this for environment variables

## Step 2: Deploy Web Service on Render

**Option A: Manual Setup (Recommended for Free Tier)**

1. In Render Dashboard, click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `NomadBuilder/Blackwire`
3. Configure:
   - **Name**: `blackwire` (or any name you prefer)
   - **Environment**: **Python 3**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 2 --timeout 120`
   - **Plan**: **Free** (512 MB RAM)
4. Go to **"Environment"** tab and add these variables:

   **Database Connection (from PostgreSQL service):**
   - `POSTGRES_HOST` - Host from PostgreSQL service (e.g., `dpg-xxxxx-a.oregon-postgres.render.com`)
   - `POSTGRES_PORT` - Port (usually `5432`)
   - `POSTGRES_USER` - Database user (e.g., `blackwire_user`)
   - `POSTGRES_PASSWORD` - Database password (from PostgreSQL service)
   - `POSTGRES_DB` - Database name (`blackwire`)

   **Application Settings:**
   - `FLASK_ENV` - `production`
   - `SECRET_KEY` - Generate a random secret key (use `openssl rand -hex 32`)

   **API Keys (from your .env file):**
   - `IPAPI_KEY` - Your ipapi.com API key
   - `VIRUSTOTAL_API_KEY` - Your VirusTotal API key
   - `NUMLOOKUP_API_KEY` - (Optional) Your numlookupapi.com API key
   - `ETHERSCAN_API_KEY` - (Optional) Your Etherscan API key

   **Neo4j (Optional - only if you want graph visualization):**
   - `NEO4J_URI` - Your Neo4j Aura URI (e.g., `neo4j+s://xxxxx.databases.neo4j.io`)
   - `NEO4J_USER` - Your Neo4j username (usually `neo4j`)
   - `NEO4J_PASSWORD` - Your Neo4j password

5. Click **"Create Web Service"**

**Option B: Blueprint Deployment (Requires Paid Plan)**

If you have a paid Render plan, you can use the `render.yaml` file:
1. In Render Dashboard, click **"New +"** → **"Blueprint"**
2. Connect your GitHub repository: `NomadBuilder/Blackwire`
3. Render will automatically detect `render.yaml` and create the services
4. You'll still need to manually add API keys in the Environment tab

## Step 3: Initialize Database

After deployment, the PostgreSQL schema will be created automatically when the app first connects. The app will create all necessary tables on first startup.

## Step 4: Access Your Application

1. Once deployed, Render will provide a URL like: `https://blackwire.onrender.com`
2. The app may take 30-60 seconds to start on first request (free tier spins down after inactivity)
3. Share this URL with users

## Important Notes

### Free Tier Limitations

- **Render Free Tier**: 
  - Spins down after 15 minutes of inactivity
  - Takes ~30 seconds to wake up on first request
  - 512 MB RAM for web service
  - 768 MB RAM for PostgreSQL

- **Neo4j**: Optional! The app works with PostgreSQL only. Graph visualization features require Neo4j, but core tracing functionality works without it.

### Troubleshooting

1. **App won't start**: Check logs in Render dashboard → "Logs" tab
2. **Database connection errors**: Verify PostgreSQL environment variables are set correctly
3. **Slow first load**: Normal on free tier - app is spinning up (~30 seconds)
4. **Graph not working**: Make sure Neo4j environment variables are set if you want graph visualization

### Upgrading (Optional)

If you need better performance:
- **Render Paid Plans**: $7/month for always-on service
- **Neo4j Aura**: Paid plans available for larger datasets

## Security Considerations

1. **Never commit** `.env` files or API keys to GitHub (already in `.gitignore`)
2. All API keys should be set in Render's Environment tab
3. Use strong `SECRET_KEY` for production
4. Consider using Render's secret management features for sensitive keys

## Environment Variables Summary

**Required:**
- `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- `FLASK_ENV=production`
- `SECRET_KEY` (generate with `openssl rand -hex 32`)

**Recommended:**
- `IPAPI_KEY` (for IP geolocation)
- `VIRUSTOTAL_API_KEY` (for threat intelligence)

**Optional:**
- `NUMLOOKUP_API_KEY` (for phone number enrichment)
- `ETHERSCAN_API_KEY` (for Ethereum wallet analysis)
- `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD` (for graph visualization)

