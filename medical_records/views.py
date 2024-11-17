from django.shortcuts import render, get_object_or_404
from .models import MedicalRecord
from users.models import Client
from django.contrib.auth.decorators import login_required, permission_required

# Vista para veterinarios: lectura y escritura
@login_required
@permission_required('medical_records.view_medicalrecord', raise_exception=True)
def list_medical_records(request):
    if request.user.groups.filter(name='Cliente').exists():
        medical_records = MedicalRecord.objects.filter(client__user=request.user)
    else:
        medical_records = MedicalRecord.objects.all()
    return render(request, 'medical_records/list_records.html', {'medical_records': medical_records})


def view_medical_record(request, pk):
    record = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'medical_records/view_record.html', {'record': record})
