from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Dashboard
    path('', views.finance_dashboard, name='finance_dashboard'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='add_category'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='edit_category'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),
    
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='edit_transaction'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='delete_transaction'),
    
    # Budgets
    path('budgets/', views.BudgetListView.as_view(), name='budget_list'),
    path('budgets/add/', views.BudgetCreateView.as_view(), name='add_budget'),
    path('budgets/<int:pk>/edit/', views.BudgetUpdateView.as_view(), name='edit_budget'),
    path('budgets/<int:pk>/delete/', views.BudgetDeleteView.as_view(), name='delete_budget'),
]
