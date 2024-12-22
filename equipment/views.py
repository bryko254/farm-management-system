from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def equipment_list(request):
    return render(request, 'equipment/equipment_list.html')

@login_required
def equipment_detail(request, pk):
    return render(request, 'equipment/equipment_detail.html')

@login_required
def equipment_create(request):
    return render(request, 'equipment/equipment_form.html')

@login_required
def maintenance_schedule(request):
    return render(request, 'equipment/maintenance_schedule.html')

@login_required
def fuel_tracking(request):
    return render(request, 'equipment/fuel_tracking.html')
