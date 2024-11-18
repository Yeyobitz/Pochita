from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Client, Pet
from .forms import CustomUserCreationForm, ClientRegistrationForm
from django.contrib.auth.models import User


def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            Client.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                email=form.cleaned_data['email']  # Adding email field here
            )
            Pet.objects.create(
                client=Client.objects.get(user=user),
                name=form.cleaned_data['pet_name'],
                species=form.cleaned_data['species'],
                breed=form.cleaned_data['breed'],
                age=form.cleaned_data['age'],
                image=request.FILES.get('image')  # Use request.FILES to get the image
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