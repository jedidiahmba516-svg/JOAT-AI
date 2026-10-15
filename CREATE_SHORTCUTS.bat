@echo off
setlocal
cd /d "%~dp0"

echo Creating J.O.A.T. shortcuts...

powershell -NoProfile -ExecutionPolicy Bypass -Command "$ws = New-Object -ComObject WScript.Shell; $root = '%~dp0'; $target = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source; if (-not $target) { $target = (Get-Command python.exe -ErrorAction SilentlyContinue).Source }; if (-not $target) { throw 'Python was not found in PATH.' }; $script = Join-Path $root 'desktop_app.py'; $icon = Join-Path $root 'joat.ico'; $desktop = [Environment]::GetFolderPath('Desktop'); $start = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs'; $folder = Join-Path $start 'J.O.A.T.'; New-Item -ItemType Directory -Force -Path $folder | Out-Null; foreach ($item in @(@{Path=(Join-Path $desktop 'J.O.A.T..lnk'); Desc='J.O.A.T. — Jack Of All Trades'}, @{Path=(Join-Path $folder 'J.O.A.T..lnk'); Desc='J.O.A.T. — Jack Of All Trades'})) { $sc = $ws.CreateShortcut($item.Path); $sc.TargetPath = $target; $sc.Arguments = '"' + $script + '"'; $sc.WorkingDirectory = $root; $sc.Description = $item.Desc; if (Test-Path $icon) { $sc.IconLocation = $icon + ',0' } else { $sc.IconLocation = $target + ',0' }; $sc.Save() }; Write-Host 'Desktop and Start Menu shortcuts created.'"

if errorlevel 1 (
    echo.
    echo Could not create the shortcuts automatically.
    echo Run this file again after confirming Python is installed and available in PATH.
    pause
    exit /b 1
)

echo.
echo Done! J.O.A.T. is now available from:
echo   - Your Desktop
echo   - Start Menu ^> J.O.A.T.
echo.
pause
