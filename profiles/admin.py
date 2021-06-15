from django.contrib import admin
from .models import Relationship, SocialProfile

admin.site.register(SocialProfile)
admin.site.register(Relationship)