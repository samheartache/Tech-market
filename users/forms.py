from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User

class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password']