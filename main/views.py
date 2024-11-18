from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

def landing_page(request):
    return render(request, 'main/landing_page.html')
