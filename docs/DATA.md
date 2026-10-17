# Formato de datos públicos (Yggdra Platform)

Todo el contenido del sitio se genera en build desde `data/*.json`.
Un workflow externo (o el diario de GitHub) puede actualizar estos archivos y
disparar deploy con `repository_dispatch` tipo `yggdra-update`.

## `data/projects.json`

Inventario público de aplicaciones que consumen Yggdra.

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

Reglas: sin rutas `api/apps/**` ni `src/**`, sin IPs, correos, tokens,
intranets ni dominios de API/staging.

## `data/activity.json`

Changelog público de alto nivel (plataforma / backend).

```json
{
  "version": 1,
  "generatedNote": "string",
  "items": [
    { "date": "2026-10-17", "summary": "…", "module": "recipes" }
  ]
}
```

## `data/clients.json`

Mapeo editable a mano `id` → producto / empresa / descripción.
No se publica solo; lo fusiona `scripts/build_public_data.py`.

## `data/github.public.json`

Metadatos de repos **públicos** (generado por el workflow diario).

```json
{
  "version": 1,
  "updatedAt": "2026-10-17T00:00:00Z",
  "repos": [
    {
      "name": "frig",
      "fullName": "felipebarraza6/frig",
      "description": "string o null",
      "language": "TypeScript",
      "updatedAt": "2026-10-17T12:00:00Z",
      "commits": [
        { "date": "2026-10-17", "summary": "…" }
      ]
    }
  ]
}
```

## Regeneración local

```bash
pip install -r requirements-data.txt
python3 scripts/build_public_data.py
python3 scripts/check_privacy.py
```

## Privacidad

`scripts/check_privacy.py` debe pasar antes de merge o deploy.
