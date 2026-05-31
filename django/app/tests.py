from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from app.models import Supermarket

User = get_user_model()


class BaseDjanGoMarketTest(TestCase):
    def setUp(self):
        self.client = Client()
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
        from app.models import Section, Product, Client
        self.section = Section.objects.create(sname='Test Section', department='General')
        self.product = Product.objects.create(name='Sample Product', brand='BrandX', price=10.00, req_cold=False, section_name=self.section)
        self.client_obj = Client.objects.create(nif=123456789, name='Test Client')
        from app.models import Purchase
        self.purchase = Purchase.objects.create(date='2026-04-11 10:00:00', supermarket=self.dummy_supermarket, client=self.client_obj)

    def test_purchase_calculated_total(self):
        from app.models import PurchaseItem
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=2, price_at_purchase=10.00)
        PurchaseItem.objects.create(purchase=self.purchase, product=self.product, quantity=1, price_at_purchase=5.00)
        self.assertEqual(self.purchase.calculated_total, 25.00)

    def test_order_calculated_total(self):
        from app.models import Order, OrderItem, Distributor
        import decimal
        distributor = Distributor.objects.create(email='dist@test.com', name='Dist Test')
        order = Order.objects.create(ord_date='2026-04-11', supermarket=self.dummy_supermarket, distributor=distributor)
        OrderItem.objects.create(order=order, product=self.product, quantity=10)
        self.assertEqual(order.calculated_total, decimal.Decimal('60.00'))
