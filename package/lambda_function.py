import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('VisitorCount')  # Use your table name

def lambda_handler(event, context):
    # Update and retrieve visitor count
    response = table.update_item(
        Key={'countID': '1'},  # Look up the item with countID "1"
        UpdateExpression="SET visitorCount = if_not_exists(visitorCount, :start) + :inc",
        ExpressionAttributeValues={':inc': 1, ':start': 0},
        ReturnValues="UPDATED_NEW"
    )

    # Return the updated visitor count
    visitor_count = response['Attributes']['visitorCount']
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Needed for frontend access
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'visitorCount': int(visitor_count)})
    }
