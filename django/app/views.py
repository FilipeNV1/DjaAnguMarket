from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.hashers import make_password
import json
from .models import (
    Supermarket,
    Section,
    Employee,
    Product,
    Warehouse,
    Distributor,
    Client,
    Purchase,
    Order,
    WareHStock,
    PurchaseItem,
    OrderItem
)
from .forms import SupermarketForm, SectionForm, EmployeeForm, ProductForm, WarehouseForm, DistributorForm, ClientForm, PurchaseForm, OrderForm

def home(request):
    return render(request, 'home.html')

@login_required
def supermarket_list(request):
    if request.user.groups.filter(name='CEO').exists():
        supermarkets = Supermarket.objects.all()
    else:
        supermarkets = Supermarket.objects.filter(id=request.user.supermarket_id)
    return render(request, 'supermarket_list.html', {'supermarkets': supermarkets})

@login_required
def section_list(request):
    sections = Section.objects.all()
    return render(request, 'section_list.html', {'sections': sections})

@login_required
def employee_list(request):
    if request.user.groups.filter(name='CEO').exists():
        employees = Employee.objects.all()
    else:
        employees = Employee.objects.filter(supermarket=request.user.supermarket)
    return render(request, 'employee_list.html', {'employees': employees})

@login_required
def product_list(request):
    products = Product.objects.select_related('section_name').all()
    return render(request, 'product_list.html', {'products': products})

@login_required
def warehouse_list(request):
    if request.user.groups.filter(name='CEO').exists():
        warehouses = Warehouse.objects.select_related('supermarket').all()
    else:
        warehouses = Warehouse.objects.filter(supermarket=request.user.supermarket)
    return render(request, 'warehouse_list.html', {'warehouses': warehouses})

@login_required
def distributor_list(request):
    distributors = Distributor.objects.all()
    return render(request, 'distributor_list.html', {'distributors': distributors})

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, 'client_list.html', {'clients': clients})

@login_required
def purchase_list(request):
    purchases = Purchase.objects.all()
    return render(request, 'purchase_list.html', {'purchases': purchases})

@login_required
def order_list(request):
    if request.user.groups.filter(name='CEO').exists():
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(supermarket=request.user.supermarket)
    return render(request, 'order_list.html', {'orders': orders})

@login_required
@permission_required('app.add_supermarket', raise_exception=True)
def supermarket_create(request):
    if request.method == 'POST':
        form = SupermarketForm(request.POST)
        if form.is_valid():
            sections = form.cleaned_data.pop('sections')
            form.cleaned_data.pop('id', None)  # Remove readonly auto-generated field
            obj = Supermarket.objects.create(**form.cleaned_data)
            if sections is not None:
                obj.sections.set(sections)
            return redirect('supermarket_list')
    else:
        form = SupermarketForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Supermarket', 'icon': 'bi-shop', 'list_url': 'supermarket_list'})

@login_required
@permission_required('app.add_section', raise_exception=True)
def section_create(request):
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            Section.objects.create(**form.cleaned_data)
            return redirect('section_list')
    else:
        form = SectionForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Section', 'icon': 'bi-tags', 'list_url': 'section_list'})

