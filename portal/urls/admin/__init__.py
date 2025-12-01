from .dashboard import urlpatterns as dashboard_urlpatterns
from .accounts import urlpatterns as accounts_urlpatterns

urlpatterns = dashboard_urlpatterns + accounts_urlpatterns
