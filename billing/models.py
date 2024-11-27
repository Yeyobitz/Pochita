from django.db import models
from users.models import Client

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='invoices')  # Relación con cliente
    date = models.DateField()  # Fecha de la factura
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monto total
    items = models.TextField()  # Detalle de los ítems
    payment_status = models.CharField(
        max_length=20, 
        choices=[
            ('paid', 'Pagado'),
            ('unpaid', 'No Pagado')
        ],
        default='unpaid'
    )  # Estado del pago
    created_at = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    updated_at = models.DateTimeField(auto_now=True)  # Fecha de última actualización

    def __str__(self):
        return f"Factura #{self.id} - {self.client.name}"
