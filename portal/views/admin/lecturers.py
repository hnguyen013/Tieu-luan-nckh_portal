# portal/views/admin/lecturers.py
from django.contrib import messages
from django.db.models import Q
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.lecturers import AdminLecturerForm
from portal.forms.lecturer_languages import LecturerLanguageFormSet
from portal.forms.lecturer_specialties import LecturerSpecialtyFormSet
from portal.models import Lecturer, Faculty


@admin_required
def lecturer_list(request):
    """
    US 3.4 — Xem danh sách giảng viên
    - Tìm kiếm theo: mã GV, họ tên, khoa, email, sđt
    """
    q = (request.GET.get("q") or "").strip()
    faculty_id = (request.GET.get("faculty") or "").strip()
    include_inactive = request.GET.get("include_inactive") == "1"

    lecturers = Lecturer.objects.all()

    if not include_inactive:
        lecturers = lecturers.filter(is_active=True)

    if q:
        lecturers = lecturers.filter(
            Q(mgv__icontains=q)
            | Q(full_name__icontains=q)
            | Q(email__icontains=q)
            | Q(phone_number__icontains=q)
            | Q(faculty__name__icontains=q)
            | Q(faculty__code__icontains=q)
        )

    if faculty_id:
        lecturers = lecturers.filter(faculty_id=faculty_id)

    lecturers = (
        lecturers.select_related("faculty")
        .prefetch_related("languages", "specialties")
        .order_by("mgv")
    )
    faculties = Faculty.objects.all().order_by("name")

    return render(
        request,
        "portal/lecturers/lecturer_list.html",
        {
            "lecturers": lecturers,
            "q": q,
            "faculty_id": faculty_id,
            "include_inactive": include_inactive,
            "faculties": faculties,
        },
    )


@admin_required
@transaction.atomic
def lecturer_create(request):
    """
    US 3.1 — Thêm giảng viên + Ngoại ngữ + Chuyên môn
    """
    if request.method == "POST":
        form = AdminLecturerForm(request.POST, request.FILES)

        if form.is_valid():
            lecturer = form.save()

            language_formset = LecturerLanguageFormSet(request.POST, instance=lecturer)
            specialty_formset = LecturerSpecialtyFormSet(request.POST, instance=lecturer)

            if language_formset.is_valid() and specialty_formset.is_valid():
                language_formset.save()
                specialty_formset.save()

                messages.success(
                    request,
                    f"Thêm giảng viên thành công: {lecturer.mgv} - {lecturer.full_name}.",
                )
                return redirect("portal:admin-lecturer-list")

            # Nếu formset lỗi -> xóa lecturer vừa tạo để tránh data rác
            lecturer.delete()

            return render(
                request,
                "portal/lecturers/lecturer_form.html",
                {
                    "form": form,
                    "language_formset": language_formset,
                    "specialty_formset": specialty_formset,
                    "title": "Thêm giảng viên",
                    "submit_label": "Thêm giảng viên",
                },
            )

        # form lỗi => vẫn tạo formset rỗng để render lại
        language_formset = LecturerLanguageFormSet(request.POST)
        specialty_formset = LecturerSpecialtyFormSet(request.POST)

        return render(
            request,
            "portal/lecturers/lecturer_form.html",
            {
                "form": form,
                "language_formset": language_formset,
                "specialty_formset": specialty_formset,
                "title": "Thêm giảng viên",
                "submit_label": "Thêm giảng viên",
            },
        )

    # GET
    form = AdminLecturerForm()
    language_formset = LecturerLanguageFormSet()
    specialty_formset = LecturerSpecialtyFormSet()

    return render(
        request,
        "portal/lecturers/lecturer_form.html",
        {
            "form": form,
            "language_formset": language_formset,
            "specialty_formset": specialty_formset,
            "title": "Thêm giảng viên",
            "submit_label": "Thêm giảng viên",
        },
    )


@admin_required
@transaction.atomic
def lecturer_edit(request, lecturer_pk: int):
    """
    US 3.2 — Sửa giảng viên + Ngoại ngữ + Chuyên môn
    """
    lecturer = get_object_or_404(Lecturer, pk=lecturer_pk)

    if request.method == "POST":
        form = AdminLecturerForm(request.POST, request.FILES, instance=lecturer)
        language_formset = LecturerLanguageFormSet(request.POST, instance=lecturer)
        specialty_formset = LecturerSpecialtyFormSet(request.POST, instance=lecturer)

        if form.is_valid() and language_formset.is_valid() and specialty_formset.is_valid():
            lecturer = form.save()
            language_formset.save()
            specialty_formset.save()

            messages.success(
                request,
                f"Cập nhật giảng viên thành công: {lecturer.mgv} - {lecturer.full_name}.",
            )
            return redirect("portal:admin-lecturer-list")
    else:
        form = AdminLecturerForm(instance=lecturer)
        language_formset = LecturerLanguageFormSet(instance=lecturer)
        specialty_formset = LecturerSpecialtyFormSet(instance=lecturer)

    return render(
        request,
        "portal/lecturers/lecturer_form.html",
        {
            "form": form,
            "language_formset": language_formset,
            "specialty_formset": specialty_formset,
            "title": f"Sửa giảng viên: {lecturer.mgv}",
            "submit_label": "Lưu thay đổi",
            "lecturer": lecturer,
        },
    )


@admin_required
def lecturer_toggle_active(request, lecturer_pk: int):
    """
    US 3.3 — Soft delete bằng is_active
    """
    lecturer = get_object_or_404(Lecturer, pk=lecturer_pk)
    lecturer.is_active = not lecturer.is_active
    lecturer.save(update_fields=["is_active", "updated_at"])

    if lecturer.is_active:
        messages.success(request, f"Đã kích hoạt lại giảng viên {lecturer.mgv}.")
    else:
        messages.success(request, f"Đã ngừng sử dụng giảng viên {lecturer.mgv}.")

    return redirect("portal:admin-lecturer-list")
