from django.contrib import admin

from .models import Institution, Student, StudyGroup


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ["name", "kind"]
    list_filter = ["kind"]


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "institution"]
    list_filter = ["institution"]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "group", "is_active"]
    list_filter = ["group__institution", "group", "is_active"]
    search_fields = ["full_name"]
