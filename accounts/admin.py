from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.http import HttpResponseRedirect
from django.urls import reverse

from unfold.admin import ModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")

    # 1) Полные fieldsets — для суперпользователя
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Персональные данные", {
            "fields": ("first_name", "last_name", "patronymic", "birth_date", "gender", "citizenship")
        }),
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Системное", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )

    filter_horizontal = ("groups", "user_permissions")

    # 2) Обычный staff НЕ может добавлять/удалять пользователей
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    # 3) Обычный staff видит в списке только себя
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    # 4) Обычный staff может редактировать только себя
    def has_change_permission(self, request, obj=None):
        perm = super().has_change_permission(request, obj=obj)
        if not perm:
            return False
        if request.user.is_superuser:
            return True
        if obj is None:
            return True  # страницу списка откроем (там будет только он)
        return obj.pk == request.user.pk

    # 5) Скрываем блок "Права доступа" полностью для НЕ-суперпользователя
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super().get_fieldsets(request, obj)

        return (
            (None, {"fields": ("email",)}),  # пароль лучше не давать менять через админку
            ("Персональные данные", {
                "fields": ("first_name", "last_name", "patronymic", "birth_date", "gender", "citizenship")
            }),
        )

    # 6) На всякий случай: даже если кто-то подделает POST — эти поля не сохранятся
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and change:
            old = User.objects.get(pk=obj.pk)
            obj.is_staff = old.is_staff
            obj.is_superuser = old.is_superuser
            obj.is_active = old.is_active
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # запрет на изменение groups/user_permissions через подделку формы
        if not request.user.is_superuser and change:
            return
        super().save_related(request, form, formsets, change)

    # 7) (Опционально) Когда staff нажимает "Пользователи" — сразу кидаем на редактирование себя
    def changelist_view(self, request, extra_context=None):
        if request.user.is_superuser:
            return super().changelist_view(request, extra_context)
        url = reverse("admin:accounts_user_change", args=[request.user.pk])
        return HttpResponseRedirect(url)