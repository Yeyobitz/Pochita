from django.db import models
from users.models import Client

class MedicalRecord(models.Model):
    pet_name = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.pet_name} ({self.client.name})"
