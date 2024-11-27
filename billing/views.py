from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Invoice
from users.models import Client
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Listar facturas (modificado para filtrar por cliente)
@login_required
def list_invoices(request):
    if request.user.groups.filter(name='Cliente').exists():  # Si es cliente
        invoices = Invoice.objects.filter(client=request.user.client).order_by('-date')
    else:  # Si es administrador o personal interno
        invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'billing/list_invoices.html', {'invoices': invoices})

# Crear factura
@login_required
def create_invoice(request):
    if request.user.groups.filter(name='Cliente').exists():
        return redirect('list_invoices')
    
    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        service = request.POST.get('service')
        amount = request.POST.get('amount')
        payment_status = request.POST.get('payment_status', 'unpaid')
        
        # Solo permitir estado "pagado" para admin y veterinario
        if payment_status == 'paid' and not (
            request.user.is_superuser or 
            request.user.groups.filter(name='Veterinario').exists()
        ):
            payment_status = 'unpaid'
        
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
    
    patients = Client.objects.all()
    is_staff = request.user.is_superuser or request.user.groups.filter(name='Veterinario').exists()
    return render(request, 'billing/create_invoice.html', {
        'patients': patients,
        'is_staff': is_staff
    })

# Ver factura (sin modificaciones, ya correcto)
@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.user.groups.filter(name='Cliente').exists() and invoice.client != request.user.client:
        # Bloquear acceso si el cliente intenta ver una factura que no es suya
        return redirect('list_invoices')
    return render(request, 'billing/view_invoice.html', {'invoice': invoice})
