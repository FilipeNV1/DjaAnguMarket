# Project 2 Plan - DjanGoMarket Angular + DRF

## Goal

Convert DjanGoMarket from a server-side-rendered Django app into a two-tier system:
- **Backend**: Django REST Framework (DRF) API with JWT authentication — lives in `django/`
- **Frontend**: Angular SPA consuming the REST API — lives in `angular/`

The existing Django templates/views are kept intact. The API layer is under `/api/`.

---

## Status

### DONE

- [x] `django/` subfolder structure (Django moved from repo root)
- [x] DRF installed and configured (settings.py: REST_FRAMEWORK, CORS, SIMPLE_JWT)
- [x] All serializers (`django/app/serializers.py`)
- [x] All ViewSets with CEO/non-CEO scoping (`django/app/api_views.py`)
- [x] JWT endpoints + `/api/me/` + DRF router (`django/DjanGoMarket/urls.py`)
- [x] Angular project scaffolded in `angular/` with `ng new`
- [x] Core: TypeScript models (interfaces matching DRF serializers)
- [x] Core: `AuthService` — login, logout, token storage, getCurrentUser
- [x] Core: `ApiService` — typed HTTP methods for all 9 entities
- [x] Core: `tokenInterceptor` — attaches Bearer token, handles 401 refresh
- [x] Core: `authGuard` — redirects to /login if not authenticated
- [x] Shared: `NavbarComponent` with role-aware links
- [x] Feature: login component
- [x] Feature: home dashboard
- [x] Feature: supermarkets — list, detail, form
- [x] Feature: sections — list, detail, form
- [x] Feature: employees — list, detail, form
- [x] Feature: products — list, detail, form
- [x] Feature: warehouses — list, detail, form
- [x] Feature: distributors — list, detail, form
- [x] Feature: clients — list, detail, form
- [x] Feature: purchases — list, detail, form (with item rows)
- [x] Feature: orders — list, detail, form (with item rows)

---

### TODO

#### Angular wiring (nothing works until this is done)

- [ ] **`angular/src/app/app.config.ts`** — add `provideHttpClient(withInterceptors([tokenInterceptor]))` so the token interceptor actually runs
- [ ] **`angular/src/app/app.routes.ts`** — define all routes (login, home, and all 9 entity routes) with `authGuard` on protected ones
- [ ] **`angular/src/app/app.ts`** — import and render `NavbarComponent` + `RouterOutlet`
- [ ] **`angular/src/app/app.html`** — replace default content with `<app-navbar>` + `<router-outlet>`
- [ ] **`angular/src/index.html`** — add Bootstrap CDN link so the UI doesn't look unstyled

#### Validation gaps (low priority, do after wiring)

- [ ] Supermarket form: close_time > opening_time (already in serializer, frontend check is a bonus)
- [ ] Purchase/Order form: at least one item required (already enforced in component, just verify)
- [ ] Employee form: salary min 0.01, age min 16 (Validators already added, just verify)

#### Deployment (last step)

- [ ] Add production Angular URL to `CORS_ALLOWED_ORIGINS` in `django/DjanGoMarket/settings.py`
- [ ] `ng build` output to serve statically or on a separate host

---

## How to run both together (dev)

### Terminal 1 — Django

```bash
cd django
source ../venv/bin/activate    # or wherever your venv lives
python3 manage.py runserver    # runs on http://localhost:8000
```

### Terminal 2 — Angular

```bash
cd angular
npm start                      # or: ng serve — runs on http://localhost:4200
```

Angular talks to Django at `http://localhost:8000/api/`.
Open `http://localhost:4200` in the browser.

Login with any employee number (e.g. `1000`) and password `password123`.

---

## File structure

```
DjanGoMarket/
  django/               <- Django backend
    manage.py
    app/
    DjanGoMarket/       <- settings, urls
    requirements.txt
    migrate.sh
    ...
  angular/              <- Angular frontend
    src/app/
      core/             <- models, services, interceptor, guard
      features/         <- one folder per entity (list/detail/form)
      shared/           <- navbar
    package.json
  .gitignore
  plan.md
```
