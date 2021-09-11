# Create by Packetsss
# Personal use is allowed
# Commercial use is prohibited

from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    


