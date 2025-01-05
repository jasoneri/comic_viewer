import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { join } from 'path'
import os from 'os';
// import VueDevTools from 'vite-plugin-vue-devtools'

function getNetworkIp() {
  let needHost = '';
  try {
    const network = os.networkInterfaces();
    for (const dev in network) {
      const iface = network[dev];
      if (iface) { // 添加这个条件检查，确保iface有被定义
        for (let i = 0; i < iface.length; i++) {
          const alias = iface[i];
          if (
            alias.family === 'IPv4' &&
            alias.address !== '127.0.0.1' && !alias.internal &&
            alias.address.startsWith("192") && !alias.address.endsWith(".1")
          ) {needHost = alias.address;}
        }
      }
    }
  } catch (e) {needHost = 'localhost';}
  return needHost;
}


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
  define: {
    'import.meta.env.LAN_IP': JSON.stringify(`http://${getNetworkIp()}:${process.env.PORT || 12345}`),
  },
})
