import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  clearScreen: false,
  server: {
    port: 6173,
    proxy: {
      '/data': {
        target: 'http://127.0.0.1:13956/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/data/, '')
      },
      '/resource': {
        target: 'http://127.0.0.1:13956/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/resource/, '')
      }
    }
  },
  resolve: {
    alias: {
      'custom-types': '/src/@types/custom-types.d.ts',
      'tab-types': '/src/@types/tab-types.d.ts',
      'config-types': '/src/@types/config-types.d.ts',
      'pdfjs-dist-types': '/src/@types/pdfjs-dist-types.d.ts',
      'resource-types': '/src/@types/resource-types.d.ts',
      'event-types': '/src/@types/event-types.d.ts'
    }
  },
  build: {
    rollupOptions: {
      input: {
        index: 'index.html',
      },
      output: {
        manualChunks(id) {
          if (id.includes('node_modules')) {
            const arr = id.toString().split('node_modules/')[1].split('/')
            switch (arr[0]) {
              case 'element-plus':
                return '_' + arr[0]
              case 'pdfjs-dist':
                if (id.includes('pdf.worker')) {
                  return '_pdfjs_worker';
                }
                return '_pdfjs';
              default:
                return '_vendor'
            }
          }
        }
      }
    },
    chunkSizeWarningLimit: 1100,
  },
  optimizeDeps: {
    include: ['pdfjs-dist'],
  },
})
