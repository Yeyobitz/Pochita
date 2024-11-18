from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    supplier = models.CharField(max_length=100)
    expiration_date = models.DateField()
    image = models.ImageField(upload_to='inventory_images/', null=True, blank=True)
    description = models.TextField(default='')
    category = models.CharField(max_length=50, default='General')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

