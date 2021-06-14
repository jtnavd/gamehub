import requests
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gamehub.settings')
django.setup()
from django.conf import settings

def gen_url(interface='ISteamUser', 
            method='GetFriendList', 
            version='1', 
            key=settings.SOCIAL_AUTH_STEAM_API_KEY, 
            steam_id='76561197972495328'):
    	return f'https://api.steampowered.com/{interface}/{method}/v{version}/'


# django module settings


# use variable to call differents informations
url = gen_url()
# send request to info
requests.get(url)

# get information into db
url = gen_url(method='GetPlayerBans')
gen_url(interface='ISteamUserStats', method='GetUserStatsForGame', version='2')
print(url)
# 76561197972495328