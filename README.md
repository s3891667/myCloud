# myCloud
## Project structure

├── cloudApp
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dbGenerator.py
├── manage.py
├── myCloud
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── __init__.py
│   │   └── __pycache__
│   ├── models.py
│   ├── static
│   │   └── myCloud
│   │       ├── css
│   │       └── javascript
│   ├── templates
│   │   └── myCloud
│   │       ├── home.html
│   │       ├── index.html
│   │       ├── index.html.save
│   │       ├── login.html
│   │       ├── musics.html
│   │       ├── musics.html.save
│   │       ├── query.html
│   │       ├── signUp.html
│   │       └── subscription.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── README.md
├── requirements.in
└── requirements.txt

## Overview
MyCloud is built using Django back-end, which interacts with AWS services, such as E2E, DyanmoDB,
API gateway and Lambda. The Website is being hosted on E2E ubuntu VM, using Gunicorn with Ngnix.

### Usage
The website allows the user to create account, therefore they are able to find songs, artists then subsribe 
to their favorites.
