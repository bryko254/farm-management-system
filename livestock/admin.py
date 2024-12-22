from django.contrib import admin
from .models import Animal, HealthRecord, Production, Breeding

# Register your models here.

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('tag_number', 'name', 'species', 'breed', 'status', 'owner', 'is_active')
    list_filter = ('species', 'status', 'is_active')
    search_fields = ('tag_number', 'name', 'breed')
    date_hierarchy = 'created_at'

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('animal', 'record_type', 'date', 'condition', 'vet_name')
    list_filter = ('record_type', 'date')
    search_fields = ('animal__tag_number', 'condition', 'treatment')

@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ('animal', 'production_type', 'date', 'quantity', 'unit')
    list_filter = ('production_type', 'date')
    search_fields = ('animal__tag_number',)

@admin.register(Breeding)
class BreedingAdmin(admin.ModelAdmin):
    list_display = ('mother', 'father', 'breeding_date', 'success')
    list_filter = ('breeding_date', 'success')
    search_fields = ('mother__tag_number', 'father__tag_number')
