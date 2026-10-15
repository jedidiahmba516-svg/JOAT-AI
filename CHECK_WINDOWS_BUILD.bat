@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo J.O.A.T. Windows Build Prerequisite Check
echo ==============================================
echo.
where python >nul 2>&1
if errorlevel 1 (
  echo [FAIL] Python command not found.
  goto end
)
python --version
echo.
python -c "import sys,struct; print('Python executable:', sys.executable); print('Architecture:', struct.calcsize('P')*8, 'bit'); raise SystemExit(0 if sys.version_info[:2] == (3,13) and struct.calcsize('P')*8 == 64 else 1)"
if errorlevel 1 echo [WARN] J.O.A.T. Beta 1 expects Python 3.13 x64.
where iscc >nul 2>&1
if not errorlevel 1 echo [OK] Inno Setup is available on PATH.
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" echo [OK] Inno Setup 6 detected.
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" echo [OK] Inno Setup 6 detected.
echo.
echo This check does not install anything.
:end
pause
