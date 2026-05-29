#!/usr/bin/env python
"""Smoke test for DjanGoMarket API — all roles (run from repo root)."""
import json
import os
import sys

import django

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjanGoMarket.settings')
django.setup()

from django.test import Client

client = Client()
ROLES = [
    ('CEO', 1000, {'products': 200, 'employees': 200, 'orders': 200}),
    ('Manager', 1001, {'products': 200, 'employees': 200, 'orders': 200}),
    ('Cashier', 1002, {'products': 200, 'purchases': 200, 'orders': 403}),
    ('Employee', 1005, {'products': 200, 'employees': 200, 'orders': 200}),
]

checks = []

health = client.get('/api/health/')
checks.append(('health', health.status_code == 200, health.status_code))

for role_name, enumber, endpoints in ROLES:
    token_resp = client.post(
        '/api/token/',
        data=json.dumps({'enumber': enumber, 'password': 'password123'}),
        content_type='application/json',
    )
    if token_resp.status_code != 200:
        checks.append((f'{role_name}/token', False, token_resp.status_code))
        continue
    checks.append((f'{role_name}/token', True, 200))
    auth = {'HTTP_AUTHORIZATION': f'Bearer {token_resp.json()["access"]}'}

    me = client.get('/api/me/', **auth)
    checks.append((f'{role_name}/me', me.status_code == 200, me.status_code))

    for endpoint, expected in endpoints.items():
        resp = client.get(f'/api/{endpoint}/', **auth)
        ok = resp.status_code == expected
        detail = resp.status_code if ok else f'{resp.status_code} (expected {expected})'
        checks.append((f'{role_name}/{endpoint}', ok, detail))

failed = [c for c in checks if not c[1]]
for name, ok, detail in checks:
    print(f"{'OK' if ok else 'FAIL'}  {name}: {detail}")

if failed:
    sys.exit(1)
print(f'\nAll {len(checks)} API smoke checks passed.')
