from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from django.urls import reverse

# Listar productos
def list_inventory(request):
    inventory = InventoryItem.objects.all().order_by('name')
    return render(request, 'inventory/list_inventory.html', {'inventory': inventory})

# Agregar o actualizar productos
def update_inventory(request, pk=None):
    item = None
    if pk:
        item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        name = request.POST['name']
        stock = request.POST['stock']
        supplier = request.POST['supplier']
        expiration_date = request.POST['expiration_date']

        if item:
            item.name = name
            item.stock = stock
            item.supplier = supplier
            item.expiration_date = expiration_date
            item.save()
        else:
            InventoryItem.objects.create(name=name, stock=stock, supplier=supplier, expiration_date=expiration_date)
        return redirect(reverse('list_inventory'))

    return render(request, 'inventory/update_inventory.html', {'item': item})
