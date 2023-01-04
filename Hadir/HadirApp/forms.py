from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django.db import models
# from .models import Class


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # clas = models.ForeignKey(Class, null=True, on_delete=models.SET_NULL)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
