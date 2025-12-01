from django.contrib.auth.decorators import user_passes_test

def is_officer(user):
    return user.is_authenticated

def admin_required(view_func):
    decorated_view = user_passes_test(
        is_officer,
        login_url="portal:login",
        redirect_field_name=None,
    )(view_func)
    return decorated_view
