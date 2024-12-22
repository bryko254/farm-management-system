from django import forms
from .models import Field, SoilAnalysis, IrrigationSystem, IrrigationSchedule

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'size', 'location', 'soil_type', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class SoilAnalysisForm(forms.ModelForm):
    class Meta:
        model = SoilAnalysis
        fields = ['test_date', 'ph_level', 'nitrogen_level', 'phosphorus_level', 
                 'potassium_level', 'organic_matter', 'notes']
        widgets = {
            'test_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class IrrigationSystemForm(forms.ModelForm):
    class Meta:
        model = IrrigationSystem
        fields = ['irrigation_type', 'installation_date', 'water_source', 
                 'flow_rate', 'coverage_area', 'maintenance_notes']
        widgets = {
            'installation_date': forms.DateInput(attrs={'type': 'date'}),
            'maintenance_notes': forms.Textarea(attrs={'rows': 3}),
        }

class IrrigationScheduleForm(forms.ModelForm):
    class Meta:
        model = IrrigationSchedule
        fields = ['start_date', 'end_date', 'frequency', 'duration_minutes', 
                 'water_amount', 'notes']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
