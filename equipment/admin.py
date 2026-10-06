from django.contrib import admin

from .models import Equipment


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'condition', 'next_maintenance', 'owner')
    list_filter = ('condition',)
    search_fields = ('name',)
