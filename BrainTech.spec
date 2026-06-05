# BrainTech.spec
# Run: pyinstaller BrainTech.spec

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# collect PyQt5 internals (helps include Qt plugins)
hidden_imports = collect_submodules('PyQt5')
datas = collect_data_files('PyQt5')

# Add project data directories and files (relative to project root)
proj_root = os.getcwd()

# Include Data folder
datas += [(os.path.join(proj_root, 'Data'), 'Data')]

# Include Database folder (medical_database.db and others)
datas += [(os.path.join(proj_root, 'Database'), 'Database')]

# Include Image folder (logo.ico, images)
datas += [(os.path.join(proj_root, 'Image'), 'Image')]

# Optionally include Models folder (may be large)
datas += [(os.path.join(proj_root, 'Models'), 'Models')]

# If you prefer to include only specific model files instead, replace the Models line above
# with explicit file tuples, e.g.:
# datas += [(os.path.join(proj_root, 'Models', 'model_v01', 'btcm-mdl-v01.h5'), 'Models\\model_v01')]

a = Analysis(
    ['Main/main-v.py'],
    pathex=[proj_root],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BrainTech',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,  # no console window
    icon=os.path.join(proj_root, 'Image', 'logo.ico')
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='BrainTech'
)
