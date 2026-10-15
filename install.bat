@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo ==========================================
echo        J.O.A.T. - INSTALLER
echo ==========================================
echo.

set "PY="

REM Prefer the Python Launcher because it can find installed Python 3.x versions.
where py >nul 2>nul
if not errorlevel 1 set "PY=py -3"

REM Otherwise use the normal python command.
if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 set "PY=python"
)

REM Try common per-user/system Python 3.13 locations if PATH is not configured.
if not defined PY if exist "%LocalAppData%\Programs\Python\Python313\python.exe" set "PY="%LocalAppData%\Programs\Python\Python313\python.exe""
if not defined PY if exist "%ProgramFiles%\Python313\python.exe" set "PY="%ProgramFiles%\Python313\python.exe""
if not defined PY if exist "%ProgramFiles(x86)%\Python313\python.exe" set "PY="%ProgramFiles(x86)%\Python313\python.exe""

if not defined PY (
    echo Python was not found on this computer.
    echo.
    echo You said you have Python 3.13. If it is installed, make sure
    echo Python is available through the Python Launcher or PATH.
    echo.
    echo Test in Command Prompt with: python --version
    echo.
    pause
    exit /b 1
)

echo Python command: %PY%
%PY% --version
if errorlevel 1 (
    echo.
    echo The detected Python command could not be started.
    pause
    exit /b 1
)

REM Verify that the selected interpreter is Python 3.11 or newer.
%PY% -c "import sys; raise SystemExit(0 if sys.version_info >= (3,11) else 1)"
if errorlevel 1 (
    echo.
    echo J.O.A.T. requires Python 3.11 or newer.
    echo Python 3.13 is supported.
    echo.
    pause
    exit /b 1
)

echo.
echo Creating virtual environment...
if not exist ".venv\Scripts\python.exe" (
    %PY% -m venv .venv
    if errorlevel 1 (
        echo.
        echo Failed to create the virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Existing virtual environment found. Keeping it.
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate the virtual environment.
    pause
    exit /b 1
)

echo.
echo Updating pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo.
    echo pip update failed.
    pause
    exit /b 1
)

echo.
echo Installing J.O.A.T. dependencies...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Dependency installation failed.
    echo Check your internet connection and run install.bat again.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo J.O.A.T. installation complete!
echo ==========================================
echo.
echo Run start.bat to launch J.O.A.T.
echo.
pause
