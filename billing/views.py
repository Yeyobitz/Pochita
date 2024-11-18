from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Invoice
from users.models import Client
from django.contrib.auth.decorators import login_required

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
    if request.method == 'POST':
        client_id = request.POST['client']
        items = request.POST['items']
        total_amount = request.POST['total_amount']
        client = get_object_or_404(Client, id=client_id)
        date = timezone.now().date()
        Invoice.objects.create(client=client, items=items, total_amount=total_amount, date=date)
        return redirect(reverse('list_invoices'))
    
    # Lista de clientes para el formulario (solo accesible por admin/personal)
    if request.user.groups.filter(name='Cliente').exists():  # Bloquea acceso a clientes
        return redirect('list_invoices')
    
    clients = Client.objects.all()
    return render(request, 'billing/create_invoice.html', {'clients': clients})

# Ver factura (sin modificaciones, ya correcto)
@login_required
def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.user.groups.filter(name='Cliente').exists() and invoice.client != request.user.client:
        # Bloquear acceso si el cliente intenta ver una factura que no es suya
        return redirect('list_invoices')
    return render(request, 'billing/view_invoice.html', {'invoice': invoice})
