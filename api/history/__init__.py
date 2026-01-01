import azure.functions as func
from azure.data.tables import TableServiceClient
import json
import os
from datetime import datetime, timedelta

# Get connection string from environment variable
AZURE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get parameters
        node_id = req.params.get('node_id')
        hours = int(req.params.get('hours', 24))

        # Connect to Azure Table Storage
        service = TableServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        table = service.get_table_client('sensorreadings')

        # Calculate time threshold
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        cutoff_key = cutoff_time.strftime('%Y%m%d%H%M%S')

        # Query for specific node or all nodes
        if node_id:
            query_filter = f"PartitionKey eq '{node_id}' and RowKey ge '{cutoff_key}'"
        else:
            query_filter = f"RowKey ge '{cutoff_key}'"

        entities = list(table.query_entities(query_filter))

        # Process entities
        readings = []
        for entity in entities:
            timestamp_str = entity['RowKey'][:14]

            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            except:
                continue

            readings.append({
                'node_id': entity['PartitionKey'],
                'timestamp': timestamp.isoformat(),
                'temperature': entity.get('temperature', 0),
                'pressure': entity.get('pressure', 0),
                'humidity': entity.get('humidity', 0),
                'battery_voltage': entity.get('battery_voltage', 0),
                'battery_percent': entity.get('battery_percent', 0),
                'soil_moisture': entity.get('soil_moisture', 0),
                'rssi': entity.get('rssi', 0),
                'snr': entity.get('snr', 0)
            })

        # Sort by timestamp
        readings.sort(key=lambda x: x['timestamp'])

        return func.HttpResponse(
            json.dumps({'readings': readings, 'count': len(readings)}),
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500,
            mimetype='application/json'
        )
