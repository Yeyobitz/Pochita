from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Appointment
from users.models import Client, Pet, Vet
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect

# Vista para listar citas
# Listar citas
@login_required
@permission_required('appointments.view_appointment', raise_exception=True)
def list_appointments(request):
    if request.user.groups.filter(name='Cliente').exists():
        appointments = Appointment.objects.filter(client__user=request.user)
    else:
        appointments = Appointment.objects.all().order_by('date', 'time')
    return render(request, 'appointments/list_appointments.html', {'appointments': appointments})

# Crear una nueva cita
@login_required
def create_appointment(request):
    # Get or create client profile for the user
    client, created = Client.objects.get_or_create(
        user=request.user,
        defaults={
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        }
    )

    if request.method == 'POST':
        pet_id = request.POST['pet']
        vet_id = request.POST['vet']
        date = request.POST['date']
        time = request.POST['time']
        
        pet = get_object_or_404(Pet, id=pet_id)
        vet = get_object_or_404(Vet, id=vet_id)
        
        Appointment.objects.create(
            client=client,
            pet=pet,
            vet=vet,
            date=date,
            time=time
        )
        return redirect('list_appointments')

    pets = Pet.objects.filter(client=client)
    vets = Vet.objects.all()
    context = {
        'client': client,
        'pets': pets,
        'vets': vets
    }
    return render(request, 'appointments/create_appointment.html', context)
# Modificar o cancelar una cita
def update_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        pet_id = request.POST['pet']
        vet_id = request.POST['vet']
        date = request.POST['date']
        time = request.POST['time']
        
        pet = get_object_or_404(Pet, id=pet_id)
        vet = get_object_or_404(Vet, id=vet_id)
        
        appointment.client = client
        appointment.pet = pet
        appointment.vet = vet
        appointment.date = date
        appointment.time = time
        appointment.save()
        
        return redirect('list_appointments')

    client = Client.objects.get(user=request.user)
    pets = Pet.objects.filter(client=client)
    vets = Vet.objects.all()
    return render(request, 'appointments/update_appointment.html', {
        'appointment': appointment,
        'client': client,
        'pets': pets,
        'vets': vets
    })
    

@login_required
def cancel_appointment(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully')
        return redirect('list_appointments')
    
    return render(request, 'appointments/cancel_appointment.html', {
        'appointment': appointment
    })
