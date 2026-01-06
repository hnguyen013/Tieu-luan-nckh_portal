# portal/views/public/projects.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Avg, Case, When, Value, CharField
from django.db.models.functions import Round

from portal.models import Project, Council


def public_project_list(request):
    """
    Danh sách đề tài NCKH public
    """
    projects = (
        Project.objects.filter(
            status__in=[
                Project.Status.IN_PROGRESS,
                Project.Status.ACCEPTED,
            ],
            is_active=True,
        )
        .select_related(
            "faculty",
            "academic_year",
            "project_type",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "portal/public/projects_list.html",
        {
            "projects": projects,
        },
    )


def public_project_detail(request, code):
    project = get_object_or_404(
        Project.objects.select_related(
            "faculty",
            "academic_year",
            "project_type",
        ).prefetch_related(
            "project_students",
            "project_lecturers",
        ),
        code=code,
        status__in=[
            Project.Status.IN_PROGRESS,
            Project.Status.ACCEPTED,
        ],
        is_active=True,
    )

    # ✅ Tính điểm + kết quả runtime (không lưu DB)
    council = (
        Council.objects.filter(project=project)
        .prefetch_related("members__lecturer")
        .annotate(
            total_score=Round(Avg("members__score"), 2),
        )
        .annotate(
            result=Case(
                When(total_score__gte=5, then=Value("PASS")),
                default=Value("FAIL"),
                output_field=CharField(),
            )
        )
        .first()
    )

    return render(
        request,
        "portal/public/projects_detail.html",
        {
            "project": project,
            "council": council,
        },
    )
