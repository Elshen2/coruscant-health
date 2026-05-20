from django.db import models
from accounts.models import User

class HealthRecord(models.Model):
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='health_records',
        limit_choices_to={'role': 'patient'}
    )
    recorded_at = models.DateTimeField(auto_now_add=True)

    heart_rate = models.IntegerField(null=True, blank=True)
    blood_pressure_sys = models.IntegerField(null=True, blank=True)
    blood_pressure_dia = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True
    )
    oxygen_level = models.DecimalField(
        max_digits=4, decimal_places=1,
        null=True, blank=True
    )
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return f"{self.patient.get_full_name()} - {self.recorded_at:%d.%m.%Y}"


class DoctorReport(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='written_reports',
        limit_choices_to={'role': 'doctor'}
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_reports',
        limit_choices_to={'role': 'patient'}
    )
    health_record = models.ForeignKey(
        HealthRecord,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='reports'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    prescription = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - Dr.{self.doctor.get_full_name()}"


class MedicalDocument(models.Model):
    DOCUMENT_TYPES = [
        ('lab',    'Laboratoriya'),
        ('image',  'Şəkil (X-ray, MRI)'),
        ('report', 'Hesabat'),
        ('other',  'Digər'),
    ]

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patient_documents',
        limit_choices_to={'role': 'patient'}
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPES,
        default='other'
    )
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/encrypted/')
    is_encrypted = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.patient.get_full_name()}"