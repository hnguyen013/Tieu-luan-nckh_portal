from django.urls import path

from portal.views.public.students import (
    student_list_public,
    student_detail_public,
)
from portal.views.public.home import public_home
from portal.views.public.projects import (
    public_project_list,
    public_project_detail, 
)

from portal.views.public.lecturers import (
    public_lecturer_list,
    public_lecturer_detail,
)

app_name = "portal"

urlpatterns = [
    path("", public_home, name="public-home"),

    # Public sinh viên
    path("students/", student_list_public, name="public-student-list"),
    path(
        "students/<str:mssv>/",
        student_detail_public,
        name="public-student-detail",
    ),

    # Public đề tài NCKH
    path(
        "projects/",
        public_project_list,
        name="public-project-list",
    ),

    path(
    "projects/<str:code>/",
    public_project_detail,
    name="public-project-detail",
    ),

    # Public giảng viên
    path("lecturers/", public_lecturer_list, name="public-lecturer-list"),
    path(
        "lecturers/<str:mgv>/",
        public_lecturer_detail,
        name="public-lecturer-detail",
    ),
]
