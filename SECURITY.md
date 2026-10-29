# Política de seguridad — yggdra-web

## Reportar una vulnerabilidad
No abras un issue público. Escribe directamente a Felipe Barraza (líder de software SmartHydro) por correo corporativo, indicando repo, archivo/endpoint, impacto y pasos para reproducir. Respondemos en un plazo de 5 días hábiles.

## Reglas del repositorio
- Nunca versionar secretos: `.env`, `env.prod*`, `*.bak`, llaves (`*.key`, `*.pem`), dumps (`*.sql`, `*.dump`, `*.rdb`, `*.sqlite3`). Están en `.gitignore`.
- Las credenciales se leen desde variables de entorno; ver `.env.example` (solo nombres).
- Los secretos de CI viven en GitHub Secrets/Environments, nunca en el YAML.
- Workflows con `permissions` mínimos; deploys solo manuales y con aprobación.
- Si un secreto se filtra: rotarlo primero y luego limpiar el historial.
