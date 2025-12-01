from .public import urlpatterns as public_urlpatterns
from .auth import urlpatterns as auth_urlpatterns
from .admin import urlpatterns as admin_urlpatterns

urlpatterns = public_urlpatterns + auth_urlpatterns + admin_urlpatterns
