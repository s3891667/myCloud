from django.shortcuts import render
import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from django.http import HttpResponse



def index(request):
    return render(request,'myCloud/index.html',{
        })


def login(request):
    return render(request, 'myCloud/login.html')


def signUp(request):
    if request.method =='POST':
        fname =request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
    return render(request,'myCloud/signUp.html')

def home(request):
    return render(request, 'myCloud/home.html')


def logout(request):
    try:
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/myCloud/login/')
