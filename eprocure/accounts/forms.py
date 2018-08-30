from django import forms
from django.contrib.auth import get_user_model
#used for creating user accounts
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from accounts.models import VendorsProfile, Item

class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email Address'
        self.fields['password'].label = 'Enter Password'
        # self.fields['password2'].label = 'Re-Enter Password'

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
    class Meta():
        model = VendorsProfile
        fields = ('brief','description','typical_clients','service_category')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['brief'].label = 'Brief Description of your business'
        self.fields['description'].label = 'Description of your business'
        self.fields['typical_clients'].label = 'What are your Typical Clients'
        self.fields['service_category'].label = 'Services that you offer'

class LocationInfoForm(forms.ModelForm):
    class Meta():
        model = VendorsProfile
        fields = ('location','service_area')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['location'].label = 'Business Location'
        self.fields['service_area'].label = 'What area are you able to service from your location'

class CompanyProfileForm(forms.ModelForm):

    b_type = forms.ChoiceField(choices=B_TYPE, widget=forms.RadioSelect())
    payments_accepted = forms.MultipleChoiceField(required=True,choices=PAYMENTS_ACCEPTED, widget=forms.CheckboxSelectMultiple())

    class Meta():
        model = VendorsProfile
        fields = ('website_link','phone_number','facebook_page','twitter_page','address_one','address_two','town_city','country','postal_address',
                'pin_number','b_type','payments_accepted','insurance')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

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

# forms wizard test

class FirstForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput, required=False)
    price = forms.DecimalField(max_digits=8, decimal_places=2)
    #add all the fields that you want to include in the form
    class Meta():
        model = Item
        fields = ('id','price')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['id'].label = 'Add ID'
        self.fields['price'].label = 'Add a price'

class SecondForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta():
        model = Item
        fields = ('image')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['image'].label = 'Add Image'


class ThirdForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta():
        model = Item
        fields = ('description')

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.fields['description'].label = 'Add Description'
