from django.urls import path
from portal.views import projects as views

urlpatterns = [
    path(
        "",
        views.public_project_list,
        name="public_project_list",
    ),
    path(
        "<str:code>/",
        views.public_project_detail,
        name="public_project_detail",
    ),
]
