import azure.functions as func
from azure.data.tables import TableServiceClient, TableEntity
import json
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Get connection string from environment variable
AZURE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', '')

def send_email_notification(name, email, organization, message):
    """
    Send email notification using SMTP
    For production, you can configure this with SendGrid or Azure Communication Services
    """
    # For now, we'll just log it. You can add SendGrid API key later.
    print(f"Email notification would be sent:")
    print(f"From: {name} ({email})")
    print(f"Organization: {organization}")
    print(f"Message: {message}")
    return True

def save_to_table_storage(name, email, organization, message):
    """Save form submission to Azure Table Storage"""
    try:
        service = TableServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

        # Create table if it doesn't exist
        table_name = 'contactsubmissions'
        try:
            service.create_table(table_name)
        except Exception as e:
            if 'TableAlreadyExists' not in str(e):
                print(f'Error creating table: {e}')

        table_client = service.get_table_client(table_name)

        # Create entity
        timestamp = datetime.utcnow()
        row_key = timestamp.strftime('%Y%m%d%H%M%S%f')

        entity = TableEntity()
        entity['PartitionKey'] = 'ContactForm'
        entity['RowKey'] = row_key
        entity['Timestamp'] = timestamp
        entity['Name'] = name
        entity['Email'] = email
        entity['Organization'] = organization if organization else ''
        entity['Message'] = message
        entity['Status'] = 'New'

        # Insert entity
        table_client.create_entity(entity)
        print(f'✅ Saved contact form submission from {name}')
        return True

    except Exception as e:
        print(f'Error saving to table storage: {e}')
        return False

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Handle contact form submissions"""

    # Enable CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }

    # Handle preflight OPTIONS request
    if req.method == 'OPTIONS':
        return func.HttpResponse(status_code=200, headers=headers)

    try:
        # Get form data
        if req.method == 'POST':
            try:
                # Try JSON first
                req_body = req.get_json()
            except ValueError:
                # Try form data
                req_body = {}
                for key in req.form.keys():
                    req_body[key] = req.form[key]

            # Extract fields
            name = req_body.get('name', '')
            email = req_body.get('email', req_body.get('_replyto', ''))
            organization = req_body.get('organization', '')
            message = req_body.get('message', '')

            # Validate required fields
            if not name or not email or not message:
                return func.HttpResponse(
                    json.dumps({
                        'success': False,
                        'error': 'Missing required fields: name, email, and message are required'
                    }),
                    status_code=400,
                    headers=headers
                )

            # Save to Azure Table Storage
            saved = save_to_table_storage(name, email, organization, message)

            # Send email notification (optional - configure later)
            # email_sent = send_email_notification(name, email, organization, message)

            if saved:
                return func.HttpResponse(
                    json.dumps({
                        'success': True,
                        'message': 'Thank you for your message! We will get back to you soon.'
                    }),
                    status_code=200,
                    headers=headers
                )
            else:
                return func.HttpResponse(
                    json.dumps({
                        'success': False,
                        'error': 'Failed to save your message. Please try again or email us directly at info@loraleaf.com'
                    }),
                    status_code=500,
                    headers=headers
                )

        else:
            return func.HttpResponse(
                json.dumps({
                    'success': False,
                    'error': 'Method not allowed. Use POST to submit the form.'
                }),
                status_code=405,
                headers=headers
            )

    except Exception as e:
        print(f'Error processing contact form: {e}')
        return func.HttpResponse(
            json.dumps({
                'success': False,
                'error': 'An error occurred processing your request. Please email us directly at info@loraleaf.com'
            }),
            status_code=500,
            headers=headers
        )
