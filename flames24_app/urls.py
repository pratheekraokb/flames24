# example/urls.py
from django.urls import path

from flames24_app import views


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
]