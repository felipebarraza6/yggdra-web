/** Identidad pública de YARQ: estudio de productos digitales. */

export const brand = {
  name: "YARQ",
  short: "YARQ",
  tagline: "Infraestructura digital para construir el futuro",
  headline: "Digitalizamos lo esencial para construir un futuro mejor",
  lede:
    "En YARQ creamos tecnología aplicada al mundo real: plataformas, automatización e inteligencia artificial sobre una base compartida para modernizar la operación diaria de organizaciones, comunidades y ciudades.",
  support:
    "De la arquitectura de datos a la automatización con IA: todo lo necesario para digitalizar operaciones críticas con continuidad real.",
};

export type Pillar = {
  code: string;
  title: string;
  body: string;
  metric: string;
};

export type BrainDistrict = {
  id: string;
  code: string;
  name: string;
  headline: string;
  summary: string;
  color: string;
  /** Coordenadas normalizadas (0..1) en la pizarra panorámica */
  nx: number;
  ny: number;
  /** Sub-elementos visibles en la "ciudad" arquitectónica */
  nodes: { label: string; dx: number; dy: number; kind?: "core" | "service" | "app" }[];
  modules: string[];
  flow: string;
  products: string[];
};

/** Pizarra viva del Cerebro YARQ (Partículas PYF + 6 distritos de infraestructura). */
export const brainMap = {
  kicker: "Nosotros · Propósito y arquitectura",
  title: "Tecnología diseñada para perdurar y escalar",
  lede:
    "Construimos un núcleo compartido de partículas PYF —multi-tenant, IA operativa, APIs abiertas e infraestructura propia— para que cada nueva plataforma nazca sólida, interoperable y lista para transformar su sector.",
  districts: [
    {
      id: "multitenant",
      code: "D01 · IDENTIDAD",
      name: "Núcleo Multi-Tenant",
      headline: "Aislamiento total por organización y sucursal",
      summary:
        "Separa datos, usuarios, roles y permisos desde la base de datos hasta la interfaz. Todos los clientes consumen contratos OpenAPI tipados generados automáticamente.",
      color: "#0284c7",
      nx: 0.21,
      ny: 0.25,
      nodes: [
        { label: "accounts", dx: -0.075, dy: -0.06, kind: "core" },
        { label: "branches", dx: 0.06, dy: -0.075, kind: "core" },
        { label: "roles & RBAC", dx: -0.09, dy: 0.045, kind: "service" },
        { label: "OpenAPI v1", dx: 0.075, dy: 0.04, kind: "core" },
        { label: "plan-checkout", dx: -0.01, dy: 0.085, kind: "service" },
      ],
      modules: ["accounts", "branches", "plan-checkout", "api-v1"],
      flow: "Sesión → Aislamiento tenant → Contrato OpenAPI tipado",
      products: ["Frig", "Cauce", "HEIR", "Forja"],
    },
    {
      id: "ai",
      code: "D02 · INTELIGENCIA",
      name: "Agentes IA y Workflows",
      headline: "Agentes conectados a herramientas reales del negocio",
      summary:
        "Orquestación de agentes con memoria aislada por organización, permisos acotados y flujos multi-paso que ejecutan reservas, consultas y automatizaciones auditables.",
      color: "#7c3aed",
      nx: 0.79,
      ny: 0.25,
      nodes: [
        { label: "ai-agents", dx: -0.065, dy: -0.065, kind: "core" },
        { label: "workflows", dx: 0.075, dy: -0.055, kind: "core" },
        { label: "memoria tenant", dx: -0.08, dy: 0.04, kind: "service" },
        { label: "tools tipadas", dx: 0.08, dy: 0.045, kind: "service" },
        { label: "Muninn · Gungir", dx: 0.0, dy: 0.09, kind: "app" },
      ],
      modules: ["ai-agents", "workflows", "campaigns", "analytics"],
      flow: "Evento / chat → Orquestador IA + tools → Acción auditada",
      products: ["Muninn", "Gungir", "Proyecto 90"],
    },
    {
      id: "domain",
      code: "D03 · DOMINIO",
      name: "Motores de Negocio",
      headline: "26 módulos productivos componibles por vertical",
      summary:
        "Ensamblamos plataformas reales combinando motores probados en calle: POS gastronómico con cocina y recetas, agua potable rural, finanzas, CRM, inventario y agendas.",
      color: "#2563eb",
      nx: 0.17,
      ny: 0.67,
      nodes: [
        { label: "sales & POS", dx: -0.07, dy: -0.055, kind: "core" },
        { label: "recipes & stock", dx: 0.075, dy: -0.06, kind: "service" },
        { label: "finance", dx: -0.08, dy: 0.05, kind: "core" },
        { label: "crm & agenda", dx: 0.065, dy: 0.055, kind: "service" },
        { label: "Frig · Cauce · Forja", dx: -0.005, dy: 0.1, kind: "app" },
      ],
      modules: ["sales", "finance", "inventory", "recipes", "crm", "scheduling"],
      flow: "Reglas verticales → Módulos ensamblados → Operación diaria",
      products: ["Frig", "Maní", "Cauce", "Forja", "Hábito Firme"],
    },
    {
      id: "apis",
      code: "D04 · CONECTIVIDAD",
      name: "APIs Externas e IoT",
      headline: "Puentes bidireccionales, webhooks y núcleos derivados",
      summary:
        "Conectamos pagos, mensajería, facturación externa y telemetría hídrica IoT. Permite derivar forks especializados por industria como Nereus API sin perder compatibilidad.",
      color: "#059669",
      nx: 0.83,
      ny: 0.67,
      nodes: [
        { label: "webhooks", dx: -0.07, dy: -0.06, kind: "core" },
        { label: "iot-telemetry", dx: 0.07, dy: -0.055, kind: "core" },
        { label: "pagos & DTE", dx: -0.075, dy: 0.045, kind: "service" },
        { label: "water & sensors", dx: 0.075, dy: 0.05, kind: "service" },
        { label: "Nereus API (fork)", dx: 0.0, dy: 0.1, kind: "app" },
      ],
      modules: ["api-v1", "iot-telemetry", "water", "public"],
      flow: "Webhook / sensor → Adaptador + cola → Estado sincronizado",
      products: ["Nereus API", "SmartAPR", "Cauce", "Nxord"],
    },
    {
      id: "runtime",
      code: "D05 · INFRAESTRUCTURA",
      name: "Runtime y Operación 24/7",
      headline: "Despliegue reproducible, colas asíncronas y respaldos",
      summary:
        "Operamos la capa completa de ejecución: contenedores Docker, Nginx + TLS automático, PostgreSQL, Redis, workers Celery, observabilidad y entregas CI verificadas.",
      color: "#0891b2",
      nx: 0.5,
      ny: 0.83,
      nodes: [
        { label: "Docker + CI", dx: -0.115, dy: -0.025, kind: "core" },
        { label: "Nginx + TLS", dx: -0.05, dy: 0.055, kind: "service" },
        { label: "PostgreSQL", dx: 0.0, dy: -0.055, kind: "core" },
        { label: "Redis + Celery", dx: 0.06, dy: 0.055, kind: "service" },
        { label: "Backups 24/7", dx: 0.12, dy: -0.02, kind: "service" },
      ],
      modules: ["services", "support", "analytics"],
      flow: "Build CI → Contenedores + TLS → Monitoreo y respaldos",
      products: ["Todas las plataformas YARQ"],
    },
    {
      id: "surface",
      code: "D06 · SUPERFICIE",
      name: "Experiencias y Clientes",
      headline: "Interfaces rápidas listas para producción real",
      summary:
        "Desde el núcleo emergen aplicaciones web, puntos de venta en local, paneles en terreno y portales públicos compartiendo diseño, velocidad y contratos estrictos.",
      color: "#0ea5e9",
      nx: 0.5,
      ny: 0.16,
      nodes: [
        { label: "Web & Portales", dx: -0.1, dy: 0.01, kind: "app" },
        { label: "POS & Terreno", dx: 0.0, dy: -0.05, kind: "app" },
        { label: "Paneles Ops", dx: 0.1, dy: 0.01, kind: "app" },
      ],
      modules: ["public", "plan-checkout", "support"],
      flow: "Núcleo PYF → Interfaces tipadas → Equipos operando en vivo",
      products: ["Maní", "SmartAPR", "Hábito Firme", "HEIR"],
    },
  ] as BrainDistrict[],
};

