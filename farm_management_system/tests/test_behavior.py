from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from compliance.models import Certification
from crop_management.models import Crop
from equipment.models import Equipment
from finance.models import Budget, Transaction
from labor.models import Task, Worker
from land_management.models import Field
from livestock.models import Animal, HealthRecord

from .factories import TODAY, make_farm, make_user

User = get_user_model()


class BaseCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice, cls.bob = make_user('alice'), make_user('bob')
        cls.a = make_farm(cls.alice)
        cls.b = make_farm(cls.bob)

    def login(self, user=None):
        self.client.force_login(user or self.alice)


class CrossTenantInjectionTests(BaseCase):
    """A user must not be able to attach their records to someone else's objects."""

    def test_health_record_for_foreign_animal_rejected(self):
        self.login()
        response = self.client.post(reverse('livestock:add_health_record'), {
            'animal': self.b['cow'].pk, 'record_type': 'CHECKUP', 'date': TODAY,
            'condition': 'x', 'treatment': 'y'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(HealthRecord.objects.filter(animal=self.b['cow'], condition='x').exists())

    def test_crop_on_foreign_field_rejected(self):
        self.login()
        response = self.client.post(reverse('crop_management:crop_create'), {
            'name': 'Evil', 'crop_type': 'CEREAL', 'variety': 'v', 'planting_date': TODAY,
            'expected_harvest_date': TODAY, 'field': self.b['field'].pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Crop.objects.filter(name='Evil').exists())

    def test_transaction_with_foreign_category_rejected(self):
        self.login()
        response = self.client.post(reverse('finance:add_transaction'), {
            'date': TODAY, 'type': 'EXPENSE', 'amount': '5', 'category': self.b['expense_cat'].pk,
            'description': 'x', 'payment_method': 'CASH'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Transaction.objects.filter(owner=self.alice, description='x').exists())

    def test_task_with_foreign_worker_rejected(self):
        self.login()
        response = self.client.post(reverse('labor:task_create'), {
            'title': 'Evil', 'assigned_to': self.b['worker'].pk, 'status': 'TODO', 'priority': 'LOW'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(title='Evil').exists())

    def test_animal_parent_must_be_own(self):
        self.login()
        response = self.client.post(reverse('livestock:animal_create'), {
            'tag_number': 'N-1', 'species': 'CATTLE', 'breed': 'x', 'gender': 'F',
            'date_of_birth': TODAY, 'weight': '10', 'status': 'HEALTHY',
            'mother': self.b['cow'].pk})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Animal.objects.filter(tag_number='N-1').exists())

    def test_cannot_hijack_owner_via_post(self):
        self.login()
        self.client.post(reverse('equipment:equipment_create'), {
            'name': 'Mine', 'purchase_date': TODAY, 'condition': 'good', 'owner': self.bob.pk})
        self.assertEqual(Equipment.objects.get(name='Mine').owner, self.alice)


class LivestockTests(BaseCase):
    def animal_payload(self, **kw):
        data = {'tag_number': 'Z-9', 'species': 'GOAT', 'breed': 'Boer', 'gender': 'F',
                'date_of_birth': TODAY, 'weight': '35', 'status': 'HEALTHY'}
        data.update(kw)
        return data

    def test_tag_unique_per_owner_not_globally(self):
        self.login()
        # make_farm gives Alice and Bob the same tags, so cross-owner reuse already works
        self.assertEqual(Animal.objects.filter(tag_number='C-1').count(), 2)
        # a duplicate within Alice's own herd is rejected
        r = self.client.post(reverse('livestock:animal_create'), self.animal_payload(tag_number='C-1'))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'already have an active animal')

    def test_delete_is_soft_and_frees_tag(self):
        self.login()
        self.client.post(reverse('livestock:animal_delete', args=[self.a['cow'].pk]))
        self.a['cow'].refresh_from_db()
        self.assertFalse(self.a['cow'].is_active)
        self.assertEqual(self.client.get(reverse('livestock:animal_detail', args=[self.a['cow'].pk])).status_code, 404)
        r = self.client.post(reverse('livestock:animal_create'), self.animal_payload(tag_number='C-1'))
        self.assertEqual(r.status_code, 302)

    def test_weight_must_be_positive(self):
        self.login()
        r = self.client.post(reverse('livestock:animal_create'), self.animal_payload(weight='0'))
        self.assertEqual(r.status_code, 200)

    def test_breeding_due_date_validation(self):
        self.login()
        r = self.client.post(reverse('livestock:add_breeding_record'), {
            'mother': self.a['cow'].pk, 'father': self.a['bull'].pk,
            'breeding_date': TODAY, 'expected_due_date': TODAY - timedelta(days=1)})
        self.assertEqual(r.status_code, 200)

    def test_delete_shows_success_message(self):
        self.login()
        r = self.client.post(reverse('livestock:delete_health_record', args=[self.a['health'].pk]), follow=True)
        self.assertContains(r, 'Health record deleted')
        self.assertFalse(HealthRecord.objects.filter(pk=self.a['health'].pk).exists())


class FinanceTests(BaseCase):
    def test_category_type_must_match_transaction_type(self):
        self.login()
        r = self.client.post(reverse('finance:add_transaction'), {
            'date': TODAY, 'type': 'INCOME', 'amount': '5', 'category': self.a['expense_cat'].pk,
            'description': 'x', 'payment_method': 'CASH'})
        self.assertEqual(r.status_code, 200)

    def test_amount_must_be_positive(self):
        self.login()
        r = self.client.post(reverse('finance:add_transaction'), {
            'date': TODAY, 'type': 'EXPENSE', 'amount': '-5', 'category': self.a['expense_cat'].pk,
            'description': 'x', 'payment_method': 'CASH'})
        self.assertEqual(r.status_code, 200)

    def test_budget_counts_only_expenses_in_range(self):
        budget = self.a['budget']  # 100 budget, one 50 expense already
        Transaction.objects.create(owner=self.alice, type='INCOME', amount=999,
                                   category=self.a['expense_cat'], description='odd', payment_method='CASH')
        Transaction.objects.create(owner=self.alice, type='EXPENSE', amount=10, category=self.a['expense_cat'],
                                   description='old', payment_method='CASH', date=TODAY - timedelta(days=400))
        self.assertEqual(budget.get_spent_amount(), Decimal('50'))
        self.assertEqual(budget.get_remaining_amount(), Decimal('50'))

    def test_budget_date_validation(self):
        self.login()
        r = self.client.post(reverse('finance:add_budget'), {
            'category': self.a['expense_cat'].pk, 'amount': '10', 'period': 'MONTHLY',
            'start_date': TODAY, 'end_date': TODAY - timedelta(days=1)})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Budget.objects.filter(owner=self.alice).count(), 1)


class OtherModuleTests(BaseCase):
    def test_certification_status(self):
        self.assertEqual(self.a['cert'].status, 'Expiring soon')
        cert = Certification(expiry_date=TODAY - timedelta(days=1))
        self.assertEqual(cert.status, 'Expired')
        self.assertEqual(Certification().status, 'No expiry')

    def test_equipment_overdue_flag_and_schedule_order(self):
        Equipment.objects.create(owner=self.alice, name='Plough', purchase_date=TODAY,
                                 next_maintenance=TODAY - timedelta(days=3))
        self.login()
        response = self.client.get(reverse('equipment:maintenance_schedule'))
        names = [e.name for e in response.context['object_list']]
        self.assertEqual(names, ['Plough', 'Tractor'])
        self.assertTrue(response.context['object_list'][0].maintenance_overdue)

    def test_worker_crud_roundtrip(self):
        self.login()
        r = self.client.post(reverse('labor:worker_create'), {
            'name': 'Mary', 'hire_date': TODAY, 'is_active': 'on', 'daily_wage': '500'})
        self.assertEqual(r.status_code, 302)
        worker = Worker.objects.get(name='Mary')
        self.assertEqual(worker.owner, self.alice)
        self.client.post(reverse('labor:worker_delete', args=[worker.pk]))
        self.assertFalse(Worker.objects.filter(pk=worker.pk).exists())

    def test_field_size_positive(self):
        self.login()
        r = self.client.post(reverse('land_management:field_create'), {
            'name': 'F', 'size': '0', 'location': 'x', 'soil_type': 'y'})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Field.objects.filter(name='F').exists())


class AccountTests(TestCase):
    def test_register_requires_unique_email_and_logs_in(self):
        payload = {'username': 'newbie', 'email': 'n@example.com',
                   'password1': 'Tr0ub4dor-horse-9', 'password2': 'Tr0ub4dor-horse-9'}
        r = self.client.post(reverse('accounts:register'), payload)
        self.assertRedirects(r, reverse('home'))
        self.client.logout()
        r = self.client.post(reverse('accounts:register'), {**payload, 'username': 'other'})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(User.objects.filter(username='other').exists())

    @override_settings(ALLOW_REGISTRATION=False)
    def test_registration_can_be_disabled(self):
        self.assertEqual(self.client.get(reverse('accounts:register')).status_code, 404)

    def test_logout_is_post_only(self):
        user = make_user()
        self.client.force_login(user)
        self.assertEqual(self.client.get(reverse('accounts:logout')).status_code, 405)
        self.client.post(reverse('accounts:logout'))
        self.assertEqual(self.client.get(reverse('home')).status_code, 302)

    def test_password_reset_sends_email(self):
        make_user('carol')
        r = self.client.post(reverse('accounts:password_reset'), {'email': 'carol@example.com'})
        self.assertRedirects(r, reverse('accounts:password_reset_done'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('/accounts/password-reset-confirm/', mail.outbox[0].body)

    def test_login_works(self):
        make_user('dave')
        r = self.client.post(reverse('accounts:login'), {'username': 'dave', 'password': 'S3cure-pass-123'})
        self.assertRedirects(r, reverse('home'))
