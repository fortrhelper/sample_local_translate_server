@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
title NLLB Translation Server

echo Checking Python installation...
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8+ from Microsoft Store or python.org
    pause
    exit /b
)

if not exist venv (
    echo.
    echo [1/3] Creating virtual environment...
    python -m venv venv
)

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate

echo.
echo Checking/Installing dependencies...
python -m pip install -r requirements.txt
python -m pip install torch

if exist nllb-200-distilled-600M-int8 goto StartServer

:ModelSetup
echo.
echo [Model Check] Model folder 'nllb-200-distilled-600M-int8' not found.
echo.
echo To run the server, we need the model.
echo I can automatically download and convert 'facebook/nllb-200-distilled-600M' for you.
echo This verify you have internet access. This involves downloading ~1GB+ data.
echo.
echo Automatically starting download and conversion...

echo.
echo Converting model using Python script...
echo This step may take a few minutes depending on your internet speed.
echo.

python convert.py

if !errorlevel! neq 0 (
    echo.
    echo Error converting model! 
    echo Please ensure dependencies installed correctly.
    pause
    exit /b
)

:StartServer
echo.
echo [3/3] Starting Server...
echo Server will run at http://127.0.0.1:8000
echo Keep this window open while using the translation feature.
echo.
python server.py

pause
