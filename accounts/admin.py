from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import HttpResponseRedirect
from django.urls import reverse

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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.pk == request.user.pk

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            return super().changelist_view(request, extra_context)

        url = reverse("admin:accounts_user_change", args=[request.user.pk])
        return HttpResponseRedirect(url)