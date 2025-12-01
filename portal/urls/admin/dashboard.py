from django.urls import path
from portal.views.admin.dashboard import dashboard

urlpatterns = [
    path("admin-panel/", dashboard, name="admin-dashboard"),
]
