#!/usr/bin/env python3
"""Package the locally built binary without changing /Applications."""
import plistlib
import shutil
import subprocess
from pathlib import Path
root = Path(__file__).resolve().parents[2]
binary = root / 'target/release/filmcraft'
app = root / 'dist/thai/FilmCraft.app'
contents = app / 'Contents'
resources = contents / 'Resources'
resources.mkdir(parents=True, exist_ok=True)
(contents / 'MacOS').mkdir(exist_ok=True)
shutil.copy2(binary, contents / 'MacOS/FilmCraft')
shutil.copy2(root / 'assets/app-icon/FilmCraft.icns', resources / 'FilmCraft.icns') if (root / 'assets/app-icon/FilmCraft.icns').exists() else shutil.copy2('/Applications/FilmCraft.app/Contents/Resources/FilmCraft.icns', resources / 'FilmCraft.icns')
for name in ['NOTICE', 'LICENSE-MIT', 'LICENSE-APACHE']:
    shutil.copy2(root / name, resources / name)
sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
text = (root / 'packaging/macos/Info.plist.in').read_text().replace('@VERSION@', '0.17.0-th.1').replace('@SHORT_VERSION@', '0.17.0').replace('@BUILD_SHA@', sha + '-thai-local')
info = plistlib.loads(text.encode())
info['FilmCraftLocalBuild'] = 'Thai localization, 2026-11-04'
(contents / 'Info.plist').write_bytes(plistlib.dumps(info))
(contents / 'PkgInfo').write_bytes(b'APPL????')
(resources / 'th.lproj').mkdir(exist_ok=True)
(resources / 'th.lproj/InfoPlist.strings').write_text('"NSMicrophoneUsageDescription" = "FilmCraft ใช้ไมโครโฟนเพื่อบันทึกเสียงบรรยายลงในไทม์ไลน์";\n"CFBundleDisplayName" = "FilmCraft";\n')
subprocess.run(['codesign', '--force', '--sign', '-', '--timestamp=none', str(app)], check=True)
subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app)], check=True)
print(app)
