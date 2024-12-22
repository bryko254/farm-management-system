from django import forms
from .models import Crop

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'crop_type', 'variety', 'planting_date', 'expected_harvest_date', 'field', 'description']
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_harvest_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'crop_type': forms.Select(attrs={'class': 'form-control'}),
            'variety': forms.TextInput(attrs={'class': 'form-control'}),
            'field': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
