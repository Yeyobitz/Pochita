from django.db import models
from users.models import Client, Pet, Vet

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Programada'),
        ('Completed', 'Completada'),
        ('Cancelled', 'Cancelada'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True)  # Add pet field
    vet = models.ForeignKey(Vet, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.client.name} - {self.date} {self.time}"
