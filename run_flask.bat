@echo off
REM Activate the virtual environment
call E:\Fix\FinalProject_Face_recognitions\venv\Scripts\activate

REM Set Flask environment variables
set FLASK_APP=run.py
set FLASK_ENV=development

REM Run the Flask application
flask run
