@echo off
setlocal
cd /d "%~dp0"
title J.O.A.T. Launcher

python -c "import webview" >nul 2>&1
if errorlevel 1 (
    echo Installing the J.O.A.T. desktop window package...
    python -m pip install pywebview
    if errorlevel 1 (
        echo.
        echo Could not install pywebview.
        echo Run INSTALL_JOAT.bat as administrator if Windows blocks the install.
        pause
        exit /b 1
    )
)

echo Starting J.O.A.T....
start "" pythonw "%~dp0desktop_app.py"
exit /b 0
