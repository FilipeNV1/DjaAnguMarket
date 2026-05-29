@echo off
start "Django API" cmd /k "%~dp0run-django.cmd"
timeout /t 2 /nobreak >nul
start "Angular UI" cmd /k "%~dp0run-angular.cmd"
echo.
echo Django:  http://127.0.0.1:8000
echo Angular: http://localhost:4200
echo Login:   1000 / password123
