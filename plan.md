# Project 2 Plan - DjanGoMarket Angular + DRF

## Goal

Convert DjanGoMarket from a server-side-rendered Django app into a two-tier system:
- **Backend**: Django REST Framework (DRF) API with JWT authentication
- **Frontend**: Angular SPA consuming the REST API

The existing Django templates/views are kept intact and untouched. The new API layer is added alongside them under the `/api/` prefix.

---

## Phase 1 - DRF Backend

### 1.1 Install & configure

```
pip install djangorestframework djangorestframework-simplejwt django-cors-headers
```

Update `requirements.txt`.

**`DjanGoMarket/settings.py` changes:**
- Add to `INSTALLED_APPS`: `rest_framework`, `rest_framework_simplejwt`, `corsheaders`
- Add `corsheaders.middleware.CorsMiddleware` at the top of `MIDDLEWARE`
- Add DRF config block (default auth classes → JWTAuthentication, default permission → IsAuthenticated)
- Add `CORS_ALLOWED_ORIGINS` with `http://localhost:4200`
- Add `SIMPLE_JWT` config (access token lifetime, refresh token lifetime)

### 1.2 Serializers - `app/serializers.py` (new file)

One serializer per model. All 11 models need coverage:
`Section`, `Supermarket`, `Employee`, `Product`, `Warehouse`, `Distributor`, `Client`, `Purchase`, `PurchaseItem`, `WareHStock`, `Order`, `OrderItem`

