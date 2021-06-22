from django.shortcuts import render
from django.http import HttpResponse
import django, os
import requests
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings
from profiles.models import Game, Profile

def gen_url(interface='ISteamUser', 
            method='GetFriendList', 
            version='1'):
    	return f'https://api.steampowered.com/{interface}/{method}/v{version}/'


def get_game_list(user, 
            key=settings.SOCIAL_AUTH_STEAM_API_KEY, 
            appid='',
            steam_id='76561197972495328'):
    steam_id = user.social_auth.first().extra_data['player']['steamid']
    url = gen_url(interface='IPlayerService', method='GetOwnedGames')

    params = {
        'key':key,
        'steamid':steam_id,
        'appid':appid,
    }
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }
    response = requests.get(url, params=params, headers=headers)
    print(response.status_code)

    # game_url = gen_url(interface='IStoreService', method='GetAppInfo') <--- old
    game_url = 'https://store.steampowered.com/api/appdetails'
    print(game_url)
 
    games_list = response.json()['response']['games']

    for game in games_list:
        print(game)
        params = {
            # 'key':key,
            # 'steamid':steam_id,
            'appids':game['appid'],
            
        }
        response = requests.get(game_url, headers=headers, params=params)
        # print(response.json())
        if response.status_code == 200:
            app_id = str(game['appid'])
            # if response.json()[game['appid']]:
            game_data=response.json()[app_id].get("data")
            if game_data:
                new_game, created = Game.objects.get_or_create(steam_id=game['appid'])
                if created:
                    new_game.game_name = game_data["name"]
                    new_game.description = game_data["detailed_description"]
                    new_game.image = game_data["header_image"]
                    # new_game.hours_played = game["playtime_forever"]
                    try :
                        date = datetime.strptime(game_data["release_date"]["date"], "%d %b, %Y")
                        new_game.release_date = date
                    # “19 Dec, 2008”
                    except ValueError:
                        pass 
                    new_game.save()
        

# https://store.steampowered.com/api/appdetails?appids=218620

# https://api.steampowered.com/IStoreService/GetAppInfo/v1/?
    
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


