#!/usr/bin/env python3
"""
CI gate: falla si data/*.json contiene patrones prohibidos en este repo público.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Patrones exactos pedidos + dominios internos de API/staging.
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("IP", re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")),
    ("@", re.compile(r"@")),
    ("token", re.compile(r"token", re.I)),
    ("secret", re.compile(r"secret", re.I)),
    ("api/apps", re.compile(r"api/apps", re.I)),
    ("src/", re.compile(r"src/", re.I)),
    ("agents-api.*", re.compile(r"agents-api\.", re.I)),
    ("api.agenciapatagoniachile.com", re.compile(r"api\.agenciapatagoniachile\.com", re.I)),
    ("api.smarthydro.app", re.compile(r"api\.smarthydro\.app", re.I)),
]


def main() -> int:
    if not DATA.is_dir():
        print("No existe data/", file=sys.stderr)
        return 1

    files = sorted(DATA.glob("*.json"))
    if not files:
        print("No hay JSON en data/", file=sys.stderr)
        return 1

    failures: list[str] = []
    for path in files:
        raw = path.read_text(encoding="utf-8")
        try:
            json.loads(raw)
        except json.JSONDecodeError as e:
            print(f"JSON inválido en {path}: {e}", file=sys.stderr)
            return 1
        rel = path.relative_to(ROOT)
        for name, pattern in PATTERNS:
            for m in pattern.finditer(raw):
                start = max(0, m.start() - 24)
                end = min(len(raw), m.end() + 24)
                snippet = raw[start:end].replace("\n", " ")
                failures.append(f"{rel}: «{name}» en …{snippet}…")

    if failures:
        print("PRIVACY GATE FAILED:\n", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(f"Privacy OK ({len(files)} archivos).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
