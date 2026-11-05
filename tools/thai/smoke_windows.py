#!/usr/bin/env python3
"""Run an isolated app smoke test on Windows using FilmCraft's documented control API."""
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parent
while root != root.parent and not (root / 'Cargo.toml').exists():
    root = root.parent

qa = root / 'target/thai-qa'
qa.mkdir(parents=True, exist_ok=True)

with socket.socket() as listener:
    listener.bind(('127.0.0.1', 0))
    port = listener.getsockname()[1]

token = secrets.token_hex(32)
env = dict(os.environ, FILMCRAFT_CONTROL_TOKEN=token)

default_binary = root / 'target/release/filmcraft.exe' if os.name == 'nt' else root / 'target/release/filmcraft'
if not default_binary.exists() and (root / 'target/debug/filmcraft.exe').exists():
    default_binary = root / 'target/debug/filmcraft.exe'

binary = Path(sys.argv[1]) if len(sys.argv) > 1 else default_binary

log = (qa / 'app.log').open('w', encoding='utf-8')
process = subprocess.Popen([str(binary), '--control', str(port), '--data-dir', str(qa / 'data'), '--empty'], env=env, stdout=log, stderr=log)

def call(method, params=None):
    with socket.create_connection(('127.0.0.1', port), timeout=30) as connection:
        request = dict(id=1, token=token, method=method, params=params or {})
        connection.sendall((json.dumps(request) + '\n').encode('utf-8'))
        reply = json.loads(connection.makefile('rb').readline().decode('utf-8'))
        if not reply.get('ok'):
            raise RuntimeError((method, reply))
        return reply.get('result')

try:
    for attempt in range(120):
        if process.poll() is not None:
            raise RuntimeError('App exited; see target/thai-qa/app.log')
        try:
            call('ui.inspect')
            break
        except (ConnectionError, OSError):
            time.sleep(0.5)
        except RuntimeError as error:
            if "still starting" not in str(error):
                raise
            time.sleep(0.5)
    assert call('ui.menu.invoke', {'id': 'app.language.thai'}) == 'th'
    call('ui.resize', {'width': 1440, 'height': 900})
    menus = call('ui.menu.list')
    (qa / 'menus.json').write_text(json.dumps(menus, ensure_ascii=False, indent=2), encoding='utf-8')
    assert any(m.get('id') == 'app.language.thai' and m.get('checked') for m in menus)
    call('engine.execute', {'command': 'file.openDemoProject', 'params': {}})
    call('ui.set', {'mode': 'edit'})
    time.sleep(1)
    call('ui.screenshot', {'path': str(qa / 'editing.png')})
    call('ui.menu.invoke', {'id': 'app.settings.general'})
    call('ui.screenshot', {'path': str(qa / 'settings.png')})
    call('ui.key', {'key': 'Escape'})
    call('ui.set', {'mode': 'export'})
    call('ui.screenshot', {'path': str(qa / 'export.png')})
    state = call('ui.inspect')
    (qa / 'state.json').write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    prefs = json.loads((qa / 'data/preferences.json').read_text(encoding='utf-8'))
    assert prefs['general']['interfaceLanguage'] == 'th'
    print('PASS: Thai menu selection, preferences, demo project, editing/settings/export screenshots')
finally:
    try:
        call('app.quit')
        process.wait(timeout=20)
    except Exception:
        process.terminate()
        process.wait(timeout=10)
    log.close()