@login_required
@permission_required('app.add_employee', raise_exception=True)
def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, user=request.user)
        if form.is_valid():
            # Extract form data
            data = form.cleaned_data.copy()
            data.pop('enumber', None)  # Remove auto-generated field
            group = data.pop('group', None)
            
            # Create employee to get auto-generated enumber
            employee = Employee.objects.create(**data)
            
            # Add group and set username using auto-generated enumber
            if group:
                employee.groups.add(group)
            
            employee.username = str(employee.enumber)
            employee.password = make_password('password123')
            employee.save()  # Model's save() will handle is_staff/is_active for CEO
            
            return redirect('employee_list')
    else:
        form = EmployeeForm(user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Employee', 'icon': 'bi-person-badge', 'list_url': 'employee_list'})

@login_required
@permission_required('app.add_product', raise_exception=True)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.cleaned_data.pop('prodid', None)  # Remove auto-generated field
            Product.objects.create(**form.cleaned_data)
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Product', 'icon': 'bi-box-seam', 'list_url': 'product_list'})

@login_required
@permission_required('app.add_warehouse', raise_exception=True)
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST, user=request.user)
        if form.is_valid():
            products = form.cleaned_data.pop('products', [])
            form.cleaned_data.pop('wnumber', None)  # Remove auto-generated field
            obj = Warehouse.objects.create(**form.cleaned_data)
            from .models import WareHStock
            for prod in products:
                WareHStock.objects.create(warehouse=obj, product=prod, wqty=0)
            return redirect('warehouse_list')
    else:
        form = WarehouseForm(user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Warehouse', 'icon': 'bi-boxes', 'list_url': 'warehouse_list'})

@login_required
@permission_required('app.add_distributor', raise_exception=True)
def distributor_create(request):
    if request.method == 'POST':
        form = DistributorForm(request.POST)
        if form.is_valid():
            Distributor.objects.create(**form.cleaned_data)
            return redirect('distributor_list')
    else:
        form = DistributorForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Distributor', 'icon': 'bi-building', 'list_url': 'distributor_list'})

@login_required
@permission_required('app.add_client', raise_exception=True)
def client_create(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            Client.objects.create(**form.cleaned_data)
            return redirect('client_list')
    else:
        form = ClientForm()
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Client', 'icon': 'bi-emoji-smile', 'list_url': 'client_list'})

@login_required
@permission_required('app.add_purchase', raise_exception=True)
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST, user=request.user)
        if form.is_valid():
            products = form.cleaned_data.pop('products', [])
            form.cleaned_data.pop('purchid', None)  # Remove auto-generated field
            form.cleaned_data.pop('total', None)  # Remove total field
            obj = Purchase.objects.create(**form.cleaned_data)
            from .models import PurchaseItem
            for prod in products:
                qty = request.POST.get(f'qty_{prod.prodid}', 1)
                try:
                    qty = int(qty)
                except ValueError:
                    qty = 1
                PurchaseItem.objects.create(purchase=obj, product=prod, quantity=qty, price_at_purchase=prod.price)
            return redirect('purchase_list')
    else:
        form = PurchaseForm(user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Purchase', 'icon': 'bi-receipt', 'list_url': 'purchase_list'})

@login_required
@permission_required('app.add_order', raise_exception=True)
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            products = form.cleaned_data.pop('products', [])
            form.cleaned_data.pop('orderid', None)
            form.cleaned_data.pop('total', None)  # Remove total field
            obj = Order.objects.create(**form.cleaned_data)
            for prod in products:
                qty = request.POST.get(f'qty_{prod.prodid}', 1)
                try:
                    qty = int(qty)
                except ValueError:
                    qty = 1
                OrderItem.objects.create(order=obj, product=prod, quantity=qty)
            return redirect('order_list')
    else:
        form = OrderForm(user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': 'Add Order', 'icon': 'bi-truck', 'list_url': 'order_list'})

@login_required
def supermarket_detail(request, pk):
    supermarket = get_object_or_404(Supermarket.objects.prefetch_related('sections'), pk=pk)
    employees = Employee.objects.filter(supermarket=supermarket).order_by('name')
    warehouses = Warehouse.objects.filter(supermarket=supermarket).order_by('wnumber')
    return render(
        request, 
        'supermarket_detail.html', 
        {
            'supermarket': supermarket, 
            'employees': employees, 
            'warehouses': warehouses
        }
    )

@login_required
def section_detail(request, pk):
    section = get_object_or_404(Section, pk=pk)
    products = Product.objects.filter(section_name=section).order_by('name')
    return render(
        request,
        'section_detail.html',
        {'section': section, 'products': products},
    )

@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee.objects.select_related('supermarket', 'supervisor'), pk=pk)
    subordinates = Employee.objects.filter(supervisor=employee).order_by('name')
    return render(
        request, 
        'employee_detail.html', 
        {'employee': employee, 'subordinates': subordinates}
    )

@login_required
def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related('section_name'),
        pk=pk,
    )
    stock_rows = (
        WareHStock.objects.filter(product=product)
        .select_related('warehouse', 'warehouse__supermarket')
        .order_by('warehouse__wnumber')
    )
    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'stock_rows': stock_rows,
        },
    )

@login_required
def warehouse_detail(request, pk):
    warehouse = get_object_or_404(
        Warehouse.objects.select_related('supermarket'),
        pk=pk,
    )
    stock_rows = (
        WareHStock.objects.filter(warehouse=warehouse)
        .select_related('product', 'product__section_name')
        .order_by('product__name')
    )
    return render(
        request,
        'warehouse_detail.html',
        {'warehouse': warehouse, 'stock_rows': stock_rows},
    )

