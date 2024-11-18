from django.shortcuts import render, get_object_or_404, redirect
from .models import MedicalRecord
from users.models import Client, Pet, Vet
from django.contrib.auth.decorators import login_required, permission_required

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

@login_required
@permission_required('medical_records.add_medicalrecord', raise_exception=True)
def create_medical_record(request):
    if request.method == 'POST':
        pet = get_object_or_404(Pet, id=request.POST['pet'])
        client = get_object_or_404(Client, id=request.POST['client'])
        
        MedicalRecord.objects.create(
            pet=pet,
            client=client,
            diagnosis=request.POST['diagnosis'],
            treatment=request.POST['treatment'],
            notes=request.POST['notes']
        )
        return redirect('list_medical_records')

    clients = Client.objects.all()
    pets = Pet.objects.all()
    context = {
        'clients': clients,
        'pets': pets
    }
    return render(request, 'medical_records/create_medical_record.html', context)

from django.http import JsonResponse

@login_required
def get_client_pets(request, client_id):
    pets = Pet.objects.filter(client_id=client_id).values('id', 'name')
    return JsonResponse(list(pets), safe=False)
