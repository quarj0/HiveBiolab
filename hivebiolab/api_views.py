from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .content_data import PROJECTS_DATA, TRAINING_PROGRAMS_DATA


@require_GET
def list_projects(request):
    """Return the curated list of Hive Biolab projects."""
    return JsonResponse({"projects": PROJECTS_DATA})


@require_GET
def list_training_programs(request):
    """Return the catalog of training programs we offer."""
    return JsonResponse({"programs": TRAINING_PROGRAMS_DATA})
