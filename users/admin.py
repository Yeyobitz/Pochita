from django.contrib import admin
from .models import Client,Pet, Vet

admin.site.register(Client)
admin.site.register(Pet)
admin.site.register(Vet)