export type ArchBranch = {
  id: string;
  code: string;
  shortLabel: string;
  title: string;
  summary: string;
  detail: string;
  color: string;
  modules: string[];
  flow: [string, string, string];
  usedBy: string[];
  /** Posición normalizada (0..100) dentro del mapa de constelación */
  x: number;
  y: number;
};

/** Explicación precisa de qué es YARQ y su arquitectura en profundidad. */
export const aboutArchitecture = {
  kicker: "Nosotros · Capa de infraestructura",
  title: "No construimos piezas sueltas. Operamos una arquitectura viva.",
  lede:
    "YARQ es un estudio y una infraestructura de productos digitales. En lugar de reinventar bases desde cero en cada proyecto, diseñamos y operamos un núcleo compartido —con aislamiento multi-tenant, contratos tipados, agentes de IA e integraciones externas— sobre el cual nacen y escalan plataformas completas.",
  identityPoints: [
    {
      label: "Qué es YARQ",
      value: "Un núcleo compartido de 26 módulos productivos y una arquitectura replicable que sostiene 18 aplicaciones en operación y evolución.",
    },
    {
      label: "Cómo operamos",
      value: "Unimos diseño de producto, arquitectura de datos, automatización con IA e infraestructura propia bajo el mismo techo.",
    },
    {
      label: "Por qué importa",
      value: "Cada producto nuevo hereda seguridad, integraciones, telemetría y despliegue continuo probados en producción real.",
    },
  ],
  branches: [
    {
      id: "core",
      code: "RAMA 01 · NÚCLEO",
      shortLabel: "Núcleo Multi-Tenant",
      title: "Identidad, aislamiento y contratos tipados",
      summary: "Cada organización y sucursal opera con datos aislados, roles granulares y una sola fuente de verdad OpenAPI.",
      detail:
        "El corazón de YARQ separa estrictamente los datos por organización y sucursal desde la base de datos hasta la interfaz. Todos los clientes web, móviles y paneles consumen contratos OpenAPI tipados automáticamente (openapi-typescript), eliminando divergencias entre backend y frontend.",
      color: "#0284c7",
      modules: ["accounts", "branches", "plan-checkout", "api-v1"],
      flow: ["Sesión y tenant activo", "Validación de rol y contrato OpenAPI", "Estado aislado por organización"],
      usedBy: ["Frig", "Cauce", "HEIR", "Forja"],
      x: 24,
      y: 22,
    },
    {
      id: "ai",
      code: "RAMA 02 · INTELIGENCIA",
      shortLabel: "IA y Agentes",
      title: "Agentes autónomos con herramientas del negocio",
      summary: "Flujos conversacionales y operativos con memoria por organización, permisos acotados y registro auditable.",
      detail:
        "Integramos agentes de IA directamente sobre las operaciones reales del negocio —no como un chat decorativo—. Cada agente accede solo a las herramientas y datos permitidos para su organización, ejecuta flujos multi-paso (reservas, consultas, alertas, soporte) y deja trazabilidad completa.",
      color: "#7c3aed",
      modules: ["ai-agents", "workflows", "campaigns", "analytics"],
      flow: ["Evento o mensaje entrante", "Orquestador IA + herramientas tipadas", "Acción ejecutada y registrada"],
      usedBy: ["Muninn", "Gungir", "Proyecto 90"],
      x: 76,
      y: 22,
    },
    {
      id: "apis",
      code: "RAMA 03 · CONECTIVIDAD",
      shortLabel: "APIs y Telemetría",
      title: "Integraciones externas, webhooks y derivados",
      summary: "Conectores bidireccionales con pagos, mensajería, sensores IoT y exposición de API v1 para terceros y forks.",
      detail:
        "La arquitectura está diseñada para dialogar hacia afuera: pasarelas de pago, canales de mensajería, facturación externa, telemetría hídrica IoT y clientes propios. Además permite derivar núcleos especializados por industria sin perder compatibilidad —como Nereus API en el ecosistema hídrico.",
      color: "#059669",
      modules: ["api-v1", "iot-telemetry", "water", "public"],
      flow: ["API externa / sensor / webhook", "Adaptador normalizado + cola", "Sincronización en tiempo real"],
      usedBy: ["Nereus API", "Cauce", "SmartAPR", "Nxord"],
      x: 75,
      y: 71,
    },
    {
      id: "domain",
      code: "RAMA 04 · DOMINIO",
      shortLabel: "Motores de Negocio",
      title: "Módulos productivos listos para cada vertical",
      summary: "Ventas, caja, cocina, recetas, inventario, finanzas, CRM, soporte y agendas componibles por industria.",
      detail:
        "En vez de empezar en blanco, ensamblamos cada plataforma combinando motores probados en calle: POS gastronómico con comandas y recetas, facturación de agua potable rural, seguimiento de cohortes y coaching o cotizadores multisucursal.",
      color: "#2563eb",
      modules: ["sales", "finance", "inventory", "recipes", "crm", "scheduling"],
      flow: ["Reglas del negocio", "Módulos de dominio ensamblados", "Operación diaria en producción"],
      usedBy: ["Frig", "Maní", "Cauce", "Forja", "Hábito Firme"],
      x: 25,
      y: 71,
    },
    {
      id: "runtime",
      code: "RAMA 05 · OPERACIÓN",
      shortLabel: "Runtime y Continuidad",
      title: "Infraestructura reproducible, colas y observabilidad",
      summary: "Contenedores, Nginx + TLS, PostgreSQL, Redis, Celery, respaldos automáticos y entrega continua verificada.",
      detail:
        "Operamos la capa completa de ejecución: entornos reproducibles con certificados TLS automáticos, procesamiento asíncrono para tareas pesadas, alertas tempranas de salud, respaldos programados y despliegues trazables sin interrumpir la operación de nuestros clientes.",
      color: "#0891b2",
      modules: ["services", "support", "analytics"],
      flow: ["Build y verificación CI", "Despliegue en contenedores + TLS", "Monitoreo 24/7 y respaldos"],
      usedBy: ["Todas las plataformas YARQ"],
      x: 50,
      y: 86,
    },
  ] as ArchBranch[],
};

