import json
import boto3

def handler(event, context):
    connection_id = event['requestContext']['connectionId']
    gatewayapi = boto3.client("apigatewaymanagementapi",
                              endpoint_url = "https://" + event["requestContext"]["domainName"] + "/" + event["requestContext"]["stage"])

    post_data = "Hello, WebSocket!"

    # Enviar mensaje de vuelta al cliente
    gatewayapi.post_to_connection(ConnectionId=connection_id, Data=post_data.encode('utf-8'))

    return {
        'statusCode': 200,
        'body': 'Message sent'
    }
