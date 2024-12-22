from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def compliance_dashboard(request):
    return render(request, 'compliance/dashboard.html')

@login_required
def certification_list(request):
    return render(request, 'compliance/certification_list.html')

@login_required
def document_list(request):
    return render(request, 'compliance/document_list.html')

@login_required
def food_safety_records(request):
    return render(request, 'compliance/food_safety_records.html')

@login_required
def environmental_compliance(request):
    return render(request, 'compliance/environmental_compliance.html')
