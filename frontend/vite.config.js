import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { join } from 'path'
import VueDevTools from 'vite-plugin-vue-devtools'

export default defineConfig({
  plugins: [
    vue(),
    // VueDevTools()
  ],
  server: {
    open: false,  //自动打开浏览器
    port: 8080,
  },
  resolve: {
    alias: {
      '@': join(__dirname, '/src')
    }
  },
})
