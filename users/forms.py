from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User
from global_utils.error_messages import INVALID_LOGIN, INACTIVE_ACC

class LoginForm(AuthenticationForm):
    email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField()

    error_messages = {
        'invalid_login': INVALID_LOGIN,
        'inactive': INACTIVE_ACC,
    }

    class Meta:
        model = User
        fields = ['email', 'username', 'password']