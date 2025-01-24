import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': '/src', // Opcional, para simplificar imports  
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000', // URL del backend
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
});