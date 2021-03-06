from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from .utils import get_random_code
from django.template.defaultfilters import slugify
from datetime import datetime
from django.db.models import Q
from django.templatetags.static import static

class ProfileManager(models.Manager):
    def get_all_profiles_to_invite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
        print(qs)

        accepted = set([])
        for rel in qs:
            if rel.status == 'accepted':
                accepted.add(rel.receiver)
                accepted.add(rel.sender)
        print(accepted)

        available = [profile for profile in profiles if profile not in accepted]
        print(available)
        return available

    def get_all_profiles(self, me):
        return Profile.objects.all().exclude(user=me)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio...', max_length=500)
    # email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.URLField(default=static('css/img/avatar.png'))
    friends = models.ManyToManyField('self', blank=True, symmetrical=False)
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    game_list = models.ManyToManyField('Game')
    steam_id = models.CharField(max_length=200)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_profile_picture(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static('css/img/avatar.png')

    def get_friends_number(self):
        return self.friends.all().count()

    def get_post_numder(self):
        return self.posts.all().count()

    def get_all_authors_post(self):
        return self.posts.all()

    def get_likes_given(self):
        likes = self.like_set.all()
        total_liked = 0
        for i in likes:
            if i.value=='like':
                total_liked += 1
        return total_liked

    def get_likes_recieved(self):
        posts = self.posts.all()
        total_liked = 0
        for i in posts:
            total_liked += i.liked.all().count()
        return total_liked

STATUS_CHOICES = (
    ('send', 'send'),
    ('acepted', 'accepted'),
)

class RelationshipManager(models.Manager):
    def invitations_received(self, receiver):
        qs = Relationship.objects.filter(receiver=receiver, status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='reciever')
    status = models.CharField(max_length=200, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

class Game(models.Model):
    steam_id = models.IntegerField(unique=True)
    game_name = models.CharField(max_length=200,null=True)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(null=True)
    # hours_played = models.IntegerField(null=True)
    release_date = models.DateField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)