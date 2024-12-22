from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Animal, HealthRecord, Production, Breeding
from .forms import AnimalForm, HealthRecordForm, ProductionForm, BreedingForm
from django.db.models import Q
import logging

logger = logging.getLogger('livestock')

# Create your views here.

@login_required
def animal_list(request):
    logger.info(f"Accessing animal list view - User: {request.user} (ID: {request.user.id})")
    
    try:
        # Log all animals in database
        all_animals = Animal.objects.all()
        logger.info(f"Total animals in database: {all_animals.count()}")
        for animal in all_animals:
            logger.debug(f"Found animal: {animal.tag_number} - Owner: {animal.owner} (ID: {animal.owner.id}) - Active: {animal.is_active}")
        
        # Get user's active animals
        animals = Animal.objects.filter(owner=request.user, is_active=True).order_by('-created_at')
        logger.info(f"Found {animals.count()} active animals for user {request.user}")
        
        return render(request, 'livestock/animal_list.html', {
            'animals': animals,
            'total_count': animals.count(),
        })
    except Exception as e:
        logger.error(f"Error in animal_list view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the animals.")
        return render(request, 'livestock/animal_list.html', {'animals': [], 'total_count': 0})

@login_required
def animal_detail(request, pk):
    logger.info(f"Accessing animal detail view - Animal ID: {pk}, User: {request.user}")
    
    try:
        animal = get_object_or_404(Animal, pk=pk, owner=request.user)
        logger.debug(f"Found animal: {animal.tag_number}")
        
        health_records = animal.health_records.all()[:5]
        production_records = animal.production_records.all()[:5]
        breeding_records_mother = animal.breeding_as_mother.all()[:5]
        breeding_records_father = animal.breeding_as_father.all()[:5]
        
        context = {
            'animal': animal,
            'health_records': health_records,
            'production_records': production_records,
            'breeding_records_mother': breeding_records_mother,
            'breeding_records_father': breeding_records_father,
        }
        return render(request, 'livestock/animal_detail.html', context)
    except Exception as e:
        logger.error(f"Error in animal_detail view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the animal details.")
        return redirect('livestock:animal_list')

@login_required
def animal_create(request):
    logger.info(f"Accessing animal create view - User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for animal creation")
        form = AnimalForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid, creating animal")
            try:
                animal = form.save(commit=False)
                animal.owner = request.user
                animal.is_active = True
                animal.save()
                logger.info(f"Created animal: {animal.tag_number} (ID: {animal.id}) for user {request.user}, is_active={animal.is_active}")
                messages.success(request, 'Animal added successfully.')
                return redirect('livestock:animal_detail', pk=animal.pk)
            except Exception as e:
                logger.error(f"Error saving animal: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while saving the animal.")
        else:
            logger.warning(f"Invalid form submission. Errors: {form.errors}")
    else:
        logger.debug("Displaying empty animal creation form")
        form = AnimalForm()
    
    return render(request, 'livestock/animal_form.html', {
        'form': form,
        'title': 'Add New Animal'
    })

@login_required
def animal_update(request, pk):
    animal = get_object_or_404(Animal, pk=pk, owner=request.user, is_active=True)  # Only get active animals
    logger.info(f"Accessing animal update view - Animal ID: {pk}, User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for animal update")
        form = AnimalForm(request.POST, instance=animal)
        
        if form.is_valid():
            logger.debug("Form is valid, updating animal")
            try:
                updated_animal = form.save(commit=False)
                # Ensure these fields are maintained
                updated_animal.is_active = True
                updated_animal.owner = request.user
                updated_animal.save()
                logger.info(f"Updated animal: {animal.tag_number} (ID: {animal.id}) for user {request.user}, is_active={updated_animal.is_active}")
                messages.success(request, 'Animal updated successfully.')
                return redirect('livestock:animal_detail', pk=animal.pk)
            except Exception as e:
                logger.error(f"Error updating animal: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while updating the animal.")
        else:
            logger.warning(f"Invalid form submission. Errors: {form.errors}")
    else:
        logger.debug("Displaying animal update form")
        form = AnimalForm(instance=animal)
    
    return render(request, 'livestock/animal_form.html', {
        'form': form,
        'title': 'Update Animal',
        'animal': animal,
    })

@login_required
def animal_delete(request, pk):
    animal = get_object_or_404(Animal, pk=pk, owner=request.user)
    logger.info(f"Accessing animal delete view - Animal ID: {pk}, User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for animal deletion")
        try:
            animal.is_active = False
            animal.save()
            logger.info(f"Deleted animal: {animal.tag_number} (ID: {animal.id}) for user {request.user}")
            messages.success(request, 'Animal deleted successfully.')
            return redirect('livestock:animal_list')
        except Exception as e:
            logger.error(f"Error deleting animal: {str(e)}", exc_info=True)
            messages.error(request, "An error occurred while deleting the animal.")
    return render(request, 'livestock/animal_confirm_delete.html', {'animal': animal})

