from django import forms
from blog.models import post, comments

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

    
