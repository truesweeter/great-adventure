# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['script.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('map.tmx', '.'), ('ground.tsx', '.'), ('data/records.json', 'data/records.json'), ('walls.tsx', '.'), ('col.tsx', '.'), ('box.tsx', '.'), ('gate.tsx', '.'), ('hero_col.tsx', '.'), ('stone.tsx', '.')],
    hiddenimports=['arcade'],
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
    name='GreatAdventure',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
