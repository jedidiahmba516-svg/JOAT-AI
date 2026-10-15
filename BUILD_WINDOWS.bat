@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"

echo.
echo ==============================================
echo   J.O.A.T. Beta 1 - Windows Release Builder
echo ==============================================
echo.

REM -------------------------------------------------
REM Find Python. Prefer the Python launcher if it exists,
REM otherwise use the normal "python" command.
REM This supports installations where Python 3.13 is
REM available as "python" but the "py" launcher is absent.
REM -------------------------------------------------
set "PYTHON_CMD="
where py >nul 2>&1
if not errorlevel 1 (
    py -3.13 -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3,13) else 1)" >nul 2>&1
    if not errorlevel 1 set "PYTHON_CMD=py -3.13"
)

if not defined PYTHON_CMD (
    where python >nul 2>&1
    if not errorlevel 1 (
        python -c "import sys; raise SystemExit(0 if sys.version_info[:2] == (3,13) else 1)" >nul 2>&1
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo ERROR: Python 3.13 was not found.
    echo.
    echo Run this command manually to check your installation:
    echo     python --version
    echo.
    goto :fail
)

for /f "delims=" %%V in ('%PYTHON_CMD% --version 2^>^&1') do echo Using %%V
for /f "delims=" %%E in ('%PYTHON_CMD% -c "import sys; print(sys.executable)"') do echo Python executable: %%E

echo.
echo [1/6] Preparing build folders...
if not exist "desktop_app.py" (
    echo ERROR: desktop_app.py was not found in this folder.
    goto :fail
)
if not exist "JOAT.spec" (
    echo ERROR: JOAT.spec was not found in this folder.
    goto :fail
)
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
mkdir "dist"
mkdir "dist\installer"


echo [2/6] Installing base build dependencies...
%PYTHON_CMD% -m pip install --upgrade pip
if errorlevel 1 goto :fail
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 goto :fail
%PYTHON_CMD% -m pip install pyinstaller
if errorlevel 1 goto :fail

echo [3/6] Checking local AI runtime...
%PYTHON_CMD% -c "import llama_cpp; print('llama-cpp-python: OK')" >nul 2>&1
if errorlevel 1 (
    echo llama-cpp-python is not installed. Installing a pre-built Windows CPU wheel...
    echo This build is configured to NEVER compile llama-cpp-python from source.
    %PYTHON_CMD% -m pip install --only-binary=llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu -r requirements-local-model.txt
    if errorlevel 1 (
        echo.
        echo ERROR: llama-cpp-python could not be installed automatically.
        echo A compatible pre-built Python 3.13 Windows wheel could not be installed.
        echo The builder intentionally refuses to compile llama-cpp-python from source.
        echo This avoids requiring the large Visual Studio C++ toolchain.
        echo.
        echo Your normal Python command is working, so Python itself is NOT the problem.
        goto :fail
    )
)
%PYTHON_CMD% -c "import llama_cpp; print('llama-cpp-python: OK')"
if errorlevel 1 goto :fail

echo [4/6] Building JOAT.exe with PyInstaller...
%PYTHON_CMD% -m PyInstaller --noconfirm --clean "JOAT.spec"
if errorlevel 1 goto :fail
if not exist "dist\JOAT.exe" (
    echo ERROR: PyInstaller finished but JOAT.exe was not created.
    goto :fail
)

for %%A in ("dist\JOAT.exe") do echo JOAT.exe created: %%~zA bytes

echo [5/6] Looking for Inno Setup 6...
set "ISCC="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not defined ISCC if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"

if not defined ISCC (
    echo.
    echo WARNING: Inno Setup 6 is not installed.
    echo JOAT.exe WAS successfully created.
    echo.
    echo Install Inno Setup 6, then run this same script again.
    echo It will reuse the project and create:
    echo     dist\installer\JOAT_Setup_1.0.0.exe
    echo.
    goto :app_only
)

echo [6/6] Building JOAT_Setup_1.0.0.exe...
"%ISCC%" "installer\JOAT.iss"
if errorlevel 1 goto :fail
if not exist "dist\installer\JOAT_Setup_1.0.0.exe" (
    echo ERROR: Inno Setup finished but the installer was not created.
    goto :fail
)

echo.
echo ==============================================
echo   J.O.A.T. WINDOWS BUILD COMPLETE
echo ==============================================
echo   App:       dist\JOAT.exe
echo   Installer: dist\installer\JOAT_Setup_1.0.0.exe
echo ==============================================
echo.
pause
exit /b 0

:app_only
echo ==============================================
echo   JOAT.exe BUILD COMPLETE
echo ==============================================
echo   App: dist\JOAT.exe
echo   Next: install Inno Setup 6 and run this file again.
echo ==============================================
echo.
pause
exit /b 0

:fail
echo.
echo ==============================================
echo   BUILD FAILED
echo ==============================================
echo Read the error above. The window will stay open.
echo ==============================================
echo.
pause
exit /b 1
