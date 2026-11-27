# yggdra-web (landing Y ARQ)

Página de servicio y portafolio técnico de **Y ARQ** (YARQ): backend
multi-tenant, API compartida, CI con impacto, productos y automatizaciones.

- URL: https://felipebarraza6.github.io/yggdra-web/
- Marca: **Y ARQ** / **YARQ**
- Identidad: laboratorio blanco — flujo continuo, glass limpio, sin revelar lo interno
- Backend: **privado** — este repo no publica código, rutas internas ni secretos
- **Alcance:** solo Y ARQ y las apps del inventario (consumidoras o en migración).
  Nada de repos ajenos al ecosistema.

Texto en **español de Chile** (registro comercial-técnico). La home es la
página de servicio de la infraestructura; las secciones profundas cubren
contratos, módulos y fichas de producto.

## Conceptos

| Concepto | Significado en el sitio |
|----------|-------------------------|
| Y / ARQ | Marca display (YARQ en prosa) |
| Servicio | Infraestructura multi-tenant que sostiene productos |
| Flujo | Hilo continuo: aislamiento → API → entrega → observación → respaldo → agentes |
| Productos | Apps del inventario que demuestran el tronco |
| Automatizaciones | Agentes y flujos sobre la misma operación |
| Raíces | Infraestructura y aislamiento |
| Tronco | API, módulos, OpenAPI |
| Ramas | Aplicaciones consumidoras |

## Rutas

- `/` — página de servicio (flujo, servicios, impacto)
- `/apps/` y `/apps/<id>/` — inventario y ficha por aplicación
- `/modulos/` y `/modulos/<id>/` — módulos/sectores y quién los usa

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
npm run check
```

Local típico: `http://127.0.0.1:4321/yggdra-web/` (el puerto puede variar).

## TODO — clientes por confirmar

Forja, Muninn, Ikolu Void, Gungir, Cotizador de oro, HEIR, Agents,
App Smoking APR. Andean Labs pendiente de inventario.
