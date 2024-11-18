from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem
from django.urls import reverse

def list_inventory(request):
    inventory = InventoryItem.objects.all()
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by in ['name', '-name', 'expiration_date', '-expiration_date', 'stock', '-stock']:
        inventory = inventory.order_by(sort_by)
    
    # Category filtering
    category = request.GET.get('category')
    if category:
        inventory = inventory.filter(category=category)
    
    # Low stock warning (less than 10 items)
    low_stock_items = inventory.filter(stock__lt=10)
    
    # Expired items
    from django.utils import timezone
    expired_items = inventory.filter(expiration_date__lt=timezone.now().date())
    
    context = {
        'inventory': inventory,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
    }
    
    return render(request, 'inventory/list_inventory.html', context)

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
            # Update existing item
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
            # Create new item
            item = InventoryItem.objects.create(
                name=name,
                stock=stock,
                supplier=supplier,
                expiration_date=expiration_date,
                description=description,
                category=category,
                price=price,
                image=image if image else None
            )
        
        return redirect('list_inventory')
    
    return render(request, 'inventory/update_inventory.html', {'item': item})

def delete_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('list_inventory')
    return render(request, 'inventory/delete_confirm.html', {'item': item})