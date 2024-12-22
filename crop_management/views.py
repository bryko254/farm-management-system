from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Crop
from .forms import CropForm

# Create your views here.

@login_required
def crop_list(request):
    crops = Crop.objects.filter(owner=request.user, is_active=True)
    return render(request, 'crop_management/crop_list.html', {'crops': crops})

@login_required
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    return render(request, 'crop_management/crop_detail.html', {'crop': crop})

@login_required
def crop_create(request):
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.owner = request.user
            crop.save()
            messages.success(request, 'Crop created successfully.')
            return redirect('crop_management:crop_detail', pk=crop.pk)
    else:
        form = CropForm()
    
    return render(request, 'crop_management/crop_form.html', {
        'form': form,
        'title': 'Add New Crop'
    })

@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = CropForm(request.POST, instance=crop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Crop updated successfully.')
            return redirect('crop_management:crop_detail', pk=crop.pk)
    else:
        form = CropForm(instance=crop)
    
    return render(request, 'crop_management/crop_form.html', {
        'form': form,
        'title': f'Update Crop: {crop.name}'
    })

@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully.')
        return redirect('crop_management:crop_list')
    return render(request, 'crop_management/crop_confirm_delete.html', {'crop': crop})

@login_required
def planting_schedule(request):
    return render(request, 'crop_management/planting_schedule.html')

@login_required
def inventory_list(request):
    return render(request, 'crop_management/inventory_list.html')

@login_required
def disease_tracking(request):
    return render(request, 'crop_management/disease_tracking.html')
