# Formato de datos públicos (Yggdra Platform)

Todo el contenido del sitio se genera en **build** desde `data/*.json`.

**Alcance:** solo Yggdra Platform y las aplicaciones del inventario que la
consumen o migran hacia ella. No se publican repos ajenos al ecosistema.

Un workflow del **repo privado** del backend puede empujar JSON actualizados y
disparar deploy con:

```http
POST /repos/felipebarraza6/yggdra-web/dispatches
Accept: application/vnd.github+json
{
  "event_type": "yggdra-update"
}
```

(el workflow `pages.yml` ya escucha `repository_dispatch` tipo `yggdra-update`).

## `data/projects.json`

Inventario público de aplicaciones sobre Yggdra.

```json
{
  "version": 1,
  "generatedNote": "string",
  "modules": ["accounts", "finance"],
  "projects": [
    {
      "id": "frig",
      "name": "FRIG (…)",
      "product": "Frig",
      "company": "Macanuo Bowl · Maní",
      "description": "string corta",
      "status": "active|migrating|legacy",
      "statusLabel": "activa|en migración|legado",
      "domains": ["frig.yggdra.cl"],
      "modules": ["accounts", "sales"],
      "contract": {
        "style": "openapi-typescript|manual|proxy|planned",
        "label": "Tipos generados desde OpenAPI"
      },
      "repo": "felipebarraza6/frig"
    }
  ]
}
```

- `repo` apunta al GitHub de la app (si existe). Si el repo es **privado**, el
  sitio solo muestra los campos del inventario (sin commits ni lenguajes).
- Sin rutas `api/apps/**` ni `src/**`, sin IPs, correos, tokens, intranets ni
  dominios de API/staging.

Generación local (desde YAML privado gitignorado):

```bash
python3 scripts/build_public_data.py --inventory _private/CONSUMERS.yaml
```

## `data/activity.json`

Changelog público de alto nivel de la **plataforma** (no de cada front).

```json
{
  "version": 1,
  "generatedNote": "string",
  "items": [
    { "date": "2026-10-17", "summary": "…", "module": "recipes" }
  ]
}
```

`summary` en lenguaje llano; `module` es un nombre de módulo público.
Sin hashes, paths internos ni secretos.

## `data/clients.json`

Mapeo editable a mano `id` → `product` / `company` / `description`.
Lo fusiona `scripts/build_public_data.py` al generar `projects.json`.

## `data/github.public.json`

Señal **solo** de repos **públicos** que aparecen en el inventario
(`projects[].repo`) más `yggdra-web`. Generado por el workflow diario
`github-public-sync.yml` (`scripts/fetch_github_public.py`).

```json
{
  "version": 1,
  "updatedAt": "2026-10-17T00:00:00Z",
  "scope": "inventory-only",
  "repos": [
    {
      "name": "frig",
      "fullName": "felipebarraza6/frig",
      "description": "string o null",
      "language": "TypeScript",
      "createdAt": "2026-08-11T05:55:15Z",
      "updatedAt": "2026-10-17T12:00:00Z",
      "pushedAt": "2026-10-17T12:00:00Z",
      "commits": [{ "date": "2026-10-17", "summary": "…" }]
    }
  ]
}

`createdAt` / `pushedAt` alimentan la vista **Historia** (trayectoria y
días de trabajo público por rama).
```

Los repos privados del ecosistema **no** se listan aquí: su ficha en el sitio
usa únicamente `projects.json`.

## Privacidad

Antes de commit o deploy:

```bash
python3 scripts/check_privacy.py
```

Falla si `data/*.json` contiene `@`, `token`, `secret`, `api/apps`, `src/`,
IPs, `intranet`, `agenciapatagoniachile`, etc.
