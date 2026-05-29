#!/usr/bin/env python
"""
Django Populate Script
Populate the database with sample data from ProjetoDML.sql
"""
import os
import django
from datetime import datetime, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjanGoMarket.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from app.models import (
    Supermarket, Section, Employee, Product, Client,
    Purchase, PurchaseItem, Warehouse, WareHStock,
    Order, OrderItem, Distributor
)

def clear_data():
    """Clear all data from tables"""
    print("Clearing existing data...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    WareHStock.objects.all().delete()
    PurchaseItem.objects.all().delete()
    Purchase.objects.all().delete()
    Product.objects.all().delete()
    Client.objects.all().delete()
    Warehouse.objects.all().delete()
    Employee.objects.all().delete()
    Section.objects.all().delete()
    Distributor.objects.all().delete()
    Supermarket.objects.all().delete()
    print("Data cleared!")

def populate_supermarkets():
    """Insert supermarkets"""
    print("Populating supermarkets...")
    supermarkets = [
        Supermarket(id=1, location='Esgueira, Aveiro', opening_time=time(8, 45), close_time=time(20, 0)),
        Supermarket(id=2, location='Arcos, Estremoz', opening_time=time(8, 0), close_time=time(22, 30)),
        Supermarket(id=3, location='Alcochete, Lisboa', opening_time=time(8, 0), close_time=time(20, 15)),
    ]
    Supermarket.objects.bulk_create(supermarkets)
    print(f"Created {len(supermarkets)} supermarkets")

def populate_sections():
    """Insert sections"""
    print("Populating sections...")
    sections = [
        Section(sname='Beverages', department='Food'),
        Section(sname='Canned Goods', department='Food'),
        Section(sname='Snacks', department='Food'),
        Section(sname='Butcher', department='Fresh'),
        Section(sname='Fishmonger', department='Fresh'),
        Section(sname='Bakery', department='Fresh'),
        Section(sname='Deli', department='Fresh'),
        Section(sname='Fruits and Vegetables', department='Fresh'),
        Section(sname='Dairy', department='Fresh'),
        Section(sname='Cleaning', department='Bazaar'),
        Section(sname='Hygiene', department='Bazaar'),
        Section(sname='Toys', department='Bazaar'),
    ]
    Section.objects.bulk_create(sections)
    print(f"Created {len(sections)} sections")

def populate_store_sections():
    """Associate sections to supermarkets"""
    print("Populating store sections...")
    supermarkets = Supermarket.objects.all()
    sections = Section.objects.all()
    
    for supermarket in supermarkets:
        supermarket.sections.add(*sections)
    print("Associated sections to all supermarkets")

def populate_distributors():
    """Insert distributors"""
    print("Populating distributors...")
    distributors = [
        Distributor(email='beverages@dist.pt', contact='220111222', name='Distributor Beverages'),
        Distributor(email='fresh@dist.pt', contact='220333444', name='Distributor Fresh'),
        Distributor(email='bazar@dist.pt', contact='220555666', name='Distributor Bazaar'),
    ]
    Distributor.objects.bulk_create(distributors)
    print(f"Created {len(distributors)} distributors")

def populate_employees():
    """Insert employees"""
    print("Populating employees...")
    
    supermarkets = {s.id: s for s in Supermarket.objects.all()}
    
    employees_data = [
        {'enumber': 1000, 'name': 'Ricardo CEO', 'role': 'CEO', 'salary': 3000.00, 'age': 55, 'contact': '900000000', 'supermarket_id': 1, 'sex': 'M', 'supervisor': None, 'group': 'CEO'},
        {'enumber': 1001, 'name': 'Antonio Silva', 'role': 'Manager', 'salary': 1800.00, 'age': 42, 'contact': '910111213', 'supermarket_id': 1, 'sex': 'M', 'supervisor': None, 'group': 'Manager'},
        {'enumber': 1002, 'name': 'Maria Santos', 'role': 'Cashier Supervisor', 'salary': 1500.00, 'age': 36, 'contact': '920222324', 'supermarket_id': 1, 'sex': 'F', 'supervisor': 1001, 'group': 'Cashier'},
        {'enumber': 1003, 'name': 'Miguel Ferreira', 'role': 'Cashier', 'salary': 850.00, 'age': 25, 'contact': '930333435', 'supermarket_id': 1, 'sex': 'M', 'supervisor': 1002, 'group': 'Cashier'},
        {'enumber': 1005, 'name': 'Carlos Oliveira', 'role': 'Stocker', 'salary': 800.00, 'age': 19, 'contact': '950555657', 'supermarket_id': 1, 'sex': 'M', 'supervisor': 1001, 'group': 'Employee'},

        {'enumber': 2001, 'name': 'Carlos Almeida', 'role': 'Manager', 'salary': 1750.00, 'age': 45, 'contact': '911121314', 'supermarket_id': 2, 'sex': 'M', 'supervisor': None, 'group': 'Manager'},
        {'enumber': 2002, 'name': 'Sofia Ribeiro', 'role': 'Cashier Supervisor', 'salary': 1450.00, 'age': 38, 'contact': '921222324', 'supermarket_id': 2, 'sex': 'F', 'supervisor': 2001, 'group': 'Cashier'},
        {'enumber': 2003, 'name': 'Ricardo Martins', 'role': 'Cashier', 'salary': 830.00, 'age': 22, 'contact': '931323334', 'supermarket_id': 2, 'sex': 'M', 'supervisor': 2002, 'group': 'Cashier'},
        {'enumber': 2005, 'name': 'Miguel Sousa', 'role': 'Stocker', 'salary': 790.00, 'age': 20, 'contact': '951525354', 'supermarket_id': 2, 'sex': 'M', 'supervisor': 2001, 'group': 'Employee'},

        {'enumber': 3001, 'name': 'Paulo Mendes', 'role': 'Manager', 'salary': 1900.00, 'age': 47, 'contact': '912131415', 'supermarket_id': 3, 'sex': 'M', 'supervisor': None, 'group': 'Manager'},
        {'enumber': 3002, 'name': 'Carla Rodrigues', 'role': 'Cashier Supervisor', 'salary': 1600.00, 'age': 39, 'contact': '922232425', 'supermarket_id': 3, 'sex': 'F', 'supervisor': 3001, 'group': 'Cashier'},
        {'enumber': 3004, 'name': 'Carlota Lopes', 'role': 'Cashier', 'salary': 870.00, 'age': 27, 'contact': '942434445', 'supermarket_id': 3, 'sex': 'F', 'supervisor': 3002, 'group': 'Cashier'},
        {'enumber': 3005, 'name': 'Hugo Dias', 'role': 'Stocker', 'salary': 820.00, 'age': 21, 'contact': '952535455', 'supermarket_id': 3, 'sex': 'M', 'supervisor': 3001, 'group': 'Employee'},
        {'enumber': 3007, 'name': 'Eduardo Fernandes', 'role': 'Security', 'salary': 900.00, 'age': 32, 'contact': '972737475', 'supermarket_id': 3, 'sex': 'M', 'supervisor': 3001, 'group': 'Employee'},
    ]
    
    employees = []
    supervisor_map = {}
    group_map = {}
    
    # First step: create all employees without supervisors
    for emp_data in employees_data:
        supervisor_id = emp_data.pop('supervisor')
        group_name = emp_data.pop('group')
        username = f"{emp_data['enumber']}"
        emp = Employee(
            username=username,
            password=make_password('password123'),
            enumber=emp_data['enumber'],
            name=emp_data['name'],
            role=emp_data['role'],
            salary=emp_data['salary'],
            age=emp_data['age'],
            contact=emp_data['contact'],
            supermarket=supermarkets[emp_data['supermarket_id']],
            sex=emp_data['sex'],
        )
        employees.append(emp)
        supervisor_map[emp_data['enumber']] = supervisor_id
        group_map[emp_data['enumber']] = group_name
    
    Employee.objects.bulk_create(employees)
    
    # Second step: update supervisors and return group_map for group assignment
    all_employees = {e.enumber: e for e in Employee.objects.all()}
    for enumber, supervisor_id in supervisor_map.items():
        if supervisor_id:
            emp = all_employees[enumber]
            emp.supervisor = all_employees[supervisor_id]
            emp.save()
    
    print(f"Created {len(employees_data)} employees")
    return group_map

def populate_products():
    """Insert products"""
    print("Populating products...")
    sections = {s.sname: s for s in Section.objects.all()}
    
    products_data = [
        (101, 'Beer 6x33cl Pack', 'Super Bock', 3.99, False, 'Beverages'),
        (102, 'Whisky', 'Ballantines', 15.99, False, 'Beverages'),
        (201, 'Tuna in oil 120g', 'Bom Petisco', 1.79, False, 'Canned Goods'),
        (202, 'Sardine in Tomato 125g', 'Ramirez', 1.59, False, 'Canned Goods'),
        (301, 'Potato Chips 150g', 'Lay\'s', 1.49, False, 'Snacks'),
        (302, 'Peanuts 200g', 'Ultje', 1.79, False, 'Snacks'),
        (401, 'Sirloin Steak kg', 'Nacional', 12.99, True, 'Butcher'),
        (402, 'Whole Chicken kg', 'Nacional', 2.99, True, 'Butcher'),
        (501, 'Boiled Shrimp 200g', 'Nacional', 4.99, True, 'Fishmonger'),
        (502, 'Dried Codfish kg', 'Noruega', 15.99, False, 'Fishmonger'),
        (601, 'Baguette', 'Padaria Propria', 0.75, False, 'Bakery'),
        (602, 'Croissant', 'Padaria Propria', 0.65, False, 'Bakery'),
        (701, 'Sliced Ham 150g', 'Nobre', 1.89, True, 'Deli'),
        (702, 'Edam Cheese kg', 'Terra Nostra', 7.99, True, 'Deli'),
        (801, 'Pears kg', 'Nacional', 1.49, False, 'Fruits and Vegetables'),
        (802, 'Bananas kg', 'Nacional', 1.29, False, 'Fruits and Vegetables'),
        (901, 'Plain Yogurt 4 Pack', 'Danone', 1.79, True, 'Dairy'),
        (902, 'Butter 250g', 'Presidente', 2.19, True, 'Dairy'),
        (1101, 'Fabric Softener 1.5L', 'Comfort', 3.29, False, 'Cleaning'),
        (1102, 'Toilet Paper 12 rolls', 'Renova', 3.49, False, 'Cleaning'),
        (1201, 'Toothpaste 75ml', 'Colgate', 2.19, False, 'Hygiene'),
        (1202, 'Roll-on Deodorant', 'Nivea', 2.39, False, 'Hygiene'),
        (1301, 'Board Game', 'Monopoly', 29.99, False, 'Toys'),
        (1302, 'Teddy Bear 25cm', 'TY', 14.99, False, 'Toys'),
    ]
    
    products = [
        Product(
            prodid=p[0],
            name=p[1],
            brand=p[2],
            price=p[3],
            req_cold=p[4],
            section_name=sections[p[5]]
        )
        for p in products_data
    ]
    Product.objects.bulk_create(products)
    print(f"Created {len(products)} products")

def populate_clients():
    """Insert clients"""
    print("Populating clients...")
    clients = [
        Client(nif=123456789, name='Maria Oliveira', fidelity=3, address='Rua das Flores 123, Aveiro', contact='912345678'),
        Client(nif=234567890, name='Joao Silva', fidelity=2, address='Avenida Central 456, Aveiro', contact='923456789'),
        Client(nif=345678901, name='Ana Santos', fidelity=5, address='Rua da Republica 78, Estremoz', contact='934567890'),
        Client(nif=456789012, name='Pedro Costa', fidelity=1, address='Rua dos Pescadores 90, Alcochete', contact='945678901'),
        Client(nif=567890123, name='Sofia Pereira', fidelity=4, address='Avenida da Liberdade 234, Lisboa', contact='956789012'),
        Client(nif=678901234, name='Miguel Ferreira', fidelity=2, address='Rua Nova 567, Aveiro', contact='967890123'),
        Client(nif=789012345, name='Carla Martins', fidelity=0, address='Rua do Comercio 890, Estremoz', contact='978901234'),
        Client(nif=890123456, name='Ricardo Almeida', fidelity=3, address='Avenida do Mar 123, Lisboa', contact='989012345'),
        Client(nif=901234567, name='Teresa Sousa', fidelity=4, address='Rua das Oliveiras 45, Aveiro', contact='990123456'),
        Client(nif=112233445, name='Paulo Rodrigues', fidelity=2, address='Rua Central 67, Lisboa', contact='911223344'),
    ]
    Client.objects.bulk_create(clients)
    print(f"Created {len(clients)} clients")

def populate_warehouses():
    """Insert warehouses"""
    print("Populating warehouses...")
    supermarkets = {s.id: s for s in Supermarket.objects.all()}
    
    warehouses = [
        Warehouse(wnumber=1, area='Warehouse Aveiro', supermarket=supermarkets[1]),
        Warehouse(wnumber=2, area='Warehouse Estremoz', supermarket=supermarkets[2]),
        Warehouse(wnumber=3, area='Warehouse Lisboa', supermarket=supermarkets[3]),
    ]
    Warehouse.objects.bulk_create(warehouses)
    print(f"Created {len(warehouses)} warehouses")

def populate_warehouse_stock():
    """Insert warehouse stock"""
    print("Populating warehouse stock...")
    warehouses = {w.wnumber: w for w in Warehouse.objects.all()}
    products = {p.prodid: p for p in Product.objects.all()}
    
    stock_data = [
        (1, 101, 50), (1, 102, 30), (1, 201, 100), (1, 202, 80),
        (1, 301, 120), (1, 302, 150), (1, 401, 40), (1, 402, 60),
        (2, 501, 25), (2, 502, 35), (2, 601, 200), (2, 602, 180),
        (2, 701, 50), (2, 702, 30), (2, 801, 100), (2, 802, 120),
        (3, 901, 75), (3, 902, 50), (3, 1101, 100), (3, 1102, 90),
        (3, 1201, 80), (3, 1202, 95), (3, 1301, 15), (3, 1302, 20),
    ]
    
    stock = [
        WareHStock(warehouse=warehouses[s[0]], product=products[s[1]], wqty=s[2])
        for s in stock_data
    ]
    WareHStock.objects.bulk_create(stock)
    print(f"Created {len(stock)} warehouse stock records")

def populate_purchases():
    """Insert purchases"""
    print("Populating purchases...")
    supermarkets = {s.id: s for s in Supermarket.objects.all()}
    clients = {c.nif: c for c in Client.objects.all()}
    
    purchases_data = [
        (1001, '2025-05-10 10:30:00', 1, 123456789),
        (1002, '2025-05-11 14:15:00', 1, 234567890),
        (1003, '2025-05-13 09:00:00', 1, None),
        (1004, '2025-05-14 16:45:00', 1, 901234567),
        (1005, '2025-05-16 11:20:00', 1, None),
        (2001, '2025-05-16 10:00:00', 2, 345678901),
        (2002, '2025-05-16 15:30:00', 2, None),
        (2003, '2025-05-13 13:00:00', 2, 789012345),
        (2004, '2025-05-11 09:15:00', 2, None),
        (2005, '2025-05-29 12:00:00', 2, 345678901),
        (3001, '2025-05-29 10:30:00', 3, 456789012),
        (3002, '2025-05-29 14:00:00', 3, None),
        (3003, '2025-05-29 11:45:00', 3, 567890123),
        (3004, '2025-05-27 16:20:00', 3, 890123456),
        (3005, '2025-05-22 09:50:00', 3, None),
    ]
    
    purchases = [
        Purchase(
            purchid=p[0],
            date=datetime.strptime(p[1], '%Y-%m-%d %H:%M:%S'),
            supermarket=supermarkets[p[2]],
            client=clients.get(p[3])
        )
        for p in purchases_data
    ]
    Purchase.objects.bulk_create(purchases)
    print(f"Created {len(purchases)} purchases")

def populate_purchase_items():
    """Insert purchase items"""
    print("Populating purchase items...")
    purchases = {p.purchid: p for p in Purchase.objects.all()}
    products = {p.prodid: p for p in Product.objects.all()}
    
    purchase_items_data = [
        (1001, 101, 2),
        (1002, 401, 2), (1002, 701, 2),
        (1003, 102, 1), (1003, 201, 1),
        (1004, 101, 3), (1004, 201, 2),
        (1005, 602, 3),
        (2001, 102, 2), (2001, 301, 1),
        (2002, 501, 1), (2002, 802, 3),
        (2003, 401, 1), (2003, 502, 1),
        (2004, 701, 2), (2004, 901, 2),
        (2005, 1301, 1), (2005, 1302, 1),
        (3001, 102, 1), (3001, 501, 1),
        (3002, 1101, 2), (3002, 1201, 2),
        (3003, 1301, 1), (3003, 1302, 1),
        (3004, 702, 2), (3004, 902, 2),
        (3005, 1102, 1), (3005, 1202, 3),
    ]
    
    purchase_items = [
        PurchaseItem(
            purchase=purchases[item[0]],
            product=products[item[1]], 
            quantity=item[2],
            price_at_purchase=products[item[1]].price
        )
        for item in purchase_items_data
    ]
    PurchaseItem.objects.bulk_create(purchase_items)
    print(f"Created {len(purchase_items)} purchase items")

def populate_orders():
    """Insert orders"""
    print("Populating orders...")
    supermarkets = {s.id: s for s in Supermarket.objects.all()}
    distributors = {d.email: d for d in Distributor.objects.all()}

    orders_data = [
        (5001, '2025-05-17', 1, 'beverages@dist.pt'),
        (5002, '2025-05-20', 1, 'fresh@dist.pt'),
        (5003, '2025-05-23', 1, 'bazar@dist.pt'),
        (5004, '2025-05-26', 1, 'fresh@dist.pt'),
        (6001, '2025-05-18', 2, 'fresh@dist.pt'),
        (6002, '2025-05-22', 2, 'beverages@dist.pt'),
        (6003, '2025-05-25', 2, 'bazar@dist.pt'),
        (6004, '2025-05-28', 2, 'fresh@dist.pt'),
        (7001, '2025-05-19', 3, 'bazar@dist.pt'),
        (7002, '2025-05-24', 3, 'fresh@dist.pt'),
        (7003, '2025-05-27', 3, 'beverages@dist.pt'),
        (7004, '2025-05-30', 3, 'bazar@dist.pt'),
    ]

    orders = [
        Order(
            orderid=o[0],
            ord_date=datetime.strptime(o[1], '%Y-%m-%d').date(),
            supermarket=supermarkets[o[2]],
            distributor=distributors[o[3]],
        )
        for o in orders_data
    ]
    Order.objects.bulk_create(orders)
    print(f"Created {len(orders)} orders")

def populate_order_items():
    """Insert order items"""
    print("Populating order items...")
    orders = {o.orderid: o for o in Order.objects.all()}
    products = {p.prodid: p for p in Product.objects.all()}

    order_items_data = [
        (5001, 101, 30), (5001, 102, 10),
        (5002, 401, 20), (5002, 701, 25), (5002, 901, 35),
        (5003, 1101, 40), (5003, 1201, 50),
        (5004, 201, 70), (5004, 301, 45),
        (6001, 501, 18), (6001, 601, 80), (6001, 802, 45),
        (6002, 201, 60), (6002, 301, 55),
        (6003, 1202, 40), (6003, 1102, 30),
        (6004, 401, 16), (6004, 702, 20),
        (7001, 1301, 8), (7001, 1302, 20),
        (7002, 702, 22), (7002, 902, 28), (7002, 1202, 35),
        (7003, 102, 12), (7003, 202, 65),
        (7004, 901, 40), (7004, 1101, 26),
    ]

    order_items = [
        OrderItem(
            order=orders[item[0]],
            product=products[item[1]],
            quantity=item[2],
        )
        for item in order_items_data
    ]
    OrderItem.objects.bulk_create(order_items)
    print(f"Created {len(order_items)} order items")

def assign_employees_to_groups(group_map):
    """Assign employees to their corresponding groups using the group_map from populate_employees"""
    print("\nAssigning employees to groups...")
    
    try:
        for enumber, group_name in group_map.items():
            employee = Employee.objects.get(enumber=enumber)
            group = Group.objects.get(name=group_name)
            employee.groups.add(group)
            employee.save()
        
        print(f"Assigned {len(group_map)} employees to groups")
    except Group.DoesNotExist:
        print("Error: Groups not found. Make sure to run 'python setup_groups.py' first!")
        raise
    except Employee.DoesNotExist as e:
        print(f"Error: Employee not found: {e}")
        raise

def populate():
    """Main populate function"""
    print("Starting database population...")
    try:
        clear_data()
        populate_supermarkets()
        populate_sections()
        populate_store_sections()
        populate_distributors()
        group_map = populate_employees()
        assign_employees_to_groups(group_map)
        populate_products()
        populate_clients()
        populate_warehouses()
        populate_warehouse_stock()
        populate_purchases()
        populate_purchase_items()
        populate_orders()
        populate_order_items()
        print("\nDatabase population completed successfully!")
    except Exception as e:
        print(f"Error during population: {e}")
        raise

if __name__ == '__main__':
    populate()
