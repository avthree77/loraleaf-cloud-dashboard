import azure.functions as func
from azure.data.tables import TableServiceClient
import json
import os
from datetime import datetime

# Get connection string from environment variable
AZURE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Get all contact form submissions"""

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        # Connect to Azure Table Storage
        service = TableServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
        table = service.get_table_client('contactsubmissions')

        # Get all submissions
        try:
            entities = list(table.list_entities())
        except Exception as e:
            # Table might not exist yet
            return func.HttpResponse(
                json.dumps({'submissions': [], 'count': 0}),
                mimetype='application/json',
                headers=headers
            )

        # Process submissions
        submissions = []
        for entity in entities:
            timestamp_str = entity['RowKey'][:14]

            try:
                timestamp = datetime.strptime(timestamp_str, '%Y%m%d%H%M%S')
            except:
                timestamp = datetime.utcnow()

            submissions.append({
                'name': entity.get('Name', ''),
                'email': entity.get('Email', ''),
                'organization': entity.get('Organization', ''),
                'message': entity.get('Message', ''),
                'status': entity.get('Status', 'New'),
                'submitted_at': timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })

        # Sort by submission time (newest first)
        submissions.sort(key=lambda x: x['submitted_at'], reverse=True)

        return func.HttpResponse(
            json.dumps({
                'submissions': submissions,
                'count': len(submissions)
            }),
            mimetype='application/json',
            headers=headers
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({'error': str(e)}),
            status_code=500,
            mimetype='application/json',
            headers=headers
        )
