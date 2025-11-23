# Setting Up Neo4j Aura for Render Deployment

Since Render doesn't provide Neo4j as a managed service, you'll need to use **Neo4j Aura** (cloud-hosted Neo4j) for graph visualization.

## Step 1: Create Neo4j Aura Account

1. Go to [https://neo4j.com/cloud/aura/](https://neo4j.com/cloud/aura/)
2. Click **"Start Free"** or **"Sign Up"**
3. Create an account (free tier available)

## Step 2: Create a Free Instance

1. Once logged in, click **"Create Instance"**
2. Choose **"Free"** tier
3. Configure:
   - **Instance Name**: `blackwire-graph` (or any name)
   - **Region**: Choose closest to your Render region
   - **Database Name**: `neo4j` (default)
4. Click **"Create Instance"**
5. Wait 2-3 minutes for instance to be created

## Step 3: Get Connection Details

1. Once the instance is ready, click on it
2. You'll see connection details:
   - **URI**: Something like `neo4j+s://xxxxx.databases.neo4j.io`
   - **Username**: Usually `neo4j`
   - **Password**: The password you set (or auto-generated)
3. **Copy these values** - you'll need them for Render environment variables

## Step 4: Test Connection (Optional)

You can test the connection using Neo4j Browser or any Neo4j client.

## Step 5: Add to Render

Add these environment variables to your Render web service:
- `NEO4J_URI` - The full URI from Aura (e.g., `neo4j+s://xxxxx.databases.neo4j.io`)
- `NEO4J_USER` - Usually `neo4j`
- `NEO4J_PASSWORD` - Your Aura password

## Free Tier Limits

- **Neo4j Aura Free**: 
  - 0.5 GB storage
  - Perfect for development and small datasets
  - Can upgrade later if needed

## Notes

- The free tier is sufficient for development and testing
- Your graph data will persist in Neo4j Aura
- You can access the Neo4j Browser from the Aura dashboard to view your graph data