Key decisions:
- `EmployeeSerializer` must **never** expose `password`. Use `extra_kwargs = {'password': {'write_only': True}}` or exclude entirely.
- `PurchaseSerializer` and `OrderSerializer` should include nested items read-only (`PurchaseItemSerializer`, `OrderItemSerializer`) for detail views. Use separate write serializers or a `write_only`/`read_only` split.
- `PurchaseSerializer` should include `calculated_total` as a read-only field (it's a `@property` on the model).
- `OrderSerializer` same for `calculated_total`.
- `EmployeeSerializer` should include the user's group name as a read-only field.

### 1.3 ViewSets - `app/api_views.py` (new file)

Use `ModelViewSet` for all 9 entities. Row-level filtering mirrors the existing `views.py` logic:

| Entity | CEO scope | Non-CEO scope |
|---|---|---|
| Supermarket | all | own supermarket only |
| Employee | all | own supermarket only |
| Warehouse | all | own supermarket only |
| Order | all | own supermarket only |
| Purchase | all | own supermarket only |
| Section | all | all (global) |
| Product | all | all (global) |
| Distributor | all | all (global) |
| Client | all | all (global) |

Override `get_queryset()` on each ViewSet. Reuse the `request.user.groups.filter(name='CEO').exists()` pattern already used in `views.py`.

Write permission enforcement via `get_permissions()` per action:
- `list`, `retrieve` → IsAuthenticated
- `create`, `update`, `partial_update`, `destroy` → map to the same DRF model-level permissions already set by `setup_groups.py`

Add a `/api/me/` endpoint (simple `RetrieveAPIView`) returning the current user's data (enumber, name, group, supermarket).

### 1.4 URLs - `DjanGoMarket/urls.py`

Register a DRF router. Mount it under `/api/`. Keep all existing Django view URLs untouched.

```
/api/token/          → JWT obtain
/api/token/refresh/  → JWT refresh
/api/me/             → current user info
/api/supermarkets/   → SupermarketViewSet
/api/sections/       → SectionViewSet
/api/employees/      → EmployeeViewSet
/api/products/       → ProductViewSet
/api/warehouses/     → WarehouseViewSet
/api/distributors/   → DistributorViewSet
/api/clients/        → ClientViewSet
/api/purchases/      → PurchaseViewSet
/api/orders/         → OrderViewSet
```

**Important**: JWT login uses `enumber` as username (Django's `USERNAME_FIELD = 'enumber'`). The default `TokenObtainPairView` works because DRF simplejwt reads `USERNAME_FIELD` from `AUTH_USER_MODEL`. No custom token view is needed.

---

## Phase 2 - Angular Frontend

### 2.1 Initialize project

```
ng new frontend --routing --style=css
```

Run from the repo root so the Angular project lives at `frontend/`. The `frontend/node_modules/` directory must be in `.gitignore`.

### 2.2 Project structure

```
frontend/src/app/
  core/
    services/
      api.service.ts       # base HTTP wrapper (get/post/put/patch/delete)
      auth.service.ts      # login, logout, token storage, current user
    interceptors/
      token.interceptor.ts # attaches Bearer token to every request
    guards/
      auth.guard.ts        # redirect to /login if not authenticated
    models/                # TypeScript interfaces matching DRF serializers
  features/
    auth/
      login/
    supermarkets/
      supermarket-list / supermarket-detail / supermarket-form
    sections/
      section-list / section-detail / section-form
    employees/
      employee-list / employee-detail / employee-form
    products/
      product-list / product-detail / product-form
    warehouses/
      warehouse-list / warehouse-detail / warehouse-form
    distributors/
      distributor-list / distributor-detail / distributor-form
    clients/
      client-list / client-detail / client-form
    purchases/
      purchase-list / purchase-detail / purchase-form
    orders/
      order-list / order-detail / order-form
    home/
  shared/
    components/            # navbar, confirm-dialog, etc.
```

### 2.3 Core: auth & HTTP

**`auth.service.ts`**
- `login(enumber, password)` → POST `/api/token/` → store access + refresh tokens in `localStorage`
- `logout()` → clear tokens
- `getAccessToken()` → return stored token
- `getCurrentUser()` → GET `/api/me/` (cache result)
- `isLoggedIn()`, `getUserGroup()` helpers

**`token.interceptor.ts`**
- Attach `Authorization: Bearer <token>` header to every outgoing request
- On 401, attempt token refresh via `/api/token/refresh/`; on refresh failure, logout + redirect to `/login`

**`api.service.ts`**
- Typed wrappers around `HttpClient` pointing at `http://localhost:8000/api/`
- One method per resource: `getSupermarkets()`, `createEmployee(data)`, etc.

**`auth.guard.ts`**
- Protect all routes except `/login`

### 2.4 Models (TypeScript interfaces)

Create interfaces in `core/models/` matching the DRF serializer shapes. Example: `Employee`, `Supermarket`, `Product`, `Purchase`, `PurchaseItem`, `Order`, `OrderItem`, etc.

### 2.5 Feature components

Each feature follows the same pattern:

**List component**
- On `ngOnInit`, fetch list via `ApiService`
- Display in a table with search/filter input
- Show Edit / Delete buttons only if user has permission (check group via `AuthService`)
- Delete triggers a confirm dialog, then calls `ApiService.delete*()`

**Detail component**
- Fetch single record + related data (e.g. purchase items, warehouse stock)
- Read-only display with a link back to the list

**Form component (create + edit)**
- `FormGroup` with `FormControl` and `Validators` mirroring backend validation
- Reused for both create and edit: pre-populate fields when `id` param is present in route
- On submit: call `create*()` or `update*()`; navigate to list on success
- Key validations to replicate from `forms.py`:
  - Supermarket: `close_time > opening_time`
  - Section: duplicate `sname` check (async validator via API)
  - Distributor: duplicate `email` check (async validator)
  - Client: duplicate `nif` check (async validator)
  - Purchase / Order: at least one product required
  - Salary: min 0.01, Age: min 16
  - Fidelity: min 0

### 2.6 Role-based UI

Use `AuthService.getUserGroup()` to hide/show buttons per component:
- Edit/Delete buttons: hidden for Employee group
- Create buttons: hidden for Employee and Cashier groups on restricted entities
- Cashier: only sees Purchases (create) + view access elsewhere

### 2.7 Routing

```
/login              → LoginComponent (unauthenticated)
/                   → HomeComponent (authGuard)
/supermarkets       → SupermarketListComponent
/supermarkets/:id   → SupermarketDetailComponent
/supermarkets/new   → SupermarketFormComponent
/supermarkets/:id/edit → SupermarketFormComponent
... (same pattern for all entities)
```

---

## Phase 3 - .gitignore updates

Add to `.gitignore`:
```
frontend/node_modules/
frontend/dist/
frontend/.angular/
```

---

## Phase 4 - Wiring & Testing

- Confirm JWT login works with `enumber` as username field
- Test each ViewSet endpoint via curl or DRF browsable API
- Test Angular auth flow end-to-end (login → token stored → interceptor attaches → API calls work → logout clears)
- Test role-based filtering (Manager only sees their supermarket's data)
- Test form validations on the Angular side match backend rejections

---

## Open Decisions / To Confirm

1. **Nested writes**: Purchase and Order creation requires creating items (PurchaseItem, OrderItem) atomically. Decide between: (a) separate `/api/purchases/{id}/items/` nested endpoints, or (b) writable nested serializers with `create()` override. Option (b) is simpler and matches the existing `views.py` pattern.

2. **Stock signal on OrderItem**: The `post_save` signal updates WareHStock automatically on the backend. The Angular form does not need to handle this - it just creates an Order with items and the backend handles the rest.

3. **Employee creation from Angular**: Must follow the same logic as `views.py` - set `username = str(enumber)` and `password = make_password('password123')` after creation. This needs to be in the `EmployeeViewSet.perform_create()` override, not on the frontend.

4. **Deployment**: Backend stays on pythonanywhere.com. Angular `ng build` output (`dist/`) can be deployed separately. API `CORS_ALLOWED_ORIGINS` will need to include the production Angular URL before deployment.
