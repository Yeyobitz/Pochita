from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.models import Client
from .models import Invoice
from django.utils import timezone

def is_not_client(user):
    return not user.groups.filter(name='Cliente').exists()

@login_required
def list_invoices(request):
    if request.user.groups.filter(name='Cliente').exists():
        invoices = Invoice.objects.filter(client__user=request.user)
    else:
        invoices = Invoice.objects.all()
    return render(request, 'billing/list_invoices.html', {'invoices': invoices})

@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.user.groups.filter(name='Cliente').exists() and invoice.client.user != request.user:
        messages.error(request, 'No tienes permiso para ver esta factura.')
        return redirect('list_invoices')
    return render(request, 'billing/view_invoice.html', {'invoice': invoice})

@login_required
@user_passes_test(is_not_client)
def create_invoice(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        service = request.POST.get('service')
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status', 'unpaid')
        
        # Verificar permisos para marcar como pagado
        if payment_status == 'paid' and not (
            request.user.is_superuser or 
            request.user.groups.filter(name='Veterinario').exists()
        ):
            payment_status = 'unpaid'
        
        # Verificar que todos los campos necesarios estén presentes
        if all([patient_id, service, amount]):
            try:
                patient = get_object_or_404(Client, id=patient_id)
                Invoice.objects.create(
                    client=patient,
                    items=service,
                    total_amount=amount,
                    payment_status=payment_status,
                    date=timezone.now().date()
                )
                messages.success(request, 'Factura creada exitosamente.')
                return redirect('list_invoices')
            except Exception as e:
                messages.error(request, f'Error al crear la factura: {str(e)}')
        else:
            messages.error(request, 'Por favor complete todos los campos.')
    
    # Obtener lista de pacientes con sus datos de usuario
    patients = Client.objects.select_related('user').all()
    
    # Debug: Imprimir información de los pacientes
    for patient in patients:
        print(f"Patient ID: {patient.id}")
        print(f"Patient user: {patient.user.get_full_name() or patient.user.username}")
    
    context = {
        'patients': patients,
        'is_staff': request.user.is_superuser or request.user.groups.filter(name='Veterinario').exists()
    }
    return render(request, 'billing/create_invoice.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='Veterinario').exists())
def delete_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    if request.method == 'POST':
        try:
            invoice.delete()
            messages.success(request, 'Factura eliminada exitosamente.')
            return redirect('list_invoices')
        except Exception as e:
            messages.error(request, f'Error al eliminar la factura: {str(e)}')
    
    return render(request, 'billing/delete_invoice.html', {'invoice': invoice})
