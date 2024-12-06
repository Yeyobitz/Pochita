from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from .models import Appointment
from users.models import Client, Pet, Vet
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from datetime import datetime, timedelta

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
        
        if all([pet_id, vet_id, date, time]):
            try:
                # Verificación estricta de disponibilidad
                existing_appointments = Appointment.objects.filter(
                    vet_id=vet_id,
                    date=date,
                    time=time,
                    status__in=['SCHEDULED', 'CONFIRMED']  # Verificar tanto citas programadas como confirmadas
                ).count()
                
                if existing_appointments > 0:
                    messages.error(request, 'El veterinario ya tiene una cita programada en este horario. Por favor seleccione otro horario.')
                    return redirect('create_appointment')

                pet = Pet.objects.get(id=pet_id)
                vet = Vet.objects.get(id=vet_id)
                
                # Verificar si el cliente ya tiene una cita en ese horario
                client_existing_appointments = Appointment.objects.filter(
                    client=client,
                    date=date,
                    time=time,
                    status__in=['SCHEDULED', 'CONFIRMED']
                ).count()
                
                if client_existing_appointments > 0:
                    messages.error(request, 'Usted ya tiene una cita programada en este horario. Por favor seleccione otro horario.')
                    return redirect('create_appointment')
                
                appointment = Appointment.objects.create(
                    client=client,
                    pet=pet,
                    vet=vet,
                    date=date,
                    time=time,
                    status='SCHEDULED'
                )
                
                messages.success(request, 'Cita agendada exitosamente.')
                return redirect('list_appointments')
                
            except Pet.DoesNotExist:
                messages.error(request, 'La mascota seleccionada no existe.')
            except Vet.DoesNotExist:
                messages.error(request, 'El veterinario seleccionado no existe.')
            except Exception as e:
                messages.error(request, f'Error al agendar la cita: {str(e)}')
        else:
            missing = []
            if not pet_id: missing.append('mascota')
            if not vet_id: missing.append('veterinario')
            if not date: missing.append('fecha')
            if not time: missing.append('hora')
            messages.error(request, f'Por favor complete los siguientes campos: {", ".join(missing)}')

    vets = Vet.objects.all()
    pets = Pet.objects.filter(client=client)
    
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
            # Verificar disponibilidad (excluyendo la cita actual)
            existing_appointment = Appointment.objects.filter(
                vet_id=vet_id,
                date=date,
                time=time,
                status='SCHEDULED'
            ).exclude(id=appointment_id).exists()
            
            if existing_appointment:
                messages.error(request, 'El veterinario ya tiene una cita programada en este horario.')
                return redirect('update_appointment', appointment_id=appointment_id)

            # Actualizar la cita
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

def check_availability(request):
    vet_id = request.GET.get('vet')
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')
    
    if not all([vet_id, date_str, time_str]):
        return JsonResponse({'available': False, 'error': 'Faltan parámetros requeridos'})
    
    try:
        # Convertir la hora seleccionada a datetime
        selected_datetime = datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        current_datetime = datetime.now()
        
        # Verificar si la hora seleccionada es del pasado
        if selected_datetime < current_datetime:
            return JsonResponse({
                'available': False,
                'error': 'No se pueden agendar citas en fechas u horas pasadas.'
            })
        
        # Obtener todas las citas del día ordenadas por hora
        existing_appointments = Appointment.objects.filter(
            vet_id=vet_id,
            date=date_str,
            status='SCHEDULED'
        ).order_by('time')
        
        # Función para verificar si una hora está disponible
        def is_time_available(check_datetime):
            # Convertir a string para comparación
            check_time_str = check_datetime.strftime('%H:%M')
            
            for apt in existing_appointments:
                apt_time_str = apt.time.strftime('%H:%M')
                apt_datetime = datetime.strptime(f"{date_str} {apt_time_str}", '%Y-%m-%d %H:%M')
                
                time_diff = abs((apt_datetime - check_datetime).total_seconds())
                if time_diff < 3600:  # menos de 1 hora de diferencia
                    return False
            return True
        
        # Verificar si la hora seleccionada está disponible
        if is_time_available(selected_datetime):
            return JsonResponse({'available': True})
        
        # Buscar horas disponibles cercanas
        available_times = []
        base_time = selected_datetime.replace(minute=0)  # Empezar desde la hora en punto
        
        # Revisar 3 horas antes y después
        for hour_offset in range(-3, 4):
            check_time = base_time + timedelta(hours=hour_offset)
            for minute in range(0, 60, 1):  # Revisar cada minuto
                check_datetime = check_time + timedelta(minutes=minute)
                if check_datetime > current_datetime and is_time_available(check_datetime):
                    available_times.append(check_datetime.strftime('%H:%M'))
        
        # Filtrar para obtener solo la hora anterior y posterior más cercanas
        available_times.sort()
        selected_time_str = selected_datetime.strftime('%H:%M')
        prev_times = [t for t in available_times if t < selected_time_str]
        next_times = [t for t in available_times if t > selected_time_str]
        
        final_times = []
        if prev_times:
            final_times.append(prev_times[-1])  # Última hora anterior disponible
        if next_times:
            final_times.append(next_times[0])   # Primera hora posterior disponible
        
        return JsonResponse({
            'available': False,
            'available_times': final_times
        })
        
    except Exception as e:
        print(f"Error en check_availability: {str(e)}")
        return JsonResponse({'available': False, 'error': str(e)})
