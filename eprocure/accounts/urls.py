from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

from accounts.forms import WhatYouDoForm,LocationInfoForm,CompanyProfileForm,LogoPicsForm,EventVideoForm,FirstForm,SecondForm,ThirdForm


app_name = 'accounts'

FORMS = [
    ('what_you_do', WhatYouDoForm),
    ('location_info', LocationInfoForm),
    ('company_profile', CompanyProfileForm),
    ('logo_pics', LogoPicsForm),
    ('event_video', EventVideoForm),
]

urlpatterns = [
    url(r'login/$',auth_views.LoginView.as_view(),name='login'),
    url(r'logout/$',auth_views.LogoutView.as_view(),name='logout'),
    # url(r'signup/$',views.SignUp.as_view(),name='signup'),
    url(r'signup/$',views.SignUp,name='signup'),
    # url(r'^vendorprofile/add/$',views.VendorProfileWizard.as_view(FORMS)),
    url(r'^create/$',views.MyWizard.as_view([FirstForm, SecondForm, ThirdForm]), name='wizards'),
    # url(r'^edit/(?P<id>\d+)/$',views.edit_wizard, name='edit_wizard'),
]
