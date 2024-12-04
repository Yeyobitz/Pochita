from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .models import Client, Pet
from .forms import CustomUserCreationForm, ClientRegistrationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse



def register_client(request):
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            
            cliente_group = Group.objects.get(name='Cliente')
            user.groups.add(cliente_group)

            client = Client.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number'],
                address=form.cleaned_data['address'],
                email=form.cleaned_data['email']
            )

            pets_count = int(request.POST.get('pets_count', 1))
            
            for i in range(pets_count):
                Pet.objects.create(
                    client=client,
                    name=request.POST.get(f'pet_{i}_name'),
                    species=request.POST.get(f'pet_{i}_species'),
                    breed=request.POST.get(f'pet_{i}_breed'),
                    age=request.POST.get(f'pet_{i}_age'),
                    image=request.FILES.get(f'pet_{i}_image')
                )

            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido a Pochita S.A.")
            return JsonResponse({'redirect_url': reverse('landing_page')})
    else:
        form = ClientRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('landing_page')
    return render(request, 'logout.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def validate_username(request):
    username = request.GET.get('username', None)
    response = {
        'is_taken': User.objects.filter(username=username).exists()
    }
    return JsonResponse(response)

def validate_email(request):
    email = request.GET.get('email', None)
    response = {
        'is_taken': User.objects.filter(email=email).exists()
    }
    return JsonResponse(response)
