from django.shortcuts import render, get_object_or_404
from portal.models import Project


def public_project_list(request):
    """
    Danh sách đề tài NCKH public
    Chỉ hiển thị đề tài đã được duyệt và đang thực hiện / đã nghiệm thu
    """
    projects = Project.objects.filter(
        status__in=[
            Project.Status.IN_PROGRESS,  # Đang thực hiện
            Project.Status.ACCEPTED,     # Đã nghiệm thu
        ],
        is_active=True,
    ).select_related(
        "faculty",
        "academic_year",
        "project_type",
    )

    return render(
        request,
        "portal/public/projects_list.html",
        {"projects": projects},
    )


def public_project_detail(request, code):
    """
    Chi tiết đề tài NCKH public
    """
    project = get_object_or_404(
        Project,
        code=code,
        status__in=[
            Project.Status.IN_PROGRESS,  # Đang thực hiện
            Project.Status.ACCEPTED,     # Đã nghiệm thu
        ],
        is_active=True,
    )

    return render(
        request,
        "portal/public/projects_detail.html",
        {"project": project},
    )
