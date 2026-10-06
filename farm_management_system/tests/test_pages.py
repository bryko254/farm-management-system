"""Every page renders for its owner, requires login, and is invisible to other users."""
from django.test import TestCase
from django.urls import reverse

from .factories import make_farm, make_user

# (url name, key of the object providing the pk or None)
LIST_PAGES = [
    ('home', None), ('land_management:field_list', None), ('crop_management:crop_list', None),
    ('livestock:animal_list', None), ('livestock:health_record_list', None),
    ('livestock:production_record_list', None), ('livestock:breeding_record_list', None),
    ('equipment:equipment_list', None), ('equipment:maintenance_schedule', None),
    ('labor:worker_list', None), ('labor:task_list', None), ('compliance:certification_list', None),
    ('finance:finance_dashboard', None), ('finance:category_list', None),
    ('finance:transaction_list', None), ('finance:budget_list', None),
    ('land_management:field_create', None), ('crop_management:crop_create', None),
    ('livestock:animal_create', None), ('livestock:add_health_record', None),
    ('livestock:add_production_record', None), ('livestock:add_breeding_record', None),
    ('equipment:equipment_create', None), ('labor:worker_create', None), ('labor:task_create', None),
    ('compliance:certification_create', None), ('finance:add_category', None),
    ('finance:add_transaction', None), ('finance:add_budget', None),
]
OBJECT_PAGES = [
    ('land_management:field_detail', 'field', 'pk'), ('land_management:field_update', 'field', 'pk'),
    ('land_management:field_delete', 'field', 'pk'),
    ('land_management:soil_analysis_create', 'field', 'field_pk'),
    ('land_management:irrigation_create', 'field', 'field_pk'),
    ('land_management:irrigation_schedule_create', 'irrigation', 'system_pk'),
    ('crop_management:crop_detail', 'crop', 'pk'), ('crop_management:crop_update', 'crop', 'pk'),
    ('crop_management:crop_delete', 'crop', 'pk'),
    ('livestock:animal_detail', 'cow', 'pk'), ('livestock:animal_update', 'cow', 'pk'),
    ('livestock:animal_delete', 'cow', 'pk'),
    ('livestock:edit_health_record', 'health', 'pk'), ('livestock:delete_health_record', 'health', 'pk'),
    ('livestock:edit_production_record', 'production', 'pk'),
    ('livestock:delete_production_record', 'production', 'pk'),
    ('livestock:edit_breeding_record', 'breeding', 'pk'), ('livestock:delete_breeding_record', 'breeding', 'pk'),
    ('equipment:equipment_update', 'equipment', 'pk'), ('equipment:equipment_delete', 'equipment', 'pk'),
    ('labor:worker_update', 'worker', 'pk'), ('labor:worker_delete', 'worker', 'pk'),
    ('labor:task_update', 'task', 'pk'), ('labor:task_delete', 'task', 'pk'),
    ('compliance:certification_update', 'cert', 'pk'), ('compliance:certification_delete', 'cert', 'pk'),
    ('finance:edit_category', 'expense_cat', 'pk'), ('finance:delete_category', 'expense_cat', 'pk'),
    ('finance:edit_transaction', 'txn', 'pk'), ('finance:delete_transaction', 'txn', 'pk'),
    ('finance:edit_budget', 'budget', 'pk'), ('finance:delete_budget', 'budget', 'pk'),
]


def _url(name, obj=None, kwarg=None):
    return reverse(name, kwargs={kwarg: obj.pk}) if obj else reverse(name)


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alice, cls.bob = make_user('alice'), make_user('bob')
        cls.farm = make_farm(cls.alice)

    def test_all_pages_render_for_owner(self):
        self.client.force_login(self.alice)
        for name, _ in LIST_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)
        for name, key, kwarg in OBJECT_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(_url(name, self.farm[key], kwarg)).status_code, 200)

    def test_pages_require_login(self):
        for name, _ in LIST_PAGES:
            with self.subTest(page=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 302)
                self.assertIn('/accounts/login/', response['Location'])
        for name, key, kwarg in OBJECT_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(_url(name, self.farm[key], kwarg)).status_code, 302)

    def test_other_users_get_404_on_object_pages(self):
        self.client.force_login(self.bob)
        for name, key, kwarg in OBJECT_PAGES:
            with self.subTest(page=name):
                self.assertEqual(self.client.get(_url(name, self.farm[key], kwarg)).status_code, 404)

    def test_other_users_cannot_delete(self):
        self.client.force_login(self.bob)
        for name, key, kwarg in OBJECT_PAGES:
            if 'delete' in name:
                with self.subTest(page=name):
                    self.client.post(_url(name, self.farm[key], kwarg))
                    self.farm[key].refresh_from_db()  # still exists

    def test_lists_do_not_leak_other_users_data(self):
        self.client.force_login(self.bob)
        for name in ['livestock:animal_list', 'crop_management:crop_list', 'finance:transaction_list',
                     'equipment:equipment_list', 'labor:worker_list', 'compliance:certification_list',
                     'livestock:health_record_list', 'livestock:breeding_record_list']:
            with self.subTest(page=name):
                body = self.client.get(reverse(name)).content.decode()
                for secret in ('C-1', 'Maize', 'Tractor', 'Joe', 'Organic'):
                    self.assertNotIn(secret, body)

    def test_healthz(self):
        response = self.client.get(reverse('healthz'))
        self.assertEqual(response.json(), {'status': 'ok'})
