from django import forms
from django.core.exceptions import ValidationError
import requests

class Submit(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
