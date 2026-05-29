from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from app.models import Supermarket

User = get_user_model()

# Create your tests here.
class BaseDjanGoMarketTest(TestCase):
    """Base class to set up the CEO user and test client for all tests."""
    def setUp(self):
        self.client = Client()
        # Setup CEO Group and User
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

class AuthAccessTests(BaseDjanGoMarketTest):
    def test_phase_1_authentication(self):
        """Test login functionality."""
        response = self.client.post('/login/', {'username': '1000', 'password': 'password123'})
        self.assertEqual(response.status_code, 302) # Should redirect on success
        
    def test_phase_2_add_forms_accessibility(self):
        """Test that the CEO can access all add forms via GET."""
        self.client.login(enumber='1000', password='password123')
        endpoints = [
            '/supermarkets/add/', '/sections/add/', '/employees/add/',
            '/products/add/', '/warehouses/add/', '/distributors/add/',
            '/clients/add/', '/purchases/add/', '/orders/add/'
        ]
        for endpoint in endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(response.status_code, 200, f"Failed to load {endpoint}")
            self.assertIn(b'<form', response.content, f"No form found on {endpoint}")

class SupermarketTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.client.login(enumber='1000', password='password123')
        self.valid_data = {
            'location': '45 Test Avenue',
            'opening_time': '08:00', 'close_time': '22:00'
        }

    def test_valid_supermarket(self):
        response = self.client.post('/supermarkets/add/', self.valid_data)
        self.assertEqual(response.status_code, 302) # 302 means success & redirect

    def test_blank_location_rejected(self):
        data = self.valid_data.copy()
        data['location'] = ''
        response = self.client.post('/supermarkets/add/', data)
        self.assertEqual(response.status_code, 200) # 200 means form failed and re-rendered

    def test_invalid_time_format(self):
        data = self.valid_data.copy()
        data['opening_time'] = 'not-a-time'
        response = self.client.post('/supermarkets/add/', data)
        self.assertEqual(response.status_code, 200)

    def test_closing_before_opening(self):
        data = self.valid_data.copy()
        data['opening_time'] = '22:00'
        data['close_time'] = '08:00'
        response = self.client.post('/supermarkets/add/', data)
        self.assertEqual(response.status_code, 200) # Should fail custom clean() validation

class DistributorTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.client.login(enumber='1000', password='password123')
        self.valid_data = {
            'name': 'Distribuidora Lda', 'email': 'geral@dist.pt',
            'contact': '210123456'
        }

    def test_valid_distributor(self):
        response = self.client.post('/distributors/add/', self.valid_data)
        self.assertEqual(response.status_code, 302)

    def test_empty_fields_rejected(self):
        response = self.client.post('/distributors/add/', {'name': '', 'email': '', 'contact': ''})
        self.assertEqual(response.status_code, 200)

    def test_invalid_email_format(self):
        data = self.valid_data.copy()
        data['email'] = 'abc##notemail'
        response = self.client.post('/distributors/add/', data)
        self.assertEqual(response.status_code, 200)

class ClientTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.client.login(enumber='1000', password='password123')
        self.valid_data = {
            'name': 'Ana Costa', 'nif': '234567890', 
            'fidelity': '50', 'address': 'Av. Almirante Reis', 'contact': '934001122'
        }

    def test_negative_fidelity_points(self):
        data = self.valid_data.copy()
        data['fidelity'] = '-999'
        response = self.client.post('/clients/add/', data)
        self.assertEqual(response.status_code, 200)

    def test_duplicate_nif_rejected(self):
        # Post once successfully
        self.client.post('/clients/add/', self.valid_data)
        # Post again with the same NIF
        data = self.valid_data.copy()
        data['name'] = 'Duplicate Client'
        response = self.client.post('/clients/add/', data)
        self.assertEqual(response.status_code, 200) # Should fail

class ProductTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.client.login(enumber='1000', password='password123')
        self.valid_data = {
            'name': 'Yogurt', 'price': '1.49', 
            'temperature_min': '2', 'temperature_max': '8', 'section_name': 'Test Section'
        }

    def test_negative_price_rejected(self):
        data = self.valid_data.copy()
        data['price'] = '-9.99'
        response = self.client.post('/products/add/', data)
        self.assertEqual(response.status_code, 200)

    def test_missing_section_rejected(self):
        data = self.valid_data.copy()
        data['section'] = ''
        response = self.client.post('/products/add/', data)
        self.assertEqual(response.status_code, 200)

class EmployeeTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        self.client.login(enumber='1000', password='password123')
        self.valid_data = {
            'employee_number': '9901', 'name': 'Worker', 
            'role': 'Cashier', 'salary': '1100.00', 'supermarket': '1'
        }

    def test_negative_salary(self):
        data = self.valid_data.copy()
        data['salary'] = '-500'
        response = self.client.post('/employees/add/', data)
        self.assertEqual(response.status_code, 200)

class LogicTests(BaseDjanGoMarketTest):
    def setUp(self):
        super().setUp()
        from app.models import Section, Product, Purchase, PurchaseItem, Client
        self.section = Section.objects.create(sname='Test Section', department='General')
        self.product = Product.objects.create(name='Sample Product', brand='BrandX', price=10.00, req_cold=False, section_name=self.section)
        self.client_obj = Client.objects.create(nif=123456789, name='Test Client')
        self.purchase = Purchase.objects.create(date='2026-04-11 10:00:00', supermarket=self.dummy_supermarket, client=self.client_obj)

    def test_purchase_calculated_total(self):
        from app.models import PurchaseItem
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=2, price_at_purchase=10.00)
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=1, price_at_purchase=5.00)
        
        # 2 * 10 + 1 * 5 = 25
        self.assertEqual(self.purchase.calculated_total, 25.00)

    def test_order_calculated_total(self):
        from app.models import Order, OrderItem, Distributor
        import decimal
        distributor = Distributor.objects.create(email='dist@test.com', name='Dist Test')
        order = Order.objects.create(ord_date='2026-04-11', supermarket=self.dummy_supermarket, distributor=distributor)
        OrderItem.objects.create(order=order, product=self.product, quantity=10)
        
        # 10 * 10.00 * 0.6 = 60.00
        self.assertEqual(order.calculated_total, decimal.Decimal('60.00'))

