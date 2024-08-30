from django.shortcuts import render
from .models import Menu


def index(request):
    menus = Menu.objects.all()
    return render(request, 'menu/index.html', {'menus': menus})
