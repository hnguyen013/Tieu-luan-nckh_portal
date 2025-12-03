from django.shortcuts import render
from portal.models import Student

def public_home(request):
    # Đếm số sinh viên (đang active)
    student_count = Student.objects.filter(is_active=True).count()

    return render(request, "portal/public_home.html", {
        "student_count": student_count,
    })
