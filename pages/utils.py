from django.shortcuts import render
from django.http import HttpResponse
import django, os
import requests
from datetime import datetime
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings
from profiles.models import Game, Profile
from django.contrib.auth.models import User

# user authenticator
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
    game_url = 'https://store.steampowered.com/api/appdetails'
    game_list = response.json()['response']['games']

    for game in game_list:
        params = {
            'appids':game['appid'],
        }

        if Game.objects.filter(steam_id=game['appid']).exists():
            continue

        response = requests.get(game_url, headers=headers, params=params)
        if response.status_code == 200:
            app_id = str(game['appid'])
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
                    except ValueError:
                        pass 
                    new_game.save()

def get_user_detail( user,
            key=settings.SOCIAL_AUTH_STEAM_API_KEY, 
            steam_id='76561197972495328'):
    user = User.objects.get()
    steam_id = user.social_auth.first().extra_data['player']['steamid']
    url = gen_url(interface='ISteamUser', method='GetPlayerSummaries', version='2')

    params = {
        'key':key,
        'steamids':steam_id,
    }
    headers = {
        'Content-Type':'application/x-www-form-urlencoded'
    }

    response = requests.get(url, params=params, headers=headers)
    user_data=response.json()['response']
    print(response.json())
    if user_data:
        new_user, created = Profile.objects.get_or_create(key=key, steam_id=steam_id)
        if created:
            new_user.steam_id = user_data['steamid']
            new_user.slug = user_data['personaname']
            new_user.avatar = user_data['avatar']
            new_user.save()

url = gen_url()
requests.get(url)

url = gen_url(method='GetPlayerBans')
gen_url(interface='ISteamUserStats', method='GetUserStatsForGame', version='2')
