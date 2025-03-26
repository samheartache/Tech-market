from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная'})


def about(request):
    return render(request, 'main/about.html', {'title': 'О нас'})
