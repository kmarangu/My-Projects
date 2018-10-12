import os
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import CreateView

from formtools.wizard.views import SessionWizardView

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render_to_response

from django.core.mail import send_mail

from django.shortcuts import render
from . import forms
from . import models

from django.views.generic import ListView,TemplateView,CreateView,UpdateView

from accounts.models import VendorsProfile,User
from accounts.forms import UserCreateForm,VendorsProfileForm,WhatYouDoForm,LocationInfoForm,CompanyProfileForm,LogoPicsForm,EventVideoForm

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class VendorDashboard(LoginRequiredMixin, TemplateView):
    template_name = 'registration/vendor-dashboard.html'

TEMPLATES = {
    'what_you_do': 'registration/what-you-do.html',
    'location_info': 'registration/location-info.html',
    'company_profile': 'registration/company-profile.html',
    'logo_pics': 'registration/logo-pics.html',
    'event_video': 'registration/event-video.html',
}

class VendorProfileWizard(LoginRequiredMixin, SessionWizardView):
    registered = False
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def dispatch(self, request, *args, **kwargs):
        self.instance = VendorsProfile()
        return super(VendorProfileWizard, self).dispatch(request, *args, **kwargs)

    def get_form_instance(self, step):
        return self.instance

    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
        vendor_profile = VendorProfile(data=request.POST)
        # Set One to One relationship between
        # model user = Form user
        self.instance.user = self.request.user
        # Now save model
        self.instance.save()
        # Registration Successful!
        registered = True
        # Page to render
        return HttpResponseRedirect(reverse("test"),
                              {
                              'registered':registered,
                              'vendor_profile':vendor_profile
                              })



# Full VendorsProfile model saving function
def VendorSignUp(request):

    registered = False

    if request.method == 'POST':
        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserCreateForm(data=request.POST)
        profile_form = VendorsProfileForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!
            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserCreateForm and VendorsProfileForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserCreateForm()
        profile_form = VendorsProfileForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'registration/signup.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})
