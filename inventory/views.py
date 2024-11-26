from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import InventoryItem
from django.contrib import messages
from django.utils import timezone

def is_not_client(user):
    return not user.groups.filter(name='Cliente').exists()

@login_required
def list_inventory(request):
    inventory = InventoryItem.objects.all()
    
    # Verificar si el usuario es cliente
    is_client = request.user.groups.filter(name='Cliente').exists()
    
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
    expired_items = inventory.filter(expiration_date__lt=timezone.now().date())
    
    context = {
        'inventory': inventory,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
        'is_client': is_client,
    }
    
    return render(request, 'inventory/list_inventory.html', context)

@login_required
@user_passes_test(is_not_client)
def update_inventory(request, pk=None):
    item = None
    if pk:
        item = get_object_or_404(InventoryItem, pk=pk)

    if request.method == 'POST':
        try:
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
                messages.success(request, 'Producto actualizado exitosamente.')
            else:
                # Create new item
                InventoryItem.objects.create(
                    name=name,
                    stock=stock,
                    supplier=supplier,
                    expiration_date=expiration_date,
                    description=description,
                    category=category,
                    price=price,
                    image=image if image else None
                )
                messages.success(request, 'Producto agregado exitosamente.')
            
            return redirect('list_inventory')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'inventory/update_inventory.html', {'item': item})

@login_required
@user_passes_test(is_not_client)
def delete_inventory(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    
    if request.method == 'POST':
        try:
            item.delete()
            messages.success(request, 'Producto eliminado exitosamente.')
            return redirect('list_inventory')
        except Exception as e:
            messages.error(request, f'Error al eliminar el producto: {str(e)}')
    
    return render(request, 'inventory/delete_confirm.html', {'item': item})