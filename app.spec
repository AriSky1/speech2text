# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[('speech2text_env\\Lib\\site-packages\\vosk\\libgcc_s_seh-1.dll', 'vosk'), ('speech2text_env\\Lib\\site-packages\\vosk\\libstdc++-6.dll', 'vosk'), ('speech2text_env\\Lib\\site-packages\\vosk\\libvosk.dll', 'vosk'), ('speech2text_env\\Lib\\site-packages\\vosk\\libwinpthread-1.dll', 'vosk')],
    datas=[('templates', 'templates'), ('static', 'static'), ('models', 'models')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
