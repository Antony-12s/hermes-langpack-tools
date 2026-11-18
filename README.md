# hermes-langpack-tools

Tooling that keeps [hermes-lang-th](https://github.com/Antony-12s/hermes-lang-th), the Thai UI language pack for [Hermes Agent](https://github.com/NousResearch/hermes-agent), in sync after `hermes update`.

This is a copy of the pack's `tools/` folder, published on its own so it can be adapted to other languages. The pack repo keeps its own copy and stays the source of truth.

## Files

- `langpack.py`: `export` dumps the current English catalogs, `diff` writes new or changed keys into chunks to translate, `merge` folds translated chunks back into the pack and validates it.
- `export.mts`: exports the TUI and Desktop catalogs (run from the workspace with its own `tsx`).
- `check.py`: checks a translated chunk (placeholders, empty values, protected tokens).
- `GUIDE.md`: translation rules and tone for the Thai pack.
- `en_snapshot.json`: the English text each Thai string was translated from; drives change detection.
- `after-update.sh`: runs `export` and `diff` after an update and sends a desktop notification if work is needed.

## Usage

```bash
python3 langpack.py export
python3 langpack.py diff
# translate WORK/chunk_NN.en.json into chunk_NN.th.json, then:
python3 langpack.py merge
```

Paths assume the pack lives at `~/.hermes/plugins/hermes-lang-th`. For another language, change `PLUGIN`, `FILES` and the snapshot in `langpack.py`.
