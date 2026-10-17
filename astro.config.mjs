import { defineConfig } from "astro/config";

// GitHub Pages: https://felipebarraza6.github.io/yggdra-web/
export default defineConfig({
  site: "https://felipebarraza6.github.io",
  base: "/yggdra-web",
  trailingSlash: "always",
  build: {
    format: "directory",
  },
});