/** Cómo construimos productos digitales. */
export const aboutYarq = {
  kicker: "Sobre YARQ",
  title: "Un estándar único para cada producto que sale a producción",
  lede:
    "Trabajamos con método, criterios claros y foco en el largo plazo. Desde la concepción inicial hasta la operación diaria, cada decisión técnica y de interfaz responde al producto real.",
  pillars: [
    {
      code: "01 · CONCEPCIÓN",
      title: "Criterio antes de escribir código",
      body: "Definimos el modelo, el alcance y la experiencia con precisión para construir exactamente lo que mueve el producto.",
      metric: "Modelo y alcance claros",
    },
    {
      code: "02 · CONSTRUCCIÓN",
      title: "Producto completo, sin costuras",
      body: "Interfaces rápidas, lógica de negocio sólida y automatización integrada sobre un núcleo consistente.",
      metric: "Base probada en producción",
    },
    {
      code: "03 · ESCALA",
      title: "Preparado para crecer sin reescribir",
      body: "Aislamiento por organización, contratos de datos limpios y despliegue replicable desde el primer día.",
      metric: "Aislamiento multiusuario",
    },
    {
      code: "04 · CONTINUIDAD",
      title: "Operación viva y evolución constante",
      body: "Observabilidad, respaldos automáticos e iteraciones continuas para que cada producto mejore con el uso.",
      metric: "Operación continua 24/7",
    },
  ] as Pillar[],
};

