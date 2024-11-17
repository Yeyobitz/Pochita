from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from .models import Client
from .forms import ClientRegistrationForm

def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            # Crear el cliente asociado al usuario
            Client.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address']
            )
            # Iniciar sesión automáticamente
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a Pochita S.A.")
            return redirect('landing_page')  # Cambia por la URL que desees redirigir
    else:
        form = ClientRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
