from django.contrib import admin
from portal.models import Faculty, Course, Student


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("code", "name")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "start_year", "end_year", "is_active", "sort_order")
    list_filter = ("is_active", "start_year")
    search_fields = ("code", "name")


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("mssv", "full_name", "class_name", "major", "course", "faculty", "is_active")
    list_filter = ("is_active", "course", "faculty")
    search_fields = ("mssv", "full_name", "class_name", "major")
