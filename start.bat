@echo off
REM Set the name of the virtual environment directory
set VENV_DIR="venv"

REM Check if Python is installed
REM 'where python' checks if python.exe is in the PATH.
REM '>nul 2>nul' suppresses output, and '%errorlevel%' checks the command's success.
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo "Python could not be found. Please install Python (and ensure it's in your PATH)."
    exit /b 1
)

REM Create virtual environment if it doesn't exist
REM 'if not exist' checks for the directory.
if not exist %VENV_DIR% (
    echo "Creating virtual environment..."
    python -m venv %VENV_DIR%
)

REM Activate the virtual environment
REM 'call' is used to execute the activation script and return control to this batch file.
call %VENV_DIR%\Scripts\activate.bat

REM Upgrade pip
echo "Upgrading pip..."
REM Use 'python -m pip' to ensure the pip from the activated venv is used.
python -m pip install --upgrade pip

REM Install dependencies from requirements.txt
if exist "requirements.txt" (
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
) else (
    echo "Error: requirements.txt not found in the current directory!"
    exit /b 1
)

REM Run the FastAPI app using uvicorn
echo "Starting FastAPI app with uvicorn..."
REM Ensure uvicorn is installed in the venv (it will be if in requirements.txt)
uvicorn main:app --reload

REM Deactivate the virtual environment (optional, can be done manually later)
REM deactivate
