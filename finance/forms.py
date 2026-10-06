from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Budget, Category, Transaction

DATE = forms.DateInput(attrs={'type': 'date'})


class CategoryForm(UserScopedForm):
    class Meta:
        model = Category
        fields = ['name', 'type', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 3})}


class TransactionForm(UserScopedForm):
    class Meta:
        model = Transaction
        fields = ['date', 'type', 'amount', 'category', 'description',
                  'payment_method', 'reference_number']
        widgets = {
            'date': DATE,
            'description': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def restrict_choices(self, user):
        self.fields['category'].queryset = Category.objects.filter(owner=user)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be greater than zero.')
        return amount

    def clean(self):
        data = super().clean()
        category, kind = data.get('category'), data.get('type')
        if category and kind and category.type != kind:
            self.add_error('category', f'This is a {category.get_type_display().lower()} category; '
                                       f'choose a matching one.')
        return data


class BudgetForm(UserScopedForm):
    class Meta:
        model = Budget
        fields = ['category', 'amount', 'start_date', 'end_date', 'period', 'notes']
        widgets = {
            'start_date': DATE,
            'end_date': DATE,
            'notes': forms.Textarea(attrs={'rows': 3}),
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
        }

    def restrict_choices(self, user):
        self.fields['category'].queryset = Category.objects.filter(owner=user, type='EXPENSE')

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Budget must be greater than zero.')
        return amount

    def clean(self):
        data = super().clean()
        start, end = data.get('start_date'), data.get('end_date')
        if start and end and start > end:
            self.add_error('end_date', 'End date must be after start date.')
        return data
