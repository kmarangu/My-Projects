from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404

from django.views.generic import CreateView
from formtools.wizard.views import SessionWizardView

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.core.mail import send_mail

from django.shortcuts import render
from . import forms
from . import models

from accounts.forms import UserCreateForm,VendorsProfileForm,WhatYouDoForm,LocationInfoForm,CompanyProfileForm,LogoPicsForm,EventVideoForm,FirstForm,SecondForm,ThirdForm

TEMPLATES = {
    'what_you_do': 'registration/what-you-do.html',
    'location_info': 'registration/location-info.html',
    'company_profile': 'registration/company-profile.html',
    'logo_pics': 'registration/logo-pics.html',
    'event_video': 'registration/event-video.html',
}

class VendorProfileWizard(SessionWizardView):

    file_storage = models.lg, models.pp

    instance = None

    def get_form_instance(self, step):
        """
        Provides us with an instance of the Model to save on completion
        """
        if self.instance is None:
            self.instance = VendorsProfile()
        return self.instance

    def done(self, form_list, **kwargs):
        """
        Save info to the DB
        """
        vendors_profile = self.instance
        vendors_profile.save()

    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        return [TEMPLATES[self.steps.current]]


# Full VendorsProfile model saving function
def SignUp(request):

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

# Wizards view test
class MyWizard(SessionWizardView):
    template_name = "registration/wizard_form.html"
    file_storage = models.img
    instance = Item()

    def dispatch(self, request, *args, **kwargs):
        return super(MyWizard, self).dispatch(request, *args, **kwargs)

    def get_form_instance(self, step):
        return self.instance

    def done(self, form_list, **kwargs):
        self.save_model()
        return render_to_response('done.html')


# class MyWizard(SessionWizardView):
#     template_name = "registration/wizard_form.html"
#     file_storage = models.img
#     #if you are uploading files you need to set FileSystemStorage
#     def done(self, form_list, **kwargs):
#         for form in form_list:
#            print(form.initial)
#         if not self.request.user.is_authenticated:
#                 raise Http404
#         id = form_list[0].cleaned_data['id']
#         try:
#                 item = Item.objects.get(pk=id)
#                 ######################   SAVING ITEM   #######################
#                 item.save()
#                 print(item)
#                 instance = item
#         except:
#                 item = None
#                 instance = None
#         if item and item.user != self.request.user:
#                 print("about to raise 404")
#                 raise Http404
#         if not item:
#                 instance = Item()
#                 for form in form_list:
#                     for field, value in form.cleaned_data.iteritems():
#                         setattr(instance, field, value)
#                 instance.user = self.request.user
#                 instance.save()
#                 return render_to_response('wizard-done.html',{ 'form_data': [form.cleaned_data for form in form_list], })
#
#
# def edit_wizard(request, id):
#     #get the object
#     item = get_object_or_404(Item, pk=id)
#     #make sure the item belongs to the user
#     if item.user != request.user:
#         raise HttpResponseForbidden()
#     else:
#         #get the initial data to include in the form
#         initial = {'0': {'id': item.id,
#                          'price': item.price,
#                          #make sure you list every field from your form definition here to include it later in the initial_dict
#         },
#                    '1': {'image': item.image,
#                    },
#                    '2': {'description': item.description,
#                    },
#         }
#         print(initial)
#         form = MyWizard.as_view([FirstForm, SecondForm, ThirdForm], initial_dict=initial)
#         return form(context=RequestContext(request), request=request)
