from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.forms import LoginForm, SignUpForm, EditProfileForm


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

                if request.POST.get('next', None):
                    return HttpResponseRedirect(request.POST.get('next'))
                
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

@login_required
def account(request):
    context = {
        'title': 'Аккаунт пользователя'
    }
    return render(request, 'account.html', context)

@login_required
def logout(request):
    auth.logout(request)
    return redirect(reverse('main:index'))

@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            if 'avatar' in request.FILES:
                print(request.user.avatar)
                request.user.avatar = request.FILES['avatar']
            form.save()
            return HttpResponseRedirect(reverse('user:account'))
        else:
            print(form.errors)
    else:
        form = EditProfileForm(instance=request.user)
    
    context = {
        'title': 'Редактирование профиля',
        'form': form
    }
    return render(request, 'editprofile.html', context)