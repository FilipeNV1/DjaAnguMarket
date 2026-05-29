# TP2 — API REST (DjanGoMarket)

Resumo técnico da API Django REST Framework no monorepo (`django/`).

---

## Estrutura

```
django/
  app/serializers.py   → JSON ↔ modelos
  app/api_views.py     → ViewSets + /api/me/
  app/jwt_views.py     → login JWT com enumber
  DjanGoMarket/urls.py → router + /api/token/
```

Frontend Angular em `angular/` consome `http://localhost:8000/api` (dev).

---

## Endpoints

| Método | URL | Descrição |
|--------|-----|-----------|
| POST | `/api/token/` | Login `{enumber, password}` → JWT |
| POST | `/api/token/refresh/` | Renovar access token |
| GET | `/api/me/` | Perfil + grupo + supermercado |
| * | `/api/supermarkets/` … `/api/orders/` | CRUD das 9 entidades |

Todas as rotas (exceto token) exigem header `Authorization: Bearer <token>`.

---

## Autenticação

- Modelo: `Employee` (`AUTH_USER_MODEL`)
- JWT via `djangorestframework-simplejwt`
- Login Angular envia `enumber` + `password`
- Permissões: `IsAuthenticated` + `DjangoModelPermissions`
- CEO vê tudo; outros roles filtrados por supermercado nos ViewSets

---

## CORS

Configurado em `settings.py` via `CORS_ALLOWED_ORIGINS` (env). Dev: `http://localhost:4200`.

---

## Como testar

```bash
cd django
python manage.py runserver
```

- Browser: http://127.0.0.1:8000/api/ (DRF browsable, precisa token)
- Login: POST http://127.0.0.1:8000/api/token/  
  `{"enumber": 1000, "password": "password123"}`

---

## Deploy

Ver `docs/DEPLOY.md`.
