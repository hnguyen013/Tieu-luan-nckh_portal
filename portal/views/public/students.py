from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from portal.models import Student, Faculty, Course


def student_list_public(request):
    q = (request.GET.get("q") or "").strip()
    faculty_id = (request.GET.get("faculty_id") or "").strip()
    course_id = (request.GET.get("course_id") or "").strip()
    class_name = (request.GET.get("class_name") or "").strip()

    students = Student.objects.filter(is_active=True)

    if q:
        students = students.filter(
            Q(mssv__icontains=q)
            | Q(full_name__icontains=q)
            | Q(class_name__icontains=q)
            | Q(major__icontains=q)
            | Q(faculty__name__icontains=q)
            | Q(course__code__icontains=q)
            | Q(course__name__icontains=q)
        )

    if faculty_id:
        students = students.filter(faculty_id=faculty_id)

    if course_id:
        students = students.filter(course_id=course_id)

    if class_name:
        students = students.filter(class_name__icontains=class_name)

    faculty_list = Faculty.objects.filter(is_active=True).order_by("sort_order", "name")
    course_list = Course.objects.filter(is_active=True).order_by("sort_order", "code")

    context = {
        "students": students,
        "q": q,
        "faculty_id": faculty_id,
        "course_id": course_id,
        "class_name": class_name,
        "faculty_list": faculty_list,
        "course_list": course_list,
    }
    return render(request, "portal/public/students_list.html", context)


def student_detail_public(request, mssv: str):
    student = get_object_or_404(
        Student,
        mssv__iexact=mssv,
        is_active=True,
    )

    projects = []  # TODO: sau này nối với đề tài

    context = {
        "student": student,
        "projects": projects,
    }
    return render(request, "portal/public/student_detail.html", context)
