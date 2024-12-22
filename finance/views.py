from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def finance_dashboard(request):
    return render(request, 'finance/dashboard.html')

@login_required
def income_list(request):
    return render(request, 'finance/income_list.html')

@login_required
def expense_list(request):
    return render(request, 'finance/expense_list.html')

@login_required
def budget_planning(request):
    return render(request, 'finance/budget_planning.html')

@login_required
def financial_reports(request):
    return render(request, 'finance/financial_reports.html')

@login_required
def payroll_management(request):
    return render(request, 'finance/payroll_management.html')
