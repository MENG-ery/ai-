// client/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import ChatView    from '../views/ChatView.vue';
import AgentView   from '../views/AgentView.vue';
import RagView     from '../views/RagView.vue';
import GraphView   from '../views/GraphView.vue';
import ProductsView from '../views/ProductsView.vue';

const routes = [
  { path: '/',         component: ChatView,     meta: { title: '首页' } },
  { path: '/agent',    component: AgentView,    meta: { title: 'Agent 订单查询' } },
  { path: '/rag',      component: RagView,      meta: { title: '知识库问答' } },
  { path: '/graph',    component: GraphView,    meta: { title: '多 Agent 中枢' } },
  { path: '/products', component: ProductsView, meta: { title: '个人及家庭产品' } },
];

export default createRouter({
  history: createWebHistory(),
  routes,
});
