import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_system.settings')
django.setup()

from livestock.models import Animal
from django.contrib.auth import get_user_model

User = get_user_model()

print("\nReactivating all animals...")

# Get all animals regardless of is_active status
animals = Animal.objects.all()
print(f"Found {animals.count()} total animals")

for animal in animals:
    print(f"\nAnimal {animal.tag_number}:")
    print(f"  - ID: {animal.id}")
    print(f"  - Owner: {animal.owner}")
    print(f"  - Is Active: {animal.is_active}")
    
    # Reactivate the animal
    animal.is_active = True
    animal.save()
    print(f"  - Status updated to active")

print("\nAll animals have been reactivated!")
