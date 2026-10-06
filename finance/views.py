from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import Category, Transaction, Budget
from farm_management_system.mixins import OwnedDeleteMixin, OwnedFormMixin, OwnedMixin

from .forms import BudgetForm, CategoryForm, TransactionForm

@login_required
def finance_dashboard(request):
    # Get date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        owner=request.user,
        date__range=[start_date, end_date]
    ).select_related('category').order_by('-date')[:5]
    
    # Calculate totals
    total_income = Transaction.objects.filter(
        owner=request.user,
        type='INCOME',
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_expenses = Transaction.objects.filter(
        owner=request.user,
        type='EXPENSE',
        date__range=[start_date, end_date]
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Get active budgets
    active_budgets = Budget.objects.filter(
        owner=request.user,
        start_date__lte=end_date,
        end_date__gte=end_date
    ).select_related('category')
    
    context = {
        'recent_transactions': recent_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': total_income - total_expenses,
        'active_budgets': active_budgets,
        'start_date': start_date,
        'end_date': end_date
    }
    
    return render(request, 'finance/dashboard.html', context)

# ---- Generic CRUD -----------------------------------------------------------

def _crud(model, form_class, prefix, noun, select=()):
    """Build list/create/update/delete views for an owner-scoped model."""
    list_url = reverse_lazy(f'finance:{prefix}_list')

    class List(OwnedMixin, ListView):
        template_name = f'finance/{prefix}_list.html'
        context_object_name = f'{prefix}s' if prefix != 'category' else 'categories'
        paginate_by = 50 if prefix == 'transaction' else None

        def get_queryset(self):
            qs = super().get_queryset()
            return qs.select_related(*select) if select else qs

    class Create(OwnedFormMixin, CreateView):
        template_name = f'finance/{prefix}_form.html'
        success_url = list_url
        success_message = f'{noun} created successfully.'

    class Update(OwnedFormMixin, UpdateView):
        template_name = f'finance/{prefix}_form.html'
        success_url = list_url
        success_message = f'{noun} updated successfully.'

    class Delete(OwnedDeleteMixin, DeleteView):
        template_name = f'finance/{prefix}_confirm_delete.html'
        success_url = list_url
        success_message = f'{noun} deleted successfully.'

    for view in (List, Create, Update, Delete):
        view.model = model
    Create.form_class = Update.form_class = form_class
    return List, Create, Update, Delete


CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView = _crud(
    Category, CategoryForm, 'category', 'Category')
TransactionListView, TransactionCreateView, TransactionUpdateView, TransactionDeleteView = _crud(
    Transaction, TransactionForm, 'transaction', 'Transaction', select=('category',))
BudgetListView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView = _crud(
    Budget, BudgetForm, 'budget', 'Budget', select=('category',))
