from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from rest_framework.test import APIClient
from app.models import (
    Supermarket, Section, Employee, Product, Warehouse, WareHStock,
    Distributor, Client, Purchase, PurchaseItem, Order, OrderItem,
)

User = get_user_model()


class BaseDjanGoMarketTest(TestCase):
    def setUp(self):
        ceo_group, _ = Group.objects.get_or_create(name='CEO')
        self.dummy_supermarket = Supermarket.objects.create(
            location='Dummy Location',
            opening_time='08:00',
            close_time='22:00'
        )
        self.ceo = User(
            enumber=1000,
            username='1000',
            name='Test CEO',
            role='CEO',
            salary=5000.00,
            age=30,
            contact='123456789',
            supermarket=self.dummy_supermarket,
            sex='M',
            is_superuser=True,
            is_staff=True
        )
        self.ceo.set_password('password123')
        self.ceo.save()
        self.ceo.groups.add(ceo_group)


class LogicTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.section = Section.objects.create(sname='Test Section', department='General')
        self.product = Product.objects.create(name='Sample Product', brand='BrandX', price=10.00, req_cold=False, section_name=self.section)
        from app.models import Client
        self.client_obj = Client.objects.create(nif=123456789, name='Test Client')
        self.purchase = Purchase.objects.create(date='2026-04-11 10:00:00', supermarket=self.dummy_supermarket, client=self.client_obj)

    def test_purchase_calculated_total(self):
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=2, price_at_purchase=10.00)
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=1, price_at_purchase=5.00)
        self.assertEqual(self.purchase.calculated_total, 25.00)

    def test_order_calculated_total(self):
        import decimal
        distributor = Distributor.objects.create(email='dist@test.com', name='Dist Test')
        order = Order.objects.create(ord_date='2026-04-11', supermarket=self.dummy_supermarket, distributor=distributor)
        OrderItem.objects.create(order=order, product=self.product, quantity=10)
        self.assertEqual(order.calculated_total, decimal.Decimal('60.00'))


def _perms_for(model, *codename_prefixes):
    ct = ContentType.objects.get_for_model(model)
    qs = Permission.objects.filter(content_type=ct)
    if codename_prefixes:
        from django.db.models import Q
        q = Q()
        for prefix in codename_prefixes:
            q |= Q(codename__startswith=prefix)
        qs = qs.filter(q)
    return list(qs)


def _setup_group_permissions():
    ceo, _ = Group.objects.get_or_create(name='CEO')
    ceo.permissions.set(Permission.objects.all())

    manager, _ = Group.objects.get_or_create(name='Manager')
    perms = []
    for model in (Employee, Supermarket, Warehouse, WareHStock, Order):
        perms += _perms_for(model)
    for model in (Section, Supermarket, Product, Distributor, Client, Purchase, PurchaseItem):
        perms += _perms_for(model, 'view_')
    manager.permissions.set(perms)

    cashier, _ = Group.objects.get_or_create(name='Cashier')
    perms = []
    for model in (Purchase, PurchaseItem):
        perms += _perms_for(model)
    for model in (Product, Client, Warehouse, WareHStock, Supermarket):
        perms += _perms_for(model, 'view_')
    cashier.permissions.set(perms)

    employee_group, _ = Group.objects.get_or_create(name='Employee')
    perms = []
    for model in (Section, Supermarket, Employee, Product, Warehouse, Distributor,
                  Client, Purchase, PurchaseItem, WareHStock, Order, OrderItem):
        perms += _perms_for(model, 'view_')
    employee_group.permissions.set(perms)


def _make_employee(enumber, name, role, supermarket, group_name, is_superuser=False, is_staff=False):
    group, _ = Group.objects.get_or_create(name=group_name)
    emp = User(
        enumber=enumber,
        username=str(enumber),
        name=name,
        role=role,
        salary=1200.00,
        age=25,
        contact='900000000',
        supermarket=supermarket,
        sex='M',
        is_superuser=is_superuser,
        is_staff=is_staff,
    )
    emp.set_password('password123')
    emp.save()
    emp.groups.add(group)
    return emp


class ApiSmokeTests(TestCase):
    def setUp(self):
        _setup_group_permissions()
        self.supermarket = Supermarket.objects.create(
            location='Test Market', opening_time='08:00', close_time='22:00'
        )
        self.users = {
            'CEO':      _make_employee(1000, 'CEO User',      'CEO',      self.supermarket, 'CEO',      is_superuser=True, is_staff=True),
            'Manager':  _make_employee(1001, 'Manager User',  'Manager',  self.supermarket, 'Manager'),
            'Cashier':  _make_employee(1002, 'Cashier User',  'Cashier',  self.supermarket, 'Cashier'),
            'Employee': _make_employee(1005, 'Employee User', 'Employee', self.supermarket, 'Employee'),
        }
        self.client = APIClient()

    def _login(self, enumber):
        resp = self.client.post('/api/token/', {'enumber': enumber, 'password': 'password123'}, format='json')
        self.assertEqual(resp.status_code, 200, f'Login failed for enumber {enumber}')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {resp.data["access"]}')

    def test_health(self):
        resp = self.client.get('/api/health/')
        self.assertEqual(resp.status_code, 200)

    def test_token_all_roles(self):
        for role, user in self.users.items():
            resp = self.client.post('/api/token/', {'enumber': user.enumber, 'password': 'password123'}, format='json')
            self.assertEqual(resp.status_code, 200, f'{role} login failed')
            self.assertIn('access', resp.data)

    def test_me_endpoint(self):
        for role, user in self.users.items():
            self._login(user.enumber)
            resp = self.client.get('/api/me/')
            self.assertEqual(resp.status_code, 200, f'/api/me/ failed for {role}')

    def test_ceo_full_access(self):
        self._login(1000)
        for endpoint in ('supermarkets', 'employees', 'products', 'orders', 'purchases'):
            resp = self.client.get(f'/api/{endpoint}/')
            self.assertEqual(resp.status_code, 200, f'CEO: /api/{endpoint}/ returned {resp.status_code}')

    def test_manager_access(self):
        self._login(1001)
        for endpoint in ('products', 'employees', 'orders'):
            resp = self.client.get(f'/api/{endpoint}/')
            self.assertEqual(resp.status_code, 200, f'Manager: /api/{endpoint}/ returned {resp.status_code}')

    def test_cashier_cannot_access_orders(self):
        self._login(1002)
        self.assertEqual(self.client.get('/api/products/').status_code, 200)
        self.assertEqual(self.client.get('/api/purchases/').status_code, 200)
        self.assertEqual(self.client.get('/api/orders/').status_code, 403)

    def test_employee_read_only(self):
        self._login(1005)
        for endpoint in ('products', 'employees'):
            resp = self.client.get(f'/api/{endpoint}/')
            self.assertEqual(resp.status_code, 200, f'Employee: /api/{endpoint}/ returned {resp.status_code}')
