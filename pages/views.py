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
    context = {
        'active_nav':'login'
    }
    return render(request, 'login.html',context)

def game_list(request, *args, **kwwargs):
    game_list = Game.objects.all()
    context = {
        'game':game_list,
        'active_nav':"my-game-library"
    }
    return render(request, 'gamelist.html', context)
