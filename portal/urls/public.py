# portal/urls/public.py
from django.urls import path

from portal.views.public.home import public_home
from portal.views.public.students import (
    student_list_public,
    student_detail_public,
)

urlpatterns = [
    path("", public_home, name="public-home"),

    # Public sinh viên
    path("students/", student_list_public, name="public-student-list"),
    path("students/<str:mssv>/", student_detail_public, name="public-student-detail"),
]
