# LoRaLeaf - Wireless Environmental Monitoring

Solar-powered LoRa sensor network for agricultural environmental monitoring. Built for farms, estates, and vineyards.

## 🌐 Live Website

- **Marketing Site**: https://blue-glacier-0ff05ed03.3.azurestaticapps.net
- **Live Dashboard**: https://blue-glacier-0ff05ed03.3.azurestaticapps.net/live
- **GitHub Repo**: https://github.com/avthree77/loraleaf-cloud-dashboard

## 📊 Current Setup

### Sensor Network

**4 Active Nodes** posting to Azure Table Storage:

- **NODE_01** - LoRa outdoor sensor (BME280)
- **NODE_02** - LoRa outdoor sensor (BME280)
- **NODE_WIFI** - Pico 2W with solar panel + battery monitoring
- **NODE_INDOORS** - Raspberry Pi 4 BME280 sensor

### Data Collection

- **Every ~4 minutes**: LoRa nodes transmit
- **Every 60 seconds**: NODE_WIFI & NODE_INDOORS post
- **Storage**: Azure Table Storage (`sensorreadings` table)
- **API**: Azure Functions provide real-time & historical data
- **Validation**: Bad readings automatically rejected (pressure, humidity ranges)

## 🚀 Azure Deployment

### Automatic Deployment

The site **auto-deploys to Azure** via **GitHub Actions** whenever you push to the `main` branch.

**Workflow**: `.github/workflows/azure-static-web-apps-*.yml`

### Azure Resources

- **Service**: Azure Static Web Apps (Free tier)
- **Storage**: Azure Table Storage (`loraleafstorage`)
- **Functions**: Python Azure Functions (API endpoints)
- **Region**: Deployed automatically

### Cost

- **~$0.50 USD/month** (mostly Azure Table Storage writes)
- Well within free tiers for Static Web Apps and Functions

## 📁 Project Structure

```
loraleaf-dashboard/
├── index.html              # Marketing homepage
├── live.html               # Live sensor dashboard
├── css/
│   └── style.css          # Website styles
├── js/
│   └── main.js            # Website JavaScript
├── images/
│   ├── LoRaLeaf-field.png     # Product photos
│   ├── LoRaLeaf-Sensor.png
│   └── loraleaf-logo.svg
├── api/                   # Azure Functions
│   ├── nodes/             # GET /api/nodes - Latest sensor data
│   ├── history/           # GET /api/history?hours=24 - Historical data
│   ├── contact/           # POST /api/contact - Contact form handler
│   └── submissions/       # GET /api/submissions - View form submissions
├── staticwebapp.config.json  # Azure routing config
├── robots.txt             # SEO - Search engine instructions
├── sitemap.xml            # SEO - Site structure
└── README.md              # This file
```

## 🛠️ API Endpoints

### `/api/nodes`

Get latest reading from each sensor node.

**Example:**
```bash
curl https://blue-glacier-0ff05ed03.3.azurestaticapps.net/api/nodes
```

**Response:**
```json
{
  "nodes": [
    {
      "node_id": "NODE_01",
      "temperature": 6.4,
      "pressure": 1012.1,
      "humidity": 81.1,
      "battery_voltage": 3.63,
      "battery_percent": 52,
      "rssi": -78,
      "snr": 3.8,
      "last_update": "2025-12-23 22:45:30",
      "seconds_since_update": 15
    }
  ]
}
```

### `/api/history?hours=24`

Get historical sensor data.

**Parameters:**
- `hours` (optional, default: 24) - Number of hours of history
- `node_id` (optional) - Filter by specific node

**Example:**
```bash
curl "https://blue-glacier-0ff05ed03.3.azurestaticapps.net/api/history?hours=24"
```

### `/api/submissions`

View all contact form submissions (stored in `contactsubmissions` table).

**Example:**
```bash
curl https://blue-glacier-0ff05ed03.3.azurestaticapps.net/api/submissions
```

## 🔧 Making Changes

### 1. Edit Files Locally

```bash
cd /Users/av3/Documents/loraleaf-dashboard
# Edit files as needed
```

### 2. Commit & Push

