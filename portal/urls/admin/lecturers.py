# portal/urls/admin/lecturers.py
from django.urls import path
from portal.views.admin import lecturers as views

urlpatterns = [
    path("admin-panel/lecturers/", views.lecturer_list, name="admin-lecturer-list"),
    path("admin-panel/lecturers/create/", views.lecturer_create, name="admin-lecturer-create"),
    path("admin-panel/lecturers/<int:lecturer_pk>/edit/", views.lecturer_edit, name="admin-lecturer-edit"),
    path(
        "admin-panel/lecturers/<int:lecturer_pk>/toggle-active/",
        views.lecturer_toggle_active,
        name="admin-lecturer-toggle-active",
    ),
]
