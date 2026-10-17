#!/usr/bin/env python3
"""
Regenera data/github.public.json desde la API pública de GitHub
(repos públicos del usuario), sin tokens adicionales más allá de GITHUB_TOKEN.
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

FORBIDDEN = re.compile(
    r"("
    r"@|"
    r"\btoken\b|"
    r"\bsecret\b|"
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


def api_get(url: str, token: str | None) -> object:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "yggdra-web-public-sync",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def clean_text(value: str | None) -> str | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip()
    if not text or FORBIDDEN.search(text):
        return None
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\s{2,}", " ", text).strip()
    return text or None


def known_project_ids() -> set[str]:
    path = DATA / "projects.json"
    if not path.exists():
        path = DATA / "consumers.public.json"
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    items = data.get("projects") or data.get("consumers") or []
    return {p["id"] for p in items if isinstance(p, dict) and "id" in p}


def list_public_repos(token: str | None) -> list[dict]:
    repos: list[dict] = []
    page = 1
    while page <= 5:
        url = (
            f"https://api.github.com/users/{OWNER}/repos"
            f"?type=public&sort=updated&per_page=100&page={page}"
        )
        batch = api_get(url, token)
        if not isinstance(batch, list) or not batch:
            break
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return repos


def recent_commits(full_name: str, token: str | None, limit: int = 5) -> list[dict]:
    url = f"https://api.github.com/repos/{full_name}/commits?per_page={limit}"
    try:
        raw = api_get(url, token)
    except urllib.error.HTTPError:
        return []
    if not isinstance(raw, list):
        return []
    out: list[dict] = []
    for item in raw:
        commit = item.get("commit") or {}
        msg = (commit.get("message") or "").split("\n", 1)[0]
        summary = clean_text(msg)
        if not summary:
            continue
        # Quitar scopes convencionales para lenguaje llano
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
    return out


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    known = known_project_ids()
    known.add("yggdra-web")

    try:
        repos_raw = list_public_repos(token)
    except Exception as exc:  # noqa: BLE001
        print(f"Error listando repos: {exc}", file=sys.stderr)
        return 1

    selected = []
    for repo in repos_raw:
        if repo.get("private"):
            continue
        name = repo.get("name") or ""
        # Priorizar repos del inventario; incluir también yggdra-web
        if known and name not in known:
            continue
        full = repo.get("full_name") or f"{OWNER}/{name}"
        desc = clean_text(repo.get("description"))
        entry = {
            "name": name,
            "fullName": full,
            "description": desc,
            "language": repo.get("language"),
            "updatedAt": repo.get("updated_at"),
            "commits": recent_commits(full, token),
        }
        selected.append(entry)

    payload = {
        "version": 1,
        "updatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generatedNote": "Metadatos públicos de repositorios. Sin credenciales ni rutas internas.",
        "repos": selected,
    }

    DATA.mkdir(parents=True, exist_ok=True)
    out = DATA / "github.public.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out} ({len(selected)} repos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
