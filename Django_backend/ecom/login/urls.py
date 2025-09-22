
from django.urls import path
from django.urls import include
from . import views
from django.shortcuts import redirect

urlpatterns = [
    path('', views.login, name='login'),
    path('index', views.index, name='index'),
    path('register', views.register, name='register'),
]