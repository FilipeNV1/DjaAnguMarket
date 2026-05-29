@echo off
REM First-time setup for DjanGoMarket TP2 (Windows CMD)
cd /d "%~dp0"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r django\requirements.txt

cd django
if not exist .env (
    if exist .env.example copy .env.example .env
    if exist ..\.env copy ..\.env .env
)

python manage.py migrate
python setup_groups.py
python populate_db.py
cd ..

cd angular
call npm install
cd ..

python django\smoke_test.py
echo.
echo Setup complete. Run run-dev.cmd to start both servers.
