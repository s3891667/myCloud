import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv
load_dotenv()

dynamodb = boto3.client('dynamodb', region_name=os.getenv('region'),
                      aws_access_key_id=os.getenv('aws_access_key_id'),
                      aws_secret_access_key=os.getenv('aws_secret_access_key')
                        )

# print(os.load_dotenv('region'))
response = dynamodb.list_tables()

print(dynamodb)




# def lambda_handler(event, context):
    # client = boto3.resource('dynamodb', region_name=os.load_dotenv('region'))
    # table = client.Table('login')   
    # response =table.query(KeyConditionExpression=Key('cloudUser').eq('s38916670@student.rmit.edu.au'))
    # items=response['Items']
    # # print(items)
    # print(response)
    # return {
        # 'statusCode': 200,
        # 'body': items
      # }


# import os
# from dotenv import load_dotenv
# load_dotenv()
# test = os.getenv('region')

# print(test)

# print(lambda_handler({},{}))
