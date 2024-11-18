from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from django.urls import reverse

def list_inventory(request):
    inventory = InventoryItem.objects.all().order_by('name')
    return render(request, 'inventory/list_inventory.html', {'inventory': inventory})

def update_inventory(request, pk=None):
    item = None
    if pk:
        item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        name = request.POST['name']
        stock = request.POST['stock']
        supplier = request.POST['supplier']
        expiration_date = request.POST['expiration_date']
        image = request.FILES.get('image')
        description = request.POST['description']
        category = request.POST['category']
        price = request.POST['price']

        if item:
            item.name = name
            item.stock = stock
            item.supplier = supplier
            item.expiration_date = expiration_date
            item.description = description
            item.category = category
            item.price = price
            if image:
                item.image = image
            item.save()
        else:
            InventoryItem.objects.create(
                name=name, 
                stock=stock, 
                supplier=supplier, 
                expiration_date=expiration_date,
                image=image,
                description=description,
                category=category,
                price=price
            )
        return redirect(reverse('list_inventory'))

    return render(request, 'inventory/update_inventory.html', {'item': item})
