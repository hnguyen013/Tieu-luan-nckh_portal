# portal/forms/lecturers.py
from django import forms
from portal.models import Lecturer, Faculty


class AdminLecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = [
            "mgv",
            "full_name",
            "date_of_birth",
            "gender",
            "email",
            "phone_number",
            "academic_rank",
            "address",
            "avatar",
            "faculty",
            "status",
            "is_active",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "gender": forms.Select(choices=[("M", "Nam"), ("F", "Nữ"), ("O", "Khác")]),
            "status": forms.Select(
                choices=[
                    ("working", "Đang công tác"),
                    ("leave", "Nghỉ/Ngưng công tác"),
                    ("retired", "Nghỉ hưu"),
                ]
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dropdown KHOA (Faculty)
        self.fields["faculty"].queryset = Faculty.objects.all().order_by("sort_order", "name")

        self.fields["faculty"].empty_label = "— Chọn khoa —"

        # Placeholder + gợi ý
        self.fields["mgv"].widget.attrs.update({"placeholder": "VD: GV00123"})
        self.fields["full_name"].widget.attrs.update({"placeholder": "Họ tên giảng viên"})
        self.fields["email"].widget.attrs.update({"placeholder": "VD: gv@hueuni.edu.vn"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "VD: 0901xxxxxx"})
        self.fields["academic_rank"].widget.attrs.update({"placeholder": "VD: Giảng viên chính / PGS / GS"})
        self.fields["address"].widget.attrs.update({"placeholder": "Địa chỉ (nếu có)"})
