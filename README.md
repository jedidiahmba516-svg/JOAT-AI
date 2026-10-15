# J.O.A.T. — Jack Of All Trades

**Beta 1 — local-first Windows desktop AI assistant**

## What this build adds
- User-supplied local GGUF model support via optional `llama-cpp-python`.
- Full settings screen for model, personality, voice, privacy, and permissions.
- Existing memory, research, tools, tasks, goals, agent planning, webpage/image intake, diagnostics, app discovery, and personality systems remain included.
- Windows EXE build with icon and version metadata.
- Inno Setup installer with Terms of Service acceptance, Start Menu shortcut, optional desktop shortcut, and uninstall support.
- GitHub Actions Windows build.

## Local model setup
1. Install the normal dependencies.
2. Install a compatible `llama-cpp-python` build using `requirements-local-model.txt`.
3. Start J.O.A.T.
4. Open **Settings → AI Model → Browse** and select your `.gguf` model.
5. Save.

J.O.A.T. does not ship a model. The user supplies one and remains responsible for its license.

## Windows build
Run `BUILD_WINDOWS.bat` on Windows. It creates `dist\JOAT.exe`. If Inno Setup 6 is installed, it also creates the installer in `dist\installer`.

The included GitHub Actions workflow can build the Windows artifacts on a Windows runner.

## Release checklist
Before public release, replace placeholder contact details in `TERMS_OF_SERVICE.md` and `PRIVACY.md`, verify all third-party licenses, sign the Windows binaries, test fresh install/uninstall, and verify every disclosed data flow.

## Version
**1.0.0 Beta 1**

## Windows Release

See `WINDOWS_RELEASE.md`. The official build outputs are `dist\\JOAT.exe` and `dist\\installer\\JOAT_Setup_1.0.0.exe`. They are generated on Windows; this source package does not pretend that a ZIP file is an EXE.
