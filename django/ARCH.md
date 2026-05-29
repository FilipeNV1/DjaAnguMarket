# DjanGoMarket - System Architecture & Access Control

## Different User Roles & Permissions

Three primary access tiers: 
- **CEO**
- **Supermarket Manager**
- **Employee**

### 1. CEO (Global Admin)
* **Scope**: Entire system
* **Permissions**: Unrestricted Full CRUD (Create, Read, Update, Delete) across all endpoints and for all supermarkets

### 2. Supermarket Manager (Local Admin)
* **Scope**: Bound strictly to their assigned Supermarket
* **Permissions**:
  * **Supermarket (`/supermarkets`)**: Can **Edit** their own supermarket details. Cannot add or delete supermarkets.
  * **Employees (`/employees`)**: Full CRUD, but **limited** to employees belonging to their specific supermarket.
  * **Warehouses (`/warehouses`)**: Full CRUD, but only for warehouses tied to their specific supermarket.
  * **Purchases (`/purchases`)**: Full CRUD within their supermarket.
  * **Orders (`/orders`)**: Full CRUD within their supermarket.
  * **Products (`/products`)**: **Read-Only**. Products are global entities affecting all supermarkets.
  * **Distributors (`/distributors`)**: **Read-Only**. Distributors operate chain-wide.
  * **Sections (`/sections`)**: **Read-Only**. Section categorizations are standardized globally.
  * **Clients (`/clients`)**: **Read-Only** (or managed via backend scripts).

### 3. Base Employee
* **Scope**: Bound to their assigned Supermarket.
* **Permissions**: **Read-Only** access. Can view lists and details of entities relevant to their supermarket (products, their supermarket details, fellow employees) but cannot create, edit, or delete any records.

---

## UI Navigation Flow

The frontend follows a **Master-Detail View** pattern

1. **Master View (Resource Lists)**
   * Each endpoint renders a datatable/list of resources (e.g., `/employees` shows all employees)
   * Features: Column sorting, search/filtering, and quick action buttons (Edit/Delete) based on the user's permissions
2. **Detail View**
   * Clicking on any row (or specific ID) opens the specific details of that entity (`/employees/{id}`).
   * Displays all data associated with the record (e.g., clicking a Purchase shows the associated `PurchaseItem`s)
3. **Cross-Linking**
   * Entities are interlinked - For example, when viewing an `Employee`'s detail page, their associated `Supermarket` is rendered as a clickable link. Clicking it immediately navigates the user to that specific Supermarket's detail page

---

## Routing & Resource Endpoints

| Entity | List View (GET/POST) | Detail View (GET/PUT/DELETE) |
| :--- | :--- | :--- |
| **Sections** | `/sections` | `/sections/{id}` |
| **Supermarkets** | `/supermarkets` | `/supermarkets/{id}` |
| **Employees** | `/employees` | `/employees/{id}` |
| **Products** | `/products` | `/products/{id}` |
| **Warehouses** | `/warehouses` | `/warehouses/{id}` |
| **Distributors** | `/distributors` | `/distributors/{id}` |
| **Clients** | `/clients` | `/clients/{id}` |
| **Purchases** | `/purchases` | `/purchases/{id}` |
| **Orders** | `/orders` | `/orders/{id}` |

> **Note on Implementation:** When a Manager makes a `GET` request to `/employees`, the backend automatically filters the queryset (`Employee.objects.filter(supermarket=request.user.supermarket)`) so they only see their own staff, maintaining data privacy between distinct supermarkets