# portal/forms/projects.py
from django import forms
from django.forms import inlineformset_factory

from portal.models import (
    Project,
    Faculty,
    AcademicYear,
    ProjectType,
    Student,
    Council,
    CouncilMember,
)

# ✅ Widget custom để cho phép multiple files
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class AdminProjectForm(forms.ModelForm):
    lecturer_ids = forms.MultipleChoiceField(
        label="Giảng viên hướng dẫn",
        required=True,
        widget=forms.SelectMultiple(attrs={"size": "6"}),
        choices=[],
    )

    student_ids = forms.MultipleChoiceField(
        label="Sinh viên tham gia",
        required=True,
        widget=forms.SelectMultiple(attrs={"size": "8"}),
        choices=[],
    )

    leader_student_id = forms.ChoiceField(
        label="Trưởng nhóm",
        required=True,
        choices=[],
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
            "code",
            "title",
            "project_level",
            "research_field",
            "host_organization",
            "implementing_organization",
            "objectives",
            "summary",
            "budget",
            "category",
            "start_year",
            "end_year",
            "faculty",
            "academic_year",
            "project_type",
            "status",
            "is_active",
        ]
        widgets = {
            "objectives": forms.Textarea(attrs={"rows": 3}),
            "summary": forms.Textarea(attrs={"rows": 4}),
            "start_year": forms.DateInput(attrs={"type": "date"}),
            "end_year": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Faculty: không có is_active/sort_order trong DB của bạn -> chỉ order theo name
        self.fields["faculty"].queryset = Faculty.objects.all().order_by("name")

        # AcademicYear / ProjectType: giữ như cũ (nếu model bạn có is_active/sort_order)
        # Nếu sau này báo FieldError thì bạn đổi tương tự sang .all().order_by(...)
        self.fields["academic_year"].queryset = AcademicYear.objects.filter(is_active=True).order_by(
            "sort_order", "code"
        )
        self.fields["project_type"].queryset = ProjectType.objects.filter(is_active=True).order_by(
            "sort_order", "name"
        )

        from portal.models import Lecturer

        lecturers = Lecturer.objects.filter(is_active=True).order_by("full_name")
        self.fields["lecturer_ids"].choices = [(str(x.id), f"{x.full_name}") for x in lecturers]

        students = Student.objects.filter(is_active=True).order_by("mssv")
        self.fields["student_ids"].choices = [(str(x.id), f"{x.mssv} - {x.full_name}") for x in students]
        self.fields["leader_student_id"].choices = [("", "— Chọn trưởng nhóm —")] + [
            (str(x.id), f"{x.mssv} - {x.full_name}") for x in students
        ]

        # Placeholders (cho dễ nhập)
        self.fields["code"].widget.attrs.update({"placeholder": "VD: DT2026-001"})
        self.fields["title"].widget.attrs.update({"placeholder": "Tên đề tài"})
        self.fields["project_level"].widget.attrs.update({"placeholder": "VD: Cấp Khoa / Cấp Trường / Cấp Bộ"})
        self.fields["host_organization"].widget.attrs.update({"placeholder": "Đơn vị chủ trì"})
        self.fields["implementing_organization"].widget.attrs.update({"placeholder": "Đơn vị thực hiện"})
        # category là select theo choices -> placeholder thường không có tác dụng, nhưng để cũng không sao
        self.fields["category"].widget.attrs.update({"placeholder": "VD: Báo cáo / Sản phẩm / Bài báo..."})

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

        # validate thời gian
        start = cleaned.get("start_year")
        end = cleaned.get("end_year")
        if start and end and end < start:
            self.add_error("end_year", "Ngày kết thúc phải lớn hơn hoặc bằng ngày bắt đầu.")

        return cleaned


# =========================
# ✅ Council forms (mới thêm)
# =========================

class CouncilForm(forms.ModelForm):
    """
    Form thông tin hội đồng (gắn với Project thông qua OneToOne Council.project)
    """
    class Meta:
        model = Council
        fields = ["council_title", "grading_date", "notes"]
        widgets = {
            "grading_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_council_title(self):
        title = (self.cleaned_data.get("council_title") or "").strip()
        # Cho phép rỗng cũng được tùy bạn, nhưng thường nên có
        if not title:
            raise forms.ValidationError("Tên hội đồng không được để trống.")
        return title


class CouncilMemberForm(forms.ModelForm):
    """
    1 dòng thành viên hội đồng + điểm
    """
    class Meta:
        model = CouncilMember
        fields = ["lecturer", "role", "component_score"]
        widgets = {
            "component_score": forms.NumberInput(attrs={"step": "0.01", "min": "0", "max": "10"}),
        }

    def clean_role(self):
        role = (self.cleaned_data.get("role") or "").strip()
        if not role:
            raise forms.ValidationError("Vai trò không được để trống.")
        return role


CouncilMemberFormSet = inlineformset_factory(
    parent_model=Council,
    model=CouncilMember,
    form=CouncilMemberForm,
    fields=["lecturer", "role", "component_score"],
    extra=3,          # hiện 3 dòng trống để nhập
    can_delete=True,  # cho phép tick xoá dòng
)
