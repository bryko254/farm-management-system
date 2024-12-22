from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Field, SoilAnalysis, IrrigationSystem, IrrigationSchedule
from .forms import FieldForm, SoilAnalysisForm, IrrigationSystemForm, IrrigationScheduleForm

@login_required
def field_list(request):
    fields = Field.objects.filter(owner=request.user, is_active=True)
    return render(request, 'land_management/field_list.html', {'fields': fields})

@login_required
def field_detail(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    soil_analyses = field.soil_analyses.all()
    irrigation_systems = field.irrigation_systems.all()
    context = {
        'field': field,
        'soil_analyses': soil_analyses,
        'irrigation_systems': irrigation_systems,
    }
    return render(request, 'land_management/field_detail.html', context)

@login_required
def field_create(request):
    if request.method == 'POST':
        form = FieldForm(request.POST)
        if form.is_valid():
            field = form.save(commit=False)
            field.owner = request.user
            field.save()
            messages.success(request, 'Field created successfully.')
            return redirect('land_management:field_detail', pk=field.pk)
    else:
        form = FieldForm()
    return render(request, 'land_management/field_form.html', {'form': form, 'title': 'Add New Field'})

@login_required
def field_update(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = FieldForm(request.POST, instance=field)
        if form.is_valid():
            form.save()
            messages.success(request, 'Field updated successfully.')
            return redirect('land_management:field_detail', pk=field.pk)
    else:
        form = FieldForm(instance=field)
    return render(request, 'land_management/field_form.html', {'form': form, 'title': 'Update Field'})

@login_required
def field_delete(request, pk):
    field = get_object_or_404(Field, pk=pk, owner=request.user)
    if request.method == 'POST':
        field.delete()
        messages.success(request, 'Field deleted successfully.')
        return redirect('land_management:field_list')
    return render(request, 'land_management/field_confirm_delete.html', {'field': field})

@login_required
def soil_analysis_list(request):
    analyses = SoilAnalysis.objects.filter(field__owner=request.user)
    return render(request, 'land_management/soil_analysis_list.html', {'analyses': analyses})

@login_required
def soil_analysis_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, owner=request.user)
    if request.method == 'POST':
        form = SoilAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.field = field
            analysis.save()
            messages.success(request, 'Soil analysis added successfully.')
            return redirect('land_management:field_detail', pk=field_pk)
    else:
        form = SoilAnalysisForm()
    return render(request, 'land_management/soil_analysis_form.html', {
        'form': form,
        'field': field,
        'title': 'Add Soil Analysis'
    })

@login_required
def irrigation_list(request):
    irrigation_systems = IrrigationSystem.objects.filter(field__owner=request.user, is_active=True)
    return render(request, 'land_management/irrigation_list.html', {'irrigation_systems': irrigation_systems})

@login_required
def irrigation_create(request, field_pk):
    field = get_object_or_404(Field, pk=field_pk, owner=request.user)
    if request.method == 'POST':
        form = IrrigationSystemForm(request.POST)
        if form.is_valid():
            system = form.save(commit=False)
            system.field = field
            system.save()
            messages.success(request, 'Irrigation system added successfully.')
            return redirect('land_management:field_detail', pk=field_pk)
    else:
        form = IrrigationSystemForm()
    return render(request, 'land_management/irrigation_form.html', {
        'form': form,
        'field': field,
        'title': 'Add Irrigation System'
    })

@login_required
def irrigation_schedule_create(request, system_pk):
    system = get_object_or_404(IrrigationSystem, pk=system_pk, field__owner=request.user)
    if request.method == 'POST':
        form = IrrigationScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.irrigation_system = system
            schedule.save()
            messages.success(request, 'Irrigation schedule added successfully.')
            return redirect('land_management:field_detail', pk=system.field.pk)
    else:
        form = IrrigationScheduleForm()
    return render(request, 'land_management/irrigation_schedule_form.html', {
        'form': form,
        'system': system,
        'title': 'Add Irrigation Schedule'
    })
