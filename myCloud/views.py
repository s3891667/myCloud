from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.sessions.backends.base import *
from django.core.paginator import Paginator
import json
import requests
import boto3
import os
from dotenv import load_dotenv
load_dotenv()


def restructureData(songs, names):
    '''This function will generate a list based on the format of Django 
    pagination from songs dictionary and songs' names list'''
    final_data = []
    for i in range(len(songs)):
        tmp_data = {
        }
        tmp_data['title'] = names[i].replace("_", " ")
        tmp_data['year'] = songs[names[i]]['Year']
        tmp_data['artist'] = songs[names[i]]['Artist']
        final_data.append(tmp_data)

    return final_data


def apiGateWay(email, password):
    '''Calling the api to login and get Session for user '''
    url = 'https://xwjymmmd28.execute-api.us-east-1.amazonaws.com/rmit/?student=' + email
    headers = {
        "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.text
    parse_json = json.loads(data)
    if not parse_json:
        return False
    if(parse_json[0]['email'] == email and parse_json[0]['password'] == password):
        user_name = parse_json[0]['user_name']
        return user_name
    return False


def index(request):
    '''Index page view'''
    if 'user' in request.session:
        return redirect('home/')
    else:
        return render(request, 'myCloud/index.html')


def login(request):
    '''Login page view'''
    if 'user' in request.session:
        return redirect('/myCloud/home/')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('pw')
        user_name = apiGateWay(email, password)
        if (user_name != False):
            request.session['user_email'] = email
            request.session['user'] = user_name
            return redirect('/myCloud/home/', {'current_user': user_name})
        else:
            return render(request, 'myCloud/login.html',
                          {"message": "Email or password is invalid"})
    return render(request, 'myCloud/login.html')


def signUp(request):
    '''Signup page view'''
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        email = request.POST.get('email')
        password = request.POST.get('pw')
        data = {
            "cloudUser": email,
            "email": email,
            "user_name": user_name,
            "password": password
        }
        url = 'https://xwjymmmd28.execute-api.us-east-1.amazonaws.com/signup/createaccount'
        response = requests.post(url, json=data)
        announcement = response.json()
        return render(request, 'myCloud/signUp.html', {'announcement': announcement['body']})
    return render(request, 'myCloud/signUp.html')


def home(request):
    '''Home page view'''
    if 'user' not in request.session:
        return redirect('/myCloud/')
    else:
        current_user = request.session['user']
        return render(request, 'myCloud/home.html', {'current_user': current_user})


def logout(request):
    '''Logout feature'''
    try:
        # This will delete the session values
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/myCloud/login/')


def addingSong(data, user_email):
    '''Function that trigger API to add song to subscription list for the user'''
    title = data['title']
    year = data['year']
    url = 'https://qd7wgwpns8.execute-api.us-east-1.amazonaws.com/updateSubscription/'
    # now  we will call an api with the attribute song thereby interacting and add it into the users vaforite map
    response = requests.post(url, json={
        "song": title,
        "user_email": user_email,
        "year": year
    })
    return response


def musics(request):
    '''Function calling API to retrieve music from the music table
    Instead of searching from the query section the user can view everything and 
    select subscribe'''
    # Note that this is my additional feature; However, the hosted website got errors,
    # So this can be ignored
    if 'user' not in request.session:
        return redirect('/myCloud/login')
    else:
        if request.method == 'POST':
            data = json.loads(request.POST.get('song'))
            user_email = request.session['user_email']
            addingSong(data, user_email)
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('music')
        data = [table.scan()][0]['Items']

        paginator = Paginator(data, 50)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        current_user = request.session['user']
        return render(request, 'myCloud/musics.html', {
            'songs': page_object,
            'current_user': current_user
        })


def subscription(request):
    '''Subscription view'''
    if 'user' not in request.session:
        return redirect('/myCloud/login/')
    if request.method == 'POST':
        # Removing songs
        song_title = json.loads(request.POST.get('song'))['title']
        user_email = request.session['user_email']
        url = 'https://u1gz12fny5.execute-api.us-east-1.amazonaws.com/removeSong/'
        response = requests.post(url, json={
            "songTitle": song_title.replace(" ", "_"),
            "userEmail": user_email
        })

    user = request.session['user_email']
    url = 'https://xwjymmmd28.execute-api.us-east-1.amazonaws.com/rmit/?student='+user

    headers = {
        "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    data = response.text
    parse_json = json.loads(data)
    subscription = parse_json[0]['subscription']
    # Restructuring the fetched values to create a list of json variables
    final_data = restructureData(subscription, list(subscription))
    # After fetching for all the in the subscription section of the user and parse it to final_data,
    # Django paginator will display it
    paginator = Paginator(final_data, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    current_user = request.session['user']

    return render(request, "myCloud/subscription.html", {
        'songs': page_object,
        'current_user': current_user})


def query(request):
    '''Query view'''
    if 'user' not in request.session:
        return redirect('/myCloud/login/')
    current_user = request.session['user']
    if request.method == 'POST':
        # When the user is press the query button
        if 'query' in request.POST:
            title = request.POST.get('title')
            year = request.POST.get('year')
            artist = request.POST.get('artist')
            data = {
                "title": title,
                "year": year,
                "artist": artist
            }
            url = 'https://118tvo0o7g.execute-api.us-east-1.amazonaws.com/querying'
            response = requests.post(url, json=data)

            value = response.text
            song = json.loads(value)['body']

            # If the song is valid it will return a list
            if (type(song) == list):
                paginator = Paginator(song, 50)
                page_number = request.GET.get('page')
                # using Django paginator to display data into to front-end
                page_object = paginator.get_page(page_number)
                return render(request, "myCloud/query.html", {
                    "current_user": current_user,
                    "songs": page_object,
                })
            # else only return a message that the song does not exist
            return render(request, "myCloud/query.html", {
                "current_user": current_user,
                "mess": song
            })
        # When the user press subscribe
        else:
            data = json.loads(request.POST.get('song'))
            user_email = request.session['user_email']
            response_data = addingSong(data, user_email)
            return render(request, "myCloud/query.html", {
                "current_user": current_user,
                "mess": json.loads(response_data.text)['body']
            })
    return render(request, "myCloud/query.html", {
        "current_user": current_user
    })
