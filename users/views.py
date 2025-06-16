from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import LoginForm, SignUpForm


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
    if request.method == 'POST':
        form = SignUpForm(data=request.POST)
        print(form)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))
    else:
        form = SignUpForm()
    
    context = {
        'title': 'Вход в аккаунт',
        'form': form,
    }
    return render(request, 'signup.html', context)


def account(request):
    context = {
        'title': 'Аккаунт пользователя'
    }
    return render(request, 'account.html', context)


def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))


def editprofile(request):
    return render(request, 'editprofile.html')