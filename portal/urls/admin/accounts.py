from django.urls import path
from portal.views.admin import accounts as views

urlpatterns = [
    path("admin-panel/accounts/", views.account_list, name="admin-account-list"),
    path("admin-panel/accounts/create/", views.account_create, name="admin-account-create"),
    path("admin-panel/accounts/<int:user_id>/edit/", views.account_edit, name="admin-account-edit"),
    path(
        "admin-panel/accounts/<int:user_id>/toggle-active/",
        views.account_toggle_active,
        name="admin-account-toggle-active",
    ),
    path(
        "admin-panel/accounts/<int:user_id>/reset-password/",
        views.account_reset_password,
        name="admin-account-reset-password",
    ),
]
