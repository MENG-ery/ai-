<!--
  极速购 AI 客服 · 首页
  Hero 风景图轮播 + 搜索框 + 热门问题 + 产品图片墙
  检索后跳转到独立对话页 /chat
-->
<template>
  <div class="home-page scroll-thin">
    <!-- Hero 横幅：风景图轮播（保留） -->
    <div class="hero-banner">
      <div
        v-for="(img, i) in heroImages"
        :key="i"
        class="hero-slide"
        :class="{ active: i === heroIndex }"
        :style="{ backgroundImage: `url(${img})` }"
      ></div>
      <div class="hero-overlay"></div>
      <div class="hero-inner">
        <span class="hero-line"></span>
        <p class="hero-sub">家生活全场景服务，定制美好生活</p>
      </div>
      <div class="hero-dots">
        <span
          v-for="(img, i) in heroImages"
          :key="i"
          :class="{ active: i === heroIndex }"
          @click="heroIndex = i"
        ></span>
      </div>
    </div>

    <!-- 搜索区 -->
    <div class="home-stage">
      <div class="search-inner">
        <div class="welcome-text">
          <h1 class="welcome-title">您好！我是极速购智能客服小购</h1>
          <p class="welcome-sub">您可以咨询购物、订单、物流等问题，也可以从下方热门问题开始</p>
        </div>

        <div class="search-box">
          <span class="search-icon"></span>
          <input
            v-model="searchText"
            placeholder="请输入您的问题，如：我的订单到哪了？"
            @keydown.enter="handleSearch"
          />
          <button class="btn-primary search-btn" @click="handleSearch">
            搜索
          </button>
        </div>

        <div class="hot-section">
          <p class="hot-label">热门问题</p>
          <div class="hot-words">
            <button
              v-for="q in hotWords"
              :key="q"
              class="haier-chip"
              @click="goAsk(q)"
            >
              {{ q }}
            </button>
          </div>
        </div>

        <!-- 产品图片墙 -->
        <div v-if="homeProducts.length" class="product-wall">
          <p class="wall-title">热销家电抢先看</p>
          <div class="wall-grid">
            <div
              v-for="p in homeProducts"
              :key="p.id"
              class="wall-card"
            >
              <span class="wall-img">
                <img :src="p.image" :alt="p.name" loading="lazy" @error="imgErr($event)" />
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const searchText = ref('');

const hotWords = [
  '推荐一款性价比高的冰箱？',
  '空调怎么选？新一级能效有什么好处？',
  '洗衣机洗烘一体值得买吗？',
  '想买一台观影效果好的电视',
  '家电保修政策是怎样的？',
  '如何选择适合自己的家电？',
];

/* ─── Hero 风景图轮播（保留） ─── */
const heroImages = [
  'https://picsum.photos/seed/haier-landscape-1/2400/600',
  'https://picsum.photos/seed/haier-landscape-2/2400/600',
  'https://picsum.photos/seed/haier-landscape-3/2400/600',
  'https://picsum.photos/seed/haier-landscape-4/2400/600',
];
const heroIndex = ref(0);
let heroTimer = null;

onMounted(() => {
  heroTimer = setInterval(() => {
    heroIndex.value = (heroIndex.value + 1) % heroImages.length;
  }, 5000);
  loadHomeProducts();
});
onUnmounted(() => {
  if (heroTimer) clearInterval(heroTimer);
});

/* ─── 首页产品图片墙 ─── */
const homeProducts = ref([]);

const loadHomeProducts = async () => {
  try {
    const res = await fetch('/hisense/products.json');
    const list = await res.json();
    const picks = list.filter((p) => p.price && p.price >= 500 && p.image).slice(0, 12);
    homeProducts.value = picks;
  } catch (e) {
    console.error('加载产品墙失败', e);
  }
};

const imgErr = (e) => {
  e.target.style.visibility = 'hidden';
};

/* ─── 跳转对话 ─── */
const goAsk = (q) => {
  if (!q || !q.trim()) return;
  router.push({ path: '/chat', query: { q: q.trim() } });
};

const handleSearch = () => {
  goAsk(searchText.value);
  searchText.value = '';
};
</script>

<style scoped>
.home-page {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  background: var(--haier-bg);
}

