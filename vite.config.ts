import path from 'path'
import { defineConfig } from 'vite'
import topLevelAwait from "vite-plugin-top-level-await"
import vue from '@vitejs/plugin-vue'
import wasm from "vite-plugin-wasm"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), wasm(), topLevelAwait()],
  clearScreen: false,
  server: {
    port: 3000,
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
      '@': path.resolve(__dirname, 'src'),
      'pdfjs-dist-types': '/src/@types/pdfjs-dist-types.d.ts',
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
    exclude: ['md_wasm', 'sim'],
  },
})
