# DjanGoMarket API Reference

Base URL: `https://djangumarket.pythonanywhere.com/api`  
All endpoints except `/token/` and `/health/` require `Authorization: Bearer <access_token>`.

---

## Authentication

### Login
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"enumber": 1000, "password": "password123"}'
```

### Refresh token
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

### Health check
```bash
curl https://djangumarket.pythonanywhere.com/api/health/
```

---

## Current User

### Get profile
```bash
curl https://djangumarket.pythonanywhere.com/api/me/ \
  -H "Authorization: Bearer <access_token>"
```

### Update profile
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/me/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "New Name", "contact": "912345678", "age": 30, "sex": "M"}'
```

### Change password
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/me/password/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "password123", "new_password": "newpassword456"}'
```

---

## Supermarkets

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/supermarkets/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/supermarkets/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/supermarkets/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"location": "Aveiro", "opening_time": "08:00:00", "close_time": "22:00:00", "section_ids": ["Fruit", "Dairy"]}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/supermarkets/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"close_time": "23:00:00"}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/supermarkets/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Sections

Primary key: `sname` (string)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/sections/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/sections/Fruit/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/sections/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"sname": "Bakery", "department": "Food"}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/sections/Bakery/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"department": "Fresh Food"}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/sections/Bakery/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Employees

Primary key: `enumber` (integer)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/employees/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/employees/1001/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/employees/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Ana Silva", "role": "Cashier", "salary": 1200.00, "age": 25, "contact": "910000001", "supermarket": 1, "sex": "F", "supervisor": 1001, "is_active": true, "group_name": "Cashier"}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/employees/1010/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"salary": 1300.00, "group_name": "Manager"}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/employees/1010/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Products

Primary key: `prodid` (integer)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/products/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/products/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/products/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "Whole Milk", "brand": "Mimosa", "price": 0.89, "req_cold": true, "section_name": "Dairy"}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/products/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"price": 0.95}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/products/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Warehouses

Primary key: `wnumber` (integer)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/warehouses/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/warehouses/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/warehouses/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"area": 200, "supermarket": 1, "product_ids": [1, 2, 3]}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/warehouses/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"area": 250, "product_ids": [1, 2, 4]}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/warehouses/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Distributors

Primary key: `email` (string — URL-encode `@`)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/distributors/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl "https://djangumarket.pythonanywhere.com/api/distributors/supplier%40example.com/" \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/distributors/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "supplier@example.com", "name": "BestSupplier Lda", "contact": "220000001"}'
```

### Update
```bash
curl -X PATCH "https://djangumarket.pythonanywhere.com/api/distributors/supplier%40example.com/" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"contact": "220000002"}'
```

### Delete
```bash
curl -X DELETE "https://djangumarket.pythonanywhere.com/api/distributors/supplier%40example.com/" \
  -H "Authorization: Bearer <access_token>"
```

---

## Clients

Primary key: `nif` (integer)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/clients/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/clients/123456789/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/clients/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"nif": 123456789, "name": "João Costa", "fidelity": 0, "address": "Rua das Flores 1, Aveiro", "contact": "912345678"}'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/clients/123456789/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"fidelity": 150}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/clients/123456789/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Purchases

Primary key: `purchid` (integer, auto-assigned)

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/purchases/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/purchases/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/purchases/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "date": "2026-05-31",
    "supermarket": 1,
    "client": 123456789,
    "item_data": [
      {"product": 1, "quantity": 2},
      {"product": 3, "quantity": 1}
    ]
  }'
```

> `client` is optional — omit or set to `null` for anonymous purchases.

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/purchases/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"item_data": [{"product": 1, "quantity": 3}]}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/purchases/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Orders

Primary key: `orderid` (integer, auto-assigned)  
Items are priced at 60% of the product price (distributor discount).

### List
```bash
curl https://djangumarket.pythonanywhere.com/api/orders/ \
  -H "Authorization: Bearer <access_token>"
```

### Detail
```bash
curl https://djangumarket.pythonanywhere.com/api/orders/1/ \
  -H "Authorization: Bearer <access_token>"
```

### Create
```bash
curl -X POST https://djangumarket.pythonanywhere.com/api/orders/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "ord_date": "2026-05-31",
    "supermarket": 1,
    "distributor": "supplier@example.com",
    "item_data": [
      {"product": 1, "quantity": 10},
      {"product": 2, "quantity": 5}
    ]
  }'
```

### Update
```bash
curl -X PATCH https://djangumarket.pythonanywhere.com/api/orders/1/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"item_data": [{"product": 1, "quantity": 20}]}'
```

### Delete
```bash
curl -X DELETE https://djangumarket.pythonanywhere.com/api/orders/1/ \
  -H "Authorization: Bearer <access_token>"
```

---

## Search & Ordering

All list endpoints support `search` and `ordering` query parameters.

```bash
# Search employees by name
curl "https://djangumarket.pythonanywhere.com/api/employees/?search=Ana" \
  -H "Authorization: Bearer <access_token>"

# Order purchases by date descending
curl "https://djangumarket.pythonanywhere.com/api/purchases/?ordering=-date" \
  -H "Authorization: Bearer <access_token>"

# Search products and order by price
curl "https://djangumarket.pythonanywhere.com/api/products/?search=milk&ordering=price" \
  -H "Authorization: Bearer <access_token>"
```
