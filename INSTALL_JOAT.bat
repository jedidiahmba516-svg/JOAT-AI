@echo off
cd /d "%~dp0"
title Install J.O.A.T.
echo Installing J.O.A.T. requirements...
python -m pip install -r requirements.txt
if errorlevel 1 (echo. & echo Installation failed. & pause & exit /b 1)

echo.
echo Creating J.O.A.T. shortcuts...
call "%~dp0CREATE_SHORTCUTS.bat"
if errorlevel 1 exit /b 1

echo.
echo J.O.A.T. installation complete.
echo You can now launch J.O.A.T. from the Desktop or Start Menu.
pause
