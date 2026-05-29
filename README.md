# DjanGoMarket - Supermarket Management System

## TP2 — Angular + Django REST Framework (current)

This repository is a **monorepo** for Practical Work 2:

| Folder | Purpose |
|--------|---------|
| `django/` | Backend API (DRF) + legacy TP1 HTML views |
| `angular/` | Angular SPA (main UI for TP2) |

### Quick start (development)

**Backend** (terminal 1):
```bash
cd django
pip install -r requirements.txt
cp .env.example .env          # or use .env at repo root
python manage.py migrate
python setup_groups.py
python populate_db.py
python manage.py runserver
```

**Frontend** (terminal 2):
```bash
cd angular
npm install
npm start
```

- Angular UI: http://localhost:4200  
- API: http://localhost:8000/api/  
- Login: employee `1000`, password `password123`

Windows: double-click **`run-dev.cmd`** (opens 2 terminals — no PowerShell policy needed)

First-time setup: double-click **`setup.cmd`** or run `setup.ps1`

More: `plan.md`, `docs/RELATORIO_TP2.md`, `docs/DEPLOY.md`

---

## Introduction (TP1)

DjanGoMarket is a web-based information system developed to help manage supermarket operations. Our system is built using **Django** platform and uses **SQLite** as the database backend with Django's Object-Relational Mapping (ORM) system. 

Our application serves as a hub for managing supermarket operations including:
- Employee and personnel management
- Product inventory and warehouse organization
- Customer purchases and transactions
- Supplier/Distributor relationships
- Store locations and section management

---

## Main Features of our App

### 1. Data Model & Database Management
- Relational database with 11 interconnected models
- **Implemented Models:**
  - `Supermarket` - Store locations with opening/closing times
  - `Section` - Product sections/departments
  - `Employee` - Staff management with roles, hierarchy (supervisor relationships), and salary tracking
  - `Product` - Product catalog with pricing and temperature requirements
  - `Warehouse` - Inventory storage locations
  - `Distributor` - Supplier information
  - `Client` - Customer data with fidelity program tracking
  - `Purchase` - Transaction management with multiple payment methods
  - `Order` - Supermarket orders with discounted pricing
  - Additional junction models for M:N relationships with attributes

### 2. Django Admin Interface
- Admin panel for CRUD operations on all models
- Data validation and constraints enforced at model level
- Pre-populated sample data available via `populate_db.py`

### 3. Form System
- Django forms for all main entities with custom validation
- **Implemented Forms:**
  - `SupermarketForm` - Manage store locations and sections
  - `SectionForm` - Create/edit product sections
  - `EmployeeForm` - Employee management with role assignment
  - `ProductForm` - Product catalog management
  - `WarehouseForm` - Warehouse and inventory management
  - `DistributorForm` - Supplier/distributor information
  - `ClientForm` - Customer management
  - `PurchaseForm` - Transaction management with product selection
  - `OrderForm` - Order management with discounted pricing (60% of original)
- Custom field types for enhanced product display with pricing
- Form validation with duplicate checking and data constraints

### 4. User Views & Templates
- **List Views**: Display all instances of each entity with search bar filtering
  - Supermarket, Section, Employee, Product, Warehouse, Distributor, Client, Purchase, Order
  - Role-based filtering (more details below)
- **Create Views**: Form-based creation with permission decorators
  - All entities use generic form template (`generic_form.html`)
  - Automatic permission validation based on user group
- **Detail Views**: Detailed information display for each entity
  - Related data display (e.g., products in sections, stock in warehouses)
  - Special views for complex entities (Product shows warehouse stock, Purchase shows items)
- **Edit/Delete Views**: Manage and remove existing records

### 5. User Authentication & Authorization
- Django authentication system with role-based access control
- **Django Groups System:**
  - CEO - Full system access
  - Manager - Supermarket-level management
  - Cashier - Transaction and sales operations
  - Employee - View-only access for assigned supermarket
- Permission-based view restrictions using `@permission_required` decorators
- Employee login using dynamic username/password (username = employee number, password = 'password123')

---

## Access Information

### Deployed Application
- **Link**: djangomarket.pythonanywhere.com

### User Authentication Information

#### User Roles & Permissions

Our system uses Django's group-based permission system to control user access. <br> 
Here's a breakdown of each role:

