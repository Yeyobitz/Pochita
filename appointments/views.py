from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Appointment
from users.models import Client, Vet
from django.urls import reverse

# Listar citas
def list_appointments(request):
    appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'appointments/list_appointments.html', {'appointments': appointments})

# Crear una nueva cita
def create_appointment(request):
    if request.method == 'POST':
        client_id = request.POST['client']
        vet_id = request.POST['vet']
        date = request.POST['date']
        time = request.POST['time']
        client = get_object_or_404(Client, id=client_id)
        vet = get_object_or_404(Vet, id=vet_id)
        Appointment.objects.create(client=client, vet=vet, date=date, time=time)
        return redirect(reverse('list_appointments'))

    clients = Client.objects.all()
    vets = Vet.objects.all()
    return render(request, 'appointments/create_appointment.html', {'clients': clients, 'vets': vets})

# Modificar o cancelar una cita
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.date = request.POST['date']
        appointment.time = request.POST['time']
        appointment.status = request.POST['status']
        appointment.save()
        return redirect(reverse('list_appointments'))

    return render(request, 'appointments/update_appointment.html', {'appointment': appointment})
