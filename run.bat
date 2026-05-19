@echo off
REM Smart Crop Health Monitor - Windows Launcher
REM This script activates the virtual environment and runs the Streamlit app

setlocal enabledelayedexpansion

echo.
echo ======================================
echo   SMART CROP HEALTH MONITOR
echo   Plant Disease Detection System
echo ======================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [!] Virtual environment not found!
    echo.
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [+] Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Check if requirements are installed
pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo [+] Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if model exists
if not exist "models\plant_model.h5" (
    echo.
    echo [!] Model not found at models\plant_model.h5
    echo.
    echo The model needs to be trained first. Would you like to train it now?
    echo This may take 30-60 minutes.
    echo.
    set /p train_choice="Train model now? (y/n): "
    
    if /i "!train_choice!"=="y" (
        echo.
        echo [+] Starting model training...
        python src\train.py
        if errorlevel 1 (
            echo [ERROR] Training failed
            pause
            exit /b 1
        )
    ) else (
        echo [!] Model training skipped. The app will not work without the model.
        echo Please run: python src\train.py
        pause
        exit /b 1
    )
)

REM Launch Streamlit app
echo.
echo [+] Launching Smart Crop Health Monitor...
echo [+] Opening browser at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app\app.py

pause
endlocal
