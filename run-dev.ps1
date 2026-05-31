Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd django; ..\\venv\\Scripts\\python.exe manage.py runserver'
Start-Process powershell -ArgumentList '-NoExit', '-Command', 'cd angular; npm start'
Write-Host 'Started Django on http://127.0.0.1:8000 and Angular on http://localhost:4200'