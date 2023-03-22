import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv
import requests
import botocore
load_dotenv()
# dynamodb = boto3.client('dynamodb', region_name=os.getenv('region'),
                      # aws_access_key_id=os.getenv('aws_access_key_id'),
                      # aws_secret_access_key=os.getenv('aws_secret_access_key')
                        # )
# response = dynamodb.list_tables()
url = 'https://bhv6323lr0.execute-api.us-east-1.amazonaws.com/deployGateway'
headers = {
    "Content-Type": "application/json"}
response = requests.get(url, headers=headers)







