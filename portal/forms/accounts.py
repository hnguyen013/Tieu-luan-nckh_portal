# portal/forms/accounts.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class AccountCreateForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Mật khẩu",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Xác nhận mật khẩu",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_superuser", "is_active"]
        labels = {
            "username": "Tên đăng nhập",
            "email": "Email",
            "is_staff": "Cán bộ Khoa/KHCN (có quyền truy cập admin)",
            "is_superuser": "Quản trị hệ thống (toàn quyền)",
            "is_active": "Hoạt động",
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get("password1")
        p2 = cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Mật khẩu nhập lại không khớp.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "is_staff", "is_superuser", "is_active"]
        labels = {
            "email": "Email",
            "is_staff": "Cán bộ Khoa/KHCN (có quyền truy cập admin)",
            "is_superuser": "Quản trị hệ thống (toàn quyền)",
            "is_active": "Hoạt động",
        }


class AccountResetPasswordForm(SetPasswordForm):
    # Dùng SetPasswordForm của Django, chỉ đổi label cho dễ hiểu
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label="Nhập lại mật khẩu mới",
        widget=forms.PasswordInput
    )