export type ServiceIcon =
  | "isolation"
  | "api"
  | "infra"
  | "delivery"
  | "telemetry"
  | "agents";

export type ServiceBay = {
  id: string;
  code: string;
  icon: ServiceIcon;
  title: string;
  body: string;
  stack?: string[];
};

/** Lo que entregamos en cada producto digital. */
export const services: ServiceBay[] = [
  {
    id: "plataformas",
    code: "01 · PLATAFORMAS",
    icon: "isolation",
    title: "Plataformas multiusuario",
    body: "Sistemas preparados para múltiples organizaciones o sucursales, con datos aislados y capacidades configurables por rol.",
  },
  {
    id: "integraciones",
    code: "02 · INTEGRACIONES",
    icon: "api",
    title: "Integraciones y APIs",
    body: "Conectamos la operación con sistemas externos y exponemos una API tipada y documentada para nuevos clientes.",
  },
  {
    id: "infra",
    code: "03 · INFRAESTRUCTURA",
    icon: "infra",
    title: "Despliegue controlado",
    body: "Entornos reproducibles con certificados, bases de datos, caché y colas de trabajo bajo control total.",
    stack: ["Contenedores", "Nginx + TLS", "PostgreSQL", "Redis", "Celery"],
  },
  {
    id: "entrega",
    code: "04 · LANZAMIENTO",
    icon: "delivery",
    title: "Entrega continua",
    body: "Cada cambio pasa por verificación automatizada antes de llegar a producción, con ciclos cortos y trazables.",
  },
  {
    id: "observacion",
    code: "05 · OPERACIÓN",
    icon: "telemetry",
    title: "Monitoreo y respaldos",
    body: "Métricas de salud, alertas tempranas y respaldos automáticos para sostener disponibilidad e integridad de datos.",
  },
  {
    id: "automatizacion",
    code: "06 · AUTOMATIZACIÓN",
    icon: "agents",
    title: "Automatización e IA",
    body: "Flujos y agentes de IA integrados a la operación diaria, con permisos acotados y registro de cada acción.",
  },
];

