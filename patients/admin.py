from django.contrib import admin
from .models import PatientProfile

@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_type', 'date_of_birth']
    search_fields = ['user__username', 'user__first_name']