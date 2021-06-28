from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.login, name='login'),
    path('profiles/', views.game_list, name='game-list')
    # path('',views.index, name = 'index'),
]