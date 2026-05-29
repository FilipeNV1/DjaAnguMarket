# Relatório TP2 — DjanGoMarket (Angular + DRF)

> Rascunho para o relatório do 2.º trabalho prático. Completar com nomes do grupo e URLs finais de deploy.

---

## 1. Introdução

O **DjanGoMarket** é um sistema de gestão de supermercados desenvolvido no TP1 com Django e templates HTML. No **TP2**, a aplicação foi convertida para arquitetura **n-tier**:

- **Frontend**: Angular (SPA)
- **Backend**: Django REST Framework (API JSON)
- **Autenticação**: JWT (Simple JWT)
- **Deploy previsto**: API no PythonAnywhere, frontend no Heroku

---

## 2. Arquitetura

```
[Utilizador]
     |
     v
[Angular SPA]  ---- HTTP/JSON + Bearer token ---->  [Django + DRF]
     :4200 / Heroku                                      :8000 / PythonAnywhere
                                                              |
                                                              v
                                                         [SQLite]
```

O browser **não** recebe HTML gerado pelo Django para a UI principal. O Angular consome endpoints REST em `/api/`.

---

## 3. Tecnologias

| Camada | Tecnologias |
|--------|-------------|
| Frontend | Angular 21, Bootstrap 5, HttpClient, RxJS |
| Backend | Django, DRF, Simple JWT, django-cors-headers |
| BD | SQLite |
| Auth | Employee como user model, grupos CEO/Manager/Cashier/Employee |

---

## 4. API REST (endpoints principais)

Base: `http://localhost:8000/api/` (dev)

| Recurso | URL | Operações |
|---------|-----|-----------|
| Auth | `/api/token/`, `/api/token/refresh/`, `/api/me/` | Login JWT, refresh, perfil |
| Supermarkets | `/api/supermarkets/` | CRUD |
| Sections | `/api/sections/` | CRUD |
| Employees | `/api/employees/` | CRUD |
| Products | `/api/products/` | CRUD |
| Warehouses | `/api/warehouses/` | CRUD |
| Distributors | `/api/distributors/` | CRUD |
| Clients | `/api/clients/` | CRUD |
| Purchases | `/api/purchases/` | CRUD (+ items na leitura) |
| Orders | `/api/orders/` | CRUD (+ items na leitura) |

Todas as rotas (exceto token) exigem **JWT** no header: `Authorization: Bearer <access_token>`.

---

## 5. Autenticação e autorização

- Login: `POST /api/token/` com `{ "enumber": 1000, "password": "password123" }`
- O Angular guarda access/refresh tokens em `localStorage`
- Interceptor HTTP anexa o token e renova em caso de 401
- **CEO**: vê todos os supermercados e dados globais
- **Manager / outros**: queryset filtrado pelo supermercado do utilizador (ViewSets)
- Permissões Django (`DjangoModelPermissions`) por grupo

---

## 6. Frontend Angular

Estrutura em `angular/src/app/`:

- `core/` — models, ApiService, AuthService, guard, interceptor
- `features/` — um módulo por entidade (list, detail, form)
- `shared/` — navbar

Rotas protegidas com `authGuard`. API URL configurável em `src/environments/`.

---

## 7. Como executar localmente

Ver `plan.md` e secção TP2 do `README.md`.

Resumo:
1. `cd django` → instalar deps, migrate, populate, `runserver`
2. `cd angular` → `npm install`, `npm start`
3. Abrir http://localhost:4200

---

## 8. Deploy

### Backend (PythonAnywhere)
- App WSGI apontando para `django/DjanGoMarket/wsgi.py`
- `.env` com `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, `CORS_ALLOWED_ORIGINS`
- `collectstatic`, migrate, populate

### Frontend (Heroku)
- Root da app Heroku: pasta `angular/`
- Buildpack Node.js
- `Procfile` + `static.json` + `heroku-postbuild` (ng build)
- Atualizar `environment.prod.ts` com URL da API em produção
- Adicionar URL Heroku em `CORS_ALLOWED_ORIGINS` no Django

Guia passo a passo: **`docs/DEPLOY.md`**

---

## 9. Conclusões

### O que correu bem
- A separação **Angular + DRF** permitiu reutilizar os modelos Django do TP1 sem reescrever a lógica de negócio.
- **JWT com `enumber`** integra-se bem com o modelo `Employee` existente.
- Os **grupos Django** (CEO/Manager/Cashier/Employee) funcionam tanto na API (`DjangoModelPermissions`) como no frontend (navbar e botões condicionais).
- O monorepo (`django/` + `angular/`) facilita o trabalho em equipa na branch `angular`.

### Dificuldades
- **CORS** entre `localhost:4200` e `127.0.0.1:8000` — resolvido com `django-cors-headers`.
- **Change detection** no Angular 21 sem `zone.js` — resolvido adicionando `zone.js` e `provideZoneChangeDetection`.
- **Auth guard** com ecrã branco — resolvido usando `router.createUrlTree(['/login'])` em vez de `navigate` + `return false`.
- Listas vazias até pesquisar — bug de `.trim()` na pesquisa e falta de atualização da UI.

### Melhorias futuras
- Password change para employees (atualmente fixa `password123`).
- Paginação server-side nas listas grandes.
- Testes automatizados E2E (Cypress/Playwright).
- WebSockets para notificações em tempo real.

### URLs de deploy
*(Atualizar após deploy)*

| Serviço | URL |
|---------|-----|
| API (PythonAnywhere) | `https://DjanGoMarket.pythonanywhere.com/api` |
| Frontend (Heroku) | *(a definir)* |

Guia completo: **`docs/DEPLOY.md`**

---

## 10. Contas de teste

| Role | enumber | Password |
|------|---------|----------|
| CEO | 1000 | password123 |
| Manager | 1001 | password123 |
| Cashier | 1002 | password123 |
| Employee | 1005 | password123 |
