# portal/views/public/lecturer.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from portal.models import Lecturer, Faculty, Project


def public_lecturer_list(request):
    lecturers = Lecturer.objects.filter(is_active=True)

    faculty_id = request.GET.get("faculty_id", "").strip()
    q = request.GET.get("q", "").strip()

    if faculty_id:
        lecturers = lecturers.filter(faculty_id=faculty_id)

    if q:
        lecturers = lecturers.filter(
            Q(mgv__icontains=q)
            | Q(full_name__icontains=q)
            | Q(email__icontains=q)
            | Q(academic_rank__icontains=q)
            | Q(address__icontains=q)
            | Q(faculty__name__icontains=q)
        )

    lecturers = lecturers.select_related("faculty").order_by("mgv")

    context = {
        "lecturers": lecturers,
        "faculty_list": Faculty.objects.all(),
        "faculty_id": faculty_id,
        "q": q,
    }

    return render(
        request,
        "portal/public/lecturers_list.html",
        context,
    )


def public_lecturer_detail(request, mgv):
    lecturer = get_object_or_404(
        Lecturer,
        mgv=mgv,
        is_active=True,
    )

    projects = (
        Project.objects.filter(
            project_lecturers__lecturer=lecturer,
            status__in=[
                Project.Status.IN_PROGRESS,
                Project.Status.ACCEPTED,
            ],
            is_active=True,
        )
        .distinct()
    )

    return render(
        request,
        "portal/public/lecturer_detail.html",
        {
            "lecturer": lecturer,
            "projects": projects,
        },
    )
