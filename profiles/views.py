from django.shortcuts import render
from .models import SocialProfile

def my_profile_view(request):
    profile = SocialProfile.objects.get(user=request.user)

    context = {
        'profile':profile,
    }

    return render(request, 'profiles/myprofile.html', context)

