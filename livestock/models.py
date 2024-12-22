from django.db import models
from django.conf import settings

class Animal(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    SPECIES_CHOICES = [
        ('CATTLE', 'Cattle'),
        ('SHEEP', 'Sheep'),
        ('GOAT', 'Goat'),
        ('PIG', 'Pig'),
        ('CHICKEN', 'Chicken'),
        ('OTHER', 'Other'),
    ]

    STATUS_CHOICES = [
        ('HEALTHY', 'Healthy'),
        ('SICK', 'Sick'),
        ('PREGNANT', 'Pregnant'),
        ('LACTATING', 'Lactating'),
        ('QUARANTINED', 'Quarantined'),
    ]

    # Basic Information
    tag_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, blank=True)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    weight = models.DecimalField(max_digits=7, decimal_places=2)  # in kg
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='HEALTHY')
    
    # Parent Information
    mother = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='offspring_as_mother')
    father = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='offspring_as_father')
    
    # Purchase Information
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    
    # Health Records
    vaccination_status = models.BooleanField(default=False)
    last_health_check = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # System Fields
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Set default to True

    def __str__(self):
        return f"{self.tag_number} - {self.name or self.species}"

    class Meta:
        ordering = ['tag_number']


class HealthRecord(models.Model):
    RECORD_TYPES = [
        ('VACCINATION', 'Vaccination'),
        ('TREATMENT', 'Treatment'),
        ('CHECKUP', 'Regular Checkup'),
        ('INJURY', 'Injury'),
        ('DISEASE', 'Disease'),
        ('OTHER', 'Other'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES)
    date = models.DateField()
    condition = models.CharField(max_length=200)
    treatment = models.TextField()
    medication = models.CharField(max_length=200, blank=True)
    dosage = models.CharField(max_length=100, blank=True)
    vet_name = models.CharField(max_length=200, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    next_check_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.tag_number} - {self.record_type} on {self.date}"

    class Meta:
        ordering = ['-date']


class Production(models.Model):
    PRODUCTION_TYPES = [
        ('MILK', 'Milk'),
        ('EGGS', 'Eggs'),
        ('WOOL', 'Wool'),
        ('MEAT', 'Meat'),
        ('OTHER', 'Other'),
    ]

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='production_records')
    production_type = models.CharField(max_length=20, choices=PRODUCTION_TYPES)
    date = models.DateField()
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    unit = models.CharField(max_length=20)  # e.g., liters, kg, pieces
    quality_grade = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.animal.tag_number} - {self.quantity} {self.unit} of {self.production_type} on {self.date}"

    class Meta:
        ordering = ['-date']


class Breeding(models.Model):
    mother = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='breeding_as_mother')
    father = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='breeding_as_father')
    breeding_date = models.DateField()
    expected_due_date = models.DateField()
    actual_birth_date = models.DateField(null=True, blank=True)
    number_of_offspring = models.IntegerField(null=True, blank=True)
    success = models.BooleanField(null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Breeding: {self.mother.tag_number} x {self.father.tag_number} on {self.breeding_date}"

    class Meta:
        ordering = ['-breeding_date']
