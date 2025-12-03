# portal/forms/students.py

from django import forms
from portal.models import Student, Faculty, Course


class AdminStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "mssv",
            "full_name",
            "year_of_birth",
            "gender",
            "class_name",
            "major",
            "course",
            "faculty",
            "email",
            "avatar",      
            "is_active",
        ]
        widgets = {
            "year_of_birth": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
            "gender": forms.Select(choices=[("M", "Nam"), ("F", "Nữ"), ("O", "Khác")]),
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*"}),  # 👈 widget upload ảnh
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dropdown KHOA (Faculty)
        self.fields["faculty"].queryset = Faculty.objects.filter(
            is_active=True
        ).order_by("sort_order", "name")
        self.fields["faculty"].empty_label = "— Chọn khoa —"

        # Dropdown KHÓA HỌC (Course)
        self.fields["course"].queryset = Course.objects.filter(
            is_active=True
        ).order_by("sort_order", "code")
        self.fields["course"].empty_label = "— Chọn khóa học —"

        # Không bắt buộc phải chọn khoa/khóa
        self.fields["faculty"].required = False
        self.fields["course"].required = False

        # Các placeholder cho đẹp
        self.fields["mssv"].widget.attrs.update({"placeholder": "VD: 21T102345"})
        self.fields["full_name"].widget.attrs.update({"placeholder": "Họ tên sinh viên"})
        self.fields["class_name"].widget.attrs.update({"placeholder": "VD: K45 Tin"})
        self.fields["major"].widget.attrs.update({"placeholder": "VD: Sư phạm Tin học"})
        self.fields["email"].widget.attrs.update({"placeholder": "VD: sv@hueuni.edu.vn"})

        # Avatar không bắt buộc
        self.fields["avatar"].required = False