/* ─── Hero 横幅：风景图轮播（保留原样） ─── */
.hero-banner {
  position: relative;
  width: 100%;
  padding: 130px 0 150px;
  flex-shrink: 0;
  overflow: hidden;
}
.hero-slide {
  position: absolute;
  inset: 0;
  background-size: cover;
  background-position: center 40%;
  opacity: 0;
  transition: opacity 1.2s ease;
}
.hero-slide.active { opacity: 1; }
.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(24, 43, 86, 0.72), rgba(47, 107, 255, 0.55));
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
.hero-sub {
  margin-top: 4px;
  font-size: 34px;
  font-weight: 700;
  color: #fff;
  letter-spacing: 4px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
}
.hero-dots {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 18px;
  z-index: 3;
  display: flex;
  justify-content: center;
  gap: 10px;
}
.hero-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: background .3s, transform .3s;
}
.hero-dots span.active {
  background: #fff;
  transform: scale(1.2);
}

/* ─── 搜索区（自然滚动，不被压缩） ─── */
.home-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 0 60px;
}
.search-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  width: 100%;
  max-width: 1040px;
  padding: 36px 28px 0;
  margin-top: -110px;
  position: relative;
  z-index: 5;
}
.welcome-text {
  padding: 26px 40px;
  border-radius: var(--haier-radius);
  background: #fff;
  box-shadow: var(--haier-shadow);
  text-align: center;
}
.welcome-title { font-size: 22px; font-weight: 700; color: var(--haier-text); letter-spacing: 1px; }
.welcome-sub { margin-top: 10px; font-size: 14px; color: var(--haier-text-sub); }

.search-box {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 760px;
  background: #fff;
  border: 2px solid var(--haier-border-2);
  border-radius: 999px;
  overflow: hidden;
  box-shadow: var(--haier-shadow);
  transition: border-color .2s, box-shadow .25s;
  flex-shrink: 0;
}
.search-box:focus-within {
  border-color: var(--haier-primary);
  box-shadow: 0 12px 32px -8px rgba(47, 107, 255, 0.28);
}
.search-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-left: 22px;
  border: 2px solid var(--haier-primary);
  border-radius: 50%;
  position: relative;
}
.search-icon::after {
  content: "";
  position: absolute;
  right: -6px;
  bottom: -4px;
  width: 7px;
  height: 2px;
  background: var(--haier-primary);
  transform: rotate(45deg);
}
.search-box input {
  flex: 1;
  min-width: 0;
  border: none;
  outline: none;
  padding: 18px 18px 18px 14px;
  font-size: 16px;
  font-family: inherit;
  color: var(--haier-text);
  background: transparent;
}
.search-box input::placeholder { color: var(--haier-text-faint); }
.search-btn {
  margin: 6px;
  padding: 0 32px;
  height: 46px;
  flex-shrink: 0;
  font-size: 15px;
  letter-spacing: 2px;
}

.hot-section { width: 100%; max-width: 880px; text-align: center; }
.hot-label {
  display: inline-block;
  padding: 0 14px;
  margin-bottom: 16px;
  border-radius: 999px;
  background: var(--haier-primary-tint);
  color: var(--haier-primary);
  font-size: 13px;
  font-weight: 600;
  letter-spacing: 2px;
  line-height: 26px;
}
.hot-words {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}
.hot-words .haier-chip { padding: 9px 18px; font-size: 13px; }

/* ─── 首页产品图片墙：一行 3 个，大图 ─── */
.product-wall {
  width: 100%;
  max-width: 960px;
  margin-top: 24px;
}
.wall-title {
  position: relative;
  display: inline-block;
  padding: 0 14px;
  margin-bottom: 18px;
  border-radius: 999px;
  background: #fff;
  color: var(--haier-primary);
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 2px;
  line-height: 30px;
  box-shadow: var(--haier-shadow);
}
.wall-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}
.wall-card {
  display: block;
  padding: 14px;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius);
  transition: box-shadow .25s, transform .25s, border-color .25s;
}
.wall-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-4px);
  border-color: var(--haier-primary);
}
.wall-img {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
}
.wall-img img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform .3s;
}
.wall-card:hover .wall-img img { transform: scale(1.06); }
</style>