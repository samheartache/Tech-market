from django.shortcuts import render


def signup(request):
    context = {
        'title': 'Регистрация'
    }
    return render(request, 'signup.html', context)


def login(request):
    context = {
        'title': 'Вход в аккаунт'
    }
    return render(request, 'login.html', context)


def account(request):
    context = {
        'title': 'Аккаунт пользователя'
    }
    return render(request, '', context)


def logout(request):
    pass
