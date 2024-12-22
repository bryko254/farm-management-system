from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Category(models.Model):
    CATEGORY_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=7, choices=CATEGORY_TYPES)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    
    PAYMENT_METHODS = [
        ('CASH', 'Cash'),
        ('MPESA', 'M-PESA'),
        ('BANK', 'Bank Transfer'),
        ('CARD', 'Credit/Debit Card'),
        ('OTHER', 'Other'),
    ]
    
    date = models.DateField(default=timezone.now)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    payment_method = models.CharField(max_length=5, choices=PAYMENT_METHODS)
    reference_number = models.CharField(max_length=50, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
        
    def __str__(self):
        return f"{self.get_type_display()} - {self.amount} - {self.date}"

class Budget(models.Model):
    PERIOD_CHOICES = [
        ('MONTHLY', 'Monthly'),
        ('QUARTERLY', 'Quarterly'),
        ('ANNUAL', 'Annual'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    period = models.CharField(max_length=9, choices=PERIOD_CHOICES)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-start_date']
        
    def __str__(self):
        return f"{self.category.name} Budget - {self.get_period_display()}"
        
    def get_spent_amount(self):
        """Calculate how much has been spent in this budget period"""
        return Transaction.objects.filter(
            owner=self.owner,
            category=self.category,
            date__range=(self.start_date, self.end_date)
        ).aggregate(total=models.Sum('amount'))['total'] or 0
        
    def get_remaining_amount(self):
        """Calculate remaining budget"""
        return self.amount - self.get_spent_amount()

    def get_spent_percentage(self):
        spent_amount = self.get_spent_amount()
        if self.amount > 0:
            return (spent_amount / self.amount) * 100
        return 0
