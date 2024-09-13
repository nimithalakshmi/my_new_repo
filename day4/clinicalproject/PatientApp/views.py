from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Patient

# List all doctors
def Patient_list(request):
    Patients = Patient.objects.all()
    return render(request, 'Patient_list.html', {'Patient': Patients})

# Create a new doctor
def Patient_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        disease = request.POST['disease']
        age = request.POST['age']
        Patient.objects.create(name=name, disease=disease, age=age)
        return redirect('Patient_list')
    return render(request, 'Patient_form.html')

# Update an existing doctor
def Patient_update(request, id):
    Patient = Patient.objects.get(id=id)
    if request.method == 'POST':
        Patient.name = request.POST['name']
        Patient.disease = request.POST['disease']
        Patient.age = request.POST['age']
        Patient.save()
        return redirect('Patient_list')
    return render(request, 'Patient_form.html', {'Patient': Patient})

# Delete a doctor
def Patient_delete(request, id):
    Patient = Patient.objects.get(id=id)
    Patient.delete()
    return redirect('Patient_list')