# portal/forms/lecturer_languages.py
from django import forms
from django.forms import inlineformset_factory

from portal.models import Lecturer, LecturerLanguage


class LecturerLanguageForm(forms.ModelForm):
    class Meta:
        model = LecturerLanguage
        fields = ["language", "level"]
        widgets = {
            "language": forms.TextInput(attrs={"placeholder": "VD: English / Japanese"}),
            "level": forms.TextInput(attrs={"placeholder": "VD: B2 / N3 / IELTS 6.5"}),
        }


LecturerLanguageFormSet = inlineformset_factory(
    parent_model=Lecturer,
    model=LecturerLanguage,
    form=LecturerLanguageForm,
    extra=1,          # mặc định 1 dòng trống
    can_delete=True,  # cho phép tick xóa
)
