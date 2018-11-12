import os
from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.utils import timezone
from django.urls import reverse

from multiselectfield import MultiSelectField
from events_app.models import SERVICES

from django import template
register = template.Library()

class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return "@{}".format(self.username)


class VendorsProfile(models.Model):

    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    # additional attributes you want to add to the table User
    # service_category = models.ManyToManyField('service_category')
    service_category = MultiSelectField(choices=SERVICES, max_choices=10)
    website_link = models.URLField(blank=True)
    phone_number = models.IntegerField(unique=False)
    logo = models.ImageField(upload_to='logo',blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    facebook_page = models.CharField(max_length=264,unique=False)
    twitter_page = models.CharField(max_length=264,unique=False)
    address_one = models.CharField(max_length=264,unique=False)
    address_two = models.CharField(max_length=264,unique=False)
    town_city = models.CharField(max_length=264,unique=False)
    country = models.CharField(max_length=264,unique=False)
    postal_address = models.CharField(max_length=264,unique=False)
    pin_number = models.CharField(max_length=264,unique=False)
    b_type = models.CharField(max_length=264,unique=False)
    payments_accepted = models.CharField(max_length=264,unique=False)
    insurance = models.CharField(max_length=3,unique=False)
    brief = models.CharField(max_length=264,unique=False)
    description = models.TextField(max_length=2000,unique=False)
    typical_clients = models.CharField(max_length=264,unique=False)
    location = models.CharField(max_length=264,unique=False,default="")
    service_area = models.CharField(max_length=264,unique=False)
    video_url = models.CharField(max_length=264,unique=False,default="video url")
    video_description = models.CharField(max_length=264,unique=False,default="description")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class service_category(models.Model):
    category = models.CharField(max_length=1000,unique=True)

    def __str__(self):
        return self.category

class profile_approved(models.Model):
    approved = models.CharField(max_length=5,unique=True)

    def __str__(self):
        return self.approved
