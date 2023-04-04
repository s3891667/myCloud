from django.urls import path, re_path
from . import views
app_name = 'myCloud'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signUp/', views.signUp, name='signUp'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('musics/', views.musics, name='musics'),
    path('query/', views.query, name='query'),
    path('subscription/', views.subscription, name='subscription'),

]
