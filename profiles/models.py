from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from .utils import get_random_code
from django.template.defaultfilters import slugify
from datetime import datetime
from django.db.models import Q
from  django.templatetags.static import static

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
    avatar = models.ImageField(default=static('css/img/avatar.png'), upload_to='avatar/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    # Steam related
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    steam_id = models.CharField(max_length=200)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d-%m-%y')}"

    def get_absolute_url(self):
        return reverse("profiles:profile-detail-view", kwargs={"slug": self.slug})

    def get_friends(self):
        return self.friends.all()

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

    # init profile name ------verify
    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.user.first_name
        self.__initial_last_name = self.user.last_name

    def save(self, *args, **kwargs):
        ex = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name or selg.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.user.first_name) + " " + str(self.user.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + " " + str(get_random_code()))
                    ex = Profile.objects.filter(slug=to_slug).exists()

            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)


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
    steam_id = models.ManyToManyField(Profile)
    game_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    hours_played = models.IntegerField(null=True)
    release_date = models.DateTimeField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    # boolean owned????????????