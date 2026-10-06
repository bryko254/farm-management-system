from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Certification

DATE = forms.DateInput(attrs={'type': 'date'})


class CertificationForm(UserScopedForm):
    class Meta:
        model = Certification
        fields = ['name', 'issuing_body', 'reference_number', 'issue_date', 'expiry_date', 'notes']
        widgets = {'issue_date': DATE, 'expiry_date': DATE, 'notes': forms.Textarea(attrs={'rows': 3})}

    def clean(self):
        data = super().clean()
        issued, expires = data.get('issue_date'), data.get('expiry_date')
        if issued and expires and expires < issued:
            self.add_error('expiry_date', 'Expiry date cannot be before the issue date.')
        return data
