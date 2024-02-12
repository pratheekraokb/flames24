# example/views.py
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request,"user_page/home.html")