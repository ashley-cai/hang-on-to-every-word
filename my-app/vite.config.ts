import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  plugins: [sveltekit()],
  optimizeDeps: {
    exclude: ['p5-svelte'], // don’t prebundle it
  },
  ssr: {
    noExternal: ['p5-svelte'], // force it to be bundled and compiled
  }
});