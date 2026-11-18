"""Keep the Thai language pack in sync with Hermes after `hermes update`.

    python3 langpack.py export   # dump current English catalogs -> WORK/en.json
    python3 langpack.py diff     # new/changed English keys -> WORK/chunk_NN.en.json (translate these)
    python3 langpack.py merge    # fold WORK/chunk_NN.th.json into the plugin, drop removed keys, validate

Translate each chunk per tools/GUIDE.md; `cd WORK && python3 check.py NN` must show 0 issues.
"""
import glob
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

HOME = Path.home() / '.hermes'
HA = HOME / 'hermes-agent'
PLUGIN = HOME / 'plugins' / 'hermes-lang-th'
TOOLS = PLUGIN / 'tools'
LOCALES = PLUGIN / 'locales'
SNAPSHOT = TOOLS / 'en_snapshot.json'  # English text each Thai string was translated from
WORK = HOME / 'cache' / 'scratch' / 'th-update'
FILES = {'core': 'th.yaml', 'tui': 'th.tui.yaml', 'desktop': 'th.desktop.yaml'}
CHUNK_KEYS = 900


def flatten(tree, prefix=''):
    for key, value in tree.items():
        path = f'{prefix}.{key}' if prefix else str(key)
        if isinstance(value, dict):
            yield from flatten(value, path)
        else:
            yield path, value


def nest(flat_map):
    tree = {}
    for dotted, text in flat_map.items():
        node = tree
        *parents, leaf = dotted.split('.')
        for part in parents:
            node = node.setdefault(part, {})
        node[leaf] = text
    return tree


def load_thai():
    thai = {}
    for surface, name in FILES.items():
        data = yaml.safe_load((LOCALES / name).read_text(encoding='utf-8')) or {}
        thai.update({f'{surface}::{k}': v for k, v in flatten(data)})
    return thai


def export():
    WORK.mkdir(parents=True, exist_ok=True)
    english = {}
    for surface, cwd in [('tui', HA / 'ui-tui'), ('desktop', HA / 'apps' / 'desktop')]:
        # v0.23.1 dropped tsx from the root node_modules; each workspace carries its own.
        tsx = next(p for p in (cwd / 'node_modules' / '.bin' / 'tsx', HA / 'node_modules' / '.bin' / 'tsx') if p.exists())
        out = WORK / f'en.{surface}.json'
        subprocess.run([str(tsx), str(TOOLS / 'export.mts'), surface, str(out)], cwd=cwd, check=True,
                       env={'PATH': '/usr/bin:/bin', 'HOME': str(Path.home()), 'HA': str(HA)})
        english.update({f'{surface}::{k}': v for k, v in json.loads(out.read_text()).items()})
    core = yaml.safe_load((HA / 'locales' / 'en.yaml').read_text(encoding='utf-8'))
    english.update({f'core::{k}': v for k, v in flatten(core) if isinstance(v, str)})
    (WORK / 'en.json').write_text(json.dumps(english, ensure_ascii=False, indent=1))
    print('english keys', len(english))


def diff():
    english = json.loads((WORK / 'en.json').read_text())
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    thai = load_thai()
    todo = {k: v for k, v in english.items()
            if v.strip() and (k not in thai or snapshot.get(k) != v)}
    removed = [k for k in thai if k not in english]
    for old in glob.glob(str(WORK / 'chunk_*.json')):
        Path(old).unlink()
    keys = sorted(todo)
    for index in range(0, len(keys), CHUNK_KEYS):
        chunk = {k: todo[k] for k in keys[index:index + CHUNK_KEYS]}
        (WORK / f'chunk_{index // CHUNK_KEYS:02d}.en.json').write_text(json.dumps(chunk, ensure_ascii=False, indent=1))
    for helper in ['GUIDE.md', 'check.py']:
        shutil.copy(TOOLS / helper, WORK / helper)
    print(f'to translate: {len(todo)} keys in {(len(keys) + CHUNK_KEYS - 1) // CHUNK_KEYS} chunk(s); '
          f'removed from English: {len(removed)}')
    print('work dir:', WORK)


def merge():
    sys.path.insert(0, str(TOOLS))
    from check import problems
    english = json.loads((WORK / 'en.json').read_text())
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    thai = {k: v for k, v in load_thai().items() if k in english and english[k].strip()}
    for english_path in sorted(glob.glob(str(WORK / 'chunk_*.en.json'))):
        thai_path = Path(english_path.replace('.en.', '.th.'))
        if not thai_path.exists():
            print('NOT TRANSLATED, skipped:', thai_path.name)
            continue
        source, translated = json.loads(Path(english_path).read_text()), json.loads(thai_path.read_text())
        bad = {line.split()[1].rstrip(':') for line in problems(source, translated)}
        for key in source.keys() - bad:
            thai[key] = translated[key]
            snapshot[key] = source[key]
        print(thai_path.name, len(source) - len(bad), 'merged', len(bad), 'dropped (English fallback)')
    by_surface = {s: {} for s in FILES}
    for key, text in thai.items():
        surface, dotted = key.split('::', 1)
        by_surface[surface][dotted] = text
    for surface, name in FILES.items():
        data = nest(by_surface[surface]) if surface == 'core' else by_surface[surface]
        with open(LOCALES / name, 'w', encoding='utf-8') as handle:
            # quote everything: YAML 1.1 reads bare y/on/no as booleans and the validator rejects them
            yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=True, width=10**6, default_style='"')
        print(surface, len(by_surface[surface]), 'keys')
    SNAPSHOT.write_text(json.dumps({k: v for k, v in snapshot.items() if k in thai}, ensure_ascii=False, indent=1))
    subprocess.run(['hermes', 'plugins', 'validate', str(PLUGIN)], check=False)


if __name__ == '__main__':
    {'export': export, 'diff': diff, 'merge': merge}[sys.argv[1]]()
