<!-- client/src/App.vue -->
<template>
  <div id="app">
    <nav class="haier-nav">
      <router-link to="/" class="nav-brand">
        <span class="brand-logo">购</span>
        <span class="brand-name">极速购<span class="brand-sub">AI 客服</span></span>
      </router-link>
      <div class="nav-links">
        <router-link to="/">首页</router-link>
        <router-link to="/products">个人及家庭产品</router-link>
      </div>
      <span class="nav-phone">客服热线 95179</span>
    </nav>
    <main class="page-body">
      <router-view />
    </main>
    <footer class="haier-footer">
      <span>© 2026 极速购 版权所有 | 家生活全场景服务，定制美好生活</span>
    </footer>
  </div>
</template>

<style>
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

/* ─── 海尔风格顶栏（白底 80px，当前项底部蓝色短条） ─── */
.haier-nav {
  display: flex;
  align-items: center;
  gap: 40px;
  padding: 0 40px;
  height: 64px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
  position: sticky;
  top: 0;
  z-index: 100;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.brand-logo {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--haier-primary);
  color: #fff;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}
.brand-name {
  font-size: 17px;
  font-weight: 700;
  color: var(--haier-text);
  letter-spacing: 1px;
}
.brand-sub {
  font-size: 12px;
  font-weight: 400;
  color: var(--haier-primary);
  margin-left: 6px;
  letter-spacing: 0;
}
.nav-links {
  display: flex;
  gap: 2px;
}
.nav-links a {
  position: relative;
  padding: 20px 16px;
  color: var(--haier-text);
  text-decoration: none;
  font-size: 15px;
  font-weight: 700;
  transition: color .2s;
}
.nav-links a:hover { color: var(--haier-primary); }
.nav-links a.router-link-active {
  color: var(--haier-primary);
}
.nav-links a.router-link-active::after {
  content: "";
  position: absolute;
  left: 16px;
  right: 16px;
  bottom: 0;
  height: 4px;
  background: var(--haier-primary);
  border-radius: 2px;
}
.nav-phone {
  margin-left: auto;
  font-size: 13px;
  color: var(--haier-text-weak);
  letter-spacing: 1px;
}

/* 主体区与页脚 */
.page-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.haier-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 18px 0;
  background: #f6f7f9;
  border-top: 1px solid var(--haier-border);
  color: var(--haier-text-weak);
  font-size: 12px;
  letter-spacing: 0.5px;
}
</style>
