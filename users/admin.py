from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser."""
    list_display = ['username', 'email', 'age', 'can_be_contacted', 'can_data_be_shared', 'is_staff']
    list_filter = ['is_staff', 'is_superuser', 'can_be_contacted', 'can_data_be_shared']
    
    # Ajoute les champs personnalisés dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('age', 'can_be_contacted', 'can_data_be_shared')
        }),
    )
    
    # Ajoute les champs personnalisés lors de la création
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations supplémentaires', {
            'fields': ('age', 'can_be_contacted', 'can_data_be_shared')
        }),
    )