export type StrandNode = {
  id: string;
  code: string;
  label: string;
};

/** Etapas del ciclo completo de un producto digital. */
export const strandNodes: StrandNode[] = [
  { id: "concepcion", code: "01", label: "Concepción" },
  { id: "diseno", code: "02", label: "Diseño" },
  { id: "desarrollo", code: "03", label: "Desarrollo" },
  { id: "lanzamiento", code: "04", label: "Lanzamiento" },
  { id: "operacion", code: "05", label: "Operación" },
  { id: "automatizacion", code: "06", label: "Automatización" },
];

export type ShowcasePiece = {
  name: string;
  category: string;
  status: string;
  description: string;
  logo?: string;
  monogram?: string;
  appId?: string;
  externalUrl?: string;
};

export const showcase: ShowcasePiece[] = [
  {
    name: "Frig",
    category: "Gastronomía · POS",
    status: "en producción",
    description:
      "Punto de venta multisucursal: caja, cocina, mesas, inventario, recetas y finanzas en una sola plataforma.",
    logo: "logos/frig.png",
    appId: "frig",
  },
  {
    name: "Muninn",
    category: "Agentes · IA",
    status: "en producción",
    description:
      "Estudio para diseñar, conectar y operar agentes de IA con flujos, canales y despliegue por organización.",
    logo: "logos/muninn.png",
    appId: "muninn",
  },
  {
    name: "Cauce",
    category: "Agua potable rural",
    status: "en producción",
    description:
      "Ciclo operativo de APR: socios, medidores, lecturas, tarifas, facturación y recaudación.",
    logo: "logos/cauce.png",
    appId: "nxrd_apr",
  },
  {
    name: "HEIR",
    category: "Comercio · Cotizaciones",
    status: "demo",
    description:
      "Plataforma comercial multisucursal con escaparate público, cotizador y gestión administrativa.",
    monogram: "HR",
    appId: "heir",
  },
  {
    name: "Forja",
    category: "Entrenamiento · SaaS",
    status: "demo",
    description:
      "Gestión integral para entrenadores personales: alumnos, rutinas, nutrición, adherencia y suscripciones.",
    logo: "logos/forja.svg",
    appId: "forja",
  },
  {
    name: "Gungir",
    category: "Salud · Agenda",
    status: "en diseño",
    description:
      "Reservas, cobros y agente conversacional para profesionales de la salud y consultas independientes.",
    monogram: "GN",
    appId: "gungir",
  },
];

export type ConsumerBrand = {
  name: string;
  sector: string;
  product: string;
  role: string;
  logo?: string;
  monogram?: string;
  appId: string;
};

export const consumerBrands: ConsumerBrand[] = [
  {
    name: "Maní",
    sector: "Gastronomía multisucursal",
    product: "Frig POS",
    role: "Operación diaria de caja, cocina, recetas e inventario separado por local.",
    logo: "logos/frig.png",
    appId: "frig",
  },
  {
    name: "SmartAPR",
    sector: "Servicios sanitarios rurales",
    product: "Cauce",
    role: "Gestión de socios, lecturas de medidores, tarifas y cobranza en terreno.",
    logo: "logos/cauce.png",
    appId: "nxrd_apr",
  },
  {
    name: "Hábito Firme",
    sector: "Programas digitales",
    product: "Proyecto 90",
    role: "Inscripción, seguimiento de cohortes y operación de programas a 90 días.",
    logo: "logos/habito.png",
    appId: "proyecto-90",
  },
  {
    name: "Nereus API",
    sector: "Núcleo derivado · Telemetría",
    product: "Fork · nereus_app · Nxord",
    role: "Plataforma derivada sobre el núcleo YARQ para operación comercial y telemetría hídrica.",
    logo: "logos/nxord.svg",
    appId: "nereus_smarthydro",
  },
];
