from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def employee_list(request):
    return render(request, 'labor/employee_list.html')

@login_required
def employee_detail(request, pk):
    return render(request, 'labor/employee_detail.html')

@login_required
def employee_create(request):
    return render(request, 'labor/employee_form.html')

@login_required
def work_schedules(request):
    return render(request, 'labor/work_schedules.html')

@login_required
def task_management(request):
    return render(request, 'labor/task_management.html')

@login_required
def performance_tracking(request):
    return render(request, 'labor/performance_tracking.html')
