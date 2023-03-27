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
    final_data = []
    print(len(songs))
    for i in range(len(songs)):
        tmp_data = {
        }
        tmp_data['title'] = names[i].replace("_", " ")
        tmp_data['year'] = songs[names[i]]['Year']
        tmp_data['artist'] = songs[names[i]]['Artist']
        final_data.append(tmp_data)

    return final_data


def apiGateWay(email, password):
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
    if 'user' in request.session:
        return redirect('home/')
    else:
        return render(request, 'myCloud/index.html')


def login(request):
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
    if 'user' not in request.session:
        return redirect('/myCloud/')
    else:
        current_user = request.session['user']
        return render(request, 'myCloud/home.html', {'current_user': current_user})


def logout(request):
    try:
        request.session.flush()
    except:
        return redirect('/login/')
    return redirect('/myCloud/login/')


def addingSong(data, user_email):
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
    # this area will display everything, such as images and its information
    # User will allow to subscribe the the music thereby I will display in their section

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
    if 'user' not in request.session:
        return redirect('/myCloud/login/')
    if request.method == 'POST':
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
    final_data = restructureData(subscription, list(subscription))

    paginator = Paginator(final_data, 10)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    current_user = request.session['user']

    return render(request, "myCloud/subscription.html", {
        'songs': page_object,
        'current_user': current_user})


def query(request):
    if 'user' not in request.session:
        return redirect('/myCloud/login/')
    current_user = request.session['user']
    if request.method == 'POST':
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
            song = (json.loads(value)['body'])
            if (type(song) == list):
                artist_retrieved = song[0]['artist']
                img_url = f'https://xwjymmmd28.execute-api.us-east-1.amazonaws.com/getSongs/subscribe?artist={artist_retrieved}'
                img = requests.get(img_url)
                return render(request, "myCloud/query.html", {
                    "current_user": current_user,
                    "songs": song,
                    "img": img.text
                })
            return render(request, "myCloud/query.html", {
                "current_user": current_user,
                "mess": song
            })

        else:
            data = json.loads(request.POST.get('song'))
            user_email = request.session['user_email']
            response_data = addingSong(data, user_email)
            print(response_data)
            return render(request, "myCloud/query.html", {
                "current_user": current_user,
                "mess": json.loads(response_data.text)['body']
            })
    return render(request, "myCloud/query.html", {
        "current_user": current_user
    })
