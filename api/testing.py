import boto3

# Create a DynamoDB client
dynamodb = boto3.client('dynamodb')

list(dynamodb.tables.all())
# Get the endpoint URL
# response = dynamodb.describe_endpoints()
# endpoint_url = response['Endpoints'][0]['Address']
# print("DynamoDB Endpoint URL:", endpoint_url)
