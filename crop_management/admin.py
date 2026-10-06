from django.contrib import admin

from .models import Crop


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'field', 'planting_date', 'expected_harvest_date', 'is_active', 'owner')
    list_filter = ('crop_type', 'is_active')
