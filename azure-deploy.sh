#!/bin/bash
# LoRaLeaf Azure Deployment Script
# Deploy to Azure Static Web Apps

set -e

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║         LoRaLeaf - Azure Static Web Apps Deployment              ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI not found. Installing..."
    echo "Run: curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash"
    exit 1
fi

echo "✓ Azure CLI found"

# Check if logged in
if ! az account show &> /dev/null; then
    echo "📝 Please log in to Azure..."
    az login
fi

echo "✓ Logged in to Azure"

# Variables (customize these)
RESOURCE_GROUP="loraleaf-rg"
LOCATION="uksouth"
APP_NAME="loraleaf"
SKU="Free"

echo ""
echo "Configuration:"
echo "  Resource Group: $RESOURCE_GROUP"
echo "  Location: $LOCATION"
echo "  App Name: $APP_NAME"
echo "  SKU: $SKU"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled."
    exit 1
fi

# Create resource group if it doesn't exist
echo ""
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Static Web App
echo ""
echo "🚀 Creating Azure Static Web App..."
az staticwebapp create \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --sku $SKU \
    --source . \
    --app-location "/" \
    --output-location "." \
    --branch main

# Get the deployment token
echo ""
echo "🔑 Retrieving deployment token..."
DEPLOYMENT_TOKEN=$(az staticwebapp secrets list \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "properties.apiKey" -o tsv)

if [ -z "$DEPLOYMENT_TOKEN" ]; then
    echo "❌ Failed to retrieve deployment token"
    exit 1
fi

echo "✓ Deployment token retrieved"

# Get the Static Web App URL
APP_URL=$(az staticwebapp show \
    --name $APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query "defaultHostname" -o tsv)

echo ""
echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    DEPLOYMENT SUCCESSFUL!                         ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Your site is available at: https://$APP_URL"
echo ""
echo "📝 Next Steps:"
echo "  1. Configure custom domains:"
echo "     az staticwebapp hostname set --name $APP_NAME --resource-group $RESOURCE_GROUP --hostname loraleaf.com"
echo "     az staticwebapp hostname set --name $APP_NAME --resource-group $RESOURCE_GROUP --hostname loraleaf.co.uk"
echo ""
echo "  2. Update DNS records at your domain registrar:"
echo "     Type: CNAME"
echo "     Name: @ (or www)"
echo "     Value: $APP_URL"
echo ""
echo "  3. Test your site: https://$APP_URL"
echo ""

# Save deployment info
cat > deployment-info.txt << EOF
LoRaLeaf Azure Deployment Information
=====================================

Deployment Date: $(date)
Resource Group: $RESOURCE_GROUP
Static Web App: $APP_NAME
Location: $LOCATION
URL: https://$APP_URL

Custom Domain Commands:
-----------------------
az staticwebapp hostname set --name $APP_NAME --resource-group $RESOURCE_GROUP --hostname loraleaf.com
az staticwebapp hostname set --name $APP_NAME --resource-group $RESOURCE_GROUP --hostname loraleaf.co.uk

Deployment Token (save this securely):
--------------------------------------
$DEPLOYMENT_TOKEN
EOF

echo "ℹ️  Deployment info saved to: deployment-info.txt"
echo ""
