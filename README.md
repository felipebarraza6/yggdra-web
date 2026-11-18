# yggdra-web (landing YARQ)

Landing y portafolio técnico de **YARQ** (Y ARQ): backend multi-tenant,
API compartida, CI con impacto, productos, agentes y puerta API → sectores.

- URL: https://felipebarraza6.github.io/yggdra-web/
- Marca: **YARQ** / **Y ARQ**
- Backend: **privado** — este repo no publica código, rutas internas ni secretos
- **Alcance:** solo YARQ y las apps del inventario (consumidoras o en migración).
  Nada de repos ajenos al ecosistema.

Texto en **español de Chile** (registro comercial-técnico). La home explica
adopción de clientes; las secciones profundizan contratos, orquestación,
CI/CD y telemetría.

## Conceptos

| Concepto | Significado en el sitio |
|----------|-------------------------|
| Y / ARQ | Marca display (YARQ en prosa) |
| Adopción | Cómo entran clientes al tronco |
| YARQ | API multi-tenant: raíces, tronco, CI, ramas |
| Productos | Apps del inventario que demuestran el tronco |
| Agentes | Muninn (+ Fly) orquestados sobre la operación |
| Puerta API | Qué puedes entrar y a qué sectores llegar |
| Raíces | Infraestructura y aislamiento |
| Tronco | API, módulos, OpenAPI |
| Ramas | Aplicaciones consumidoras |
| Nornas | Orquestación e impacto |
| Bifröst | Integraciones y despliegue |

## Rutas

- `/` — landing de impacto + profundidad técnica
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

Local típico: `http://127.0.0.1:4323/yggdra-web/` (el puerto puede variar).

## TODO — clientes por confirmar

Forja, Muninn, Ikolu Void, Gungir, Cotizador de oro, HEIR, Agents,
App Smoking APR. Andean Labs pendiente de inventario.
