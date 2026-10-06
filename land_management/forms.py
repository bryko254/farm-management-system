from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Field, SoilAnalysis, IrrigationSystem, IrrigationSchedule

class FieldForm(UserScopedForm):
    class Meta:
        model = Field
        fields = ['name', 'size', 'location', 'soil_type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
            'size': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def clean_size(self):
        size = self.cleaned_data['size']
        if size <= 0:
            raise forms.ValidationError('Size must be greater than zero.')
        return size


class SoilAnalysisForm(UserScopedForm):
    class Meta:
        model = SoilAnalysis
        fields = ['test_date', 'ph_level', 'nitrogen_level', 'phosphorus_level', 
                 'potassium_level', 'organic_matter', 'notes']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class IrrigationSystemForm(UserScopedForm):
    class Meta:
        model = IrrigationSystem
        fields = ['irrigation_type', 'installation_date', 'water_source', 
                 'flow_rate', 'coverage_area', 'maintenance_notes']
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'maintenance_notes': forms.Textarea(attrs={'rows': 3}),
        }

class IrrigationScheduleForm(UserScopedForm):
    class Meta:
        model = IrrigationSchedule
        fields = ['start_date', 'end_date', 'frequency', 'duration_minutes', 
                 'water_amount', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        data = super().clean()
        start, end = data.get('start_date'), data.get('end_date')
        if start and end and end < start:
            self.add_error('end_date', 'End date cannot be before start date.')
        return data
