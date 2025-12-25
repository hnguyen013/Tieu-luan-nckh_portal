# portal/urls/admin/projects.py
from django.urls import path
from portal.views.admin import projects as views

urlpatterns = [
    path("admin-panel/projects/", views.project_list, name="admin-project-list"),
    path("admin-panel/projects/create/", views.project_create, name="admin-project-create"),
    path("admin-panel/projects/<int:project_id>/edit/", views.project_edit, name="admin-project-edit"),
    path("admin-panel/projects/<int:project_id>/toggle-active/", views.project_toggle_active, name="admin-project-toggle-active"),
    path("admin-panel/projects/<int:project_id>/status/", views.project_update_status, name="admin-project-status"),
]
