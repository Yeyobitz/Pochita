from django.db import models
from users.models import Client

class Invoice(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    items = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.client.name}"
