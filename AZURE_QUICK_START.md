# LoRaLeaf - Azure Quick Start

## Fastest Way to Deploy to Azure

### Prerequisites Check
```bash
# Check if Azure CLI is installed
az --version

# If not installed, run:
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
```

### 3-Minute Deployment

#### Option 1: Automated Script (Easiest!)

```bash
cd /home/av3/loraleaf-website
./azure-deploy.sh
```

That's it! The script handles everything.

#### Option 2: Manual Commands

```bash
cd /home/av3/loraleaf-website

# Login to Azure
az login

# Create resource group
az group create --name loraleaf-rg --location uksouth

# Create Static Web App
az staticwebapp create \
  --name loraleaf \
  --resource-group loraleaf-rg \
  --location uksouth \
  --sku Free \
  --source . \
  --branch main

# Get your site URL
az staticwebapp show \
  --name loraleaf \
  --resource-group loraleaf-rg \
  --query "defaultHostname" -o tsv
```

### Add Your Domains

```bash
# Add loraleaf.com
az staticwebapp hostname set \
  --name loraleaf \
  --resource-group loraleaf-rg \
  --hostname loraleaf.com

# Add loraleaf.co.uk
az staticwebapp hostname set \
  --name loraleaf \
  --resource-group loraleaf-rg \
  --hostname loraleaf.co.uk
```

### Update DNS at Your Registrar

Azure will tell you what DNS records to add. Typically:

```
Type: CNAME
Name: www
Value: loraleaf.azurestaticapps.net

Type: TXT
Name: _dnsauth
Value: [provided by Azure]
```

### That's It!

Your site will be live at:
- https://loraleaf.azurestaticapps.net (Azure URL)
- https://loraleaf.com (after DNS propagates)
- https://loraleaf.co.uk (after DNS propagates)

### Cost: FREE
Azure Static Web Apps Free tier includes:
- 100 GB bandwidth/month
- Free SSL certificates
- Global CDN
- Custom domains

Perfect for LoRaLeaf!

---

Need more details? See **AZURE_DEPLOYMENT.md**