@login_required
def distributor_detail(request, pk):
    distributor = get_object_or_404(Distributor, pk=pk)
    orders = Order.objects.filter(distributor=distributor).order_by('-ord_date')
    return render(
        request, 
        'distributor_detail.html', 
        {'distributor': distributor, 'orders': orders}
    )

@login_required
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    purchases = Purchase.objects.filter(client=client).order_by('-date')
    return render(
        request, 
        'client_detail.html', 
        {'client': client, 'purchases': purchases}
    )

@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase.objects.select_related('supermarket', 'client'), pk=pk)
    items = purchase.purchaseitem_set.select_related('product').all()
    return render(
        request, 
        'purchase_detail.html', 
        {'purchase': purchase, 'items': items}
    )

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related('supermarket', 'distributor'), pk=pk)
    items = order.orderitem_set.select_related('product').all()
    return render(
        request, 
        'order_detail.html', 
        {'order': order, 'items': items}
    )

@login_required
@permission_required('app.delete_supermarket', raise_exception=True)
def supermarket_delete(request, pk):
    supermarket = get_object_or_404(Supermarket, pk=pk)
    if request.method == 'POST':
        supermarket.delete()
        return redirect('supermarket_list')
    return render(request, 'generic_delete.html', {'item': supermarket, 'list_url': 'supermarket_list', 'item_name': f'Supermarket #{supermarket.id}'})

@login_required
@permission_required('app.delete_section', raise_exception=True)
def section_delete(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        section.delete()
        return redirect('section_list')
    return render(request, 'generic_delete.html', {'item': section, 'list_url': 'section_list', 'item_name': f'Section {section.sname}'})

@login_required
@permission_required('app.delete_employee', raise_exception=True)
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    # Prevent non-CEO users from deleting CEO employees
    is_ceo_user = request.user.groups.filter(name='CEO').exists()
    target_is_ceo = employee.groups.filter(name='CEO').exists()
    
    if target_is_ceo and not is_ceo_user:
        return render(request, '403.html', status=403)
    
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    return render(request, 'generic_delete.html', {'item': employee, 'list_url': 'employee_list', 'item_name': f'Employee {employee.name}'})

@login_required
@permission_required('app.delete_product', raise_exception=True)
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'generic_delete.html', {'item': product, 'list_url': 'product_list', 'item_name': f'Product {product.name}'})

