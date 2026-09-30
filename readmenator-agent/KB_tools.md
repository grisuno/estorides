# Subsystem: tools

## tools/split_sources.py
- Layer: utility
- Doc: Split legacy grouped source files into one addon per file.  Reads every multi-document ``sources/NN_xxx.yaml`` and write
- Language: py
- Symbols:
  - `main` (function, line 19) `def main()`

## tools/sync_docs.py
- Layer: utility
- Doc: tools.sync_docs =============== Generate docs manifest from source truth and fail on drift.  I scan spec/*.md headings p
- Language: py
- Symbols:
  - `collect` (function, line 20) `def collect()`
  - `main` (function, line 36) `def main(argv)`
- Depends on: `estorides_web.py`
