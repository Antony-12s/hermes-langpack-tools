"""Check a translated chunk: python3 check.py NN  -> verifies chunk_NN.th.json against chunk_NN.en.json."""
import json
import re
import sys

PLACEHOLDER = re.compile(r'\{[A-Za-z0-9_]*\}')


def problems(english, thai):
    found = []
    for key, source in english.items():
        if key not in thai:
            found.append(f'MISSING {key}')
            continue
        target = thai[key]
        if not isinstance(target, str) or not target.strip():
            found.append(f'EMPTY/NONSTRING {key}')
            continue
        if sorted(PLACEHOLDER.findall(source)) != sorted(PLACEHOLDER.findall(target)):
            found.append(f'PLACEHOLDER {key}: en={PLACEHOLDER.findall(source)} th={PLACEHOLDER.findall(target)}')
        lead = len(source) - len(source.lstrip(' '))
        if lead and not target.startswith(' ' * lead):
            found.append(f'LEADING-SPACES {key}: keep {lead} leading spaces')
    found += [f'EXTRA {key}' for key in thai if key not in english]
    return found


if __name__ == '__main__':
    chunk = sys.argv[1]
    english = json.load(open(f'chunk_{chunk}.en.json'))
    thai = json.load(open(f'chunk_{chunk}.th.json'))
    issues = problems(english, thai)
    print('\n'.join(issues[:80]))
    print(f'{len(english)} keys, {len(issues)} issues')
    sys.exit(1 if issues else 0)
