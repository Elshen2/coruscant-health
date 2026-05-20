from django.contrib import admin
from .models import ServiceOrder

@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ['patient', 'service_type', 'status',
                    'ordered_by', 'created_at']
    list_filter = ['status', 'service_type']
    search_fields = ['patient__username']