from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from crop_management.models import Crop
from equipment.models import Equipment
from land_management.models import Field
from livestock.models import Animal


def healthz(request):
    """Liveness/readiness probe for load balancers: checks the database is reachable."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception:
        return JsonResponse({'status': 'error'}, status=503)
    return JsonResponse({'status': 'ok'})


@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {
        'title': 'Farm Management System',
        'field_count': Field.objects.filter(owner=user, is_active=True).count(),
        'crop_count': Crop.objects.filter(owner=user, is_active=True).count(),
        'livestock_count': Animal.objects.filter(owner=user, is_active=True).count(),
        'equipment_count': Equipment.objects.filter(owner=user).count(),
    })
