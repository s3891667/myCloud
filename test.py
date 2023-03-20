import boto3
dynamodb = boto3.client('dynamodb', region_name='us-east-1',
                      aws_access_key_id='AKIAZ2A4PAUCTGBJCSXX',
                      aws_secret_access_key='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')


response = dynamodb.list_tables()

print(response)
