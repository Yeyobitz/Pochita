from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from apps.inventory.models import Media
from apps.inventory.forms import MediaForm
from django.urls import reverse

@login_required
def list_inventory(request):
    inventory = Media.objects.all()
    
    # Sorting
    sort_by = request.GET.get('sort', 'name')
    if sort_by in ['name', '-name', 'expiration_date', '-expiration_date', 'stock', '-stock']:
        inventory = inventory.order_by(sort_by)
    
    # Category filtering
    category = request.GET.get('category')
    if category:
        inventory = inventory.filter(category=category)
    
    context = {
        'inventory': inventory,
        'is_client': request.user.groups.filter(name='Cliente').exists()
    }
    
    return render(request, 'inventory/list_inventory.html', context)

@login_required
@permission_required('inventory.add_media', raise_exception=True)
def add_inventory(request):
    if request.user.groups.filter(name='Cliente').exists():
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('list_inventory')
        
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('list_inventory')
    else:
        form = MediaForm()
    
    return render(request, 'inventory/inventory_form.html', {
        'form': form,
        'title': 'Agregar Producto',
        'button_text': 'Agregar'
    })

@login_required
@permission_required('inventory.change_media', raise_exception=True)
def update_inventory(request, pk):
    if request.user.groups.filter(name='Cliente').exists():
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('list_inventory')
        
    item = get_object_or_404(Media, pk=pk)
    
    if request.method == 'POST':
        form = MediaForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('list_inventory')
    else:
        form = MediaForm(instance=item)
    
    return render(request, 'inventory/inventory_form.html', {
        'form': form,
        'title': 'Editar Producto',
        'button_text': 'Actualizar'
    })

@login_required
@permission_required('inventory.delete_media', raise_exception=True)
def delete_inventory(request, pk):
    if request.user.groups.filter(name='Cliente').exists():
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('list_inventory')
        
    item = get_object_or_404(Media, pk=pk)
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('list_inventory')
    
    return render(request, 'inventory/confirm_delete.html', {
        'item': item
    }) 