from django.urls import path
from .views import post_comment_create_list, like_unlike_post

app_name = 'posts'

urlpatterns = [
    path('', post_comment_create_list, name='main-post-view'),
    path('liked/', like_unlike_post, name='like-post-view'),
]