<!-- client/src/views/ProductsView.vue（产品中心：海信全品类智能家电） -->
<template>
  <div class="products-page">
    <!-- 页头 -->
    <div class="page-head">
      <div class="page-head-inner">
        <h1>产品中心</h1>
        <p class="head-sub">海信全品类智能家电，为美好生活而来 · 点击产品卡片即可咨询智能客服</p>
      </div>
    </div>

    <!-- 产品网格 -->
    <div class="products-main scroll-thin">
      <p class="section-title">全品类智能家电</p>
      <div class="product-grid">
        <div
          v-for="p in products"
          :key="p.label"
          class="product-card"
          @click="consult(p.label)"
        >
          <div class="product-img" :style="{ backgroundImage: `url(${p.img})` }"></div>
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
    path: '/chat',
    query: { q: `我想了解一下${label}，可以帮我推荐一下吗？` },
  });
};
</script>

<style scoped>
.products-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow: hidden;
}

/* 页头 */
.page-head {
  flex-shrink: 0;
  background: linear-gradient(120deg, rgba(47, 107, 255, 0.08), rgba(91, 140, 255, 0.06));
  border-bottom: 1px solid var(--haier-border);
}
.page-head-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 34px 24px;
  text-align: center;
}
.page-head h1 {
  font-size: 24px;
  font-weight: 700;
  color: var(--haier-text);
  letter-spacing: 2px;
}
.head-sub {
  margin-top: 10px;
  font-size: 13px;
  color: var(--haier-text-sub);
}

/* 产品网格 */
.products-main {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 16px 48px;
}
.section-title {
  margin-bottom: 20px;
  font-size: 18px;
  font-weight: 700;
  color: var(--haier-text);
  letter-spacing: 2px;
}
.product-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.product-card {
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius);
  overflow: hidden;
  cursor: pointer;
  transition: box-shadow .25s, transform .25s, border-color .25s;
}
.product-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-4px);
  border-color: var(--haier-primary);
}
.product-img {
  height: 220px;
  background-size: cover;
  background-position: center;
  background-color: var(--haier-bg);
}
.product-info { padding: 16px 18px 18px; }
.product-name { font-size: 16px; font-weight: 700; color: var(--haier-text); }
.product-desc {
  margin-top: 8px;
  font-size: 13px;
  color: var(--haier-text-sub);
  line-height: 1.6;
}
.product-cta {
  display: inline-flex;
  align-items: center;
  margin-top: 12px;
  padding: 5px 14px;
  border-radius: 999px;
  background: var(--haier-primary-tint);
  color: var(--haier-primary);
  font-size: 13px;
  font-weight: 600;
  transition: background .2s, color .2s;
}
.product-card:hover .product-cta {
  background: var(--haier-primary);
  color: #fff;
}
</style>