from django.db import models
from django.conf import settings

# Create your models here.

class Crop(models.Model):
    CROP_TYPES = [
        ('CEREAL', 'Cereal'),
        ('VEGETABLE', 'Vegetable'),
        ('FRUIT', 'Fruit'),
        ('LEGUME', 'Legume'),
        ('TUBER', 'Tuber'),
        ('OTHER', 'Other'),
    ]

    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    variety = models.CharField(max_length=100)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    field = models.ForeignKey('land_management.Field', on_delete=models.CASCADE, related_name='crops')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.variety})"

    class Meta:
        ordering = ['-planting_date']
