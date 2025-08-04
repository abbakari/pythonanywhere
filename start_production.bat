@echo off
REM Production startup script for Django IT Helpdesk
REM This script starts the application in production mode

echo Starting Django IT Helpdesk in Production Mode...

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Set production environment
set DJANGO_SETTINGS_MODULE=helpdesk.settings_production

REM Start Gunicorn server
echo Starting Gunicorn server...
gunicorn helpdesk.wsgi:application -c gunicorn.conf.py

pause
