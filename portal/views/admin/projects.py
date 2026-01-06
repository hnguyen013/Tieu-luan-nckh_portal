# portal/views/admin/projects.py
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.projects import (
    AdminProjectForm,
    CouncilForm,
    CouncilMemberFormSet,
)
from portal.models import (
    Project,
    ProjectLecturer,
    ProjectStudent,
    ProjectAttachment,
    ProjectStatusLog,
    Council,
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

    projects = projects.select_related("faculty", "academic_year", "project_type").order_by("-created_at")

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
    """
    Tạo đề tài (CHƯA nhập hội đồng/điểm).
    Hội đồng + điểm chỉ nhập khi đề tài sang trạng thái ACCEPTED.
    """
    if request.method == "POST":
        form = AdminProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = request.user
            project.save()

            # lecturers
            for lid in form.cleaned_data["lecturer_ids"]:
                ProjectLecturer.objects.create(project=project, lecturer_id=int(lid))

            # students + roles
            student_ids = form.cleaned_data["student_ids"]
            leader_id = int(form.cleaned_data["leader_student_id"])
            for sid in student_ids:
                role = ProjectStudent.Role.LEADER if int(sid) == leader_id else ProjectStudent.Role.MEMBER
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

        messages.error(request, "Có lỗi dữ liệu. Vui lòng kiểm tra lại.")
    else:
        form = AdminProjectForm()

    return render(
        request,
        "portal/projects/project_form.html",
        {
            "form": form,
            # ✅ không render hội đồng khi create
            "council_form": None,
            "member_formset": None,
            "title": "Thêm đề tài",
            "submit_label": "Tạo đề tài",
        },
    )


@admin_required
@transaction.atomic
def project_edit(request, project_id: int):
    """
    Sửa đề tài.
    Hội đồng + điểm chỉ hiện và chỉ lưu khi project.status == ACCEPTED.
    """
    project = get_object_or_404(Project, pk=project_id)

    # ✅ chỉ cho nhập hội đồng/điểm khi nghiệm thu
    show_council = project.status == Project.Status.ACCEPTED

    # Nếu đã nghiệm thu mà không phải superuser thì vẫn chặn sửa (giữ logic cũ của bạn)
    if project.status == Project.Status.ACCEPTED and not request.user.is_superuser:
        messages.error(request, "Đề tài đã nghiệm thu. Bạn không có quyền chỉnh sửa.")
        return redirect("portal:admin-project-list")

    council = None
    if show_council:
        council, _ = Council.objects.get_or_create(
            project=project,
            defaults={"council_title": f"Hội đồng chấm {project.code}"},
        )

    if request.method == "POST":
        form = AdminProjectForm(request.POST, request.FILES, instance=project)

        # ✅ chỉ bind council forms khi show_council
        council_form = CouncilForm(request.POST, instance=council) if show_council else None
        member_formset = CouncilMemberFormSet(request.POST, instance=council) if show_council else None

        ok = form.is_valid()
        if show_council:
            ok = ok and council_form.is_valid() and member_formset.is_valid()

        if ok:
            old_status = project.status
            project = form.save()

            # reset relations
            ProjectLecturer.objects.filter(project=project).delete()
            ProjectStudent.objects.filter(project=project).delete()

            for lid in form.cleaned_data["lecturer_ids"]:
                ProjectLecturer.objects.create(project=project, lecturer_id=int(lid))

            student_ids = form.cleaned_data["student_ids"]
            leader_id = int(form.cleaned_data["leader_student_id"])
            for sid in student_ids:
                role = ProjectStudent.Role.LEADER if int(sid) == leader_id else ProjectStudent.Role.MEMBER
                ProjectStudent.objects.create(project=project, student_id=int(sid), role=role)

            # attachments append
            for f in request.FILES.getlist("attachments"):
                ProjectAttachment.objects.create(
                    project=project,
                    file=f,
                    original_name=getattr(f, "name", ""),
                    uploaded_by=request.user,
                )

            # ✅ lưu hội đồng/điểm nếu đang ACCEPTED
            if show_council:
                council_form.save()
                member_formset.save()

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

        messages.error(request, "Có lỗi dữ liệu. Vui lòng kiểm tra lại.")
    else:
        form = AdminProjectForm(instance=project)

        # init selected ids
        form.initial["lecturer_ids"] = [str(x.lecturer_id) for x in project.project_lecturers.all()]
        selected_students = list(project.project_students.values_list("student_id", flat=True))
        form.initial["student_ids"] = [str(x) for x in selected_students]
        leader = project.project_students.filter(role=ProjectStudent.Role.LEADER).first()
        if leader:
            form.initial["leader_student_id"] = str(leader.student_id)

        council_form = CouncilForm(instance=council) if show_council else None
        member_formset = CouncilMemberFormSet(instance=council) if show_council else None

    return render(
        request,
        "portal/projects/project_form.html",
        {
            "form": form,
            "council_form": council_form,
            "member_formset": member_formset,
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
