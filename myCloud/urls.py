from django.urls import path,re_path
from . import views
urlpatterns = [

    path('', views.index, name='index'),
    path('/login', views.login, name='login'),
    path('/signUp', views.signUp, name='signUp'),
    path('/home', views.home, name='home'),
]

