from django import forms

from farm_management_system.mixins import UserScopedForm

from .models import Task, Worker

DATE = forms.DateInput(attrs={'type': 'date'})


class WorkerForm(UserScopedForm):
    class Meta:
        model = Worker
        fields = ['name', 'role', 'phone', 'email', 'hire_date', 'daily_wage', 'is_active', 'notes']
        widgets = {
            'hire_date': DATE,
            'notes': forms.Textarea(attrs={'rows': 3}),
            'daily_wage': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }

    def clean_daily_wage(self):
        wage = self.cleaned_data['daily_wage']
        if wage is not None and wage < 0:
            raise forms.ValidationError('Wage cannot be negative.')
        return wage


class TaskForm(UserScopedForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date', 'status', 'priority']
        widgets = {'description': forms.Textarea(attrs={'rows': 3}), 'due_date': DATE}

    def restrict_choices(self, user):
        self.fields['assigned_to'].queryset = Worker.objects.filter(owner=user, is_active=True)
