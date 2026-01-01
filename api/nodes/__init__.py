import azure.functions as func
from azure.data.tables import TableServiceClient
import json
import os
from datetime import datetime, timedelta

# Get connection string from environment variable
AZURE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Connect to Azure Table Storage
        service = TableServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        table = service.get_table_client('sensorreadings')
        
        # Get all entities
        entities = list(table.list_entities())
        
        # Group by node and get latest reading for each
        nodes_dict = {}
        for entity in entities:
            node_id = entity['PartitionKey']
            timestamp_str = entity['RowKey'][:14]  # YYYYMMDDHHMMSS
            
            # Parse timestamp
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            except:
                continue
            
            # Calculate seconds since update
            seconds_since_update = int((datetime.utcnow() - timestamp).total_seconds())
            
            # Keep only the latest reading per node
            if node_id not in nodes_dict or timestamp > nodes_dict[node_id]['timestamp']:
                nodes_dict[node_id] = {
                    'node_id': node_id,
                    'temperature': entity.get('temperature', 0),
                    'pressure': entity.get('pressure', 0),
                    'humidity': entity.get('humidity', 0),
                    'battery_voltage': entity.get('battery_voltage', 0),
                    'battery_percent': entity.get('battery_percent', 0),
                    'soil_moisture': entity.get('soil_moisture', 0),
                    'rssi': entity.get('rssi', 0),
                    'snr': entity.get('snr', 0),
                    'last_update': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                    'seconds_since_update': seconds_since_update,
                    'timestamp': timestamp
                }
        
        # Convert to list and remove timestamp object
        nodes = []
        for node in nodes_dict.values():
            del node['timestamp']
            nodes.append(node)
        
        # Sort by node_id
        nodes.sort(key=lambda x: x['node_id'])
        
        return func.HttpResponse(
            json.dumps({'nodes': nodes}),
            mimetype='application/json',
            headers={'Access-Control-Allow-Origin': '*'}
        )
        
    except Exception as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500,
            mimetype='application/json'
        )
