import unicodedata

from django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.text import capfirst
from django.utils.translation import gettext, gettext_lazy as _

from events_app.models import SERVICES

UserModel = get_user_model()

from django import forms

from django.contrib.auth.forms import UserCreationForm
from accounts.models import VendorsProfile, service_category

class ReadOnlyPasswordHashWidget(forms.Widget):
    template_name = 'auth/widgets/read_only_password_hash.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        summary = []
        if not value or value.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary.append({'label': gettext("No password set.")})
        else:
            try:
                hasher = identify_hasher(value)
            except ValueError:
                summary.append({'label': gettext("Invalid password format or unknown hashing algorithm.")})
            else:
                for key, value_ in hasher.safe_summary(value).items():
                    summary.append({'label': gettext(key), 'value': value_})
        context['summary'] = summary
        return context


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super().__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

    def has_changed(self, initial, data):
        return False


class UsernameField(forms.CharField):
    def to_python(self, value):
        return unicodedata.normalize('NFKC', super().to_python(value))

class UserCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label= ("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text= ("Enter the same password as before, for verification."),
    )
    class Meta():
        model = get_user_model()
        fields = ("username","first_name","last_name", "email", "password1", "password2")
        field_classes = {'username': UsernameField}

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({'autofocus': True})

        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text= (
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )

    class Meta:
        model = User
        fields = '__all__'
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

        # Set the max length and label for the "username" field.
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        self.fields['username'].max_length = self.username_field.max_length or 254
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.
        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.
        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):
        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label= ("Email"), max_length=254)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()

    def get_users(self, email):
        """Given an email, return matching user(s) who should receive a reset.
        This allows subclasses to more easily customize the default policies
        that prevent inactive users and users with unusable passwords from
        resetting their password.
        """
        active_users = UserModel._default_manager.filter(**{
            '%s__iexact' % UserModel.get_email_field_name(): email,
            'is_active': True,
        })
        return (u for u in active_users if u.has_usable_password())

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None, html_email_template_name=None,
             extra_email_context=None):
        """
        Generate a one-use only link for resetting password and send it to the
        user.
        """
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            context = {
                'email': email,
                'domain': domain,
                'site_name': site_name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name, email_template_name, context, from_email,
                email, html_email_template_name=html_email_template_name,
            )

