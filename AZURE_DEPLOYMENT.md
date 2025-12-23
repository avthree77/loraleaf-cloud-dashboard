# LoRaLeaf - Azure Deployment Guide

Complete guide to deploy your LoRaLeaf website to Microsoft Azure.

## Recommended: Azure Static Web Apps

Azure Static Web Apps is perfect for this site - it's free, fast, and includes:
- Global CDN
- Free SSL certificates
- Custom domains
- Built-in CI/CD
- Forms support (via Azure Functions)

## Prerequisites

1. **Azure Account**
   - Sign up at [portal.azure.com](https://portal.azure.com)
   - Free tier available (perfect for this site)

2. **Azure CLI** (install if needed)
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

## Method 1: Automated Deployment (Recommended)

Use the provided deployment script:

```bash
cd /home/av3/loraleaf-website
./azure-deploy.sh
```

This script will:
1. Check Azure CLI installation
2. Log you into Azure (if needed)
3. Create a resource group
4. Create an Azure Static Web App
5. Deploy your website
6. Provide your site URL
7. Save deployment information

**Location**: UK South (closest to Cornwall)

## Method 2: Manual Deployment via Azure Portal

### Step 1: Create Static Web App

1. Go to [Azure Portal](https://portal.azure.com)
2. Click **Create a resource**
3. Search for **Static Web Apps**
4. Click **Create**

### Step 2: Configure

**Basics:**
- Subscription: Your subscription
- Resource Group: Create new → `loraleaf-rg`
- Name: `loraleaf`
- Plan type: Free
- Region: UK South

**Deployment:**
- Source: Other (we'll upload manually)

Click **Review + Create** → **Create**

### Step 3: Upload Website

1. Once created, go to your Static Web App resource
2. Click **Browse** to see your empty site
3. Download the **deployment token** from the "Manage deployment token" section
4. Install SWA CLI:
   ```bash
   npm install -g @azure/static-web-apps-cli
   ```
5. Deploy:
   ```bash
   cd /home/av3/loraleaf-website
   swa deploy --deployment-token YOUR_TOKEN_HERE
   ```

## Method 3: Azure Storage + CDN (Alternative)

If you prefer traditional static hosting:

### Create Storage Account

```bash
# Variables
RESOURCE_GROUP="loraleaf-rg"
LOCATION="uksouth"
STORAGE_ACCOUNT="loraleafstorage"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create storage account
az storage account create \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --sku Standard_LRS \
  --kind StorageV2

# Enable static website
az storage blob service-properties update \
  --account-name $STORAGE_ACCOUNT \
  --static-website \
  --404-document index.html \
  --index-document index.html

# Upload files
az storage blob upload-batch \
  --account-name $STORAGE_ACCOUNT \
  --destination '$web' \
  --source .

# Get website URL
az storage account show \
  --name $STORAGE_ACCOUNT \
  --resource-group $RESOURCE_GROUP \
  --query "primaryEndpoints.web" \
  --output tsv
```

## Configure Custom Domains

### For Azure Static Web Apps

1. Go to your Static Web App in Azure Portal
2. Navigate to **Custom domains**
3. Click **+ Add**
4. Enter your domain: `loraleaf.com`
5. Choose DNS provider validation
6. Add the provided DNS records to your domain registrar

**DNS Records to Add:**

For **loraleaf.com**:
```
Type: CNAME
Name: www
Value: <your-app-name>.azurestaticapps.net

Type: TXT
Name: _dnsauth
Value: <validation-code-provided-by-azure>
```

For apex domain (@):
```
Type: ALIAS or ANAME (if supported)
Name: @
Value: <your-app-name>.azurestaticapps.net

OR if ALIAS not supported:
Type: A
Name: @
Value: 20.36.120.208 (check current Azure IPs)
```

7. Repeat for `loraleaf.co.uk`

### SSL Certificates

- Azure automatically provisions free SSL certificates
- Certificates auto-renew
- HTTPS enforced by default

## Configure Contact Form

### Option 1: Azure Functions (Built-in with Static Web Apps)

1. Create a folder: `api/`
2. Add a function to handle form submissions
3. Update form action to point to `/api/contact`

Example function (`api/contact/index.js`):
```javascript
module.exports = async function (context, req) {
    const { name, email, message } = req.body;

    // Send email via SendGrid, Azure Communication Services, etc.

    context.res = {
        status: 200,
        body: JSON.stringify({ success: true })
    };
};
```

### Option 2: Keep Formspree

No changes needed - Formspree works great with Azure Static Web Apps.

## Testing

After deployment:

1. **Test the site**: Visit your Azure URL
2. **Check all pages**: Navigate through all sections
3. **Test contact form**: Submit a test message
4. **Mobile test**: Check on mobile devices
5. **SSL**: Verify HTTPS is working

## Monitoring & Analytics

### Enable Application Insights

```bash
# Create Application Insights
az monitor app-insights component create \
  --app loraleaf-insights \
  --location uksouth \
  --resource-group loraleaf-rg

# Get instrumentation key
az monitor app-insights component show \
  --app loraleaf-insights \
  --resource-group loraleaf-rg \
  --query instrumentationKey
```

Add to your `index.html` before `</head>`:
```html
<script type="text/javascript">
var sdkInstance="appInsightsSDK";
window[sdkInstance]="appInsights";
// Application Insights code here
</script>
```

## Updating the Website

### Manual Updates

```bash
cd /home/av3/loraleaf-website
# Make your changes
swa deploy --deployment-token YOUR_TOKEN
```

### Automatic Updates (CI/CD)

1. Push code to GitHub
2. Azure Static Web Apps automatically deploys on push
3. Preview deployments for pull requests

## Cost Estimation

**Azure Static Web Apps (Free Tier):**
- 100 GB bandwidth/month
- 0.5 GB storage
- Custom domains: Free
- SSL certificates: Free
- Global CDN: Included

**Perfect for LoRaLeaf!** You'll stay in the free tier.

## Domain Registrar DNS Setup

At your domain registrar (e.g., Namecheap, GoDaddy, 123-reg):

1. **Log in** to your domain registrar
2. **Find DNS settings** for loraleaf.com
3. **Add these records**:

```
# For www.loraleaf.com
Type: CNAME
Host: www
Value: loraleaf.azurestaticapps.net
TTL: Automatic

# For loraleaf.com (apex/root domain)
Type: ALIAS or ANAME (if available)
Host: @
Value: loraleaf.azurestaticapps.net
TTL: Automatic

# For Azure validation
Type: TXT
Host: _dnsauth
Value: [provided by Azure]
TTL: Automatic
```

4. **Repeat for loraleaf.co.uk**
5. **Wait** 1-4 hours for DNS propagation
6. **Verify** in Azure Portal under Custom Domains

## Troubleshooting

### Site not loading
- Check DNS propagation: [whatsmydns.net](https://whatsmydns.net)
- Verify deployment: Check Azure Portal deployment logs
- Clear browser cache

### SSL errors
- Wait 10-15 minutes for certificate provisioning
- Ensure DNS is correctly configured
- Check Azure Portal SSL status

### Contact form not working
- Verify Formspree endpoint is correct
- Check browser console for errors
- Test with network tab open

## Useful Commands

```bash
# Login to Azure
az login

# List all resources
az resource list --resource-group loraleaf-rg --output table

# View Static Web App details
az staticwebapp show --name loraleaf --resource-group loraleaf-rg

# Get app URL
az staticwebapp show --name loraleaf --resource-group loraleaf-rg --query "defaultHostname" -o tsv

# Delete everything (be careful!)
az group delete --name loraleaf-rg --yes --no-wait
```

## Support

- Azure Documentation: [docs.microsoft.com/azure/static-web-apps](https://docs.microsoft.com/azure/static-web-apps)
- Azure Support: Available in portal
- Community: Stack Overflow (tag: azure-static-web-apps)

## Security Best Practices

✓ HTTPS enforced (automatic)
✓ Security headers configured (see staticwebapp.config.json)
✓ CSP policy in place
✓ CORS configured
✓ DDoS protection (via Azure)

---

Ready to deploy? Run:
```bash
cd /home/av3/loraleaf-website
./azure-deploy.sh
```

Your LoRaLeaf website will be live on Azure in minutes!
