<!-- client/src/App.vue -->
<template>
  <div id="app">
    <!-- 顶栏 -->
    <header class="topbar">
      <div class="topbar-inner">
        <router-link to="/" class="brand">
          <img class="brand-logo-img" src="/brand-fumanhai.png" alt="服满海" />
        </router-link>
        <span class="brand-badge">AI 客服</span>
        <div class="topbar-right">
          <span class="online-chip"><i class="dot-online"></i>7×24 在线</span>
          <span class="phone">客服热线 95179</span>
        </div>
      </div>
    </header>

    <!-- 主体：左导航 + 内容 -->
    <div class="app-body">
      <nav class="sidebar">
        <router-link v-for="s in sections" :key="s.path" :to="s.path" class="side-link">
          <span class="side-icon">{{ s.icon }}</span>
          <span class="side-meta">
            <span class="side-title">{{ s.title }}</span>
            <span class="side-desc">{{ s.desc }}</span>
          </span>
        </router-link>

        <div class="sidebar-foot">
          <div class="model-wrap">
            <button class="model-bar" @click.stop="showModelMenu = !showModelMenu">
              <span class="model-dot"></span>
              <span class="model-meta">
                <span class="model-label">当前大模型</span>
                <span class="model-name">{{ currentModelDisplay() }}</span>
              </span>
              <span class="model-arrow">⌄</span>
            </button>
            <div v-if="showModelMenu" class="model-menu">
              <button
                v-for="p in PROVIDERS"
                :key="p.name"
                class="model-opt"
                @click="applyProvider(p); showModelMenu = false"
              >
                <span class="model-opt-name">{{ p.name }}</span>
                <span class="model-opt-sub">{{ p.model }}</span>
              </button>
              <router-link to="/settings" class="model-opt model-opt-link" @click="showModelMenu = false">
                设置页自定义 ›
              </router-link>
            </div>
          </div>
          <router-link to="/settings" class="foot-link">设置</router-link>
          <p class="foot-title">服满海 AI 客服</p>
          <p class="foot-desc">家生活全场景服务，定制美好生活</p>
        </div>
      </nav>

      <main class="page-body">
        <router-view />
      </main>
    </div>

    <footer class="footer">
      <span>© 2026 服满海 版权所有 | 家生活全场景服务，定制美好生活</span>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useModel } from './composables/useModel.js';

const { PROVIDERS, currentModelDisplay, applyProvider } = useModel();
const showModelMenu = ref(false);

const sections = [
  { path: '/',         icon: '问', title: '智能客服', desc: '对话咨询' },
  { path: '/rag',      icon: '知', title: '知识库', desc: '海尔产品' },
  { path: '/products', icon: '品', title: '产品中心', desc: '全品类家电' },
];
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: var(--haier-bg);
}

/* ─── 顶栏 ─── */
.topbar {
  flex-shrink: 0;
  height: 60px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.topbar-inner {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  gap: 20px;
}
.brand {
  display: flex;
  align-items: center;
  text-decoration: none;
}
.brand-logo-img {
  height: 34px;
  width: auto;
  display: block;
}
.brand-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--haier-primary-tint);
  color: var(--haier-primary);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 1px;
}
.topbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 16px;
}
.online-chip {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.1);
  color: #0b9a66;
  font-size: 12px;
  font-weight: 600;
}
.phone {
  font-size: 13px;
  color: var(--haier-text-sub);
  letter-spacing: 1px;
}

/* ─── 主体 ─── */
.app-body {
  flex: 1;
  display: flex;
  min-height: 0;
}

/* 侧边导航 */
.sidebar {
  width: 236px;
  flex-shrink: 0;
  background: #fff;
  border-right: 1px solid var(--haier-border);
  display: flex;
  flex-direction: column;
  padding: 16px 12px;
  overflow-y: auto;
}
.side-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 11px 12px;
  border-radius: 12px;
  margin-bottom: 4px;
  text-decoration: none;
  transition: background .2s;
}
.side-link:hover { background: var(--haier-bg); }
.side-link.router-link-active { background: var(--haier-primary-tint); }
.side-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 700;
  background: var(--haier-bg);
  color: var(--haier-text-sub);
}
.side-link.router-link-active .side-icon {
  background: var(--haier-primary);
  color: #fff;
  box-shadow: 0 6px 14px -4px rgba(47, 107, 255, 0.5);
}
.side-meta { display: flex; flex-direction: column; min-width: 0; }
.side-title { font-size: 14px; font-weight: 600; color: var(--haier-text); }
.side-desc { font-size: 11px; color: var(--haier-text-faint); margin-top: 2px; }
.sidebar-foot {
  margin-top: auto;
  padding: 14px 8px 4px;
  border-top: 1px solid var(--haier-border);
}
.foot-title { font-size: 13px; font-weight: 700; color: var(--haier-text); }
.foot-desc { font-size: 11px; color: var(--haier-text-faint); margin-top: 4px; line-height: 1.5; }

/* 左下角大模型栏 */
.model-wrap { position: relative; margin-bottom: 12px; }
.model-bar {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 10px;
  background: var(--haier-primary-tint);
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius-sm);
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  transition: border-color .2s, box-shadow .2s;
}
.model-bar:hover { border-color: var(--haier-primary); box-shadow: var(--haier-shadow); }
.model-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--haier-emerald);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.18);
  flex-shrink: 0;
}
.model-meta { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.model-label { font-size: 10px; color: var(--haier-text-faint); letter-spacing: 1px; }
.model-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--haier-primary-d);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.model-arrow { font-size: 12px; color: var(--haier-text-faint); flex-shrink: 0; }

.model-menu {
  position: absolute;
  left: 0;
  right: 0;
  bottom: calc(100% + 6px);
  z-index: 60;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius-sm);
  box-shadow: var(--haier-shadow);
  padding: 6px;
}
.model-opt {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 10px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  text-align: left;
}
.model-opt:hover { background: var(--haier-primary-tint); }
.model-opt-name { font-size: 13px; font-weight: 600; color: var(--haier-text); }
.model-opt-sub { font-size: 11px; color: var(--haier-text-faint); }
.model-opt-link {
  display: block;
  margin-top: 4px;
  padding: 8px 10px;
  font-size: 12px;
  color: var(--haier-primary);
  text-decoration: none;
  border-radius: 8px;
}
.model-opt-link:hover { background: var(--haier-primary-tint); }
.foot-link {
  display: inline-block;
  margin-bottom: 10px;
  padding: 4px 12px;
  border-radius: 999px;
  background: var(--haier-bg);
  color: var(--haier-text-sub);
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  transition: all .2s;
}
.foot-link:hover { background: var(--haier-primary-tint); color: var(--haier-primary); }

/* 内容区 */
.page-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

/* 页脚 */
.footer {
  flex-shrink: 0;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  border-top: 1px solid var(--haier-border);
  color: var(--haier-text-faint);
  font-size: 12px;
}
</style>