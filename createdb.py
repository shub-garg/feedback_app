import boto3
import config

session = boto3.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name= "us-west-2"
)

def create_table(dynamodb=None):
    if not dynamodb:
        dynamodb = session.resource('dynamodb')

    table = dynamodb.create_table(
        TableName='feedback_table',
        KeySchema=[
            {
                'AttributeName': 'timestamp',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'date',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'timestamp',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'date',
                'AttributeType': 'S'
                
            }
        

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    return table


if __name__ == '__main__':
    my_table = create_table()
    print("Table status:", my_table.table_status)