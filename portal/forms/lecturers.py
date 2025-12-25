# portal/forms/lecturers.py
from django import forms
from portal.models import Lecturer, Faculty


class AdminLecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = [
            "lecturer_id",
            "full_name",
            "year_of_birth",
            "gender",
            "faculty",
            "email",
            "phone_number",
            "academic_rank",
            "degree",
            "avatar",
            "is_active",
        ]
        widgets = {
            "year_of_birth": forms.NumberInput(attrs={"min": 1900, "max": 2100}),
            "gender": forms.Select(choices=[("M", "Nam"), ("F", "Nữ"), ("O", "Khác")]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dropdown KHOA (Faculty)
        self.fields["faculty"].queryset = Faculty.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )
        self.fields["faculty"].empty_label = "— Chọn khoa —"

        # Placeholder + gợi ý
        self.fields["lecturer_id"].widget.attrs.update({"placeholder": "VD: GV00123"})
        self.fields["full_name"].widget.attrs.update({"placeholder": "Họ tên giảng viên"})
        self.fields["email"].widget.attrs.update({"placeholder": "VD: gv@hueuni.edu.vn"})
        self.fields["phone_number"].widget.attrs.update({"placeholder": "VD: 0901xxxxxx"})
        self.fields["academic_rank"].widget.attrs.update({"placeholder": "VD: Giảng viên chính / PGS / GS"})
        self.fields["degree"].widget.attrs.update({"placeholder": "VD: ThS / TS"})
