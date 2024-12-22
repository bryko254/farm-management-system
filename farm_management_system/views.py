from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from livestock.models import Animal
from crop_management.models import Crop
from equipment.models import Equipment
from land_management.models import Field

@login_required
def home(request):
    """Home page view."""
    context = {
        'title': 'Farm Management System',
        'field_count': Field.objects.filter(owner=request.user).count(),
        'crop_count': Crop.objects.filter(owner=request.user, is_active=True).count(),
        'livestock_count': Animal.objects.filter(owner=request.user, is_active=True).count(),
        'equipment_count': Equipment.objects.filter(owner=request.user).count(),
    }
    return render(request, 'home.html', context)
