from django.shortcuts import render
from .models import Post

def post_comment_create_list(request):
    qs = Post.objects.all()

    context = {
        'qs':qs,
    }

    return render(request, 'post/main.html', context)