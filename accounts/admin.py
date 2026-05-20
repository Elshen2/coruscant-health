from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'get_full_name', 
                    'role', 'is_approved', 'created_at']
    list_filter = ['role', 'is_approved']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    actions = ['approve_users', 'disapprove_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "İstifadəçilər təsdiqləndi!")
    approve_users.short_description = "Seçilənləri təsdiqlə"

    def disapprove_users(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_users.short_description = "Təsdiqi geri al"

    fieldsets = UserAdmin.fieldsets + (
        ('CHA Məlumatları', {
            'fields': ('role', 'phone', 'is_approved')
        }),
    )