@login_required
@permission_required('app.delete_warehouse', raise_exception=True)
def warehouse_delete(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        warehouse.delete()
        return redirect('warehouse_list')
    return render(request, 'generic_delete.html', {'item': warehouse, 'list_url': 'warehouse_list', 'item_name': f'Warehouse #{warehouse.wnumber}'})

@login_required
@permission_required('app.delete_distributor', raise_exception=True)
def distributor_delete(request, pk):
    distributor = get_object_or_404(Distributor, pk=pk)
    if request.method == 'POST':
        distributor.delete()
        return redirect('distributor_list')
    return render(request, 'generic_delete.html', {'item': distributor, 'list_url': 'distributor_list', 'item_name': f'Distributor {distributor.name}'})

@login_required
@permission_required('app.delete_client', raise_exception=True)
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('client_list')
    return render(request, 'generic_delete.html', {'item': client, 'list_url': 'client_list', 'item_name': f'Client {client.name}'})

@login_required
@permission_required('app.delete_purchase', raise_exception=True)
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        purchase.delete()
        return redirect('purchase_list')
    return render(request, 'generic_delete.html', {'item': purchase, 'list_url': 'purchase_list', 'item_name': f'Purchase #{purchase.purchid}'})

@login_required
@permission_required('app.delete_order', raise_exception=True)
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('order_list')
    return render(request, 'generic_delete.html', {'item': order, 'list_url': 'order_list', 'item_name': f'Order #{order.orderid}'})

@login_required
@permission_required('app.change_section', raise_exception=True)
def section_edit(request, pk):
    section = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        form = SectionForm(request.POST, is_editing=True)
        if form.is_valid():
            section.department = form.cleaned_data['department']
            section.save()
            return redirect('section_list')
    else:
        form = SectionForm(initial={'sname': section.sname, 'department': section.department}, is_editing=True)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Section: {section.sname}', 'icon': 'bi-tags', 'list_url': 'section_list'})

@login_required
@permission_required('app.change_supermarket', raise_exception=True)
def supermarket_edit(request, pk):
    supermarket = get_object_or_404(Supermarket, pk=pk)
    if request.method == 'POST':
        form = SupermarketForm(request.POST, is_editing=True)
        if form.is_valid():
            supermarket.location = form.cleaned_data['location']
            supermarket.opening_time = form.cleaned_data['opening_time']
            supermarket.close_time = form.cleaned_data['close_time']
            supermarket.save()
            sections = form.cleaned_data.get('sections')
            if sections:
                supermarket.sections.set(sections)
            return redirect('supermarket_list')
    else:
        form = SupermarketForm(initial={
            'id': supermarket.id,
            'location': supermarket.location,
            'opening_time': supermarket.opening_time,
            'close_time': supermarket.close_time,
            'sections': supermarket.sections.all()
        }, is_editing=True)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Supermarket: {supermarket.location}', 'icon': 'bi-shop', 'list_url': 'supermarket_list'})

@login_required
@permission_required('app.change_employee', raise_exception=True)
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    
    # Prevent non-CEO users from editing CEO employees
    is_ceo_user = request.user.groups.filter(name='CEO').exists()
    target_is_ceo = employee.groups.filter(name='CEO').exists()
    
    if target_is_ceo and not is_ceo_user:
        return render(request, '403.html', status=403)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, is_editing=True, user=request.user)
        if form.is_valid():
            employee.name = form.cleaned_data['name']
            employee.role = form.cleaned_data['role']
            employee.salary = form.cleaned_data['salary']
            employee.age = form.cleaned_data['age']
            employee.contact = form.cleaned_data['contact']
            employee.supermarket = form.cleaned_data['supermarket']
            employee.sex = form.cleaned_data['sex']
            employee.supervisor = form.cleaned_data['supervisor']
            group = form.cleaned_data.get('group')
            
            if group and group.name == 'CEO':
                employee.is_staff = True
                employee.is_superuser = True
            else:
                employee.is_staff = False
                employee.is_superuser = False
                
            if group:
                employee.groups.set([group])
            employee.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm(initial={
            'enumber': employee.enumber,
            'name': employee.name,
            'group': employee.groups.first() if employee.groups.exists() else None,
            'role': employee.role,
            'salary': employee.salary,
            'age': employee.age,
            'contact': employee.contact,
            'supermarket': employee.supermarket,
            'sex': employee.sex,
            'supervisor': employee.supervisor
        }, is_editing=True, user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Employee: {employee.name}', 'icon': 'bi-person-badge', 'list_url': 'employee_list'})

@login_required
@permission_required('app.change_product', raise_exception=True)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, is_editing=True)
        if form.is_valid():
            product.name = form.cleaned_data['name']
            product.brand = form.cleaned_data['brand']
            product.price = form.cleaned_data['price']
            product.req_cold = form.cleaned_data['req_cold']
            product.section_name = form.cleaned_data['section_name']
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm(initial={
            'prodid': product.prodid,
            'name': product.name,
            'brand': product.brand,
            'price': product.price,
            'req_cold': product.req_cold,
            'section_name': product.section_name
        }, is_editing=True)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Product: {product.name}', 'icon': 'bi-box-seam', 'list_url': 'product_list'})

@login_required
@permission_required('app.change_warehouse', raise_exception=True)
def warehouse_edit(request, pk):
    warehouse = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, is_editing=True, user=request.user)
        if form.is_valid():
            warehouse.area = form.cleaned_data['area']
            warehouse.supermarket = form.cleaned_data['supermarket']
            warehouse.save()
            products = form.cleaned_data.get('products', [])
            current_products = set(warehouse.products.all())
            new_products = set(products)
            # remove old prods
            for product in current_products - new_products:
                WareHStock.objects.filter(warehouse=warehouse, product=product).delete()
            # add new prods
            for product in new_products - current_products:
                WareHStock.objects.create(warehouse=warehouse, product=product, wqty=0)
            return redirect('warehouse_list')
    else:
        form = WarehouseForm(initial={
            'wnumber': warehouse.wnumber,
            'area': warehouse.area,
            'supermarket': warehouse.supermarket,
            'products': warehouse.products.all()
        }, is_editing=True, user=request.user)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Warehouse: {warehouse.wnumber}', 'icon': 'bi-boxes', 'list_url': 'warehouse_list'})

