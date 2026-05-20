from django.db import models
from accounts.models import User

class PatientProfile(models.Model):
    BLOOD_TYPES = [
        ('A+','A+'), ('A-','A-'),
        ('B+','B+'), ('B-','B-'),
        ('AB+','AB+'), ('AB-','AB-'),
        ('O+','O+'), ('O-','O-'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )

    date_of_birth = models.DateField(null=True, blank=True)
    blood_type = models.CharField(
        max_length=5,
        choices=BLOOD_TYPES,
        blank=True
    )
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    medical_history = models.TextField(blank=True)

    def __str__(self):
        return f"Xəstə: {self.user.get_full_name()}"