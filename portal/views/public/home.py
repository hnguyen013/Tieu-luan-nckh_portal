from django.shortcuts import render

def public_home(request):
    return render(request, "portal/public_home.html")
