# DjanGoMarket - Supermarket Management System

## TP2 - Angular + Django REST Framework

This repository is a **monorepo** for Practical Work 2:

| Folder | Purpose |
|--------|---------|
| `django/` | Backend API (DRF) + legacy TP1 HTML views |
| `angular/` | Angular SPA (main UI for TP2) |

---

## Quick Start (Development)

**Backend** (terminal 1):
```bash
cd django
pip install -r requirements.txt
./make-env.sh          # generates .env with SECRET_KEY
./migrate.sh           # wipes migrations, recreates, applies
python3 setup_groups.py
python3 populate_db.py  # optional sample data
python3 manage.py runserver
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

**Windows**: double-click `run-dev.cmd` (opens 2 terminals) or `run-dev.ps1`. First-time setup: run `setup.cmd` or `setup.ps1`.

---

## Architecture

```
[Browser]
    |
    v
[Angular SPA :4200]  ── HTTP/JSON + Bearer token ──>  [Django + DRF :8000]
                                                             |
                                                             v
                                                         [SQLite]
```

The browser receives no Django-rendered HTML for the main UI. Angular consumes REST endpoints at `/api/`.

---

## API Endpoints

Base: `http://localhost:8000/api/` (dev)

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/token/` | Login `{enumber, password}` → JWT |
| POST | `/api/token/refresh/` | Refresh access token |
| GET | `/api/me/` | Current user profile + group + supermarket |
| * | `/api/supermarkets/` | CRUD |
| * | `/api/sections/` | CRUD |
| * | `/api/employees/` | CRUD |
| * | `/api/products/` | CRUD |
| * | `/api/warehouses/` | CRUD |
| * | `/api/distributors/` | CRUD |
| * | `/api/clients/` | CRUD |
| * | `/api/purchases/` | CRUD (items nested on read) |
| * | `/api/orders/` | CRUD (items nested on read) |

All routes except `/api/token/` require: `Authorization: Bearer <access_token>`.

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

## Main Features

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
  - Role-based filtering
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
- Permission-based view restrictions
- Employee login using dynamic username/password (username = employee number, password = `password123`)

---

## Access Information

### Deployed Application
- **Link**: djangomarket.pythonanywhere.com

### User Roles & Permissions

Our system uses Django's group-based permission system to control user access.

##### CEO (Admin)
- Full system access and control
- View all data across all supermarkets; full CRUD on all entities
- `is_staff=True`, can access admin panel
- **Data Scope:** Global - all supermarkets and data

##### Manager
- Supermarket-level management
- Full CRUD on employees, warehouses, purchases, orders within their supermarket
- Read-only on products, sections, distributors
- **Data Scope:** Limited to their assigned supermarket

##### Cashier
- Create purchases (point of sale transactions)
- View purchase history, products, orders
- **Data Scope:** Transaction-related data only

##### Employee
- View-only access to company data
- Cannot create, edit, or delete any records
- **Data Scope:** Limited to their supermarket (view-only)

### Demo Accounts

| Role | Username (enumber) | Password |
|------|-------------------|----------|
| CEO (Admin) | `1000` | `password123` |
| Manager | `1001` | `password123` |
| Cashier | `1002` | `password123` |
| Employee | `1005` | `password123` |

Any other employee ID (e.g., 1003) with password `password123` will also work.

---

## Configuration for Running Locally

### Prerequisites
- Python 3.8+
- Node.js 18+
- Virtual Environment (venv)
- Git

### Installation Steps

1. **Clone the project:**
```bash
git clone https://github.com/samuelvinhas/DjanGoMarket.git
cd DjanGoMarket
git checkout angular
```

2. **Backend setup:**
```bash
cd django
python3 -m venv ../venv && source ../venv/bin/activate
pip install -r requirements.txt
./make-env.sh
./migrate.sh
python3 setup_groups.py
python3 populate_db.py   # optional
python3 manage.py runserver
```

3. **Frontend setup (new terminal):**
```bash
cd angular
npm install
npm start
```

- Angular: http://localhost:4200
- Admin Panel: http://localhost:8000/admin/
- Legacy HTML views: http://localhost:8000/supermarkets/, /employees/, /products/, etc.

---

## Deploy

### Backend - PythonAnywhere

```bash
# On PythonAnywhere Bash console
git clone https://github.com/samuelvinhas/DjanGoMarket.git
cd DjanGoMarket && git checkout angular
mkvirtualenv --python=/usr/bin/python3.10 djangomarket
pip install -r django/requirements.txt
```

Create `django/.env`:
```env
SECRET_KEY=<strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=YOURUSER.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://YOUR-APP.herokuapp.com,http://localhost:4200
```

```bash
cd django
python manage.py migrate
python setup_groups.py
python populate_db.py
python manage.py collectstatic --noinput
```

**WSGI configuration file** (PythonAnywhere Web tab):
```python
import os, sys

path = '/home/YOURUSER/DjanGoMarket/django'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjanGoMarket.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static files** (Web tab): URL `/static/` → `/home/YOURUSER/DjanGoMarket/django/staticfiles`

### Frontend - Heroku

Update `angular/src/environments/environment.prod.ts`:
```typescript
export const environment = {
  production: true,
  apiUrl: 'https://YOURUSER.pythonanywhere.com/api',
};
```

```bash
cd angular
heroku login
heroku create djangomarket-frontend
git subtree push --prefix angular heroku main
```

After Heroku deploy, add the Heroku URL to `CORS_ALLOWED_ORIGINS` in the PythonAnywhere `.env` and reload the web app.

### Recommended deploy order
1. Deploy API to PythonAnywhere
2. Test `/api/token/` with Postman
3. Update `environment.prod.ts` with API URL
4. Deploy Angular to Heroku
5. Add Heroku URL to CORS in Django

### Common issues

| Problem | Solution |
|---------|---------|
| CORS error in browser | Add exact Heroku URL to `CORS_ALLOWED_ORIGINS` |
| 401 on all routes | Get token from `/api/token/` and send `Authorization: Bearer ...` header |
| Angular 404 on page refresh | `static.json` with `"/**": "index.html"` |
| `SECRET_KEY` missing | Create `django/.env` or set env vars on PythonAnywhere |
| WSGI import error | Verify `sys.path` points to `django/` folder |

---

## Conclusions

#### What Went Well
The Django framework made a lot of things easier than expected. The ORM let us focus on modeling the real-world relationships between entities without worrying too much about raw SQL. Setting up role-based access with Django Groups also turned out to be simpler than anticipated, and it gave the system a realistic feel - different users actually see and can do different things depending on their role.

The Angular + DRF split allowed us to reuse all Django models and business logic from TP1 without rewriting anything. JWT authentication integrates naturally with the `Employee` model.

#### Limitations
The biggest limitation is the default password setup for employees - obviously not something you'd ship in a real product, but as this was not the main focus of the project, we went with a simple approach.

#### What We'd Improve
Given more time, the most valuable addition would be password change functionality for employees. Better server-side pagination for large lists and automated E2E tests (Cypress/Playwright) would also be priorities.

#### Final Thoughts
Overall, DjanGoMarket does what it set out to do. Building a full supermarket management system and then converting it to a proper n-tier architecture was a great learning experience.

---
