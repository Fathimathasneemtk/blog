from django import forms
from .models import *

class BlogForms(forms.ModelForm):
    class Meta:
        model=Blog
        fields="__all__"


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields="__all__"
