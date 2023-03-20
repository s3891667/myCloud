from django.shortcuts import render
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.http import HttpResponse


def awsCloud():
    dynamodb = boto3.client('dynamodb', region_name='us-east-1',
                          aws_access_key_id='AKIAZ2A4PAUCTGBJCSXX',
                          aws_secret_access_key='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')
    response = dynamodb.list_tables()
    return response

def index(request):
    return render(request,'myCloud/index.html',{
        'data': awsCloud()
        })

