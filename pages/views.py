from django.shortcuts import render
from django.http import HttpResponse
import django, os
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings

def index(request):
    return render(request, 'index.html')

def home_view(request):
    user = request.user
    hello = 'hello world'

    context = {
        'user_t':user,
        'hello' :hello,
    }
    return render(request, 'main/home.html', context)

def gen_url(interface='ISteamUser', 
            method='GetFriendList', 
            version='1', 
            key=settings.SOCIAL_AUTH_STEAM_API_KEY, 
            steam_id='76561197972495328'):
    	return f'https://api.steampowered.com/{interface}/{method}/v{version}/'

# use variable to call differents informations
url = gen_url()
# send request to info
requests.get(url)

# get information into db
url = gen_url(method='GetPlayerBans')
gen_url(interface='ISteamUserStats', method='GetUserStatsForGame', version='2')

# gen_url(interface='ISteamUser', method='CheckAppOwnership', version='2')
print(gen_url()) 





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


