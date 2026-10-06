from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from farm_management_system.mixins import OwnedDeleteMixin, OwnedFormMixin, OwnedMixin

from .forms import AnimalForm, BreedingForm, HealthRecordForm, ProductionForm
from .models import Animal, Breeding, HealthRecord, Production


@login_required
def animal_list(request):
    animals = Animal.objects.filter(owner=request.user, is_active=True)
    return render(request, 'livestock/animal_list.html', {
        'animals': animals,
        'total_count': animals.count(),
    })


@login_required
def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk, owner=request.user, is_active=True)
    return render(request, 'livestock/animal_detail.html', {
        'animal': animal,
        'health_records': animal.health_records.all()[:5],
        'production_records': animal.production_records.all()[:5],
        'breeding_records_mother': animal.breeding_as_mother.all()[:5],
        'breeding_records_father': animal.breeding_as_father.all()[:5],
    })


@login_required
def animal_create(request):
    form = AnimalForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        animal = form.save(commit=False)
        animal.owner = request.user
        animal.save()
        messages.success(request, 'Animal added successfully.')
        return redirect('livestock:animal_detail', pk=animal.pk)
    return render(request, 'livestock/animal_form.html', {'form': form, 'title': 'Add New Animal'})


@login_required
def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk, owner=request.user, is_active=True)
    form = AnimalForm(request.POST or None, instance=animal, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Animal updated successfully.')
        return redirect('livestock:animal_detail', pk=animal.pk)
    return render(request, 'livestock/animal_form.html', {
        'form': form, 'title': 'Update Animal', 'animal': animal,
    })


@login_required
def animal_delete(request, pk):
    """Soft delete: history (health/production/breeding) stays intact."""
    animal = get_object_or_404(Animal, pk=pk, owner=request.user, is_active=True)
    if request.method == 'POST':
        animal.is_active = False
        animal.save(update_fields=['is_active', 'updated_at'])
        messages.success(request, 'Animal deleted successfully.')
        return redirect('livestock:animal_list')
    return render(request, 'livestock/animal_confirm_delete.html', {'animal': animal})


# ---- Health records -------------------------------------------------------

class HealthRecordListView(OwnedMixin, ListView):
    model = HealthRecord
    owner_lookup = 'animal__owner'
    template_name = 'livestock/health_record_list.html'
    context_object_name = 'health_records'

    def get_queryset(self):
        return super().get_queryset().select_related('animal')


class HealthRecordCreateView(OwnedFormMixin, CreateView):
    model = HealthRecord
    form_class = HealthRecordForm
    owner_lookup = 'animal__owner'
    assign_owner = False
    template_name = 'livestock/health_record_form.html'
    success_url = reverse_lazy('livestock:health_record_list')
    success_message = 'Health record added.'

    def get_initial(self):
        initial = super().get_initial()
        if animal := self.request.GET.get('animal'):
            initial['animal'] = animal
        return initial


class HealthRecordUpdateView(OwnedFormMixin, UpdateView):
    model = HealthRecord
    form_class = HealthRecordForm
    owner_lookup = 'animal__owner'
    assign_owner = False
    template_name = 'livestock/health_record_form.html'
    success_url = reverse_lazy('livestock:health_record_list')
    success_message = 'Health record updated.'


class HealthRecordDeleteView(OwnedDeleteMixin, DeleteView):
    model = HealthRecord
    owner_lookup = 'animal__owner'
    template_name = 'livestock/health_record_confirm_delete.html'
    success_url = reverse_lazy('livestock:health_record_list')
    success_message = 'Health record deleted.'


# ---- Production records ---------------------------------------------------

class ProductionRecordListView(OwnedMixin, ListView):
    model = Production
    owner_lookup = 'animal__owner'
    template_name = 'livestock/production_record_list.html'
    context_object_name = 'production_records'

    def get_queryset(self):
        return super().get_queryset().select_related('animal')


class ProductionRecordCreateView(OwnedFormMixin, CreateView):
    model = Production
    form_class = ProductionForm
    owner_lookup = 'animal__owner'
    assign_owner = False
    template_name = 'livestock/production_record_form.html'
    success_url = reverse_lazy('livestock:production_record_list')
    success_message = 'Production record added.'

    def get_initial(self):
        initial = super().get_initial()
        if animal := self.request.GET.get('animal'):
            initial['animal'] = animal
        return initial


class ProductionRecordUpdateView(OwnedFormMixin, UpdateView):
    model = Production
    form_class = ProductionForm
    owner_lookup = 'animal__owner'
    assign_owner = False
    template_name = 'livestock/production_record_form.html'
    success_url = reverse_lazy('livestock:production_record_list')
    success_message = 'Production record updated.'


class ProductionRecordDeleteView(OwnedDeleteMixin, DeleteView):
    model = Production
    owner_lookup = 'animal__owner'
    template_name = 'livestock/production_record_confirm_delete.html'
    success_url = reverse_lazy('livestock:production_record_list')
    success_message = 'Production record deleted.'


# ---- Breeding records -----------------------------------------------------

class _BreedingOwned(OwnedMixin):
    model = Breeding

    def get_queryset(self):
        # Both parents are validated as the user's own animals on save.
        return Breeding.objects.filter(
            Q(mother__owner=self.request.user) & Q(father__owner=self.request.user)
        ).select_related('mother', 'father')


class BreedingRecordListView(_BreedingOwned, ListView):
    template_name = 'livestock/breeding_record_list.html'
    context_object_name = 'breeding_records'


class BreedingRecordCreateView(OwnedFormMixin, CreateView):
    model = Breeding
    form_class = BreedingForm
    assign_owner = False
    template_name = 'livestock/breeding_record_form.html'
    success_url = reverse_lazy('livestock:breeding_record_list')
    success_message = 'Breeding record added.'

    def get_queryset(self):
        return Breeding.objects.none()


class BreedingRecordUpdateView(OwnedFormMixin, _BreedingOwned, UpdateView):
    form_class = BreedingForm
    assign_owner = False
    template_name = 'livestock/breeding_record_form.html'
    success_url = reverse_lazy('livestock:breeding_record_list')
    success_message = 'Breeding record updated.'


class BreedingRecordDeleteView(OwnedDeleteMixin, _BreedingOwned, DeleteView):
    template_name = 'livestock/breeding_record_confirm_delete.html'
    success_url = reverse_lazy('livestock:breeding_record_list')
    success_message = 'Breeding record deleted.'
