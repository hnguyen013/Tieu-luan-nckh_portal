from django.contrib import admin
from portal.models import Faculty, Course, Student


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "name")  # đổi theo field thật của Course
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("mssv", "full_name", "gender", "date_of_birth", "major", "course", "faculty", "status", "email")
    list_filter = ("status", "course", "faculty", "gender")
    search_fields = ("mssv", "full_name", "major", "email")

