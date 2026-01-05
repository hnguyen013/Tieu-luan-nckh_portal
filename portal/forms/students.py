# portal/forms/students.py
from django import forms
from portal.models import Student, Faculty, Course, Major


class AdminStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "mssv",
            "full_name",
            "date_of_birth",
            "gender",
            "major",
            "faculty",
            "course",
            "address",
            "email",
            "avatar",
            "status",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "gender": forms.Select(choices=[("M", "Nam"), ("F", "Nữ")]),
            "status": forms.Select(
                choices=[
                    ("studying", "Đang học"),
                    ("leave", "Nghỉ"),
                    ("reserved", "Bảo lưu"),
                    ("graduated", "Tốt nghiệp"),
                ]
            ),
            "avatar": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dropdown NGÀNH (Major)
        self.fields["major"].queryset = Major.objects.all().order_by("name")
        self.fields["major"].empty_label = "— Chọn ngành —"

        # Dropdown KHOA (Faculty)
        self.fields["faculty"].queryset = Faculty.objects.all().order_by("name")
        self.fields["faculty"].empty_label = "— Chọn khoa —"

        # Dropdown KHÓA HỌC (Course)
        self.fields["course"].queryset = Course.objects.all().order_by("name")
        self.fields["course"].empty_label = "— Chọn khóa học —"

        # Placeholder
        self.fields["mssv"].widget.attrs.update({"placeholder": "VD: 21T102345"})
        self.fields["full_name"].widget.attrs.update({"placeholder": "Họ tên sinh viên"})
        self.fields["email"].widget.attrs.update({"placeholder": "VD: sv@hueuni.edu.vn"})
        self.fields["address"].widget.attrs.update({"placeholder": "Địa chỉ liên hệ (có thể bỏ trống)"})

        # Optional fields
        self.fields["avatar"].required = False
        self.fields["address"].required = False
