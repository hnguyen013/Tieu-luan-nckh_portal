# portal/urls/admin/students.py
from django.urls import path

from portal.views.admin import students as views

urlpatterns = [
    path(
        "admin-panel/students/",
        views.student_list,
        name="admin-student-list",
    ),
    path(
        "admin-panel/students/create/",
        views.student_create,
        name="admin-student-create",
    ),
    path(
        "admin-panel/students/<int:student_id>/edit/",
        views.student_edit,
        name="admin-student-edit",
    ),
    path(
        "admin-panel/students/<int:student_id>/toggle-active/",
        views.student_toggle_active,
        name="admin-student-toggle-active",
    ),
]
