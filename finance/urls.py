from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.finance_dashboard, name='finance_dashboard'),
    path('income/', views.income_list, name='income_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('budget/', views.budget_planning, name='budget_planning'),
    path('reports/', views.financial_reports, name='financial_reports'),
    path('payroll/', views.payroll_management, name='payroll_management'),
]
