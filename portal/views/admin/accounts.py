from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from portal.decorators import admin_required
from portal.forms.accounts import (
    AccountCreateForm,
    AccountUpdateForm,
    AccountResetPasswordForm,
)


from functools import wraps


def superuser_required(view_func):
    """
    Chỉ superuser mới được dùng các chức năng quản lý tài khoản.
    - Nếu chưa đăng nhập -> chuyển về trang login.
    - Nếu đã đăng nhập nhưng không phải superuser -> báo 'không đủ quyền'
      và chuyển về dashboard admin.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        # Chưa đăng nhập -> cho về login như bình thường
        if not request.user.is_authenticated:
            return redirect("portal:login")

        # Đã đăng nhập nhưng không phải superuser
        if not request.user.is_superuser:
            messages.error(request, "Bạn không có quyền truy cập chức năng này.")
            return redirect("portal:admin-dashboard")

        # Đủ quyền -> cho chạy view gốc
        return view_func(request, *args, **kwargs)

    return _wrapped


@admin_required
@superuser_required
def account_list(request):
    users = User.objects.order_by("username")
    return render(request, "portal/accounts/account_list.html", {"users": users})


@admin_required
@superuser_required
def account_create(request):
    if request.method == "POST":
        form = AccountCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tạo tài khoản mới thành công.")
            return redirect("portal:admin-account-list")
    else:
        form = AccountCreateForm(initial={"is_active": True, "is_staff": True})

    return render(
        request,
        "portal/accounts/account_form.html",
        {
            "form": form,
            "title": "Tạo tài khoản mới",
            "submit_label": "Tạo tài khoản",
        },
    )


@admin_required
@superuser_required
def account_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = AccountUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Cập nhật tài khoản thành công.")
            return redirect("portal:admin-account-list")
    else:
        form = AccountUpdateForm(instance=user)

    return render(
        request,
        "portal/accounts/account_form.html",
        {
            "form": form,
            "title": f"Chỉnh sửa tài khoản: {user.username}",
            "submit_label": "Lưu thay đổi",
        },
    )


@admin_required
@superuser_required
def account_toggle_active(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Không cho tự khóa chính mình
    if user == request.user:
        messages.error(request, "Không thể khóa tài khoản đang đăng nhập.")
        return redirect("portal:admin-account-list")

    user.is_active = not user.is_active
    user.save()
    state = "mở khóa" if user.is_active else "khóa"
    messages.success(request, f"Đã {state} tài khoản {user.username}.")
    return redirect("portal:admin-account-list")


@admin_required
@superuser_required
def account_reset_password(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == "POST":
        form = AccountResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Đã đặt lại mật khẩu cho {user.username}.")
            return redirect("portal:admin-account-list")
    else:
        form = AccountResetPasswordForm(user)

    return render(
        request,
        "portal/accounts/account_reset_password.html",
        {
            "form": form,
            "title": f"Đặt lại mật khẩu: {user.username}",
        },
    )
