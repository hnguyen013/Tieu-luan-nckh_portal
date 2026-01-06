# portal/views/admin/councils.py
from django.shortcuts import render
from django.db.models import Avg, Case, When, Value, CharField
from django.db.models.functions import Round

from portal.decorators import admin_required
from portal.models import Council


@admin_required
def council_list(request):
    councils = (
        Council.objects.select_related("project")
        .prefetch_related("members")
        .annotate(total_score=Round(Avg("members__score"), 2))
        .annotate(
            result=Case(
                When(total_score__gte=5, then=Value("PASS")),
                default=Value("FAIL"),
                output_field=CharField(),
            )
        )
        .order_by("-grading_date", "code")
    )

    return render(
        request,
        "admin/councils/list.html",
        {"councils": councils},
    )
