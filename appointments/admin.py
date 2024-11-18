from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'pet', 'vet', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'vet')
    search_fields = ('client__name', 'pet__name', 'vet__name')
