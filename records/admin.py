from django.contrib import admin
from .models import HealthRecord, DoctorReport, MedicalDocument

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'heart_rate', 'temperature',
                    'oxygen_level', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['patient__username']

@admin.register(DoctorReport)
class DoctorReportAdmin(admin.ModelAdmin):
    list_display = ['title', 'doctor', 'patient', 'created_at']
    search_fields = ['title', 'doctor__username', 'patient__username']

@admin.register(MedicalDocument)
class MedicalDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'patient', 'document_type',
                    'is_encrypted', 'uploaded_at']