from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Equipment(models.Model):
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('maintenance', 'Under Maintenance'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    purchase_date = models.DateField()
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']
