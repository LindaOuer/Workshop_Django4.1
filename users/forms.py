from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import *


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['cin', 'username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit)
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ('username', 'password')
    password = forms.CharField(widget=forms.PasswordInput)