from django import forms
from .models import Animal, HealthRecord, Production, Breeding

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        exclude = ['owner', 'created_at', 'updated_at', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'last_health_check': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tag_number': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'species': forms.Select(attrs={'class': 'form-control'}),
            'breed': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'mother': forms.Select(attrs={'class': 'form-control'}),
            'father': forms.Select(attrs={'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'next_check_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'record_type': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.TextInput(attrs={'class': 'form-control'}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'medication': forms.TextInput(attrs={'class': 'form-control'}),
            'dosage': forms.TextInput(attrs={'class': 'form-control'}),
            'vet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
            'production_type': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
            'quality_grade': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BreedingForm(forms.ModelForm):
    class Meta:
        model = Breeding
        fields = '__all__'
        widgets = {
            'breeding_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expected_due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'actual_birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'mother': forms.Select(attrs={'class': 'form-control'}),
            'father': forms.Select(attrs={'class': 'form-control'}),
            'number_of_offspring': forms.NumberInput(attrs={'class': 'form-control'}),
            'success': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
