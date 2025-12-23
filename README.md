# LoRaLeaf Azure Dashboard

Real-time sensor data dashboard for the LoRaLeaf sensor network, deployed on Azure Static Web Apps.

## Features

- Real-time sensor data display from Azure Table Storage
- Auto-refresh every 30 seconds
- Stats summary with network averages
- Battery monitoring with visual indicators
- Active/inactive node status (5-minute timeout)
- Responsive design

## Architecture

- **Frontend**: HTML/CSS/JavaScript (vanilla, no frameworks)
- **Backend**: Azure Functions (Python)
- **Data Storage**: Azure Table Storage
- **Hosting**: Azure Static Web Apps

## Setup

### Prerequisites

- Azure subscription
- Azure Storage Account with Table Storage
- Azure Static Web App

### Environment Variables

Set the following environment variable in your Azure Static Web App:

```
AZURE_STORAGE_CONNECTION_STRING=<your_connection_string>
```

To set this in Azure:
1. Go to your Static Web App in Azure Portal
2. Navigate to **Configuration**
3. Add a new application setting:
   - Name: `AZURE_STORAGE_CONNECTION_STRING`
   - Value: Your Azure Storage connection string

### Deployment

This project uses GitHub Actions for automatic deployment. When you push to the `main` branch, the app will automatically deploy to Azure Static Web Apps.

#### Setup GitHub Secret

1. Go to your GitHub repository settings
2. Navigate to **Secrets and variables** → **Actions**
3. Add a new repository secret:
   - Name: `AZURE_STATIC_WEB_APPS_API_TOKEN`
   - Value: Your Azure Static Web App deployment token

To get the deployment token:
```bash
az staticwebapp secrets list --name loraleaf --resource-group loraleaf-rg --query "properties.apiKey" -o tsv
```

## Project Structure

```
loraleaf-dashboard/
├── index.html                    # Main dashboard page
├── api/
│   ├── nodes.py                  # Azure Function: Get sensor data
│   └── function.json             # Function configuration
├── .github/
│   └── workflows/
│       └── azure-static-web-apps.yml  # GitHub Actions deployment
├── host.json                     # Azure Functions host config
├── requirements.txt              # Python dependencies
└── staticwebapp.config.json      # Static Web App configuration
```

## API Endpoints

### GET /api/nodes

Returns the latest sensor data for all nodes.

**Response:**
```json
{
  "nodes": [
    {
      "node_id": "NODE_01",
      "temperature": 19.5,
      "pressure": 1013.2,
      "humidity": 45.3,
      "battery_voltage": 3.8,
      "battery_percent": 67,
      "rssi": -85,
      "snr": 8.5,
      "last_update": "2025-12-23 12:30:45",
      "seconds_since_update": 15
    }
  ]
}
```

## Data Flow

1. Sensor nodes post data to Pi4 via LoRa/WiFi
2. Pi4 Flask app stores data in both:
   - Local SQLite database
   - Azure Table Storage (via `azure_storage_helper.py`)
3. Azure Functions API queries Azure Table Storage
4. Dashboard fetches data from Azure Functions API
5. Dashboard updates every 30 seconds

## Table Storage Schema

**Table Name:** `sensorreadings`

- **PartitionKey:** `node_id` (e.g., "NODE_01")
- **RowKey:** `YYYYMMDDHHMMSSffffff` (timestamp)
- **Fields:**
  - temperature (float)
  - pressure (float)
  - humidity (float)
  - battery_voltage (float)
  - battery_percent (int)
  - rssi (int)
  - snr (float)

## Node Types

- **NODE_01, NODE_02:** LoRa outdoor sensor nodes
- **NODE_INDOORS:** Indoor reference node (excluded from averages)
- **NODE_WIFI:** WiFi-connected outdoor node (excluded from averages)

## Development

### Local Testing

1. Install Azure Functions Core Tools
2. Create a `local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AZURE_STORAGE_CONNECTION_STRING": "<your_connection_string>"
  }
}
```
3. Run: `func start`

### Frontend Testing

Simply open `index.html` in a browser or use a local web server:
```bash
python -m http.server 8000
```

## License

MIT

## Credits

Built with Claude Code
