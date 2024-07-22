import logging
import os
import json 
import base64 
from azure.cosmos import CosmosClient
import azure.functions as func

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="main")
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve Cosmos DB credentials from environment variables
    endpoint = os.getenv('COSMOS_DB_ENDPOINT')
    key = os.getenv('COSMOS_DB_KEY')

    # Check if the environment variables are set
    if not endpoint or not key:
        return func.HttpResponse(
            json.dumps({"error": "Cosmos DB credentials are not set"}),
            status_code=500,
            mimetype='application/json'
        )

    # Validate the key
    try:
        base64.b64decode(key)
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Invalid Cosmos DB key: {e}"}),
            status_code=500,
            mimetype='application/json'
        )

    # Initialize the CosmosClient
    try:
        client = CosmosClient(endpoint, key)
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Failed to initialize CosmosClient: {e}"}),
            status_code=500,
            mimetype='application/json'
        )
    
    database_name = 'cloudresumechallenge'
    container_name = '2'
    try:
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Failed to get database or container client: {e}"}),
            status_code=500,
            mimetype='application/json'
        )
    
    # Query to retrieve the document
    query = "SELECT * FROM c WHERE c.id='1'"
    try:
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Failed to query items: {e}"}),
            status_code=500,
            mimetype='application/json'
        )
    
    if not items:
        return func.HttpResponse(
            json.dumps({"error": "Document not found"}),
            status_code=404,
            mimetype='application/json'
        )
    
    item = items[0]
    
    # Retrieve and increment the count
    count = item.get('count', 0)
    count += 1
    item['count'] = count
    
    # Update the document
    try:
        container.upsert_item(item)
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": f"Failed to upsert item: {e}"}),
            status_code=500,
            mimetype='application/json'
        )
    
    return func.HttpResponse(
        json.dumps({"message": "Updated count", "count": count}),
        mimetype='application/json'
    )