@login_required
def health_record_list(request):
    logger.info(f"Accessing health record list view - User: {request.user}")
    
    try:
        records = HealthRecord.objects.filter(animal__owner=request.user)
        logger.info(f"Found {records.count()} health records for user {request.user}")
        return render(request, 'livestock/health_record_list.html', {'records': records})
    except Exception as e:
        logger.error(f"Error in health_record_list view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the health records.")
        return render(request, 'livestock/health_record_list.html', {'records': []})

@login_required
def health_record_create(request, animal_pk):
    animal = get_object_or_404(Animal, pk=animal_pk, owner=request.user)
    logger.info(f"Accessing health record create view - Animal ID: {animal_pk}, User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for health record creation")
        form = HealthRecordForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid, creating health record")
            try:
                record = form.save(commit=False)
                record.animal = animal
                record.save()
                logger.info(f"Created health record for animal: {animal.tag_number} (ID: {animal.id}) for user {request.user}")
                messages.success(request, 'Health record added successfully.')
                return redirect('livestock:animal_detail', pk=animal.pk)
            except Exception as e:
                logger.error(f"Error saving health record: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while saving the health record.")
        else:
            logger.warning(f"Invalid form submission. Errors: {form.errors}")
    else:
        logger.debug("Displaying empty health record creation form")
        form = HealthRecordForm(initial={'animal': animal})
    
    return render(request, 'livestock/health_record_form.html', {
        'form': form,
        'animal': animal,
        'title': 'Add Health Record'
    })

@login_required
def production_record_list(request):
    logger.info(f"Accessing production record list view - User: {request.user}")
    
    try:
        records = Production.objects.filter(animal__owner=request.user)
        logger.info(f"Found {records.count()} production records for user {request.user}")
        return render(request, 'livestock/production_record_list.html', {'records': records})
    except Exception as e:
        logger.error(f"Error in production_record_list view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the production records.")
        return render(request, 'livestock/production_record_list.html', {'records': []})

@login_required
def production_record_create(request, animal_pk):
    animal = get_object_or_404(Animal, pk=animal_pk, owner=request.user)
    logger.info(f"Accessing production record create view - Animal ID: {animal_pk}, User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for production record creation")
        form = ProductionForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid, creating production record")
            try:
                record = form.save(commit=False)
                record.animal = animal
                record.save()
                logger.info(f"Created production record for animal: {animal.tag_number} (ID: {animal.id}) for user {request.user}")
                messages.success(request, 'Production record added successfully.')
                return redirect('livestock:animal_detail', pk=animal.pk)
            except Exception as e:
                logger.error(f"Error saving production record: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while saving the production record.")
        else:
            logger.warning(f"Invalid form submission. Errors: {form.errors}")
    else:
        logger.debug("Displaying empty production record creation form")
        form = ProductionForm(initial={'animal': animal})
    
    return render(request, 'livestock/production_record_form.html', {
        'form': form,
        'animal': animal,
        'title': 'Add Production Record'
    })

@login_required
def breeding_record_list(request):
    logger.info(f"Accessing breeding record list view - User: {request.user}")
    
    try:
        records = Breeding.objects.filter(
            Q(mother__owner=request.user) | Q(father__owner=request.user)
        ).distinct()
        logger.info(f"Found {records.count()} breeding records for user {request.user}")
        return render(request, 'livestock/breeding_record_list.html', {'records': records})
    except Exception as e:
        logger.error(f"Error in breeding_record_list view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the breeding records.")
        return render(request, 'livestock/breeding_record_list.html', {'records': []})

@login_required
def breeding_record_create(request):
    logger.info(f"Accessing breeding record create view - User: {request.user}")
    
    if request.method == 'POST':
        logger.debug("Processing POST request for breeding record creation")
        form = BreedingForm(request.POST)
        
        if form.is_valid():
            logger.debug("Form is valid, creating breeding record")
            try:
                record = form.save()
                logger.info(f"Created breeding record for user {request.user}")
                messages.success(request, 'Breeding record added successfully.')
                return redirect('livestock:breeding_record_list')
            except Exception as e:
                logger.error(f"Error saving breeding record: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while saving the breeding record.")
        else:
            logger.warning(f"Invalid form submission. Errors: {form.errors}")
    else:
        logger.debug("Displaying empty breeding record creation form")
        form = BreedingForm()
    
    return render(request, 'livestock/breeding_record_form.html', {
        'form': form,
        'title': 'Add Breeding Record'
    })
