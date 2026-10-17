from django.contrib import admin

from .models import Event, Institution, Parent, Student, StudyGroup


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


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone"]
    search_fields = ["full_name", "phone"]
    filter_horizontal = ["children"]


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "group", "date", "total_cost", "from_piggy_bank"]
    list_filter = ["group__institution", "group"]
    search_fields = ["title"]
