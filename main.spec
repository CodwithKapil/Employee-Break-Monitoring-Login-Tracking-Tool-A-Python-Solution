# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py', 'dashboard.py', 'bg.py'],
    pathex=[],
    binaries=[],
    datas=[(r'C:\Users\Server_M\Documents\WindowsPowerShell\Crystalvoxx_Employee Managment\cybernetic-muse-415516-b7d092189c6a.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Crystalvoxx Employee Monitor',
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
