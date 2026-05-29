# Project 2 Plan - DjanGoMarket Angular + DRF

## Goal

Convert DjanGoMarket from a server-side-rendered Django app into a two-tier system:
- **Backend**: Django REST Framework (DRF) API with JWT authentication — lives in `django/`
- **Frontend**: Angular SPA consuming the REST API — lives in `angular/`

The existing Django templates/views are kept intact under `django/app/templates/` for reference (TP1).

---

## Status: DONE (dev)

- [x] Monorepo structure (`django/` + `angular/`)
- [x] DRF + JWT + CORS + role-scoped ViewSets
- [x] All serializers and API endpoints for 9 entities
- [x] Angular: models, ApiService, AuthService, interceptor, guard
- [x] Angular: login, home, list/detail/form for all entities
- [x] App wiring: routes, navbar, Bootstrap, HttpClient + interceptor
- [x] Environment files (`environment.ts` / `environment.prod.ts`)
- [x] Dev proxy (`angular/proxy.conf.json`) — Angular calls `/api` without CORS issues
- [x] Global UI theme (green navbar, brand buttons)
- [x] `setup.ps1` / `setup.cmd` + `django/smoke_test.py` for one-command local setup
- [x] API health endpoint `/api/health/`
- [x] Search/ordering on all ViewSets (`?search=`, `?ordering=`)
- [x] Role-based navbar and home (CEO/Manager/Cashier/Employee)
- [x] Loading/error states on all list pages
- [x] Cross-linking on detail pages (products, sections, purchases, orders, etc.)
- [x] Smoke tests for all 4 roles

---

## TODO (delivery)

- [ ] Deploy API to PythonAnywhere (update `CORS_ALLOWED_ORIGINS` with Heroku URL)
- [ ] Deploy Angular to Heroku (set `environment.prod.ts` apiUrl)
- [ ] Final TP2 report conclusions + group names in `docs/RELATORIO_TP2.md`

---

## How to run (dev)

### Backend
```bash
cd django
pip install -r requirements.txt
cp .env.example .env   # or use repo root .env
python manage.py migrate
python setup_groups.py
python populate_db.py
python manage.py runserver
```

### Frontend
```bash
cd angular
npm install
npm start
```

Open **http://localhost:4200** — login: employee `1000`, password `password123`.

Or on Windows: `.\run-dev.ps1`

---

## Architecture

```
Browser (Angular :4200)  --JWT JSON-->  Django DRF (:8000)  -->  SQLite
```
