from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    """
    Trang đăng nhập quản trị.
    """
    context = {}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        context["username"] = username  # giữ lại username khi nhập sai

        if not username or not password:
            messages.error(request, "Vui lòng nhập đầy đủ tài khoản và mật khẩu")
            return render(request, "portal/login.html", context)

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Sai tài khoản hoặc mật khẩu")
            return render(request, "portal/login.html", context)

        if not user.is_active:
            messages.error(request, "Tài khoản đã bị khóa. Liên hệ quản trị viên.")
            return render(request, "portal/login.html", context)

        # Đăng nhập OK
        login(request, user)
        return redirect("portal:admin-dashboard")

    # GET hoặc POST lần đầu
    return render(request, "portal/login.html", context)


def logout_view(request):
    """
    Đăng xuất và quay về trang public.
    """
    logout(request)
    return redirect("portal:public-home")
