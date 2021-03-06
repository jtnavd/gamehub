from django.core.exceptions import MultipleObjectsReturned
from django.db.models.fields import related_descriptors
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Profile, Relationship, Game
from .forms import ProfileModelForm
from datetime import datetime

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profile/detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for i in rel_receiver:
            rel_receiver.append(i.receiver.user)
        for i in rel_sender:
            rel_sender.append(i.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['posts'] = self.get_object().get_all_authors_post()
        context['len_posts'] = True if len(self.get_object().get_all_authors_post()) > 0 else False
        return context

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profile_list.html'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for i in rel_receiver:
            rel_receiver.append(i.receiver.user)
        for i in rel_sender:
            rel_sender.append(i.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

def my_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile':profile,
        'form': form,
        'confirm': confirm,
        "active_nav": "my-profile-view",
    }
    return render(request, 'profiles/myprofile.html', context)

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')

    else:
        return render(request,'profiles/detail.html', {'object':request.user.profile})

def logout(request):
    auth.logout(request)
    return redirect('/')

# need search bar ~~~~~~~~~~~~~~~~~~~~~~
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs': qs, 
                "active_nav": "all-profiles-view"}

    return render(request, 'profiles/profile_list.html', context)

# RELATION SYSTEM
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)
    results = list(map(lambda x: x.sender, qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {'qs': results,
                'is_empty': is_empty,
                "active_nav": "invite-profiles-view"
                }

    return render(request, 'profiles/to_invite_list.html', context)

def send_invitation(request):
    if request.method =='POST':
        pk= request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(user=user)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:my-profile-view')

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    context = {'qs': qs,
                "active_nav": "my-invites-view",
    }

    return render(request, 'profiles/my_invites.html', context)

def accept_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('profile:my-invites-view', context)

def reject_invitation(request):
    if request.method=='POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
        
    return redirect('profile:my-invites-view') 

def remove_from_friends(request):
    if request.method =='POST':
        pk= request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender)& Q(receiver=receiver)) | Q(sender=receiver) & Q(receiver=sender)
            )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profile:my-profile-view')

# GAME LIBRARY
def game_list(request):
    games = Game.objects.all()
    context = {
        'games':games,
        'active_nav':"my-game-library"
    }
    return render(request, 'pages/gamelist.html', context)