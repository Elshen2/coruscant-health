from django.db import models
from accounts.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctor_profile'
    )
    specialization = models.CharField(max_length=100)
    license_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialization}"