class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label= ("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label= ("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
class PasswordChangeForm(SetPasswordForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    error_messages = {
        **SetPasswordForm.error_messages,
        'password_incorrect': ("Your old password was entered incorrectly. Please enter it again."),
    }
    old_password = forms.CharField(
        label= ("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': True}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

class AdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label= ("Password"),
        widget=forms.PasswordInput(attrs={'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label= ("Password (again)"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    @property
    def changed_data(self):
        data = super().changed_data
        for name in self.fields:
            if name not in data:
                return []
        return ['password']


B_TYPE=[('SP','Sole Proprietor'),
        ('LC','Limited Company'),
        ('PS','Partnership'),
        ('LLP','Limited Liability Partnership'),
        ('PLC','Public Limited Company'),
        ('CH','Charity'),
        ]

PAYMENTS_ACCEPTED=[('MPESA','Mpesa'),
                   ('CASH','Cash'),
                   ('CHEQUE','Cheque'),
                   ('RTGS','RTGS Transfer'),
                   ('PAYPAL','paypal'),
                   ('VISA','Visa'),
                   ('MASTERCARD','Mastercard'),
                   ('AMEX','American Express'),
                   ]

INSURANCE=[('YES','Yes'),
           ('NO','No'),
            ]

SERVICE_AREA=[('10','10 KILOMETERS'),
              ('20','20 KILOMETERS'),
              ('30','30 KILOMETERS'),
              ('40','40 KILOMETERS'),
              ('50','50 KILOMETERS'),
              ('60','60 KILOMETERS'),
              ('70','70 KILOMETERS'),
              ('80','80 KILOMETERS'),
              ('90','90 KILOMETERS'),
              ('100','100 KILOMETERS'),
              ('COUNTY WIDE','COUNTY WIDE'),
              ('COUNTRY WIDE','COUNTRY WIDE'),
                   ]

class VendorsProfileForm(forms.ModelForm):

    b_type = forms.ChoiceField(required=True,choices=B_TYPE, widget=forms.RadioSelect())
    payments_accepted = forms.MultipleChoiceField(required=True,choices=PAYMENTS_ACCEPTED, widget=forms.CheckboxSelectMultiple())
    insurance = forms.ChoiceField(required=True,choices=INSURANCE,widget=forms.RadioSelect())
    service_area = forms.ChoiceField(required=True,choices=SERVICE_AREA,widget=forms.Select())

    class Meta():
        model = VendorsProfile
        fields = ('service_category','website_link','profile_pic','logo','phone_number','facebook_page','twitter_page','address_one','address_two','town_city','country','postal_address',
                'pin_number','b_type','payments_accepted','insurance','brief','description','typical_clients','location','service_area','video_url','video_description')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['service_category'].label = 'Services that you offer'
        self.fields['website_link'].label = 'Website Address'
        self.fields['profile_pic'].label = 'Images of your business services'
        self.fields['logo'].label = 'Company Logo'
        self.fields['phone_number'].label = 'Telephone Number'
        self.fields['facebook_page'].label = 'Facebook page'
        self.fields['twitter_page'].label = 'Twitter Handle'
        self.fields['address_one'].label = 'Physical Address Line 1'
        self.fields['address_two'].label = 'Physical Address Line 2'
        self.fields['town_city'].label = 'City / Town'
        self.fields['country'].label = 'Country'
        self.fields['postal_address'].label = 'Postal Address'
        self.fields['pin_number'].label = 'PIN Number'
        self.fields['b_type'].label = 'Business Type'
        self.fields['payments_accepted'].label = 'Payments Accepted by your company'
        self.fields['insurance'].label = 'Do you have Insurance for your service'
        self.fields['brief'].label = 'Brief Description of your business'
        self.fields['description'].label = 'Description of your business'
        self.fields['typical_clients'].label = 'What are your Typical Clients'
        self.fields['location'].label = 'Business Location'
        self.fields['service_area'].label = 'What area are you able to service from your location'
        self.fields['video_url'].label = 'Add a link of your Youtube or Vimeo video.'
        self.fields['video_description'].label = 'Add a description for the video'


class WhatYouDoForm(forms.ModelForm):

    service_category = forms.MultipleChoiceField(required=True,choices=SERVICES,widget=forms.SelectMultiple(attrs={'class':'form-control','id':'exampleFormControlSelect2','size':'20'}))

    class Meta():
        model = VendorsProfile
        fields = ('brief','description','typical_clients','service_category')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['brief'].label = 'Name of your business?'
        self.fields['description'].label = 'Brief description of your business'
        self.fields['typical_clients'].label = 'Who are your Typical Clients'
        self.fields['service_category'].label = 'Select the services that you offer, (press CTRL to select Multiple)'

class LocationInfoForm(forms.ModelForm):

    service_area = forms.ChoiceField(required=True,choices=SERVICE_AREA,widget=forms.Select())

    class Meta():
        model = VendorsProfile
        fields = ('location','service_area')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['location'].label = 'Business Location'
        self.fields['service_area'].label = 'What area radius are you able to service from your location'

class CompanyProfileForm(forms.ModelForm):

    website_link = forms.URLField(widget=forms.URLInput(attrs={'class':'form-control','id':'inputAddress','placeholder':'Website Address'}))
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control','id':'inputAddress','placeholder':'Phone Number'}))
    b_type = forms.ChoiceField(choices=B_TYPE, widget=forms.RadioSelect())
    payments_accepted = forms.MultipleChoiceField(required=True,choices=PAYMENTS_ACCEPTED, widget=forms.CheckboxSelectMultiple())
    insurance = forms.ChoiceField(required=True,choices=INSURANCE,widget=forms.RadioSelect())

    class Meta():
        model = VendorsProfile
        fields = ('website_link','phone_number','facebook_page','twitter_page','address_one','address_two','town_city','country','postal_address',
                'pin_number','b_type','payments_accepted','insurance')

    def __init__(self,*args,**kwargs):
        super(CompanyProfileForm, self).__init__(*args,**kwargs)

        self.fields['website_link'].label = 'Website Address'
        self.fields['phone_number'].label = 'Telephone Number'
        self.fields['facebook_page'].label = 'Facebook page'
        self.fields['twitter_page'].label = 'Twitter Handle'
        self.fields['address_one'].label = 'Physical Address Line 1'
        self.fields['address_two'].label = 'Physical Address Line 2'
        self.fields['town_city'].label = 'City / Town'
        self.fields['country'].label = 'Country'
        self.fields['postal_address'].label = 'Postal Address'
        self.fields['pin_number'].label = 'PIN Number'
        self.fields['b_type'].label = 'Business Type'
        self.fields['payments_accepted'].label = 'Payments Accepted by you'
        self.fields['insurance'].label = 'Do you have Insurance for your service'

class LogoPicsForm(forms.ModelForm):
    class Meta():
        model = VendorsProfile
        fields = ('profile_pic','logo')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['profile_pic'].label = 'Company Logo or Your Profile Picture'
        self.fields['logo'].label = 'Company Logo'

class EventVideoForm(forms.ModelForm):
    class Meta():
        model = VendorsProfile
        fields = ('video_url','video_description')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['video_url'].label = 'Add a link of your Youtube or Vimeo video.'
        self.fields['video_description'].label = 'Add a description for the video'
