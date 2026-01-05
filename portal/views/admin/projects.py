# portal/views/admin/projects.py
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.projects import AdminProjectForm
from portal.models import (
    Project,
    ProjectLecturer,
    ProjectStudent,
    ProjectAttachment,
    ProjectStatusLog,
)


@admin_required
def project_list(request):
    q = (request.GET.get("q") or "").strip()
    status = (request.GET.get("status") or "").strip()
    include_inactive = request.GET.get("include_inactive") == "1"

    projects = Project.objects.all()

    if not include_inactive:
        projects = projects.filter(is_active=True)

    if q:
        projects = projects.filter(
            Q(code__icontains=q)
            | Q(title__icontains=q)
            | Q(project_level__icontains=q)
            | Q(research_field__icontains=q)
            | Q(host_organization__icontains=q)
            | Q(implementing_organization__icontains=q)
            | Q(category__icontains=q)
            | Q(faculty__name__icontains=q)
        )

    if status:
        projects = projects.filter(status=status)

    projects = projects.select_related(
        "faculty", "academic_year", "project_type"
    ).order_by("-created_at")

    return render(
        request,
        "portal/projects/project_list.html",
        {
            "projects": projects,
            "q": q,
            "status": status,
            "include_inactive": include_inactive,
            "status_choices": Project.Status.choices,
        },
    )

@admin_required
@transaction.atomic
def project_create(request):
    if request.method == "POST":
        form = AdminProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            # lecturers
            lecturer_ids = form.cleaned_data["lecturer_ids"]
            for lid in lecturer_ids:
                ProjectLecturer.objects.create(project=project, lecturer_id=int(lid))

            # students + roles
            student_ids = form.cleaned_data["student_ids"]
            leader_id = int(form.cleaned_data["leader_student_id"])
            for sid in student_ids:
                role = (
                    ProjectStudent.Role.LEADER
                    if int(sid) == leader_id
                    else ProjectStudent.Role.MEMBER
                )
                ProjectStudent.objects.create(project=project, student_id=int(sid), role=role)

            # attachments (multiple)
            for f in request.FILES.getlist("attachments"):
                ProjectAttachment.objects.create(
                    project=project,
                    file=f,
                    original_name=getattr(f, "name", ""),
                    uploaded_by=request.user,
                )

            # log status create
            ProjectStatusLog.objects.create(
                project=project,
                from_status="",
                to_status=project.status,
                changed_by=request.user,
                note="Tạo mới đề tài",
            )

            messages.success(request, f"Đã thêm đề tài: {project.code} - {project.title}")
            return redirect("portal:admin-project-list")
    else:
        form = AdminProjectForm()

    return render(
        request,
        "portal/projects/project_form.html",
        {
            "form": form,
            "title": "Thêm đề tài",
            "submit_label": "Tạo đề tài",
        },
    )


@admin_required
@transaction.atomic
def project_edit(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)

    # Hạn chế sửa nếu đã nghiệm thu: tuỳ quyền (ở đây: chỉ admin mới cho sửa)
    if project.status == Project.Status.ACCEPTED and not request.user.is_superuser:
        messages.error(request, "Đề tài đã nghiệm thu. Bạn không có quyền chỉnh sửa.")
        return redirect("portal:admin-project-list")

    if request.method == "POST":
        form = AdminProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            old_status = project.status
            project = form.save()

            # reset relations
            ProjectLecturer.objects.filter(project=project).delete()
            ProjectStudent.objects.filter(project=project).delete()

            lecturer_ids = form.cleaned_data["lecturer_ids"]
            for lid in lecturer_ids:
                ProjectLecturer.objects.create(project=project, lecturer_id=int(lid))

            student_ids = form.cleaned_data["student_ids"]
            leader_id = int(form.cleaned_data["leader_student_id"])
            for sid in student_ids:
                role = (
                    ProjectStudent.Role.LEADER
                    if int(sid) == leader_id
                    else ProjectStudent.Role.MEMBER
                )
                ProjectStudent.objects.create(project=project, student_id=int(sid), role=role)

            # attachments append
            for f in request.FILES.getlist("attachments"):
                ProjectAttachment.objects.create(
                    project=project,
                    file=f,
                    original_name=getattr(f, "name", ""),
                    uploaded_by=request.user,
                )

            # log status if changed
            if old_status != project.status:
                ProjectStatusLog.objects.create(
                    project=project,
                    from_status=old_status,
                    to_status=project.status,
                    changed_by=request.user,
                    note="Cập nhật đề tài",
                )

            messages.success(request, f"Đã cập nhật đề tài: {project.code}")
            return redirect("portal:admin-project-list")
    else:
        # init selected ids
        form = AdminProjectForm(instance=project)
        form.initial["lecturer_ids"] = [str(x.lecturer_id) for x in project.project_lecturers.all()]
        selected_students = list(project.project_students.values_list("student_id", flat=True))
        form.initial["student_ids"] = [str(x) for x in selected_students]
        leader = project.project_students.filter(role=ProjectStudent.Role.LEADER).first()
        if leader:
            form.initial["leader_student_id"] = str(leader.student_id)

    return render(
        request,
        "portal/projects/project_form.html",
        {
            "form": form,
            "title": f"Sửa đề tài: {project.code}",
            "submit_label": "Lưu thay đổi",
            "project": project,
        },
    )


@admin_required
def project_toggle_active(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)

    project.is_active = not project.is_active
    project.save(update_fields=["is_active", "updated_at"])

    if project.is_active:
        messages.success(request, f"Đã kích hoạt lại đề tài {project.code}.")
    else:
        messages.success(request, f"Đã ẩn đề tài {project.code}.")

    return redirect("portal:admin-project-list")


@admin_required
@transaction.atomic
def project_update_status(request, project_id: int):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        new_status = (request.POST.get("status") or "").strip()
        note = (request.POST.get("note") or "").strip()

        if new_status not in dict(Project.Status.choices):
            messages.error(request, "Trạng thái không hợp lệ.")
            return redirect("portal:admin-project-status", project_id=project.id)

        old_status = project.status
        if old_status == new_status:
            messages.info(request, "Trạng thái không thay đổi.")
            return redirect("portal:admin-project-status", project_id=project.id)

        project.status = new_status
        project.save(update_fields=["status", "updated_at"])

        ProjectStatusLog.objects.create(
            project=project,
            from_status=old_status,
            to_status=new_status,
            changed_by=request.user,
            note=note,
        )

        messages.success(request, "Cập nhật trạng thái thành công.")
        return redirect("portal:admin-project-list")

    return render(
        request,
        "portal/projects/project_status.html",
        {
            "project": project,
            "status_choices": Project.Status.choices,
        },
    )
