from django import forms
from django.contrib.auth.forms import AuthenticationForm

from users.models import User

class LoginForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Почта',})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'placeholder': 'Имя пользователя'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                           'placeholder': 'Пароль',})
    )
    class Meta:
        model = User
        fields = ['email', 'username', 'password']