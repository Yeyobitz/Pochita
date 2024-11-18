from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Client
from django.core.exceptions import ValidationError
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo electrónico")
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        

class ClientRegistrationForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'phone_number', 'address']
        labels = {
            'name': 'Nombre Completo',
            'phone_number': 'Teléfono',
            'address': 'Dirección',
        }
        
        
class ClientRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, label="Usuario")
    email = forms.EmailField(required=True, label="Correo electrónico")
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Confirmar contraseña")
    name = forms.CharField(max_length=100, required=True, label="Nombre completo")
    phone_number = forms.CharField(max_length=15, required=True, label="Teléfono")
    address = forms.CharField(widget=forms.Textarea, required=True, label="Dirección")
    
    # New pet fields
    pet_name = forms.CharField(max_length=100, required=True, label="Nombre de la mascota")
    species = forms.CharField(max_length=50, required=True, label="Especie")
    breed = forms.CharField(max_length=50, required=True, label="Raza")
    age = forms.IntegerField(required=True, min_value=0, label="Edad")
    image = forms.ImageField(required=False, label="Foto de la mascota")


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data