import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farm_management_system.settings')
django.setup()

from livestock.models import Animal

print("Activating all animals...")
Animal.objects.update(is_active=True)
print("Done! All animals are now active.")
