// client/vite.config.js
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

const PORT = 5173;
const HOST = '0.0.0.0';
const ALLOWED_HOSTS = ['.cosmoplat.cn', '.cosmoplat.com', '.cosmoplat.net'];

// 前端开发/预览都需要把 /api 转发到 Python 后端，并代理带防盗链的商品图
const PROXY = {
  '/api': {
    target: 'http://localhost:3000',
    changeOrigin: true,
  },
  // 海信官方商城图片有防盗链，浏览器直连会 403；由服务器带合法 Referer 代理
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
};

export default defineConfig({
  plugins: [vue()],
  server: {
    host: HOST,
    port: PORT,
    allowedHosts: ALLOWED_HOSTS,
    proxy: PROXY,
  },
  // 生产预览：serve 已构建的 dist，SPA 回退到 index.html（根路径即首页，不列目录）
  preview: {
    host: HOST,
    port: PORT,
    strictPort: true,
    allowedHosts: ALLOWED_HOSTS,
    proxy: PROXY,
  },
});
