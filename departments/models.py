from django.db import models
from accounts.models import User

class ServiceOrder(models.Model):
    SERVICE_TYPES = [
        ('ct_scan',  'CT Scan'),
        ('pet_scan', 'PET Scan'),
        ('mri',      'MRI'),
        ('xray',     'X-Ray'),
        ('blood',    'Qan analizi'),
        ('urine',    'Sidik analizi'),
        ('echo',     'EXO (ürək)'),
        ('other',    'Digər'),
    ]

    STATUS_CHOICES = [
        ('pending',    'Gözləyir'),
        ('in_progress','İcra olunur'),
        ('completed',  'Tamamlandı'),
        ('cancelled',  'Ləğv edildi'),
    ]

    ordered_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders_given',
        limit_choices_to={'role': 'doctor'}
    )
    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='service_orders'
    )
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    notes = models.TextField(blank=True)
    result = models.TextField(blank=True)
    result_file = models.FileField(
        upload_to='results/',
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_service_type_display()} - {self.patient_get_full_name()}"