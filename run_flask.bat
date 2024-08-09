@echo off
REM Activate the virtual environment
call D:\xampp\htdocs\project\venv\Scripts\activate

REM Set Flask environment variables
set FLASK_APP=run.py
set FLASK_ENV=development

REM Run the Flask application
flask run
