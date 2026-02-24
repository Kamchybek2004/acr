from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from unfold.admin import ModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ("is_staff", "is_active", "gender")
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),

        ('Персональные данные', {
            'fields': (
                'first_name', 
                'last_name',
                'patronymic',
                'birth_date',
                'gender',
                'citizenship',
                )
            }),

        ('Права доступа', {
            'fields': (
                'is_active', 
                'is_staff', 
                'is_superuser', 
                'groups', 
                'user_permissions'
                )
            }),

        ('Системное', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
