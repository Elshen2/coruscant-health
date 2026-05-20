from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient',     'Xəstə'),
        ('doctor',      'Həkim'),
        ('admin',       'Administrator'),
        ('emergency',   'Təcili Yardım'),
        ('department',  'Şöbə'),
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )
    phone = models.CharField(max_length=20, blank=True)
    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def is_patient(self):
        return self.role == 'patient'
    
    def is_doctor(self):
        return self.role == 'doctor'