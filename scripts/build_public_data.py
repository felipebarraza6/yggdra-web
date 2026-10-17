#!/usr/bin/env python3
"""
Genera data/consumers.public.json y data/activity.json a partir de insumos privados.

Uso:
  python3 scripts/build_public_data.py \\
    --inventory _private/CONSUMERS.yaml \\
    --commits _private/recent_main_commits.txt

No escribe rutas internas (api/apps/**, src/**), dominios de API/staging,
correos, tokens ni IPs. Solo nombres de producto, dominios públicos de app,
estado y módulos (tags / segmentos de paths públicos).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Instala PyYAML: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

# Dominios públicos de apps en producción (permitidos). Todo lo demás se filtra.
# No incluir intranets de clientes ni dominios de agencia/API.
PUBLIC_APP_DOMAINS = {
    "frig.yggdra.cl",
    "cauce.smartapr.cl",
    "90dias.habitofirme.app",
}

FORBIDDEN_DOMAIN_FRAGMENTS = (
    "agents-api.",
    "api.smarthydro.app",
    "api.yggdra.cl",
    "intranet",
    "agenciapatagoniachile",
)

STATUS_ES = {
    "active": "activa",
    "migrating": "en migración",
    "legacy": "legado",
}

# Prefijos de commit → módulo público
MODULE_HINTS = [
    (r"\brecipes?\b", "recipes"),
    (r"\baccounts?\b", "accounts"),
    (r"\bbranches?\b", "branches"),
    (r"\bforja\b", "forja"),
    (r"\bp90\b|/api/p90", "coaching"),
    (r"\bcoaching\b", "coaching"),
    (r"\bfinance\b", "finance"),
    (r"\bsupport\b", "support"),
    (r"\biot[-_]?telemetry\b|\bwater\b", "iot-telemetry"),
    (r"\binventory\b", "inventory"),
    (r"\bsales\b", "sales"),
    (r"\bcustomers?\b", "customers"),
    (r"\btimezone\b|\bfecha", "shared"),
    (r"\bsecurity\b|admins? provision", "accounts"),
    (r"\binventario de consumidores|\breporte de impacto", "orquestación"),
    (r"\bci\b|\bcd\b|\bnginx\b|\bcompose\b", "infra"),
    (r"\bapi\b.*frig|frig.*\bapi\b|sesiones concurrentes", "accounts"),
]


def module_from_path(path: str) -> str | None:
    """Deriva nombre de módulo desde un glob /api/<mod>/**; nunca expone paths internos."""
    if not isinstance(path, str):
        return None
    if path.startswith("api/apps/") or path.startswith("src/"):
        return None
    m = re.match(r"^/api/([^/\*]+)", path)
    if m:
        seg = m.group(1)
        if seg == "v1":
            return "api-v1"
        return seg
    if path.startswith("/smarthydro"):
        return "smarthydro"
    return None


def sanitize_domains(domains: list | None) -> list[str]:
    out: list[str] = []
    for d in domains or []:
        if not isinstance(d, str):
            continue
        host = d.strip().lower().removeprefix("https://").removeprefix("http://").split("/")[0]
        if any(frag in host for frag in FORBIDDEN_DOMAIN_FRAGMENTS):
            continue
        if host in PUBLIC_APP_DOMAINS:
            out.append(host)
    return out


def sanitize_consumer(raw: dict) -> dict | None:
    if not isinstance(raw, dict) or "id" not in raw:
        return None
    tags = []
    for t in (raw.get("uses") or {}).get("tags") or []:
        if isinstance(t, str) and t.strip():
            tags.append(t.strip())
    modules: list[str] = []
    seen: set[str] = set()
    # Preferir tags OpenAPI; si no hay tags, derivar módulos desde paths públicos.
    if tags:
        for t in tags:
            if t not in seen:
                seen.add(t)
                modules.append(t)
    else:
        for p in (raw.get("uses") or {}).get("paths") or []:
            mod = module_from_path(p)
            if mod and mod not in seen:
                seen.add(mod)
                modules.append(mod)

    status = raw.get("status") or "active"
    return {
        "id": raw["id"],
        "name": raw.get("name") or raw["id"],
        "status": status,
        "statusLabel": STATUS_ES.get(status, status),
        "domains": sanitize_domains(raw.get("domains")),
        "modules": modules,
    }


def load_clients() -> dict:
    path = DATA / "clients.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("clients") if isinstance(data, dict) and "clients" in data else data


def merge_clients(consumers: list[dict], clients: dict) -> list[dict]:
    for c in consumers:
        entry = clients.get(c["id"]) or {}
        if isinstance(entry, str):
            entry = {"company": entry}
        c["company"] = (entry.get("company") or "").strip()
        c["product"] = (entry.get("product") or "").strip() or c["name"]
        c["description"] = (entry.get("description") or "").strip()
    return consumers


def plain_summary(title: str) -> str:
    """Quita prefijos convencionales y referencias a PRs; deja lenguaje llano."""
    t = title.strip()
    t = re.sub(r"\s*\(#\d+\)\s*$", "", t)
    t = re.sub(r"^Merge pull request #\d+ from \S+\s*", "", t)
    t = re.sub(
        r"^(feat|fix|ci|cd|chore|docs|refactor|perf|test)(\([^)]+\))?:\s*",
        "",
        t,
        flags=re.I,
    )
    # Quitar paths de API y detalles técnicos sensibles
    t = re.sub(r"/api/[^\s,;]+", "el módulo correspondiente", t)
    t = re.sub(r"\bsrc/[^\s,;]+", "", t)
    t = re.sub(r"\bapi/apps/[^\s,;]+", "", t)
    t = re.sub(r"https?://\S+", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip(" .")
    if t:
        t = t[0].upper() + t[1:]
    return t or "Actualización del backend"


def detect_module(title: str) -> str:
    lower = title.lower()
    # Prefer scope in conventional commit: feat(recipes):
    m = re.match(r"^(?:feat|fix|ci|cd|chore|docs|refactor|perf|test)\(([^)]+)\)", title, re.I)
    if m:
        scope = m.group(1).lower()
        scope_map = {
            "recipes": "recipes",
            "accounts": "accounts",
            "branches": "branches",
            "forja": "forja",
            "p90": "coaching",
            "finance": "finance",
            "support": "support",
            "timezone": "shared",
            "security": "accounts",
            "api": "shared",
            "cd": "infra",
            "ci": "infra",
        }
        if scope in scope_map:
            return scope_map[scope]
    for pattern, mod in MODULE_HINTS:
        if re.search(pattern, lower, re.I):
            return mod
    return "shared"


def build_activity(commits_path: Path, limit: int = 25) -> list[dict]:
    lines = commits_path.read_text(encoding="utf-8").strip().splitlines()
    items: list[dict] = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # fecha ISO + título
        parts = line.split(" ", 1)
        if len(parts) != 2:
            continue
        date_raw, title = parts
        if re.search(r"(token|secret|password|@|\d+\.\d+\.\d+\.\d+)", title, re.I):
            continue
        if "api/apps" in title or "src/" in title:
            continue
        date = date_raw.replace("T", " ").rstrip("Z")[:10]
        items.append(
            {
                "date": date,
                "summary": plain_summary(title),
                "module": detect_module(title),
            }
        )
        if len(items) >= limit:
            break
    return items


def collect_modules(consumers: list[dict]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for c in consumers:
        for m in c.get("modules") or []:
            if m not in seen:
                seen.add(m)
                ordered.append(m)
    return ordered


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera JSON públicos de Yggdra Web")
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "_private" / "CONSUMERS.yaml",
        help="YAML de inventario (no se publica)",
    )
    parser.add_argument(
        "--commits",
        type=Path,
        default=ROOT / "_private" / "recent_main_commits.txt",
        help="Títulos de commits recientes (no se publica)",
    )
    parser.add_argument("--out-dir", type=Path, default=DATA)
    args = parser.parse_args()

    if not args.inventory.exists():
        print(f"No se encontró inventario: {args.inventory}", file=sys.stderr)
        print("Copia un YAML saneado a _private/CONSUMERS.yaml o pasa --inventory.", file=sys.stderr)
        return 1

    raw = yaml.safe_load(args.inventory.read_text(encoding="utf-8"))
    consumers_raw = raw.get("consumers") if isinstance(raw, dict) else None
    if not isinstance(consumers_raw, list):
        print("Inventario sin lista consumers[]", file=sys.stderr)
        return 1

    consumers = []
    for item in consumers_raw:
        clean = sanitize_consumer(item)
        if clean:
            consumers.append(clean)

    clients = load_clients()
    consumers = merge_clients(consumers, clients)

    public = {
        "version": 1,
        "generatedNote": "Inventario público de apps que usan Yggdra. Sin rutas internas ni credenciales.",
        "modules": collect_modules(consumers),
        "consumers": consumers,
    }

    args.out_dir.mkdir(parents=True, exist_ok=True)
    out_consumers = args.out_dir / "consumers.public.json"
    out_consumers.write_text(
        json.dumps(public, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {out_consumers} ({len(consumers)} apps)")

    if args.commits.exists():
        activity = {
            "version": 1,
            "generatedNote": "Avances recientes del backend Yggdra, en lenguaje llano.",
            "items": build_activity(args.commits),
        }
        out_act = args.out_dir / "activity.json"
        out_act.write_text(
            json.dumps(activity, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {out_act} ({len(activity['items'])} entries)")
    else:
        print(f"Aviso: sin archivo de commits ({args.commits}); no se regeneró activity.json")

    return 0


if __name__ == "__main__":
    sys.exit(main())
