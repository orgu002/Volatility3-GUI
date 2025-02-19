# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Screens/ui/NavigationBar.ui', 'ui'), ('Screens/ui/DataAnalyze.ui', 'ui'), ('Screens/ui/FileUploader.ui', 'ui'), ('Screens/ui/Homepage.ui', 'ui'), ('Screens/ui/Os.ui', 'ui'), ('Screens/ui/Plugins.ui', 'ui'), ('Screens/ui/PluginsResponsive.ui', 'ui'), ('Screens/ui/Settings.ui', 'ui'), ('Screens/ui/SettingsDark.ui', 'ui'), ('Screens/ui/SettingsLight.ui', 'ui'), ('Design/Settings.png', 'png'), ('Design/Close.png', 'png'), ('Design/cloudUploadIcon.png', 'png'), ('Design/Columns.png', 'png'), ('Design/done.png', 'png'), ('Design/Export.png', 'png'), ('Design/logo 2.png', 'png'), ('Design/Mnemonic logo.png', 'png'), ('Design/mnemonic logo white no icon no text.png', 'png'), ('Design/mnemonic logo white1.png', 'png'), ('Design/mnemonic logo white 2.png', 'png'), ('Design/Simple Analyze.png', 'png'), ('Design/Simple_AnalyzeHomepageLogo.png', 'png'), ('Design/Vector.png', 'png'), ('Design/mnemonic.ico', 'ico')],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='Design/mnemonic.ico',
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)