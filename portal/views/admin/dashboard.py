from django.shortcuts import render
from portal.decorators import admin_required

@admin_required
def dashboard(request):
    return render(request, "portal/admin_dashboard.html", {})
