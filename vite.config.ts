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
        target: 'http://127.0.0.1:8000/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/data/, '') // 不可以省略rewrite
      }
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
              case '@vue':
              case 'pinia':
              case 'pdfjs-dist':
              case 'element-plus':
                return '_' + arr[0]
                break
              default:
                return '__vendor'
                break
            }
          }
        }
      }
    },
  },
  optimizeDeps: {
    include: ['pdfjs-dist'],
  },
})
