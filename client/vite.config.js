// client/vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: ['.cosmoplat.cn', '.cosmoplat.com', '.cosmoplat.net'],
    proxy: {
      '/api': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      },
      // 海信官方商城图片有防盗链，浏览器直连会 403；由开发服务器带合法 Referer 代理
      '/hisense-img': {
        target: 'https://img.shop.hisense.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/hisense-img/, ''),
        headers: {
          Referer: 'https://www.hisense.com/',
          'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
      },
      // 海尔官方商城图片同样有防盗链，需带 haier.com Referer 代理
      '/haier-img': {
        target: 'https://image.haier.com',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/haier-img/, ''),
        headers: {
          Referer: 'https://www.haier.com/',
          'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        },
      },
    },
  },
});
