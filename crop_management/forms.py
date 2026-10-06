from django import forms

from farm_management_system.mixins import UserScopedForm
from land_management.models import Field

from .models import Crop

DATE = forms.DateInput(attrs={'type': 'date'})


class CropForm(UserScopedForm):
    class Meta:
        model = Crop
        fields = ['name', 'crop_type', 'variety', 'planting_date', 'expected_harvest_date',
                  'field', 'description']
        widgets = {
            'planting_date': DATE,
            'expected_harvest_date': DATE,
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def restrict_choices(self, user):
        self.fields['field'].queryset = Field.objects.filter(owner=user, is_active=True)

    def clean(self):
        data = super().clean()
        planted, harvest = data.get('planting_date'), data.get('expected_harvest_date')
        if planted and harvest and harvest < planted:
            self.add_error('expected_harvest_date', 'Harvest date cannot be before planting date.')
        return data
