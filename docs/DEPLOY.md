# Deploy — DjanGoMarket TP2

Guia para publicar **API (Django/DRF)** no PythonAnywhere e **frontend (Angular)** no Heroku.

---

## 1. PythonAnywhere (backend API)

### 1.1 Clonar / atualizar o repo

No Bash console do PythonAnywhere:

```bash
cd ~
git clone https://github.com/samuelvinhas/DjanGoMarket.git
cd DjanGoMarket
git checkout angular
```

### 1.2 Virtualenv e dependências

```bash
mkvirtualenv --python=/usr/bin/python3.10 djangomarket
workon djangomarket
pip install -r django/requirements.txt
```

### 1.3 Variáveis de ambiente

Criar `django/.env`:

```env
SECRET_KEY=<chave-secreta-forte>
DEBUG=False
ALLOWED_HOSTS=SEUUSER.pythonanywhere.com,djangomarket.pythonanywhere.com
CORS_ALLOWED_ORIGINS=https://SEU-APP.herokuapp.com,http://localhost:4200
```

### 1.4 Base de dados

```bash
cd ~/DjanGoMarket/django
python manage.py migrate
python setup_groups.py
python populate_db.py
python manage.py collectstatic --noinput
```

### 1.5 WSGI

No painel **Web** → **WSGI configuration file**, usar algo como:

```python
import os
import sys

path = '/home/SEUUSER/DjanGoMarket/django'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjanGoMarket.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Substituir `SEUUSER` pelo username PythonAnywhere.

### 1.6 Static files

Em **Web** → **Static files**:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/SEUUSER/DjanGoMarket/django/staticfiles` |

### 1.7 Testar

- `https://SEUUSER.pythonanywhere.com/api/` (com login JWT)
- `POST https://SEUUSER.pythonanywhere.com/api/token/`  
  Body: `{"enumber": 1000, "password": "password123"}`

---

## 2. Heroku (frontend Angular)

### 2.1 Preparar `environment.prod.ts`

Em `angular/src/environments/environment.prod.ts`:

```typescript
export const environment = {
  production: true,
  apiUrl: 'https://SEUUSER.pythonanywhere.com/api',
};
```

### 2.2 Deploy

```bash
cd angular
heroku login
heroku create djangomarket-frontend   # nome livre
git subtree push --prefix angular heroku main
# ou: deploy só a pasta angular como repo separado
```

O projeto já inclui:
- `Procfile` → serve SPA em `$PORT`
- `static.json` → routing SPA (todas as rotas → index.html)
- `heroku-postbuild` → `ng build`

### 2.3 Buildpack

Heroku deve detetar **Node.js** automaticamente (`package.json` na raiz de `angular/`).

Se fizeres deploy da pasta `angular` como root do Heroku app, está correto.

### 2.4 CORS

Depois do deploy Heroku, copia a URL (ex. `https://djangomarket-frontend.herokuapp.com`) para `CORS_ALLOWED_ORIGINS` no `.env` do PythonAnywhere e reinicia a web app.

---

## 3. Ordem recomendada

1. Deploy **API** no PythonAnywhere  
2. Testar `/api/token/` e `/api/products/` com Postman  
3. Atualizar `environment.prod.ts` com URL da API  
4. Deploy **Angular** no Heroku  
5. Adicionar URL Heroku ao CORS no Django  
6. Testar login no browser (Heroku → API)

---

## 4. Contas de teste

| Role | enumber | password |
|------|---------|----------|
| CEO | 1000 | password123 |
| Manager | 1001 | password123 |
| Cashier | 1002 | password123 |
| Employee | 1005 | password123 |

---

## 5. Problemas comuns

| Problema | Solução |
|----------|---------|
| CORS error no browser | Adicionar URL exacta do Heroku em `CORS_ALLOWED_ORIGINS` |
| 401 em todas as rotas | Obter token em `/api/token/` e enviar header `Authorization: Bearer ...` |
| Angular 404 ao refrescar página | `static.json` com `"/**": "index.html"` |
| `SECRET_KEY` missing | Criar `django/.env` ou variáveis no PA |
| WSGI import error | Verificar `sys.path` aponta para pasta `django/` |
