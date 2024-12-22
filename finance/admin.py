from django.contrib import admin
from .models import Category, Transaction, Budget

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'owner')
    list_filter = ('type', 'owner')
    search_fields = ('name', 'description')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'amount', 'category', 'payment_method', 'owner')
    list_filter = ('type', 'payment_method', 'category', 'owner', 'date')
    search_fields = ('description', 'reference_number')
    date_hierarchy = 'date'

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'amount', 'period', 'start_date', 'end_date', 'owner')
    list_filter = ('period', 'category', 'owner')
    search_fields = ('notes',)
    date_hierarchy = 'start_date'
