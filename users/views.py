from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Client
from .forms import CustomUserCreationForm, ClientRegistrationForm

def register_client(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        client_form = ClientRegistrationForm(request.POST)
        if user_form.is_valid() and client_form.is_valid():
            user = user_form.save()
            Client.objects.create(
                user=user,
                name=client_form.cleaned_data['name'],
                phone_number=client_form.cleaned_data['phone_number'],
                address=client_form.cleaned_data['address']
            )
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a Pochita S.A.")
            return redirect('landing_page')
    else:
        form = ClientRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('landing_page')
    return render(request, 'logout.html')