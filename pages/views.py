from django.shortcuts import render
from django.http import HttpResponse
import django, os
import requests
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings
from .utils import get_game_list
from profiles.models import Game, Profile

def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def home_view(request):
    user = request.user
    get_game_list(request.user)
    context = {
        'user_t':user,
        # 'hello' :hello,
    }
    return render(request, 'main/home.html', context)


# RESPONSE TEST
# from django.http import HttpResponse
# from django.shortcuts import render

# def home_view(request):
#     user = request.user
#     hello = 'hello world'

#     context = {
#         'user_t':user,
#         'hello' :hello,
#     }
#     return render(request, 'main/home.html', context)
#     return HttpResponse('Hello world')


