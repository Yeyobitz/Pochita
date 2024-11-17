from django.shortcuts import render, get_object_or_404
from .models import MedicalRecord
from users.models import Client

# Vista para veterinarios: lectura y escritura
def list_medical_records(request):
    medical_records = MedicalRecord.objects.all()
    return render(request, 'medical_records/list_records.html', {'medical_records': medical_records})

def view_medical_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'medical_records/view_record.html', {'record': record})
