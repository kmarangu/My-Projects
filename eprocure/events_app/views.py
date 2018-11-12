import os
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)

from formtools.wizard.views import SessionWizardView

from django.core.files.storage import FileSystemStorage

from django.conf import settings
from django.shortcuts import render_to_response
from django.shortcuts import render

from django.core.mail import send_mail

from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views import generic

from . import forms
from . import models

from django.views.generic import ListView,TemplateView,CreateView,UpdateView

from events_app.models import Group,GroupMember

from events_app.forms import (
                                ServiceCategoryForm,
                                ServiceCategoryFS1Form,
                                ServiceCategoryFS2Form,
                                CateringTypesForm,
                                StartersDesertsForm,
                                DietaryRequirementsForm,
                                BuffetTypesForm,
                                VenueTypeForm,
                                GuestsExpectedForm,
                                ChildrenCountForm,
                                PaymentTermsForm,
                                ServiceLevelForm,
                                EventTypeForm,
                                EventVenueForm,
                                EventDateForm,
                                MessageToVendorForm,
                                ContactMobileForm,
                                AuthorsRoleForm,
                                TermsConditionsForm,
        )

REQUESTS_TEMPLATES = {
    'service_category': 'requests/service_category.html',
    'service_category_FS1': 'requests/service_category.html',
    'service_category_FS2': 'requests/service_category.html',
    'authors_role': 'requests/authors_role.html',
    'catering_types': 'requests/catering_types.html',
    'children_count': 'requests/children_count.html',
    'contact_mobile': 'requests/contact_mobile.html',
    'event_date': 'requests/event_date.html',
    'event_type': 'requests/event_type.html',
    'event_venue': 'requests/event_venue.html',
    'guests_expected': 'requests/guests_expected.html',
    'message_to_vendor': 'requests/message_to_vendor.html',
    'payment_terms': 'requests/payment_terms.html',
    'terms_conditions': 'requests/terms_conditions.html',
    'service_level':'requests/service_level.html',
    'venue_type': 'requests/venue_type.html',
    'starters_deserts': 'requests/starters_deserts.html',
    'dietary_requirements': 'requests/dietary_requirements.html',
    'buffet_types': 'requests/buffet_types.html',
}

class FORMS_SET_1_Wizard(LoginRequiredMixin, SessionWizardView):
    model = Group
    registered = False
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def dispatch(self, request, *args, **kwargs):
        self.instance = Group()
        return super(FORMS_SET_1_Wizard, self).dispatch(request, *args, **kwargs)

    def get_form_instance(self, step):
        return self.instance

    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        return [REQUESTS_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
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
                              })

class FORMS_SET_2_Wizard(LoginRequiredMixin, SessionWizardView):
    model = Group
    registered = False
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'))

    def dispatch(self, request, *args, **kwargs):
        self.instance = Group()
        return super(FORMS_SET_2_Wizard, self).dispatch(request, *args, **kwargs)

    def get_form_instance(self, step):
        return self.instance

    def get_template_names(self):
        """
        Custom templates for the different steps
        """
        return [REQUESTS_TEMPLATES[self.steps.current]]

    def done(self, form_list, **kwargs):
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
                              })

class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ("name", "description")
    model = Group

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(LoginRequiredMixin, generic.ListView):
    model = Group
    # template_name = 'groups/group_base.html'

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("events_app:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)

        except IntegrityError:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("events_app:single",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):

        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )
        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)