##### 1. CEO (Admin)
- **Full system access and control**
- Permissions:
  - View all data across all supermarkets
  - Create, edit, delete supermarkets
  - Create, edit, delete sections globally
  - Manage all employees across all supermarkets
  - Create, edit, delete products
  - Manage all warehouses
  - Create, edit, delete distributors
  - Manage all clients
  - View and manage all purchases
  - View and manage all orders
- **Access Level:** `is_staff=True`, can access admin panel
- **Data Scope:** Global - all supermarkets and data

##### 2. Manager
- **Supermarket-level management**
- Permissions:
  - View supermarket assigned to them
  - Create and manage employees within their supermarket
  - View and manage employees
  - Create, edit, delete warehouse records for their supermarket
  - Create and manage purchases
  - Create and manage orders
  - View products and sections (company-wide)
- **Access Level:** Regular user, no admin panel access
- **Data Scope:** Limited to their assigned supermarket

##### 3. Cashier
- **Sales and transaction operations**
- Permissions:
  - Create purchases (point of sale transactions)
  - View purchase history
  - View product and pricing information
  - View orders
- **Access Level:** Regular user, limited view access
- **Data Scope:** Transaction-related data only

##### 4. Employee
- **View-only access**
- Permissions:
  - View-only access to company data
  - Cannot create, edit, or delete any records
  - Can view products, employees, warehouses, etc. in read-only mode
- **Access Level:** Regular user, no modification rights
- **Data Scope:** Limited to their supermarket (view-only)

#### Demo Accounts

All employees have accounts created. The following are example accounts for each role:

| Role | Username | Password | ID |
|------|----------|----------|-----|
| CEO (Admin) | `1000` | `password123` | 1000 |
| Manager | `1001` | `password123` | 1001 |
| Cashier | `1002` | `password123` | 1002 |
| Employee | `1005` | `password123` | 1005 |

**Note**: Any other employee ID (e.g., 1003) with password `password123` will also work. You can create additional employees through the system and an account will be automatically generated for them with the same password.

---

## Configuration for Running Locally

### Prerequisites
- Python 3.8+
- Virtual Environment (venv)
- Git

### Installation Steps

1. **Clone/Navigate to the project:**
```bash
git clone https://github.com/samuelvinhas/DjanGoMarket.git
cd DjanGoMarket
```

2. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Setup Environment Variables:**
```bash
chmod +x make-env.sh
./make-env.sh
```
This script generates a random Django `SECRET_KEY` and creates a `.env` file with required environment variables.

5. **Apply Database Migrations:**
```bash
chmod +x migrate.sh
./migrate.sh
```

5. **Configure Groups:**
```bash
python3 setup_groups.py
```

6. **Populate Database with Data (Optional):**
```bash
python3 populate_db.py
```

7. **Run Development Server:**
```bash
python3 manage.py runserver
```
- Access: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Supermarket Management: http://localhost:8000/supermarkets/
- Employee Management: http://localhost:8000/employees/
- Product Management: http://localhost:8000/products/
- Warehouse Management: http://localhost:8000/warehouses/
- Purchase Management: http://localhost:8000/purchases/
- Orders Management: http://localhost:8000/orders/
- Section Management: http://localhost:8000/sections/
- Distributor Management: http://localhost:8000/distributors/
- Client Management: http://localhost:8000/clients/

**Attention**: More urls are available, for example http://localhost:8000/supermarkets/1/, every "item" has a detail page, so you can access http://localhost:8000/supermarkets/2/ and so on, the same applies to employees, products, warehouses, purchases, orders, sections, distributors and clients.

---

## Conclusions

#### What Went Well
The Django framework made a lot of things easier than expected. The ORM let us focus on modeling the real-world relationships between entities without worrying too much about raw SQL. 
Setting up role-based access with Django Groups also turned out to be simpler than anticipated, and it gave the system a realistic feel - different users actually see and can do different things depending on their role.

#### Limitations
The biggest limitation is the default password setup for employees. Is obviously not something you'd ship in a real product but as this was not the main focus of the project, we went with a simple approach.

#### What We'd Improve
Given more time, the most valuable addition would probably be adding the change password functionality for employees. Besides that, if the system had lots of sections and products, the product listing pages could get unwieldy, so implementing better filtering and search capabilities would be a priority.

#### Final Thoughts
Overall, DjanGoMarket does what it set out to do. Making this project was a great experience and we believed that the final work was successful. Building a full supermarket management system from scratch using Django wasn't always straightforward, but the end result made us proud of what we accomplished.

---