@login_required
@permission_required('app.change_distributor', raise_exception=True)
def distributor_edit(request, pk):
    distributor = get_object_or_404(Distributor, pk=pk)
    if request.method == 'POST':
        form = DistributorForm(request.POST, is_editing=True)
        if form.is_valid():
            distributor.name = form.cleaned_data['name']
            distributor.contact = form.cleaned_data['contact']
            distributor.save()
            return redirect('distributor_list')
    else:
        form = DistributorForm(initial={
            'email': distributor.email,
            'contact': distributor.contact,
            'name': distributor.name
        }, is_editing=True)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Distributor: {distributor.name}', 'icon': 'bi-building', 'list_url': 'distributor_list'})

@login_required
@permission_required('app.change_client', raise_exception=True)
def client_edit(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if request.method == 'POST':
        form = ClientForm(request.POST, is_editing=True, client_pk=client.nif)
        if form.is_valid():
            client.nif = form.cleaned_data['nif']
            client.name = form.cleaned_data['name']
            client.fidelity = form.cleaned_data['fidelity']
            client.address = form.cleaned_data['address']
            client.contact = form.cleaned_data['contact']
            client.save()
            return redirect('client_list')
    else:
        form = ClientForm(initial={
            'nif': client.nif,
            'name': client.name,
            'fidelity': client.fidelity,
            'address': client.address,
            'contact': client.contact
        }, is_editing=True, client_pk=client.nif)
    return render(request, 'generic_form.html', {'form': form, 'title': f'Edit Client: {client.name}', 'icon': 'bi-emoji-smile', 'list_url': 'client_list'})

@login_required
@permission_required('app.change_purchase', raise_exception=True)
def purchase_edit(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, is_editing=True, user=request.user)
        if form.is_valid():
            purchase.date = form.cleaned_data['date']
            purchase.supermarket = form.cleaned_data['supermarket']
            purchase.client = form.cleaned_data['client']
            purchase.save()
            products = form.cleaned_data.get('products', [])
            
            new_products = set(products)
            for product in new_products:
                # get quantity from POST data, default to 1 if not provided or invalid
                qty = request.POST.get(f'qty_{product.prodid}', 1)
                try:
                    qty = int(qty)
                except ValueError:
                    qty = 1
                PurchaseItem.objects.update_or_create(
                    purchase=purchase, 
                    product=product,
                    defaults={'quantity': qty, 'price_at_purchase': product.price}
                )
            PurchaseItem.objects.filter(purchase=purchase).exclude(product__in=new_products).delete()
            return redirect('purchase_list')
    else:
        form = PurchaseForm(initial={
            'purchid': purchase.purchid,
            'date': purchase.date,
            'supermarket': purchase.supermarket,
            'client': purchase.client,
            'products': purchase.products.all()
        }, is_editing=True, user=request.user)
    
    quantities = {item.product.prodid: item.quantity for item in purchase.purchaseitem_set.all()}
    return render(request, 'generic_form.html', {
        'form': form, 
        'title': f'Edit Purchase: #{purchase.purchid}', 
        'icon': 'bi-receipt', 
        'list_url': 'purchase_list',
        'initial_quantities': json.dumps(quantities)
    })

@login_required
@permission_required('app.change_order', raise_exception=True)
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, is_editing=True, user=request.user)
        if form.is_valid():
            order.ord_date = form.cleaned_data['ord_date']
            order.supermarket = form.cleaned_data['supermarket']
            order.distributor = form.cleaned_data['distributor']
            order.save()
            products = form.cleaned_data.get('products', [])
            new_products = set(products)
            for product in new_products:
                qty = request.POST.get(f'qty_{product.prodid}', 1)
                try:
                    qty = int(qty)
                except ValueError:
                    qty = 1
                
                OrderItem.objects.update_or_create(
                    order=order,
                    product=product,
                    defaults={'quantity': qty}
                )
            OrderItem.objects.filter(order=order).exclude(product__in=new_products).delete()
            return redirect('order_list')
    else:
        form = OrderForm(initial={
            'orderid': order.orderid,
            'ord_total': order.calculated_total,
            'ord_date': order.ord_date,
            'supermarket': order.supermarket,
            'distributor': order.distributor,
            'products': order.products.all()
        }, is_editing=True, user=request.user)
    
    quantities = {item.product.prodid: item.quantity for item in order.orderitem_set.all()}
    return render(request, 'generic_form.html', {
        'form': form, 
        'title': f'Edit Order: #{order.orderid}', 
        'icon': 'bi-truck', 
        'list_url': 'order_list',
        'initial_quantities': json.dumps(quantities)
    })
