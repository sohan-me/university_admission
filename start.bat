@echo off
REM Set the name of the virtual environment directory
set VENV_DIR=venv

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python could not be found. Please install Python and ensure it's in your PATH.
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
call %VENV_DIR%\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
) else (
    echo Error: requirements.txt not found!
    exit /b 1
)

REM Run Aerich migrations
echo Running Aerich migrations...

REM Initialize Aerich if needed (only run once per project)
REM Uncomment the line below only if it's the first time
REM aerich init -t core.tortoise_config.TORTOISE_ORM

REM Generate migration file (if models changed)
aerich migrate

REM Apply migrations to the database
aerich upgrade

REM Start FastAPI app with uvicorn
echo Starting FastAPI app with uvicorn...
uvicorn main:app --reload

REM Optional: deactivate
REM deactivate
