# portal/views/admin/students.py
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.students import AdminStudentForm
from portal.models import Student


@admin_required
def student_list(request):
    """
    US 2.4 — Xem danh sách sinh viên.
    - Tìm kiếm theo MSSV, họ tên, lớp, khoa.
    """

    q = (request.GET.get("q") or "").strip()
    faculty = (request.GET.get("faculty") or "").strip()
    class_name = (request.GET.get("class_name") or "").strip()
    include_inactive = request.GET.get("include_inactive") == "1"

    students = Student.objects.all()

    # Mặc định chỉ hiển thị SV đang active, trừ khi tick "include_inactive"
    if not include_inactive:
        students = students.filter(is_active=True)

    if q:
        students = students.filter(
            Q(mssv__icontains=q)
            | Q(full_name__icontains=q)
            | Q(class_name__icontains=q)
            | Q(major__icontains=q)
            | Q(faculty__name__icontains=q)    # 🔹 tìm theo tên khoa
            | Q(faculty__code__icontains=q)    # 🔹 hoặc mã khoa (nếu có)
        )

    if faculty:
        # Ở đây 'faculty' là text người dùng gõ, mình cho match theo name
        students = students.filter(
            Q(faculty__name__icontains=faculty)
            | Q(faculty__code__icontains=faculty)
        )

    if class_name:
        students = students.filter(class_name__icontains=class_name)

    # Tăng hiệu năng / tránh query lặp
    students = students.select_related("faculty", "course").order_by("mssv")

    context = {
        "students": students,
        "q": q,
        "faculty": faculty,
        "class_name": class_name,
        "include_inactive": include_inactive,
    }
    return render(request, "portal/students/student_list.html", context)


@admin_required
def student_create(request):
    """
    US 2.1 — Thêm sinh viên.
    """
    if request.method == "POST":
        form = AdminStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Thêm sinh viên thành công: {student.mssv} - {student.full_name}.",
            )
            return redirect("portal:admin-student-list")
    else:
        form = AdminStudentForm()

    return render(
        request,
        "portal/students/student_form.html",
        {
            "form": form,
            "title": "Thêm sinh viên",
            "submit_label": "Thêm sinh viên",
        },
    )


@admin_required
def student_edit(request, student_id: int):
    """
    US 2.2 — Sửa thông tin sinh viên.
    """
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        form = AdminStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Cập nhật thông tin sinh viên thành công: {student.mssv} - {student.full_name}.",
            )
            return redirect("portal:admin-student-list")
    else:
        form = AdminStudentForm(instance=student)

    return render(
        request,
        "portal/students/student_form.html",
        {
            "form": form,
            "title": f"Sửa sinh viên: {student.mssv}",
            "submit_label": "Lưu thay đổi",
        },
    )


@admin_required
def student_toggle_active(request, student_id: int):
    """
    US 2.3 — Ngừng sử dụng / xóa sinh viên

    Hiện tại:
      - Chỉ toggle is_active (soft delete).
    Sau này:
      - Nếu sinh viên đã có ràng buộc với Đề tài (ProjectStudent)
        thì chỉ cho phép is_active=False, không xóa cứng để giữ lịch sử.
    """
    student = get_object_or_404(Student, pk=student_id)

    student.is_active = not student.is_active
    student.save()

    if student.is_active:
        messages.success(
            request,
            f"Đã kích hoạt lại sinh viên {student.mssv} - {student.full_name}.",
        )
    else:
        messages.success(
            request,
            f"Đã ngừng theo dõi sinh viên {student.mssv} - {student.full_name}.",
        )

    return redirect("portal:admin-student-list")
