# portal/forms/lecturer_specialties.py
from django import forms
from django.forms import inlineformset_factory

from portal.models import Lecturer, LecturerSpecialty


class LecturerSpecialtyForm(forms.ModelForm):
    class Meta:
        model = LecturerSpecialty
        fields = ["specialty"]
        widgets = {
            "specialty": forms.TextInput(attrs={"placeholder": "VD: Trí tuệ nhân tạo / Mạng máy tính / CSDL ..."}),
        }


LecturerSpecialtyFormSet = inlineformset_factory(
    parent_model=Lecturer,
    model=LecturerSpecialty,
    form=LecturerSpecialtyForm,
    extra=1,
    can_delete=True,
)
