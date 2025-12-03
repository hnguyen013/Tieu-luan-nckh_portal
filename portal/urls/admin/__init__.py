from .dashboard import urlpatterns as dashboard_urlpatterns
from .accounts import urlpatterns as accounts_urlpatterns
from .students import urlpatterns as students_urlpatterns

urlpatterns = (
    dashboard_urlpatterns
    + accounts_urlpatterns
    + students_urlpatterns
)
