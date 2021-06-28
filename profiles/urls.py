from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='all-profiles-view'),
    path('gamelist/', views.my_profile_view,name='my-profile-view'),
    path('myprofile/', views.my_profile_view,name='my-game-library'),
    path('my-invites/', views.invites_received_view, name='my-invites-view'),
    path('to-invite/', views.invite_profiles_list_view, name='invite-profiles-view'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friends/', views.remove_from_friends, name='remove-friends'),
    path('my-invites/accept/', views.accept_invitation, name='accept-invite'),
    path('my-invites/reject/', views.reject_invitation, name='reject-invite'),
    path('home/', views.home, name='home'),
]