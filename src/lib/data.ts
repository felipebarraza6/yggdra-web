import projectsData from "../../data/projects.json";
import activityData from "../../data/activity.json";
import githubData from "../../data/github.public.json";

export type Project = (typeof projectsData.projects)[number];
export type ActivityItem = (typeof activityData.items)[number];
export type GithubRepo = (typeof githubData.repos)[number];

export const projects = projectsData.projects as Project[];
export const modules = projectsData.modules as string[];
export const activity = activityData.items as ActivityItem[];
export const githubRepos = (githubData.repos || []) as GithubRepo[];

/** Módulos del inventario + los que aparecen en activity (p. ej. infra, orquestación). */
export const allModuleIds = [
  ...new Set([...modules, ...activity.map((a) => a.module).filter(Boolean)]),
];

export function getProject(id: string) {
  return projects.find((p) => p.id === id);
}

export function projectsForModule(moduleId: string) {
  return projects.filter((p) => p.modules.includes(moduleId));
}

export function activityForModules(mods: string[], limit = 12) {
  const set = new Set(mods);
  return activity.filter((a) => set.has(a.module)).slice(0, limit);
}

export function githubForProject(project: Project) {
  const name = project.repo?.split("/")[1] || project.id;
  return githubRepos.find((r) => r.name === name || r.fullName === project.repo);
}

/**
 * Envuelve referencias internas de la vertical hídrica bajo el ecosistema Nereus API
 * y normaliza la marca pública a Y ARQ.
 */
export function publicOrg(company?: string): string {
  const raw = (company || "").trim();
  if (!raw) return "Ecosistema YARQ";
  if (/smarthydro/i.test(raw)) return "Nereus API";
  return raw;
}

export function publicLabel(project: Project): string {
  const raw = project.product || project.name;
  if (project.id === "nereus_smarthydro") return "nereus_app";
  return raw
    .replace(/SmartHydro/gi, "Nereus")
    .replace(/Yggdra/gi, "YARQ");
}

export function publicCopy(text?: string): string {
  if (!text) return "";
  return text
    .replace(/Panel operativo SmartHydro sobre Yggdra\.?/gi, "Suite operativa core sobre Nereus API (fork de YARQ).")
    .replace(/SmartHydro/gi, "Nereus API")
    .replace(/Yggdra/gi, "YARQ");
}

export const counts = {
  total: projects.length,
  active: projects.filter((c) => c.status === "active").length,
  migrating: projects.filter((c) => c.status === "migrating").length,
  legacy: projects.filter((c) => c.status === "legacy").length,
  modules: modules.length,
};
