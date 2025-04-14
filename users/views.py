from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import LoginForm


def login(request):

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = auth.authenticate(username=username, password=password, email=email)
            if user:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = LoginForm()
    
    context = {
        'title': 'Вход в аккаунт',
        'form': form,
    }
    return render(request, 'login.html', context)


def signup(request):
    context = {
        'title': 'Регистрация'
    }
    return render(request, 'signup.html', context)


def account(request):
    context = {
        'title': 'Аккаунт пользователя'
    }
    return render(request, '', context)


def logout(request):
    pass
