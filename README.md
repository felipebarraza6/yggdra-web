# Yggdra Web

Sitio público de la **plataforma Yggdra**: portafolio vivo de productos, clientes y módulos sobre un backend transversal multi-tenant.

- URL: https://felipebarraza6.github.io/yggdra-web/
- Repo: público (este)
- Backend: **privado** (`felipebarraza6/yggdra_infra`) — no se publica código, rutas internas, secretos ni dominios de API/staging

Todo el texto visible está en **español de Chile** (registro neutro).

## Qué hay en el sitio

1. Portada — modelo de plataforma (multi-tenant, OpenAPI, orquestación, despliegue continuo)  
2. Mapa interactivo app ↔ módulos (matriz / grafo)  
3. Fichas por producto y cliente  
4. Timeline de avances recientes  
5. Orquestación — reporte de impacto automático → ajustes por app → promoción conjunta  

## Datos públicos

| Archivo | Rol |
|---------|-----|
| `data/consumers.public.json` | Inventario saneado (apps, estado, dominios públicos, módulos) |
| `data/clients.json` | Mapeo editable app → cliente/empresa (a mano) |
| `data/activity.json` | Changelog público de alto nivel |

### Actualizar el inventario

1. En un entorno privado, coloca una copia del inventario en `_private/CONSUMERS.yaml` (carpeta gitignorada; **no** la subas a este repo).
2. Edita `data/clients.json` si hay clientes nuevos claros.
3. Opcional: `_private/recent_main_commits.txt` con líneas `YYYY-MM-DDTHH:MM:SSZ título`.
4. Regenera:

```bash
pip install -r requirements-data.txt
python3 scripts/build_public_data.py
python3 scripts/check_privacy.py
```

5. Commitea solo los JSON en `data/` y el script. **Nunca** `CONSUMERS.yaml` crudo.

### Actualizar clientes a mano

`data/clients.json` mapea `id` de app → `product`, `company`, `description`.  
Si el cliente no se deduce de un nombre o dominio público, deja `company` vacío.

### Disparo remoto (repo privado)

El workflow de Pages acepta `repository_dispatch` con `event_type: yggdra-update` (además de `workflow_dispatch` y push a `main`). Así el backend privado puede pedir regenerar/desplegar cuando empuje datos actualizados.

## Privacidad (regla dura)

Este repo es público. **Prohibido** publicar:

- Código del backend, rutas `api/apps/**` o `src/**`
- Variables de entorno, IPs, tokens, correos
- Dominios internos de API/staging (`agents-api.*`, `api.smarthydro.app`, etc.), cualquier host con `intranet` o `agenciapatagoniachile`, e intranets de clientes
- IDs de organizaciones/sucursales o datos de clientes finales

**Sí** se puede: nombre de producto, empresa, dominio público de app en producción, estado (`activa` / `en migración` / `legado`) y nombres de módulo (`accounts`, `recipes`, `iot-telemetry`, …).

El job de CI `scripts/check_privacy.py` **falla** si `data/*.json` contiene patrones prohibidos (`@`, `token`, `secret`, `api/apps`, `src/`, IPs, dominios internos).

## Desarrollo local

```bash
npm install
npm run dev
```

Build estático (base `/yggdra-web/` para GitHub Pages):

```bash
npm run build
npm run preview
```

## TODO — clientes por confirmar

Apps con `company` vacío en `data/clients.json` (no inventar):

- Forja  
- Muninn  
- Ikolu Void  
- Gungir  
- Cotizador de oro  
- HEIR  
- Yggdra Agents  
- App Smoking APR (legado)  

También pendiente de inventario público: **Andean Labs**. Agregarlo cuando exista entrada clara.

## Stack

- Astro (sitio estático, sin backend)
- GitHub Pages (`build_type=workflow`)
- Python 3 para saneamiento de datos y gate de privacidad
