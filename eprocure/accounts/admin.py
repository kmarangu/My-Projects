from django.contrib import admin
from accounts.models import VendorsProfile,service_category,profile_approved
# Register your models here.
admin.site.register(VendorsProfile)
admin.site.register(service_category)
admin.site.register(profile_approved)
