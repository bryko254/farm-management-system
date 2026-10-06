from django.contrib import admin

from .models import Field, IrrigationSchedule, IrrigationSystem, SoilAnalysis


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'location', 'is_active', 'owner')
    search_fields = ('name', 'location')


admin.site.register(SoilAnalysis)
admin.site.register(IrrigationSystem)
admin.site.register(IrrigationSchedule)
