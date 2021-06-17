from django.urls import path
from .views import post_comment_create_list

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_list, name='main-post-view')
]