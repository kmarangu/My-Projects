from django import forms
from django.contrib.auth.models import User
from events_app.models import post,comments

class postForm(forms.ModelForm):

    class Meta():
        model = post
        fields = ('author','title','text')

        # css styling
        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
        }

class commentsForm(forms.ModelForm):

    class Meta():
        model = comments
        fields = ('author','text')
    # css styling
    widgets = {
        'author':forms.TextInput(attrs={'class':'textinputclass'}),
        'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
    }


# class UserForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta():
#         model = User
#         fields = ('username','email','password','first_name','last_name')


# class business_type_Form(forms.ModelForm):
#     model = business_type
#     fields = ('type')
#
# class payment_modes_Form(forms.ModelForm):
#     model = payment_modes
#     fields = ('mode')
#
# class insurance_status_Form(forms.ModelForm):
#     model = insurance_status
#     fields = ('status')
#
# class service_category_Form(forms.ModelForm):
#     model = service_category
#     fields = ('category')
#
# class coverage_distance_Form(forms.ModelForm):
#     model = coverage_distance
#     fields = ('service_area')

# Quote request forms