```bash
git add .
git commit -m "Your change description"
git push origin main
```

### 3. Auto-Deploy

GitHub Actions automatically deploys to Azure within ~2 minutes.

Watch deployment progress: https://github.com/avthree77/loraleaf-cloud-dashboard/actions

## 📡 Sensor Network Setup

### Pi4 Sensor Hub (192.168.1.85)

**Location**: `/home/pi/`

**Key Files:**
- `lora_sensor_web_gui.py` - Flask server handling LoRa nodes (NODE_01, NODE_02)
- `indoor_bme280_logger.py` - Indoor sensor logger (NODE_INDOORS)
- `azure_storage_helper.py` - Azure Table Storage posting (with validation)
- `lora_sensor_data.db` - Local SQLite database

**Services:**
- Web GUI: http://192.168.1.85:5000 (local network only)
- Auto-posts to Azure every reading

### Data Validation

Bad sensor readings are automatically rejected:
- Temperature: -40°C to 60°C
- Pressure: 950 to 1100 hPa
- Humidity: 0.1% to 99.9% (excludes exactly 0 or 100)
- Battery: 0V to 5V

Invalid data is logged but not posted to Azure.

## 🎨 SEO & Marketing

### Meta Tags

- **Title**: LoRaLeaf | Wireless Environmental Monitoring for Agriculture & Farms
- **Description**: Solar-powered LoRa sensor network...
- **Keywords**: LoRa sensors, agricultural monitoring, farm sensors, etc.
- **Open Graph**: Social media preview cards (Facebook, Twitter, LinkedIn)
- **Geo Tags**: Cornwall, UK location targeting

### Structured Data

- Schema.org Product markup
- Schema.org Organization markup
- Google-friendly rich search results

### Sitemap & Robots

- `sitemap.xml` - All pages indexed
- `robots.txt` - Search engine guidance
- Submit to Google Search Console for faster indexing

## 📊 Live Dashboard Features

**URL**: `/live`

**Features:**
- Real-time sensor data (auto-refresh every 30 seconds)
- 4 node cards showing current readings
- Key statistics (average temp, pressure, humidity)
- Barometric pressure trend indicator (rising/falling/steady)
- Historical graphs (24 hours):
  - Temperature (NODE_01 & NODE_02)
  - Pressure (NODE_01 & NODE_02)
  - Humidity (NODE_01 & NODE_02)
- Charts auto-refresh every 5 minutes

**Data Source**: Outdoor LoRa nodes (NODE_01, NODE_02) only

## 🔐 Security Notes

- **Public APIs**: All endpoints are public (no authentication)
- **Form Submissions**: Stored in Azure Table Storage
- **Connection Strings**: Stored in Azure environment variables (not in code)
- **CSP Headers**: Content Security Policy configured in `staticwebapp.config.json`

## 🌍 Contact

- **Email**: info@loraleaf.com
- **Location**: Cornwall, UK
- **Company**: AV3 Media

## 📝 Version History

- **2025-12-23**: Initial website launch with marketing site + live dashboard
- **2025-12-23**: Added real product photos
- **2025-12-23**: Enhanced SEO metadata and structured data
- **2025-12-23**: Added historical graphing and barometer
- **2025-12-23**: Simplified contact to email button

## 🎯 Future Enhancements (Optional)

- [ ] Email notifications for new contact form submissions (SendGrid)
- [ ] Custom domain (loraleaf.com)
- [ ] SSL certificate for custom domain
- [ ] Admin dashboard for viewing/managing form submissions
- [ ] Export sensor data to CSV
- [ ] Alert system for frost/extreme conditions
- [ ] Mobile app

## 💰 Cost Breakdown

**Monthly Costs (Estimated):**

- Azure Static Web Apps: **$0** (free tier)
- Azure Functions: **$0** (free tier - under 1M executions)
- Azure Table Storage: **~$0.50** (75k writes/month + storage)
- **Total: ~$0.50 USD/month**

## 🎄 Merry Christmas!

Deployed and running smoothly. Enjoy collecting data over the holidays!

---

Built with ❤️ in Cornwall by AV3 Media
