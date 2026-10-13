// client/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ChatView    from '../views/ChatView.vue';
import ChatPage    from '../views/ChatPage.vue';
import RagView     from '../views/RagView.vue';
import ProductsView from '../views/ProductsView.vue';
import SettingsView from '../views/SettingsView.vue';

const routes = [
  { path: '/',         component: ChatView,     meta: { title: '首页' } },
  { path: '/chat',     component: ChatPage,     meta: { title: '智能客服对话' } },
  { path: '/rag',      component: RagView,      meta: { title: '知识库' } },
  { path: '/products', component: ProductsView, meta: { title: '个人及家庭产品' } },
  { path: '/settings', component: SettingsView, meta: { title: '设置' } },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
