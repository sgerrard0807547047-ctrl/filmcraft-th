#!/usr/bin/env python3
"""Merge optional draft JSONL into the catalog, then apply reviewed translations.

Usage: python3 tools/thai/merge_catalog.py /path/to/drafts.jsonl
Draft rows: {"key": [context, source], "translation": "..."}
Existing manually translated rows take priority over draft rows.
"""
import json
import re
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[2]
p = root / 'crates/ui-egui/src/i18n/th.tsv'
rows = {}
for line in p.read_text(encoding='utf-8').splitlines():
    if line and not line.startswith('#'):
        c, s, t = line.split('\t')
        rows[(c, s)] = t
if len(sys.argv) > 1:
    for line in Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
        d = json.loads(line)
        rows.setdefault(tuple(d['key']), d['translation'])
for line in (root / 'tools/thai/reviewed.tsv').read_text(encoding='utf-8').splitlines():
    source, translated = line.split('\t')
    rows[('', source)] = translated
for key, translated in list(rows.items()):
    # Project is the same editing concept throughout the catalog.
    translated = translated.replace('โครงการ', 'โปรเจกต์').replace('คีย์สั้น', 'แป้นพิมพ์ลัด').replace('ค่าตั้งค่า', 'ค่าที่ตั้งไว้')
    assert sorted(re.findall(r'\{[^{}]*\}', key[1])) == sorted(re.findall(r'\{[^{}]*\}', translated)), key
    assert key[1].endswith('…') == translated.endswith('…'), key
    rows[key] = translated
header = '''# Thai (th) interface catalog. context<TAB>English source<TAB>Thai translation
# Escapes: \\n, \\t, \\\\. Keep placeholders and terminal ellipsis unchanged.
# AI-assisted translations; core editing terminology reviewed. Full human linguistic review pending.
# Technical formats, product names, language names and keyboard key names retain their spelling.
'''
p.write_text(header + ''.join('\t'.join((*k, v)) + '\n' for k, v in sorted(rows.items())), encoding='utf-8')
print(f'Wrote {len(rows)} Thai entries')
