from django.db import models
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.files.storage import FileSystemStorage

lg = FileSystemStorage(location='/media/logo')
pp = FileSystemStorage(location='/media/profile_pic')
img = FileSystemStorage(location='/media/logo')

class VendorsProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # additional attributes you want to add to the table User
    service_category = models.ForeignKey(
        'service_category',
        on_delete=models.DO_NOTHING,
    )
    website_link = models.URLField(blank=True)
    phone_number = models.CharField(max_length=264,unique=False)
    logo = models.ImageField(upload_to='logo',blank=True,storage=lg)
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True,storage=pp)
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

    profile_approved = models.ForeignKey(
        'profile_approved',
        on_delete=models.DO_NOTHING,null=True
    )

    def __str__(self):
        return self.user.username


class service_category(models.Model):
    category = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category

class profile_approved(models.Model):
    approved = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.approved

# Wizard Test
class Item(models.Model):
    user=models.ForeignKey(User,
    on_delete=models.DO_NOTHING)
    price=models.DecimalField(max_digits=8,decimal_places=2)
    image=models.ImageField(upload_to="assets/",blank=True,storage=img)
    description=models.TextField(blank=True)

    def __unicode__(self):
        return '%s-%s' %(self.user.username, self.price)
