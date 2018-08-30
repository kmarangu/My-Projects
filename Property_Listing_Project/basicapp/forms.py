from django import forms
from basicapp.models import User
# Used for validation of forms
from django.core import validators


# Custom validator for a field
# def check_for_e(value):
#     if value[0].lower() != 'e':
#         raise forms.ValidationError("Name Needs to start with letter e")

class FormName(forms.ModelForm):
    class Meta():
        model = User
        fields = '__all__'

#     name = forms.CharField(validators=[check_for_e])
#     name = forms.CharField()
#     email = forms.EmailField()
#     verify_email = forms.EmailField(label='Enter your email again.')
#     text = forms.CharField(widget=forms.Textarea)
#     botcatcher = forms.CharField(required=False,
#                                     widget=forms.HiddenInput,
#                                     validators=[validators.MaxLengthValidator(0)])
# # How to clean the entire form
#     def clean(self):
#         all_clean_data = super().clean()
#         email = all_clean_data['email']
#         vmail = all_clean_data['verify_email']
#
#         if email != vmail:
#             raise forms.ValidationError("Please make sure emails match!")


# HOW TO USE clean_botcatcher TO STOP bootstrap
    # def clean_botcatcher(self):
    #     botcatcher = self.cleaned_data['botcatcher']
    #     if len(botcatcher) > 0:
    #         raise forms.ValidationError("GOTCHA BOT!")
    #     return botcatcher
