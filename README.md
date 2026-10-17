# Yggdra Platform (web pública)

Sitio explicativo de **Yggdra Platform**: portafolio técnico de la arquitectura
multi-tenant y de las aplicaciones que la consumen.

- URL: https://felipebarraza6.github.io/yggdra-web/
- Marca: **Yggdra Platform**
- Backend: **privado** — este repo no publica código, rutas internas ni secretos
- **Alcance:** solo Yggdra y las apps del inventario (consumidoras o en migración).
  Nada de repos ajenos al ecosistema.

Texto en **español de Chile** (registro neutro). No es una página de venta:
explica el oficio (arquitectura, contratos, orquestación, CI/CD, telemetría).

## Conceptos (nórdicos, sutiles)

| Concepto | Significado en el sitio |
|----------|-------------------------|
| Raíces | Infraestructura y aislamiento |
| Tronco | API, módulos, OpenAPI |
| Ramas | Aplicaciones consumidoras |
| Nornas | Orquestación e impacto |
| Bifröst | Integraciones y despliegue |

## Rutas

- `/` — portada con diagramas y gráficos
- `/apps/` y `/apps/<id>/` — inventario y ficha por aplicación
- `/modulos/` y `/modulos/<id>/` — módulos y quién los usa

## Datos (contenido que muta solo)

Todo se genera desde `data/*.json` en build. Formato documentado en
[`docs/DATA.md`](docs/DATA.md).

| Archivo | Rol |
|---------|-----|
| `data/projects.json` | Inventario público de apps |
| `data/activity.json` | Changelog de la plataforma |
| `data/clients.json` | Mapeo editable app → cliente |
| `data/github.public.json` | Señal pública de repos (workflow diario) |
| `data/consumers.public.json` | Compatibilidad con el artefacto anterior |

### Actualizar inventario

```bash
pip install -r requirements-data.txt
# colocar YAML privado en _private/CONSUMERS.yaml (gitignorado)
python3 scripts/build_public_data.py
python3 scripts/check_privacy.py
```

### Disparo remoto

`repository_dispatch` con `event_type: yggdra-update` regenera/despliega Pages
(ver `.github/workflows/pages.yml`).

### Sync diario de repos públicos (solo inventario)

`.github/workflows/github-public-sync.yml` recorre `projects[].repo` del
inventario, consulta la API pública con `GITHUB_TOKEN` y escribe
`data/github.public.json` **únicamente** para repos públicos de ese listado
(+ `yggdra-web`). Los privados quedan solo con los datos del inventario.
Pasa el gate de privacidad y hace commit si hay cambios.

## Privacidad

Prohibido en `data/*.json`: IPs, `@`, `token`, `secret`, `api/apps`, `src/`,
`intranet`, `agenciapatagoniachile`, dominios de API/staging.

```bash
python3 scripts/check_privacy.py
```

## Desarrollo

```bash
npm install
npm run dev
npm run build
```

## TODO — clientes por confirmar

Forja, Muninn, Ikolu Void, Gungir, Cotizador de oro, HEIR, Yggdra Agents,
App Smoking APR. Andean Labs pendiente de inventario.
