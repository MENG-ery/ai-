<!-- client/src/views/ProductsView.vue（个人及家庭产品：海信全品类智能家电） -->
<template>
  <div class="haier-page">
    <!-- Hero 横幅（海报素材） -->
    <div class="hero-banner">
      <div class="hero-overlay"></div>
      <div class="hero-inner">
        <span class="hero-line"></span>
        <h1>个人及家庭产品</h1>
        <p class="hero-sub">海信全品类智能家电，为美好生活而来</p>
      </div>
    </div>

    <!-- 面包屑 -->
    <div class="crumbs">
      <router-link to="/">首页</router-link>
      <span class="sep">&gt;</span>
      <span class="cur">个人及家庭产品</span>
    </div>

    <!-- 产品网格 -->
    <div class="products-main">
      <p class="section-title">全品类智能家电</p>
      <p class="section-sub">点击产品卡片，即可咨询智能客服获取推荐</p>
      <div class="product-grid">
        <div
          v-for="p in products"
          :key="p.label"
          class="product-card"
          @click="consult(p.label)"
        >
          <div
            class="product-img"
            :style="{ backgroundImage: `url(${p.img})` }"
          ></div>
          <div class="product-info">
            <p class="product-name">{{ p.label }}</p>
            <p class="product-desc">{{ p.desc }}</p>
            <span class="product-cta">咨询这款产品 ›</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const products = [
  { label: '海信电视',     img: '/hisense/tv.jpg',      desc: '画质旗舰 智能大屏，ULED/Mini LED 显示技术' },
  { label: '海信空调',     img: '/hisense/air.jpg',     desc: '新风舒适 智能控温，净化除菌更健康' },
  { label: '海信冰箱',     img: '/hisense/fridge.jpg',  desc: '真空保鲜 超大容量，锁住营养不流失' },
  { label: '海信洗衣机',   img: '/hisense/wash.jpg',    desc: '洗烘一体 除菌除螨，AI 智慧投放' },
  { label: '海信冷柜·冰吧', img: '/hisense/freezer.jpg', desc: '风冷无霜 囤鲜无忧，-40℃ 深冷速冻' },
  { label: '海信厨卫',     img: '/hisense/kitchen.jpg', desc: '烟灶联动 净享烹饪，静音大吸力' },
  { label: '海信 UX 电视', img: '/hisense/tv-ux.jpg',    desc: 'RGB-Mini LED，跨代引领 万色生辉' },
  { label: '海信大力神空调 U6', img: '/hisense/air-u6.jpg', desc: '超大新风 神机妙算，强劲制冷热' },
  { label: '海信空调智慧风 E5L', img: '/hisense/air-e5l.jpg', desc: '滑启智慧风，主动识人防直吹' },
  { label: '海信洗衣机大薄荷 2.0', img: '/hisense/wash-2e5s.jpg', desc: '自由组合 衣鞋同净，除菌除螨' },
  { label: '海信静烟机',   img: '/hisense/range-hood.jpg', desc: '行业静烟机开创者，安静无油烟' },
  { label: 'AI 真空净味冰箱', img: '/hisense/fridge-ai.jpg', desc: '嗅出异味 管理新鲜，真空保鲜' },
];

const consult = (label) => {
  router.push({
    path: '/',
    query: { ask: `我想了解一下${label}，可以帮我推荐一下吗？` },
  });
};
</script>

<style scoped>
.haier-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", sans-serif;
}

.hero-banner {
  position: relative;
  width: 100%;
  padding: 104px 0 92px;
  flex-shrink: 0;
  overflow: hidden;
  background: url('/haier/haibao1.webp') center / cover no-repeat;
  background-color: #0c5ca8;
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: rgba(12, 92, 168, 0.5);
}
.hero-inner {
  position: relative;
  z-index: 2;
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}
.hero-line {
  display: block;
  width: 44px;
  height: 6px;
  margin: 0 auto 18px;
  background: #fff;
  border-radius: 3px;
}
.hero-inner h1 {
  font-size: 34px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 4px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}
.hero-sub {
  margin-top: 12px;
  font-size: 16px;
  color: #eaf2fc;
  letter-spacing: 2px;
}

.crumbs {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 44px;
  padding: 0 40px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
  font-size: 13px;
  color: var(--haier-text-sub);
  flex-shrink: 0;
}
.crumbs a { color: var(--haier-text-sub); text-decoration: none; }
.crumbs a:hover { color: var(--haier-primary); }
.crumbs .sep { color: var(--haier-text-faint); }
.crumbs .cur { color: var(--haier-primary); }

.products-main {
  flex: 1;
  overflow-y: auto;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 16px 48px;
}
.section-title {
  position: relative;
  padding: 12px 0 8px;
  font-size: 22px;
  font-weight: 700;
  color: var(--haier-text);
  text-align: center;
  letter-spacing: 2px;
}
.section-title::before {
  content: "";
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 34px;
  height: 5px;
  background: var(--haier-primary);
  border-radius: 2px;
}
.section-sub {
  margin-bottom: 24px;
  font-size: 13px;
  color: var(--haier-text-weak);
  text-align: center;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.product-card {
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow .25s, transform .25s;
}
.product-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-4px);
}
.product-img {
  height: 240px;
  background-size: cover;
  background-position: center;
  background-color: #eef2f7;
}
.product-info {
  padding: 16px 18px 18px;
}
.product-name {
  font-size: 16px;
  font-weight: 700;
  color: var(--haier-text);
}
.product-desc {
  margin-top: 8px;
  font-size: 13px;
  color: var(--haier-text-weak);
  line-height: 1.6;
}
.product-cta {
  display: inline-block;
  margin-top: 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--haier-primary);
}
</style>
