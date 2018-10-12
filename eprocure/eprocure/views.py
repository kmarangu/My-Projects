from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView,CreateView,UpdateView,DetailView
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.decorators import login_required
# from django.db import transaction

# Added forms and models 200718
from accounts import forms
# from accounts import models
from accounts.models import User,VendorsProfile
from accounts.forms import UserCreateForm,VendorsProfileForm

class TestPage(LoginRequiredMixin, TemplateView):
    template_name = 'test.html'

    def get(self, request):
        my_vendorsprofile = VendorsProfile.objects.all()
        approvedstatus = VendorsProfile.approved

        args = {'my_vendorsprofile': my_vendorsprofile,
                'approvedstatus': approvedstatus}
        return render(request, self.template_name,args)

    def get_queryset(self):
        user = self.request.user
        approved = VendorsProfile.objects.filter(user=user)\
                         .values_list('VendorsProfile', flat=True)
        return Performance.objects.filter(VendorsProfile__in=approved)

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # if statement below should have 'and models.vendor_profile approved' then load accounts page otherwise load vendor_profile
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("test"))
        return super().get(request, *args, **kwargs)
