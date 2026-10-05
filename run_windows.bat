@echo off
echo ==============================================
echo  Bilingual Stroop Experiment - Setup ^& Run
echo ==============================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python (3.9 to 3.11 recommended) from python.org and check "Add Python to PATH".
    pause
    exit /b
)

echo Setting up virtual environment (this may take a few seconds)...
if not exist ".venv" (
    python -m venv .venv
)

echo Activating virtual environment and installing dependencies...
call .venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Launching the experiment...
echo.
python run_experiment.py

echo.
pause
