# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.http import HttpResponseRedirect

from unfold.admin import ModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {
            "fields": (
                "first_name", "last_name", "patronymic",
                "birth_date", "gender", "citizenship",
                "photo",   # если поле фото есть
            )
        }),
        ("Права доступа", {
            "fields": (
                "is_active", "is_staff", "is_superuser",
                "groups", "user_permissions",
            )
        }),
        ("Системное", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
    )

    filter_horizontal = ("groups", "user_permissions")

    # --- 1) superuser ВСЕГДА без ограничений ---
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        # базовая проверка Django (нужна)
        perm = super().has_change_permission(request, obj=obj)
        if not perm:
            return False

        if request.user.is_superuser:
            return True

        # staff может менять только себя
        if obj is None:
            return True  # список откроется, там будет только он
        return obj.pk == request.user.pk

    # --- 2) скрываем блок прав для НЕ-суперпользователя ---
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)

        return (
            (None, {"fields": ("email",)}),
            ("Персональные данные", {
                "fields": (
                    "first_name", "last_name", "patronymic",
                    "birth_date", "gender", "citizenship",
                    "photo",
                )
            }),
        )

    # --- 3) защита от подделки POST: права не меняются у staff ---
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and change:
            old = User.objects.get(pk=obj.pk)
            obj.is_staff = old.is_staff
            obj.is_superuser = old.is_superuser
            obj.is_active = old.is_active
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        if not request.user.is_superuser and change:
            return
        super().save_related(request, form, formsets, change)

    # --- 4) (опционально) staff кликает "Пользователи" -> сразу к себе ---
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            return super().changelist_view(request, extra_context)
        url = reverse("admin:accounts_user_change", args=[request.user.pk])
        return HttpResponseRedirect(url)