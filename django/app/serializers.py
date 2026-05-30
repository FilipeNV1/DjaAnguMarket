from decimal import Decimal
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
from .models import (
    Section, Supermarket, Employee, Product, Warehouse,
    Distributor, Client, Purchase, PurchaseItem, WareHStock, Order, OrderItem,
)

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['sname', 'department']

class SupermarketSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    section_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Section.objects.all(),
        source='sections', required=False,
    )

    class Meta:
        model = Supermarket
        fields = ['id', 'location', 'opening_time', 'close_time', 'sections', 'section_ids']

    def validate(self, data):
        opening = data.get('opening_time')
        closing = data.get('close_time')
        if opening and closing and closing <= opening:
            raise serializers.ValidationError({'close_time': 'Close time must be after opening time.'})
        return data

    def create(self, validated_data):
        sections = validated_data.pop('sections', [])
        supermarket = Supermarket.objects.create(**validated_data)
        supermarket.sections.set(sections)
        return supermarket

    def update(self, instance, validated_data):
        sections = validated_data.pop('sections', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if sections is not None:
            instance.sections.set(sections)
        return instance

class EmployeeSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    group_name = serializers.CharField(write_only=True, required=False)
    supermarket_location = serializers.CharField(source='supermarket.location', read_only=True)

    class Meta:
        model = Employee
        fields = [
            'enumber', 'name', 'role', 'salary', 'age', 'contact',
            'supermarket', 'supermarket_location', 'sex', 'supervisor',
            'is_active', 'group', 'group_name',
        ]
        read_only_fields = ['enumber']

    def get_group(self, obj):
        g = obj.groups.first()
        return g.name if g else None

    def create(self, validated_data):
        group_name = validated_data.pop('group_name', None)
        employee = Employee.objects.create(**validated_data)
        employee.username = str(employee.enumber)
        employee.password = make_password('password123')
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                employee.groups.set([group])
            except Group.DoesNotExist:
                pass
        employee.save()
        return employee

    def update(self, instance, validated_data):
        group_name = validated_data.pop('group_name', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                instance.groups.set([group])
                if group_name == 'CEO':
                    instance.is_staff = True
                    instance.is_superuser = True
                else:
                    instance.is_staff = False
                    instance.is_superuser = False
            except Group.DoesNotExist:
                pass
        instance.save()
        return instance

class ProductSerializer(serializers.ModelSerializer):
    section = serializers.CharField(source='section_name.sname', read_only=True)

    class Meta:
        model = Product
        fields = ['prodid', 'name', 'brand', 'price', 'req_cold', 'section_name', 'section']

class WareHStockSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True,
    )

    class Meta:
        model = WareHStock
        fields = ['product', 'product_name', 'product_price', 'wqty']

class WarehouseSerializer(serializers.ModelSerializer):
    stock = WareHStockSerializer(source='warehstock_set', many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Product.objects.all(), required=False,
    )
    supermarket_location = serializers.CharField(source='supermarket.location', read_only=True)

    class Meta:
        model = Warehouse
        fields = ['wnumber', 'area', 'supermarket', 'supermarket_location', 'stock', 'product_ids']
        read_only_fields = ['wnumber']

    def create(self, validated_data):
        products = validated_data.pop('product_ids', [])
        warehouse = Warehouse.objects.create(**validated_data)
        for product in products:
            WareHStock.objects.create(warehouse=warehouse, product=product, wqty=0)
        return warehouse

    def update(self, instance, validated_data):
        products = validated_data.pop('product_ids', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if products is not None:
            current = set(instance.products.all())
            new = set(products)
            for p in current - new:
                WareHStock.objects.filter(warehouse=instance, product=p).delete()
            for p in new - current:
                WareHStock.objects.create(warehouse=instance, product=p, wqty=0)
        return instance

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = ['email', 'contact', 'name']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['nif', 'name', 'fidelity', 'address', 'contact']

class PurchaseItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PurchaseItem
        fields = ['product', 'product_name', 'quantity', 'price_at_purchase']

class PurchaseSerializer(serializers.ModelSerializer):
    items = PurchaseItemSerializer(source='purchaseitem_set', many=True, read_only=True)
    item_data = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
    calculated_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    client_name = serializers.CharField(source='client.name', read_only=True, default=None)

    class Meta:
        model = Purchase
        fields = [
            'purchid', 'date', 'supermarket', 'client', 'client_name',
            'items', 'item_data', 'calculated_total',
        ]
        read_only_fields = ['purchid']

    def create(self, validated_data):
        item_data = validated_data.pop('item_data', [])
        purchase = Purchase.objects.create(**validated_data)
        for item in item_data:
            try:
                product = Product.objects.get(pk=int(item['product']))
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=int(item.get('quantity', 1)),
                    price_at_purchase=product.price,
                )
            except (Product.DoesNotExist, KeyError, ValueError):
                pass
        return purchase

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item_data', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if item_data is not None:
            new_ids = set()
            for item in item_data:
                try:
                    product = Product.objects.get(pk=int(item['product']))
                    new_ids.add(product.pk)
                    PurchaseItem.objects.update_or_create(
                        purchase=instance, product=product,
                        defaults={
                            'quantity': int(item.get('quantity', 1)),
                            'price_at_purchase': product.price,
                        },
                    )
                except (Product.DoesNotExist, KeyError, ValueError):
                    pass
            PurchaseItem.objects.filter(purchase=instance).exclude(product_id__in=new_ids).delete()
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'product_name', 'quantity', 'discounted_price']

    def get_discounted_price(self, obj):
        return obj.product.price * Decimal('0.6')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    item_data = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
    calculated_total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    distributor_name = serializers.CharField(source='distributor.name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'orderid', 'ord_date', 'supermarket', 'distributor', 'distributor_name',
            'items', 'item_data', 'calculated_total',
        ]
        read_only_fields = ['orderid']

    def create(self, validated_data):
        item_data = validated_data.pop('item_data', [])
        order = Order.objects.create(**validated_data)
        for item in item_data:
            try:
                product = Product.objects.get(pk=int(item['product']))
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=int(item.get('quantity', 1)),
                )
            except (Product.DoesNotExist, KeyError, ValueError):
                pass
        return order

    def update(self, instance, validated_data):
        item_data = validated_data.pop('item_data', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if item_data is not None:
            new_ids = set()
            for item in item_data:
                try:
                    product = Product.objects.get(pk=int(item['product']))
                    new_ids.add(product.pk)
                    OrderItem.objects.update_or_create(
                        order=instance, product=product,
                        defaults={'quantity': int(item.get('quantity', 1))},
                    )
                except (Product.DoesNotExist, KeyError, ValueError):
                    pass
            OrderItem.objects.filter(order=instance).exclude(product_id__in=new_ids).delete()
        return instance

class MeSerializer(serializers.ModelSerializer):
    group = serializers.SerializerMethodField()
    supermarket_id = serializers.IntegerField(source='supermarket.id', read_only=True)
    supermarket_location = serializers.CharField(source='supermarket.location', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.name', read_only=True, default=None)

    class Meta:
        model = Employee
        fields = [
            'enumber', 'name', 'role', 'group', 'supermarket_id', 'supermarket_location',
            'salary', 'age', 'contact', 'sex', 'supervisor_name',
        ]
        # Self-editable via PATCH /api/me/: name, contact, age, sex.
        # Everything else is read-only so a user can't change their own salary/role/store.
        read_only_fields = ['enumber', 'role', 'salary']

    def get_group(self, obj):
        g = obj.groups.first()
        return g.name if g else None