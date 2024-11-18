from django.db import models
from users.models import Client, Pet

class MedicalRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    diagnosis = models.TextField()
    treatment = models.TextField()
    prescription = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Record for {self.pet.name} ({self.client.name})"
