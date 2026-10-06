from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CropForm
from .models import Crop


@login_required
def crop_list(request):
    crops = Crop.objects.filter(owner=request.user, is_active=True).select_related('field')
    return render(request, 'crop_management/crop_list.html', {'crops': crops})


@login_required
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    return render(request, 'crop_management/crop_detail.html', {'crop': crop})


@login_required
def crop_create(request):
    form = CropForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        crop = form.save(commit=False)
        crop.owner = request.user
        crop.save()
        messages.success(request, 'Crop created successfully.')
        return redirect('crop_management:crop_detail', pk=crop.pk)
    return render(request, 'crop_management/crop_form.html', {'form': form, 'title': 'Add New Crop'})


@login_required
def crop_update(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    form = CropForm(request.POST or None, instance=crop, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Crop updated successfully.')
        return redirect('crop_management:crop_detail', pk=crop.pk)
    return render(request, 'crop_management/crop_form.html', {
        'form': form, 'title': f'Update Crop: {crop.name}',
    })


@login_required
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk, owner=request.user)
    if request.method == 'POST':
        crop.delete()
        messages.success(request, 'Crop deleted successfully.')
        return redirect('crop_management:crop_list')
    return render(request, 'crop_management/crop_confirm_delete.html', {'crop': crop})
