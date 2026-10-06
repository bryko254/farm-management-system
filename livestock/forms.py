from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Animal, Breeding, HealthRecord, Production

DATE = forms.DateInput(attrs={'type': 'date'})


class AnimalForm(UserScopedForm):
    class Meta:
        model = Animal
        exclude = ['owner', 'created_at', 'updated_at', 'is_active']
        widgets = {
            'date_of_birth': DATE,
            'purchase_date': DATE,
            'last_health_check': DATE,
            'weight': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'purchase_price': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def restrict_choices(self, user):
        others = Animal.objects.filter(owner=user, is_active=True).exclude(pk=self.instance.pk)
        self.fields['mother'].queryset = others.filter(gender='F')
        self.fields['father'].queryset = others.filter(gender='M')

    def clean_tag_number(self):
        tag = self.cleaned_data['tag_number'].strip()
        taken = Animal.objects.filter(owner=self.user, tag_number=tag, is_active=True)
        if self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        if taken.exists():
            raise forms.ValidationError('You already have an active animal with this tag number.')
        return tag

    def clean_weight(self):
        weight = self.cleaned_data['weight']
        if weight <= 0:
            raise forms.ValidationError('Weight must be greater than zero.')
        return weight


class _AnimalRecordForm(UserScopedForm):
    def restrict_choices(self, user):
        self.fields['animal'].queryset = Animal.objects.filter(owner=user, is_active=True)


class HealthRecordForm(_AnimalRecordForm):
    class Meta:
        model = HealthRecord
        fields = ['animal', 'record_type', 'date', 'condition', 'treatment', 'medication',
                  'dosage', 'vet_name', 'cost', 'next_check_date', 'notes']
        widgets = {
            'date': DATE,
            'next_check_date': DATE,
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
            'cost': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }


class ProductionForm(_AnimalRecordForm):
    class Meta:
        model = Production
        fields = ['animal', 'production_type', 'date', 'quantity', 'unit', 'quality_grade', 'notes']
        widgets = {
            'date': DATE,
            'quantity': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class BreedingForm(UserScopedForm):
    class Meta:
        model = Breeding
        fields = ['mother', 'father', 'breeding_date', 'expected_due_date',
                  'actual_birth_date', 'number_of_offspring', 'success', 'notes']
        widgets = {
            'breeding_date': DATE,
            'expected_due_date': DATE,
            'actual_birth_date': DATE,
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def restrict_choices(self, user):
        animals = Animal.objects.filter(owner=user, is_active=True)
        self.fields['mother'].queryset = animals.filter(gender='F')
        self.fields['father'].queryset = animals.filter(gender='M')

    def clean(self):
        data = super().clean()
        bred, due = data.get('breeding_date'), data.get('expected_due_date')
        if bred and due and due < bred:
            self.add_error('expected_due_date', 'Due date cannot be before the breeding date.')
        return data
