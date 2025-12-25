# portal/forms/projects.py
from django import forms
from portal.models import (
    Project, Faculty, AcademicYear, ProjectType, Student
)

# ✅ Widget custom để cho phép multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdminProjectForm(forms.ModelForm):
    lecturer_ids = forms.MultipleChoiceField(
        label="Giảng viên hướng dẫn",
        required=True,
        widget=forms.SelectMultiple(attrs={"size": "6"}),
        choices=[]
    )

    student_ids = forms.MultipleChoiceField(
        label="Sinh viên tham gia",
        required=True,
        widget=forms.SelectMultiple(attrs={"size": "8"}),
        choices=[]
    )

    leader_student_id = forms.ChoiceField(
        label="Trưởng nhóm",
        required=True,
        choices=[]
    )

    # ✅ dùng widget custom MultipleFileInput
    attachments = forms.FileField(
        label="File đính kèm (đề cương/báo cáo)",
        required=False,
        widget=MultipleFileInput(attrs={"multiple": True}),
    )

    class Meta:
        model = Project
        fields = [
            "code", "title", "summary",
            "faculty", "academic_year", "project_type", "status",
            "is_active",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["faculty"].queryset = Faculty.objects.filter(is_active=True).order_by("sort_order", "name")
        self.fields["academic_year"].queryset = AcademicYear.objects.filter(is_active=True).order_by("sort_order", "code")
        self.fields["project_type"].queryset = ProjectType.objects.filter(is_active=True).order_by("sort_order", "name")

        from portal.models import Lecturer
        lecturers = Lecturer.objects.filter(is_active=True).order_by("full_name")
        self.fields["lecturer_ids"].choices = [(str(x.id), f"{x.full_name}") for x in lecturers]

        students = Student.objects.filter(is_active=True).order_by("mssv")
        self.fields["student_ids"].choices = [(str(x.id), f"{x.mssv} - {x.full_name}") for x in students]
        self.fields["leader_student_id"].choices = [("", "— Chọn trưởng nhóm —")] + [
            (str(x.id), f"{x.mssv} - {x.full_name}") for x in students
        ]

    def clean_code(self):
        code = (self.cleaned_data.get("code") or "").strip()
        if not code:
            raise forms.ValidationError("Mã đề tài không được để trống.")
        return code

    def clean(self):
        cleaned = super().clean()

        lecturer_ids = cleaned.get("lecturer_ids") or []
        student_ids = cleaned.get("student_ids") or []
        leader_id = cleaned.get("leader_student_id")

        if not lecturer_ids:
            self.add_error("lecturer_ids", "Phải chọn ít nhất 1 giảng viên hướng dẫn.")
        if not student_ids:
            self.add_error("student_ids", "Phải chọn ít nhất 1 sinh viên tham gia.")
        if leader_id and student_ids and (leader_id not in student_ids):
            self.add_error("leader_student_id", "Trưởng nhóm phải nằm trong danh sách sinh viên tham gia.")

        return cleaned
