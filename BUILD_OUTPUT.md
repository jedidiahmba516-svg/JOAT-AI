# J.O.A.T. Beta 1 Windows Build

Run `BUILD_WINDOWS.bat` from the project folder on Windows.

The builder accepts either the Windows `py -3.13` launcher or the normal `python` command.

Expected outputs after a successful build:
- `dist\JOAT.exe`
- `dist\installer\JOAT_Setup_1.0.0.exe` (when Inno Setup 6 is installed)

If the installer is not built, install Inno Setup 6 and run `BUILD_WINDOWS.bat` again.
