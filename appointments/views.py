from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Appointment
from users.models import Client, Pet, Vet
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

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
        pet_id = request.POST.get('pet')
        vet_id = request.POST.get('vet')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        # Debug logs
        print("==== DEBUG CREATE APPOINTMENT ====")
        print(f"POST data: {request.POST}")
        print(f"Pet ID: {pet_id}")
        print(f"Vet ID: {vet_id}")
        print(f"Date: {date}")
        print(f"Time: {time}")
        
        if all([pet_id, vet_id, date, time]):
            try:
                # Intentar obtener las instancias necesarias
                pet = Pet.objects.get(id=pet_id)
                print(f"Pet found: {pet}")
                
                vet = Vet.objects.get(id=vet_id)
                print(f"Vet found: {vet}")
                
                # Crear la cita
                appointment = Appointment.objects.create(
                    client=client,
                    pet=pet,
                    vet=vet,
                    date=date,
                    time=time,
                    status='SCHEDULED'
                )
                print(f"Appointment created: {appointment}")
                
                messages.success(request, 'Cita agendada exitosamente.')
                return redirect('list_appointments')
            except Pet.DoesNotExist:
                print("Error: Pet not found")
                messages.error(request, 'La mascota seleccionada no existe.')
            except Vet.DoesNotExist:
                print("Error: Vet not found")
                messages.error(request, 'El veterinario seleccionado no existe.')
            except Exception as e:
                print(f"Error: {str(e)}")
                messages.error(request, f'Error al agendar la cita: {str(e)}')
        else:
            missing = []
            if not pet_id: missing.append('mascota')
            if not vet_id: missing.append('veterinario')
            if not date: missing.append('fecha')
            if not time: missing.append('hora')
            print(f"Missing fields: {', '.join(missing)}")
            messages.error(request, f'Por favor complete los siguientes campos: {", ".join(missing)}')

    # Obtener las opciones para el formulario
    vets = Vet.objects.all()
    pets = Pet.objects.filter(client=client)
    
    # Debug log de opciones disponibles
    print("==== Available Options ====")
    print(f"Vets: {list(vets.values_list('id', 'user__username'))}")
    print(f"Pets: {list(pets.values_list('id', 'name'))}")
    
    context = {
        'client': client,
        'pets': pets,
        'vets': vets
    }
    return render(request, 'appointments/create_appointment.html', context)

# Modificar o cancelar una cita
@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Verificar permisos
    if request.user.groups.filter(name='Cliente').exists() and appointment.client.user != request.user:
        return redirect('list_appointments')
    
    if request.method == 'POST':
        pet_id = request.POST.get('pet')
        vet_id = request.POST.get('vet')
        date = request.POST.get('date')
        time = request.POST.get('time')
        status = request.POST.get('status')
        
        # Validar estados permitidos para clientes
        if request.user.groups.filter(name='Cliente').exists():
            if status not in ['SCHEDULED', 'CANCELLED']:
                status = 'SCHEDULED'
        
        try:
            appointment.pet_id = pet_id
            appointment.vet_id = vet_id
            appointment.date = date
            appointment.time = time
            appointment.status = status
            appointment.save()
            
            messages.success(request, 'Cita actualizada exitosamente.')
            return redirect('list_appointments')
        except Exception as e:
            messages.error(request, f'Error al actualizar la cita: {str(e)}')
    
    # Definir estados disponibles según el tipo de usuario
    if request.user.groups.filter(name='Cliente').exists():
        status_choices = [
            ('SCHEDULED', 'Programado'),
            ('CANCELLED', 'Cancelado')
        ]
    else:
        status_choices = Appointment.STATUS_CHOICES
    
    context = {
        'appointment': appointment,
        'pets': Pet.objects.filter(client=appointment.client),
        'vets': Vet.objects.all(),
        'status_choices': status_choices,
        'is_client': request.user.groups.filter(name='Cliente').exists()
    }
    
    return render(request, 'appointments/update_appointment.html', context)
    

@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Verificar si el usuario tiene permiso para cancelar la cita
    if request.user.groups.filter(name='Cliente').exists() and appointment.client.user != request.user:
        messages.error(request, 'No tienes permiso para eliminar esta cita.')
        return redirect('list_appointments')
    
    try:
        # Eliminar la cita en lugar de cambiar su estado
        appointment.delete()
        messages.success(request, 'Cita eliminada exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al eliminar la cita: {str(e)}')
    
    return redirect('list_appointments')
