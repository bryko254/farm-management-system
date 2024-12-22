import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_system.settings')
django.setup()

from livestock.models import Animal

print("\nChecking all animals in database:")
for animal in Animal.objects.all():
    print(f"Animal {animal.tag_number}:")
    print(f"  - ID: {animal.id}")
    print(f"  - Owner: {animal.owner}")
    print(f"  - Is Active: {animal.is_active}")
    print()
