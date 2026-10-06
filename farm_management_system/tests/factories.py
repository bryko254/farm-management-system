from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model

from compliance.models import Certification
from crop_management.models import Crop
from equipment.models import Equipment
from finance.models import Budget, Category, Transaction
from labor.models import Task, Worker
from land_management.models import Field, IrrigationSchedule, IrrigationSystem, SoilAnalysis
from livestock.models import Animal, Breeding, HealthRecord, Production

User = get_user_model()
TODAY = date.today()


def make_user(name='alice'):
    return User.objects.create_user(name, f'{name}@example.com', 'S3cure-pass-123')


def make_farm(user):
    """One row of everything, owned by ``user``. Returns a dict of the objects."""
    f = {}
    f['field'] = Field.objects.create(owner=user, name='North', size=Decimal('4.5'),
                                      location='Nakuru', soil_type='Loam')
    f['soil'] = SoilAnalysis.objects.create(field=f['field'], test_date=TODAY, ph_level=6.5,
                                            nitrogen_level=10, phosphorus_level=10,
                                            potassium_level=10, organic_matter=3)
    f['irrigation'] = IrrigationSystem.objects.create(
        field=f['field'], irrigation_type='drip', installation_date=TODAY, water_source='Well',
        flow_rate=10, coverage_area=2)
    f['schedule'] = IrrigationSchedule.objects.create(
        irrigation_system=f['irrigation'], start_date=TODAY, end_date=TODAY + timedelta(days=7),
        frequency='daily', duration_minutes=30, water_amount=100)
    f['crop'] = Crop.objects.create(owner=user, name='Maize', crop_type='CEREAL', variety='H614',
                                    planting_date=TODAY, expected_harvest_date=TODAY + timedelta(days=90),
                                    field=f['field'])
    f['cow'] = Animal.objects.create(owner=user, tag_number='C-1', name='Daisy', species='CATTLE',
                                     breed='Friesian', gender='F', date_of_birth=TODAY - timedelta(days=900),
                                     weight=400)
    f['bull'] = Animal.objects.create(owner=user, tag_number='B-1', name='Max', species='CATTLE',
                                      breed='Friesian', gender='M', date_of_birth=TODAY - timedelta(days=900),
                                      weight=600)
    f['health'] = HealthRecord.objects.create(animal=f['cow'], record_type='CHECKUP', date=TODAY,
                                              condition='Fine', treatment='None', cost=10)
    f['production'] = Production.objects.create(animal=f['cow'], production_type='MILK', date=TODAY,
                                                quantity=20, unit='L')
    f['breeding'] = Breeding.objects.create(mother=f['cow'], father=f['bull'], breeding_date=TODAY,
                                            expected_due_date=TODAY + timedelta(days=280))
    f['equipment'] = Equipment.objects.create(owner=user, name='Tractor', purchase_date=TODAY,
                                              next_maintenance=TODAY + timedelta(days=10))
    f['worker'] = Worker.objects.create(owner=user, name='Joe', role='Milker')
    f['task'] = Task.objects.create(owner=user, title='Milk cows', assigned_to=f['worker'])
    f['cert'] = Certification.objects.create(owner=user, name='Organic', issuing_body='KEBS',
                                             issue_date=TODAY, expiry_date=TODAY + timedelta(days=10))
    f['expense_cat'] = Category.objects.create(owner=user, name='Feed', type='EXPENSE')
    f['income_cat'] = Category.objects.create(owner=user, name='Milk sales', type='INCOME')
    f['txn'] = Transaction.objects.create(owner=user, type='EXPENSE', amount=50, category=f['expense_cat'],
                                          description='Feed', payment_method='CASH')
    f['budget'] = Budget.objects.create(owner=user, category=f['expense_cat'], amount=100,
                                        start_date=TODAY - timedelta(days=1),
                                        end_date=TODAY + timedelta(days=30), period='MONTHLY')
    return f
