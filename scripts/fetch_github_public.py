#!/usr/bin/env python3
"""
Refresca data/github.public.json SOLO para repos del inventario Yggdra
(data/projects.json) que sean públicos.

- Alcance: aplicaciones que consumen Yggdra (o migran a él) + yggdra-web.
- Repos privados: no se consultan commits; quedan solo con datos del inventario.
- API pública de GitHub; GITHUB_TOKEN opcional (rate limit).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OWNER = "felipebarraza6"
# Sitio público de la plataforma (relacionado con Yggdra; no es un producto cliente).
PLATFORM_SITE_REPO = f"{OWNER}/yggdra-web"

FORBIDDEN = re.compile(
    r"("
    r"@|"
    r"token|"
    r"secret|"
    r"api/apps|"
    r"src/|"
    r"agents-api\.|"
    r"api\.smarthydro\.app|"
    r"intranet|"
    r"agenciapatagoniachile|"
    r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
    r")",
    re.I,
)


def api_get(url: str, token: str | None) -> object | None:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "yggdra-web-public-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if exc.code in (404, 403, 401):
            return None
        raise


def clean_text(value: str | None) -> str | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if not text or FORBIDDEN.search(text):
        return None
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text or None


def inventory_repos() -> list[str]:
    """Lista full_name (owner/name) desde projects.json; sin inventar repos ajenos."""
    path = DATA / "projects.json"
    if not path.exists():
        print("Falta data/projects.json", file=sys.stderr)
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("projects") or []
    out: list[str] = []
    seen: set[str] = set()
    for p in items:
        if not isinstance(p, dict):
            continue
        repo = p.get("repo")
        if not isinstance(repo, str):
            # Fallback estable: owner/<id> solo si id es slug seguro
            pid = p.get("id")
            if isinstance(pid, str) and re.fullmatch(r"[A-Za-z0-9_.-]+", pid):
                repo = f"{OWNER}/{pid}"
            else:
                continue
        repo = repo.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            continue
        # Solo repos del owner de la plataforma
        if not repo.startswith(f"{OWNER}/"):
            continue
        if repo not in seen:
            seen.add(repo)
            out.append(repo)
    if PLATFORM_SITE_REPO not in seen:
        out.append(PLATFORM_SITE_REPO)
    return out


def recent_commits(full_name: str, token: str | None, limit: int = 30) -> list[dict]:
    """Hasta `limit` commits públicos, paginando de a 30."""
    out: list[dict] = []
    page = 1
    while len(out) < limit and page <= 3:
        per = min(30, limit - len(out))
        raw = api_get(
            f"https://api.github.com/repos/{full_name}/commits?per_page={per}&page={page}",
            token,
        )
        if not isinstance(raw, list) or not raw:
            break
        for item in raw:
            commit = item.get("commit") or {}
            msg = (commit.get("message") or "").split("\n", 1)[0]
            summary = clean_text(msg)
            if not summary:
                continue
            summary = re.sub(
                r"^(feat|fix|ci|cd|chore|docs|refactor|perf|test)(\([^)]+\))?:\s*",
                "",
                summary,
                flags=re.I,
            )
            summary = re.sub(r"\s*\(#\d+\)\s*$", "", summary).strip()
            if summary:
                summary = summary[0].upper() + summary[1:]
            date = ((commit.get("author") or {}).get("date") or "")[:10]
            if not date:
                continue
            out.append({"date": date, "summary": summary})
            if len(out) >= limit:
                break
        if len(raw) < per:
            break
        page += 1
    return out


def fetch_public_repo(full_name: str, token: str | None) -> dict | None:
    meta = api_get(f"https://api.github.com/repos/{full_name}", token)
    if not isinstance(meta, dict):
        return None
    if meta.get("private"):
        # Privado: no publicar actividad GitHub; el inventario ya cubre la ficha.
        return None
    name = meta.get("name") or full_name.split("/")[-1]
    created = meta.get("created_at")
    updated = meta.get("updated_at")
    pushed = meta.get("pushed_at")
    return {
        "name": name,
        "fullName": meta.get("full_name") or full_name,
        "description": clean_text(meta.get("description")),
        "language": meta.get("language"),
        "createdAt": created,
        "updatedAt": updated,
        "pushedAt": pushed,
        "commits": recent_commits(full_name, token),
    }


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    targets = inventory_repos()
    if not targets:
        print("Inventario vacío: nada que sincronizar", file=sys.stderr)
        return 1

    selected: list[dict] = []
    skipped_private_or_missing = 0
    for full in targets:
        try:
            entry = fetch_public_repo(full, token)
        except Exception as exc:  # noqa: BLE001
            print(f"Aviso: no se pudo leer {full}: {exc}", file=sys.stderr)
            skipped_private_or_missing += 1
            continue
        if entry is None:
            skipped_private_or_missing += 1
            continue
        selected.append(entry)

    payload = {
        "version": 1,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generatedNote": (
            "Actividad pública solo de repos del inventario Yggdra. "
            "Repos privados no se listan aquí."
        ),
        "scope": "inventory-only",
        "repos": selected,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "github.public.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Wrote {out} ({len(selected)} públicos; "
        f"{skipped_private_or_missing} omitidos/privados/ausentes de {len(targets)} del inventario)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
