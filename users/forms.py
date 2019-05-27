from .models import CustomUser
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm
)
from django.contrib.auth import forms

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = (
            'username', 
            'email', 
            'first_name', 
            'last_name', 
            'dob', 
            'address'
        )

class CustomUserUpdateForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = (
            'username',
            'email', 
            'first_name', 
            'last_name',
            'address',
        )