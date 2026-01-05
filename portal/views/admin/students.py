# portal/views/admin/students.py
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.students import AdminStudentForm
from portal.models import Student, Faculty, Course


@admin_required
def student_list(request):
    """
    US 2.4 — Xem danh sách sinh viên.
    - Tìm kiếm theo MSSV, họ tên, ngành, email, khoa, khóa học
    - Lọc theo khoa, khóa học, tình trạng
    """
    q = (request.GET.get("q") or "").strip()
    faculty_id = (request.GET.get("faculty_id") or "").strip()
    course_id = (request.GET.get("course_id") or "").strip()
    status = (request.GET.get("status") or "").strip()

    students = Student.objects.filter(is_active=True)


    if q:
        students = students.filter(
            Q(mssv__icontains=q)
            | Q(full_name__icontains=q)
            | Q(major__name__icontains=q)
            | Q(email__icontains=q)
            | Q(faculty__name__icontains=q)
            | Q(course__name__icontains=q)
        )

    if faculty_id:
        students = students.filter(faculty_id=faculty_id)

    if course_id:
        students = students.filter(course_id=course_id)

    if status:
        students = students.filter(status=status)

    students = students.select_related("faculty", "course").order_by("mssv")

    # dữ liệu dropdown filter
    faculties = Faculty.objects.all().order_by("name")
    courses = Course.objects.all().order_by("name")

    context = {
        "students": students,
        "q": q,
        "faculties": faculties,
        "courses": courses,
        "faculty_id": faculty_id,
        "course_id": course_id,
        "status": status,
        "status_choices": Student.STATUS_CHOICES,
    }
    return render(request, "portal/students/student_list.html", context)


@admin_required
def student_create(request):
    """US 2.1 — Thêm sinh viên."""
    if request.method == "POST":
        form = AdminStudentForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Thêm sinh viên thành công: {student.mssv} - {student.full_name}.")
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
    """US 2.2 — Sửa thông tin sinh viên."""
    student = get_object_or_404(Student, pk=student_id)

    if request.method == "POST":
        form = AdminStudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Cập nhật sinh viên thành công: {student.mssv} - {student.full_name}.")
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
    student = get_object_or_404(Student, pk=student_id)
    student.is_active = not student.is_active
    student.save()

    if student.is_active:
        messages.success(request, f"Đã kích hoạt lại sinh viên {student.mssv} - {student.full_name}.")
    else:
        messages.success(request, f"Đã ngừng theo dõi sinh viên {student.mssv} - {student.full_name}.")
    return redirect("portal:admin-student-list")
