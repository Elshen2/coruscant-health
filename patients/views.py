import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.files.base import ContentFile
from cryptography.fernet import Fernet
from records.models import HealthRecord, DoctorReport, MedicalDocument
from .forms import HealthRecordForm, MedicalDocumentForm

ENCRYPTION_KEY = b'6lBWUSKpAJWk9PHhGUov0zNJ0iUYwh9x6lBWUSKpAJW='

def patient_required(view_func):
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'patient':
            messages.error(request, 'Bu səhifəyə giriş icazəniz yoxdur.')
            return redirect('dashboard')
        if not request.user.is_approved:
            return redirect('pending_approval')
        return view_func(request, *args, **kwargs)
    wrapper.__name__ = view_func.__name__
    return wrapper

@patient_required
def patient_dashboard(request):
    user = request.user
    records = HealthRecord.objects.filter(patient=user)[:5]
    reports = DoctorReport.objects.filter(patient=user)[:5]
    context = {
        'records_count': HealthRecord.objects.filter(patient=user).count(),
        'reports_count': DoctorReport.objects.filter(patient=user).count(),
        'recent_records': records,
        'recent_reports': reports,
    }
    return render(request, 'patients/dashboard.html', context)

@patient_required
def upload_record(request):
    form = HealthRecordForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        record = form.save(commit=False)
        record.patient = request.user
        record.save()
        messages.success(request, 'Sağlamlıq məlumatı uğurla yükləndi!')
        return redirect('my_records')
    return render(request, 'patients/upload_record.html', {'form': form})

@patient_required
def my_records(request):
    records = HealthRecord.objects.filter(patient=request.user)
    return render(request, 'patients/my_records.html', {'records': records})

@patient_required
def my_reports(request):
    reports = DoctorReport.objects.filter(patient=request.user)
    return render(request, 'patients/my_reports.html', {'reports': reports})

@patient_required
def my_documents(request):
    documents = MedicalDocument.objects.filter(patient=request.user)
    return render(request, 'patients/my_documents.html', {'documents': documents})

@patient_required
def upload_document(request):
    form = MedicalDocumentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        doc = form.save(commit=False)
        doc.patient = request.user
        doc.uploaded_by = request.user
        
        uploaded_file = request.FILES['file']
        file_data = uploaded_file.read()
        
        f = Fernet(ENCRYPTION_KEY)
        encrypted_data = f.encrypt(file_data)
        
        encrypted_file = ContentFile(encrypted_data, name=uploaded_file.name)
        doc.file = encrypted_file
        doc.is_encrypted = True
        
        doc.save()
        messages.success(request, 'Sənəd təhlükəsizlik standartlarına uyğun olaraq şifrələnərək yükləndi!')
        return redirect('my_documents')
    return render(request, 'patients/upload_document.html', {'form': form})