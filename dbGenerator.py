import urllib.request
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr
import os
from dotenv import load_dotenv
import requests
import botocore
import base64
load_dotenv()


file = open('./a1.json', 'r')
data = json.loads(file.read())


def create_table(songs):
    '''This function will fisrt create a table for the musics'''
    client = boto3.client('dynamodb')
    table_creation_resp = client.create_table(
        TableName='music',
        KeySchema=[
            {
                'AttributeName': 'title',
                'KeyType': 'HASH'  # Partition Key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'title',
                'AttributeType': 'S'  # string data type
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': len(songs),
            'WriteCapacityUnits': len(songs)
        }
    )


# create_table(songs)


def createItem(songs):
    '''This loops through the music list then add song to the database'''
    client = boto3.resource('dynamodb', region_name='us-east-1')
    table_name = 'music'
    table = client.Table(table_name)
    for i in range(len(songs)):
        item = {
            'title': songs[i]['title'],
            'year': songs[i]['year'],
            'artist': songs[i]['artist'],
            'web_url': songs[i]['web_url'],
            'img_url': songs[i]['img_url']
        }
        # insert the item into the table
        create = table.put_item(TableName=table_name, Item=item)


# createItem(songs)


def download(songs):
    '''Downloading all the songs from link in the a1.json file'''
    folder_path = "./musicImgs"
    for i in range(len(songs)):
        print(i)
        url = songs[i]['img_url']
        file = (url.split('/')[-1]).split('.')[0]
        print(file)
        file_name = os.path.join(folder_path, url.split("/")[-1])
        urllib.request.urlretrieve(url, file_name)


# download(songs)


def uploadingFiles(songs):
    '''Uploading those file to the s3 bucket '''
    s3_client = boto3.client('s3')
    bucket = 'myartistbucket'
    folder_path = './musicImgs/'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            response = s3_client.upload_file(file_path, bucket, filename)


# uploadingFiles(songs)


def lambda_handler(event, context):
    client = boto3.client('dynamodb', region_name='us-east-1')
    title = "#40"
    year = ""
    artist = ""
    dataList = {'title': title, 'year': year, 'artist': artist}
    queryData = {}
    for key, value in dataList.items():
        if(value):
            queryData[key] = {
                'AttributeValueList': [{
                    'S': value
                }],
                'ComparisonOperator': 'EQ'
            }

    response = client.scan(TableName='music', ScanFilter=queryData)
    if(response['Items']):
        return {
            'body': [
                {
                    # remove the data type prefix
                    key: value[list(value.keys())[0]]
                    for key, value in item.items()
                }
                for item in response['Items']
            ]
        }
    return{
        'body': 'Error'
    }


print(lambda_handler({}, {}))
