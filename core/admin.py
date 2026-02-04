from django.contrib import admin
from .models import (
    Major, Profile, Module,
    ProfileDocument, CompetencePassport,
    License, Order, Schedule
)

admin.site.site_header = "Панель управления аккредитацией"
admin.site.site_title = "Админ панель"
admin.site.index_title = "Аккредитация"


# =======================
# Inlines
# =======================

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    ordering = ('name',)
    show_change_link = True
    classes = ('collapse',)


class ProfileDocumentInline(admin.TabularInline):
    model = ProfileDocument
    extra = 0
    show_change_link = True
    classes = ('collapse',)


class CompetencePassportInline(admin.TabularInline):
    model = CompetencePassport
    extra = 0
    show_change_link = True
    classes = ('collapse',)


# =======================
# Major
# =======================

@admin.register(Major)
class MajorAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'edu_level')
    search_fields = ('code', 'name')
    list_filter = ('edu_level',)
    ordering = ('code',)
    list_per_page = 25


# =======================
# Profile  
# =======================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'major', 'study_form')
    list_filter = ('study_form', 'major')
    search_fields = ('name',)
    autocomplete_fields = ('major',)
    readonly_fields = ('slug',)

    inlines = (
        ModuleInline,
        ProfileDocumentInline,
        CompetencePassportInline,
    )

    fieldsets = (
        (None, {
            'fields': ('name', 'major', 'study_form')
        }),
        ('Системные поля', {
            'fields': ('slug',),
            'classes': ('collapse',)
        }),
    )


# =======================
# Module
# =======================

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'profile')
    search_fields = ('name',)
    autocomplete_fields = ('profile',)
    list_filter = ('profile',)


# =======================
# Documents
# =======================

@admin.register(ProfileDocument)
class ProfileDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile')
    search_fields = ('title',)
    autocomplete_fields = ('profile',)


@admin.register(CompetencePassport)
class CompetencePassportAdmin(admin.ModelAdmin):
    list_display = ('title', 'profile')
    autocomplete_fields = ('profile',)


# =======================
# License & Order
# =======================

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')
    search_fields = ('title', 'text')

    fields = ('title', 'file', 'text')  # порядок полей в форме


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('title','category') 
    list_filter = ('category',)
    search_fields = ('title',)

    fields = ('title', 'file', 'category')


 
# =======================
# Schedule
# =======================

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty')
    list_filter = ('faculty',)
    search_fields = ('title',)

