from django.shortcuts import render
from django.http import HttpResponse
import django, os
import requests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings

def gen_url(interface='ISteamUser', 
            method='GetFriendList', 
            version='1'):
    	return f'https://api.steampowered.com/{interface}/{method}/v{version}/'


def get_game_list(user, 
            key=settings.SOCIAL_AUTH_STEAM_API_KEY, 
            steam_id='76561197972495328'):
    steam_id = user.social_auth.first().extra_data['player']['steamid']
    url = gen_url(interface='IPlayerService', method='GetOwnedGames')
    print(url)

    params = {
        'key':key,
        'steamid':steam_id,
    }
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)
    
    games_list = response.json()['response']['games']

    game_url = gen_url(interface='IStoreService', method='GetAppInfo')

    # for game in game_list:
    #     params = {
    #         'key':key,
    #         'appid':appid,
    #     }
    #     response = requests.get(url, params=params)
    #     print(game)


# https://api.steampowered.com/IStoreService/GetAppInfo/v1/?
# ##############################################################################################
def get_game_name(appid, name):
    pass
    
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



# use variable to call differents informations
url = gen_url()
# send request to info
requests.get(url)

# get information into db
url = gen_url(method='GetPlayerBans')
gen_url(interface='ISteamUserStats', method='GetUserStatsForGame', version='2')



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


