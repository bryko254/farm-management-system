from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Equipment

DATE = forms.DateInput(attrs={'type': 'date'})


class EquipmentForm(UserScopedForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'purchase_date', 'condition',
                  'last_maintenance', 'next_maintenance']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'purchase_date': DATE, 'last_maintenance': DATE, 'next_maintenance': DATE,
        }

    def clean(self):
        data = super().clean()
        last, nxt = data.get('last_maintenance'), data.get('next_maintenance')
        if last and nxt and nxt < last:
            self.add_error('next_maintenance', 'Next maintenance cannot be before the last one.')
        return data
