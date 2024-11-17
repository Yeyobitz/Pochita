from django.shortcuts import render, redirect
from .models import Invoice
from users.models import Client
from django.urls import reverse

# Listar facturas
def list_invoices(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'billing/list_invoices.html', {'invoices': invoices})

# Crear factura
from django.utils import timezone

def create_invoice(request):
    if request.method == 'POST':
        client_id = request.POST['client']
        items = request.POST['items']
        total_amount = request.POST['total_amount']
        client = get_object_or_404(Client, id=client_id)
        date = timezone.now().date()
        Invoice.objects.create(client=client, items=items, total_amount=total_amount, date=date)
        return redirect(reverse('list_invoices'))
    clients = Client.objects.all()
    return render(request, 'billing/create_invoice.html', {'clients': clients})


def view_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'billing/view_invoice.html', {'invoice': invoice})