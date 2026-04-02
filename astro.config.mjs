// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://hskf.dk',
  vite: {
    plugins: [tailwindcss()],
  },
  output: 'static',
  integrations: [sitemap()],
});
