import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    open: true,
    host: '0.0.0.0',
    proxy: {
      '/auth': { target: 'http://api:8000', changeOrigin: true },
      '/users': { target: 'http://api:8000', changeOrigin: true },
      '/resumes': { target: 'http://api:8000', changeOrigin: true },
    },
  },
})

