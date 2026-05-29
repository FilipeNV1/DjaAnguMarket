import decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

class Section(models.Model):
    sname = models.CharField(max_length=64, primary_key=True)
    department = models.CharField(max_length=64)
    def __str__(self):
        return self.sname

class Supermarket(models.Model):
    id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=128)
    opening_time = models.TimeField()
    close_time = models.TimeField()
    sections = models.ManyToManyField(Section)
    def __str__(self):
        return f"{self.location}"

class Employee(AbstractUser):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    enumber = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    role = models.CharField(max_length=32)
    salary = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    age = models.IntegerField(validators=[MinValueValidator(16)])
    contact = models.CharField(max_length=64)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    supervisor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')

    USERNAME_FIELD = 'enumber'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Automatically set is_staff and is_active for CEO employees"""
        # Only check groups if object has already been saved (has a primary key)
        if self.pk is not None:
            if self.groups.filter(name='CEO').exists():
                self.is_staff = True
                self.is_active = True
        super().save(*args, **kwargs)

class Product(models.Model):
    prodid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    req_cold = models.BooleanField()
    section_name = models.ForeignKey(Section, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Warehouse(models.Model):
    wnumber = models.AutoField(primary_key=True)
    area = models.CharField(max_length=64)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='WareHStock')
    def __str__(self):
        return f"Warehouse {self.wnumber}"

class Distributor(models.Model):
    email = models.EmailField(primary_key=True)
    contact = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=128)
    def __str__(self):
        return self.name

class Client(models.Model):
    nif = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64, blank=True)
    fidelity = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=128, blank=True)
    contact = models.CharField(max_length=64, blank=True)
    def __str__(self):
        return self.name or f"Client {self.nif}"

class Purchase(models.Model):
    purchid = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True)
    products = models.ManyToManyField(Product, through='PurchaseItem')
    def __str__(self):
        return f"Purchase {self.purchid}"
    @property
    def calculated_total(self):
        result = self.purchaseitem_set.aggregate(
                total_cost=models.Sum(models.F('quantity') * models.F('price_at_purchase'))
            )
        return result['total_cost'] or 0.00
    
class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    def __str__(self):
        return f"{self.purchase.purchid} - {self.product.name}"

class WareHStock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    wqty = models.IntegerField(validators=[MinValueValidator(0)])
    def __str__(self):
        return f"{self.warehouse.wnumber} - {self.product.name}: {self.wqty}"

class Order(models.Model):
    orderid = models.AutoField(primary_key=True)
    ord_date = models.DateField()
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
    distributor = models.ForeignKey(Distributor, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    def __str__(self):
        return f"Order {self.orderid}"
    
    @property
    def calculated_total(self):
        result = self.orderitem_set.aggregate(
                total_cost=models.Sum(models.F('quantity') * models.F('product__price') * decimal.Decimal('0.6'))
            )
        return result['total_cost'] or 0.00

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    def __str__(self):
        return f"{self.order.orderid} - {self.product.name}"