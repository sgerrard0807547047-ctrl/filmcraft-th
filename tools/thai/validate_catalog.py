#!/usr/bin/env python3
"""Check Thai catalog structure, placeholders and union coverage; no dependencies."""
import re
from pathlib import Path
root = Path(__file__).resolve().parents[2]
folder = root / 'crates/ui-egui/src/i18n'
def entries(path):
    result = {}
    for n, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if not line.strip() or line.startswith('#'):
            continue
        cols = line.split('\t')
        assert len(cols) == 3 and cols[1] and cols[2], (path, n, cols)
        key = tuple(cols[:2])
        assert key not in result, (path, n, 'duplicate', key)
        result[key] = cols[2]
    return result
thai = entries(folder / 'th.tsv')
for (_, source), translated in thai.items():
    assert sorted(re.findall(r'\{[^{}]*\}', source)) == sorted(re.findall(r'\{[^{}]*\}', translated)), source
    assert source.endswith('…') == translated.endswith('…'), source
    for escape in ('\\n', '\\t'):
        assert source.count(escape) == translated.count(escape), (source, escape)
union = set()
for path in folder.glob('*.tsv'):
    union.update(entries(path))
missing = sorted(union - thai.keys())
print(f'Thai: {len(thai)} entries; {len(missing)} union keys missing')
for key in missing:
    print(key)
assert not missing, 'Thai catalog does not yet cover the existing catalog union'
