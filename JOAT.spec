# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('webview') + collect_submodules('speech_recognition')
datas = []
for pkg in ('webview', 'pyttsx3'):
    try:
        datas += collect_data_files(pkg)
    except Exception:
        pass

datas += [
    ('templates', 'templates'),
    ('static', 'static'),
    ('data', 'data'),
    ('engines', 'engines'),
    ('tools', 'tools'),
]

analysis = Analysis(
    ['desktop_app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports + ['llama_cpp'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(analysis.pure)
exe = EXE(
    pyz,
    analysis.scripts,
    analysis.binaries,
    analysis.datas,
    [],
    name='JOAT',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon='assets_joat.ico',
    version='build_version.txt',
)
