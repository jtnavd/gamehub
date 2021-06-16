from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    # path('',views.index, name = 'index'),
    path('', views.home_view, name='main\home_view'),
]