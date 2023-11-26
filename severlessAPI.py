import json
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('YourTableName')

def lambda_handler(event, context):
    # Extract user's name from the payload
    user_name = event.get('name', 'Unknown User')

    # Handle different API endpoints
    if event['operation'] == 'retrieve':
        return retrieve_data(event['id'])
    elif event['operation'] == 'store':
        return store_data(user_name)
    elif event['operation'] == 'edit':
        return edit_data(event['id'], user_name)
    elif event['operation'] == 'delete':
        return delete_data(event['id'])

def retrieve_data(item_id):
    try:
        response = table.get_item(Key={'id': item_id})
        item = response.get('Item')
        return {'message': 'Data retrieved successfully', 'data': item}
    except ClientError as e:
        return {'error': str(e)}

def store_data(user_name):
    item_id = generate_unique_id(user_name)
    try:
        table.put_item(Item={'id': item_id, 'name': user_name})
        return {'message': f'Welcome, {user_name}! Data stored successfully.', 'user_id': item_id}
    except ClientError as e:
        return {'error': str(e)}

def edit_data(item_id, user_name):
    try:
        table.update_item(
            Key={'id': item_id},
            UpdateExpression='SET #name = :val1',
            ExpressionAttributeNames={'#name': 'name'},
            ExpressionAttributeValues={':val1': user_name}
        )
        return {'message': f'Data updated successfully for {item_id}'}
    except ClientError as e:
        return {'error': str(e)}

def delete_data(item_id):
    try:
        table.delete_item(Key={'id': item_id})
        return {'message': f'Data deleted successfully for {item_id}'}
    except ClientError as e:
        return {'error': str(e)}

def generate_unique_id(name):
    # Implement a method to generate a unique ID based on the user's name
    return name.lower().replace(" ", "_")