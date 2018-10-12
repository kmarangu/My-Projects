from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from accounts.forms import UserCreateForm,WhatYouDoForm,LocationInfoForm,CompanyProfileForm,LogoPicsForm,EventVideoForm


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
    url(r'signup/$',views.SignUp.as_view(),name='signup'),
    url(r'^vendorprofile/add/$',views.VendorProfileWizard.as_view(FORMS),name='vendorprofile'),
    url(r'^vendordashboard/$', views.VendorDashboard.as_view(), name="vendordashboard"),
]
