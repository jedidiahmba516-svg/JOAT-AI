# J.O.A.T. Beta 1 — Windows Release Build

## What this package does

This package is a **Windows build pipeline**. When run on Windows, it produces the actual application and installer:

- `dist\\JOAT.exe`
- `dist\\installer\\JOAT_Setup_1.0.0.exe`

The source ZIP itself is not the finished EXE.

## Your Python installation

J.O.A.T.'s builder accepts either:

- the `py -3.13` launcher, or
- a normal `python` command reporting Python 3.13.

You do **not** need to install Python again just because the `py` launcher is missing.

## Build

1. Extract the ZIP.
2. Run `CHECK_WINDOWS_BUILD.bat` once if you want to inspect prerequisites.
3. Run `BUILD_WINDOWS.bat`.
4. The script keeps the terminal open when something fails.
5. If `JOAT.exe` is created but Inno Setup is missing, install **Inno Setup 6** and run `BUILD_WINDOWS.bat` again.

## Local model runtime

The build checks for `llama-cpp-python`. If it is missing, the script attempts to install the package listed in `requirements-local-model.txt`.

The user supplies the `.gguf` model separately. J.O.A.T. does not bundle a model.

## Expected output

```text
dist\\JOAT.exe
dist\\installer\\JOAT_Setup_1.0.0.exe
```

The installer includes the Terms of Service and Privacy Policy acceptance pages.
