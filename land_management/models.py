from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Field(models.Model):
    name = models.CharField(max_length=100)
    size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Size in acres")
    location = models.CharField(max_length=255)
    soil_type = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.size} acres)"

class SoilAnalysis(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='soil_analyses')
    test_date = models.DateField()
    ph_level = models.DecimalField(max_digits=4, decimal_places=2)
    nitrogen_level = models.DecimalField(max_digits=5, decimal_places=2, help_text="N content in ppm")
    phosphorus_level = models.DecimalField(max_digits=5, decimal_places=2, help_text="P content in ppm")
    potassium_level = models.DecimalField(max_digits=5, decimal_places=2, help_text="K content in ppm")
    organic_matter = models.DecimalField(max_digits=4, decimal_places=2, help_text="Percentage")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-test_date']
        verbose_name_plural = "Soil analyses"

    def __str__(self):
        return f"Soil Analysis for {self.field.name} on {self.test_date}"

class IrrigationSystem(models.Model):
    IRRIGATION_TYPES = [
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler System'),
        ('flood', 'Flood Irrigation'),
        ('center_pivot', 'Center Pivot'),
        ('other', 'Other'),
    ]

    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='irrigation_systems')
    irrigation_type = models.CharField(max_length=20, choices=IRRIGATION_TYPES)
    installation_date = models.DateField()
    water_source = models.CharField(max_length=100)
    flow_rate = models.DecimalField(max_digits=8, decimal_places=2, help_text="Flow rate in gallons per minute")
    coverage_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Coverage area in acres")
    maintenance_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_irrigation_type_display()} for {self.field.name}"

class IrrigationSchedule(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('custom', 'Custom'),
    ]

    irrigation_system = models.ForeignKey(IrrigationSystem, on_delete=models.CASCADE, related_name='schedules')
    start_date = models.DateField()
    end_date = models.DateField()
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    duration_minutes = models.IntegerField(help_text="Duration in minutes")
    water_amount = models.DecimalField(max_digits=8, decimal_places=2, help_text="Amount in gallons")
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Schedule for {self.irrigation_system.field.name} ({self.start_date} to {self.end_date})"
