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

gen_url(interface='ISteamUser', method='CheckAppOwnership', version='2')
print(gen_url())

# # steam_id
# # 76561197972495328






# import requests

# class Game():

# # object pulling from steam friends list
# class Friend():
# 	original_profile = fk to profile
# 	steam_id = OneToOneField(Profile, on_delete=models.CASCADE, primary_key=True,)
# 	target_profile = null=True fk

# #  API cursor (check doc for parameters)
# def gen_url(interface='ISteamUser', method='GetFriendList', version='1', key=settings.STEAM_API_KEY, steam_id=''):
# 	return f'https://api.steampowered.com/{interface}/{method}/v{version}/'

# # loop through friends list
# def get_friends_list(profile):

# 	base_url = gen_url() + f'?api_key={settings.API_KEY}&steam_id={profile.user.social_auths.first().extra_data['player']['steamid']}'
# 	response = requests.get(base_url)
#     # check if the token pass
# 	if response.status_code == 200:
#         # pull json format of friends profile informations
# 		for friend_dict in response.json():
#             #  create profile object with all informations provided
# 			Friend.objects.get_or_create(original_profile=profile, steam_id=friend_dict['player']['steamid'])
# new_profile = Profile.objects.create(user=user)
# get_friends_list(new_profile)
# gen_url()
# gen_url(method='GetPlayerBans')