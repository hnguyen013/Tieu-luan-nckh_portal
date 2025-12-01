from django.urls import path
from portal.views.public.home import public_home

urlpatterns = [
    path("", public_home, name="public-home"),
]
