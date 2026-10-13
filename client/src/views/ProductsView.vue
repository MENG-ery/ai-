<!-- client/src/views/ProductsView.vue（产品中心：海尔全品类智能家电） -->
<template>
  <div class="products-page">
    <!-- 页头 -->
    <div class="page-head">
      <div class="page-head-inner">
        <h1>产品中心</h1>
        <p class="head-sub">海尔全品类智能家电，为美好生活而来 · 点击产品卡片即可咨询智能客服</p>
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
  { label: '海尔电视',       img: '/haier/dianshi.jpg',   desc: '全场景智慧屏，Mini LED 高画质，客厅娱乐中心' },
  { label: '海尔空调',       img: '/haier/kongtiao.jpg',  desc: '自清洁变频，新风净化，舒适健康又省电' },
  { label: '海尔冰箱',       img: '/haier/bingxiang.jpg', desc: '全空间保鲜，风冷无霜，锁住食材原鲜' },
  { label: '海尔洗衣机',     img: '/haier/xiyiji.jpg',    desc: '直驱变频，洗烘一体，除菌除螨更安心' },
  { label: '海尔冷柜',       img: '/haier/lenggui.jpg',   desc: '大容量强冷速冻，囤鲜无忧低噪省电' },
  { label: '海尔冰吧·酒柜',  img: '/haier/jiugui.jpg',    desc: '恒温储酒，独立控温，品味生活之选' },
  { label: '海尔热水器',     img: '/haier/reshuiqi.jpg',  desc: '速热恒温，安全防电墙，畅享沐浴' },
  { label: '海尔厨电',       img: '/haier/chufang.jpg',   desc: '烟灶联动，大吸力静音，净享烹饪' },
  { label: '海尔电脑',       img: '/haier/diannao.jpg',   desc: '轻薄办公，性能强劲，畅快高效' },
  { label: '海尔智能家居',   img: '/haier/jiqiren.jpg',   desc: '智慧互联，全屋联动，一句话操控' },
  { label: '海尔智慧家庭',   img: '/haier/shenghuo.jpg',  desc: '智家场景定制，让生活更美好' },
  { label: '海尔冰吧',       img: '/haier/bingba.jpg',    desc: '分区储藏，冷藏保鲜，即取即享' },
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