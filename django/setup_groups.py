#!/usr/bin/env python
"""
Django Groups and Permissions Setup Script
Sets up user groups (CEO, Manager, Cashier, Employee) with appropriate permissions
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjanGoMarket.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from app.models import (
    Section, Supermarket, Employee, Product, Warehouse, Distributor,
    Client, Purchase, PurchaseItem, WareHStock, Order
)

def create_groups():
    """Create the four user groups"""
    groups = ['CEO', 'Manager', 'Cashier', 'Employee']
    for group_name in groups:
        Group.objects.get_or_create(name=group_name)
    print(f"Created {len(groups)} groups: {', '.join(groups)}")

def get_model_permissions(model):
    """Get all CRUD permissions for a given model"""
    content_type = ContentType.objects.get_for_model(model)
    return Permission.objects.filter(content_type=content_type)

def setup_ceo_permissions():
    """CEO: All permissions across all models"""
    print("\nSetting up CEO permissions...")
    ceo_group = Group.objects.get(name='CEO')
    
    # Get all permissions
    all_permissions = Permission.objects.all()
    ceo_group.permissions.set(all_permissions)
    
    print(f"CEO: {ceo_group.permissions.count()} permissions assigned (all permissions)")

def setup_manager_permissions():
    """Manager: Standard permissions for Employee, Supermarket, Warehouse, WareHStock and Order; view permissions for other models"""
    print("\nSetting up Manager permissions...")
    manager_group = Group.objects.get(name='Manager')
    
    models_with_crud = [Employee, Supermarket, Warehouse, WareHStock, Order]
    permissions = []
    
    for model in models_with_crud:
        perms = get_model_permissions(model)
        permissions.extend(perms)
    
    # Also give view permissions for other models
    view_only_models = [Section, Supermarket, Distributor, Client, Purchase, PurchaseItem]
    for model in view_only_models:
        view_perms = get_model_permissions(model).filter(codename__startswith='view_')
        permissions.extend(view_perms)
    
    manager_group.permissions.set(permissions)
    print(f"Manager: {manager_group.permissions.count()} permissions assigned")
    print(f"  - CRUD for: Employee, Supermarket, Warehouse, WareHStock, Order")
    print(f"  - View for: Section, Supermarket, Distributor, Client, Purchase, PurchaseItem")

def setup_cashier_permissions():
    """Cashier: Permissions for Purchase and PurchaseItem (add, change, delete, view)"""
    print("\nSetting up Cashier permissions...")
    cashier_group = Group.objects.get(name='Cashier')
    
    models_with_crud = [Purchase, PurchaseItem]
    permissions = []
    
    for model in models_with_crud:
        perms = get_model_permissions(model)
        permissions.extend(perms)
    
    # Also give view permissions for related models
    view_only_models = [Product, Client, Warehouse, WareHStock, Supermarket]
    for model in view_only_models:
        view_perms = get_model_permissions(model).filter(codename__startswith='view_')
        permissions.extend(view_perms)
    
    cashier_group.permissions.set(permissions)
    print(f"Cashier: {cashier_group.permissions.count()} permissions assigned")
    print(f"  - CRUD for: Purchase, PurchaseItem")
    print(f"  - View for: Product, Client, Warehouse, WareHStock, Supermarket")

def setup_employee_permissions():
    """Employee: View-only permissions for all models"""
    print("\nSetting up Employee permissions...")
    employee_group = Group.objects.get(name='Employee')
    
    models_to_view = [
        Section, Supermarket, Employee, Product, Warehouse, Distributor,
        Client, Purchase, PurchaseItem, WareHStock
    ]
    
    permissions = []
    for model in models_to_view:
        view_perms = get_model_permissions(model).filter(codename__startswith='view_')
        permissions.extend(view_perms)
    
    employee_group.permissions.set(permissions)
    print(f"Employee: {employee_group.permissions.count()} permissions assigned (view-only)")
    print(f"  - View for: All models")

def setup_all_groups():
    """Main function to set up all groups and permissions"""
    print("Starting group and permission setup...\n")
    try:
        create_groups()
        setup_ceo_permissions()
        setup_manager_permissions()
        setup_cashier_permissions()
        setup_employee_permissions()
        print("\nAll groups and permissions configured successfully!")
    except Exception as e:
        print(f"\nError during setup: {e}")
        raise

if __name__ == '__main__':
    setup_all_groups()
