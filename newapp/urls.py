from django.contrib import admin
from django.urls import path, include
from newapp import views
from django.views.decorators.csrf import csrf_exempt
from .views import *

urlpatterns = [
    path('', views.index),
]
