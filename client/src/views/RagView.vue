<!-- client/src/views/RagView.vue（现代 AI 客服风格：页头 + 商品分类 + 海尔商品库 + 聊天问答） -->
<template>
  <div class="rag-page">
    <!-- 页头 -->
    <div class="page-head">
      <div class="page-head-inner">
        <h1>知识库 · 海尔官方商城商品</h1>
        <p class="head-sub">共 {{ products.length }} 款商品（名称 / 型号 / 价格，来源海尔官方商城），可搜索筛选并咨询智能客服</p>
      </div>
    </div>

    <!-- 横向主区域 -->
    <div class="dialogue-stage">
      <!-- 商品分类 -->
      <aside class="module-side">
        <p class="side-heading">商品分类</p>
        <div class="module-grid">
          <button
            v-for="cat in categories"
            :key="cat.key"
            class="module-card"
            :class="{ active: activeCat === cat.key }"
            @click="activeCat = cat.key"
          >
            <span class="module-icon">{{ cat.icon }}</span>
            <span class="module-title">{{ cat.label }}</span>
            <span class="module-desc">{{ cat.count }} 款</span>
          </button>
        </div>
      </aside>

      <!-- 商品列表 -->
      <section class="product-panel card">
        <header class="panel-header">
          <div class="search-box">
            <span class="search-icon"></span>
            <input v-model="keyword" placeholder="搜索商品名称或型号，如：冰箱 / KFR-" />
          </div>
          <span class="result-count">{{ filterProducts.length }} 款</span>
        </header>
        <main class="product-list scroll-thin">
          <div
            v-for="p in filterProducts"
            :key="p.id"
            class="product-card"
            @click="askProduct(p)"
          >
            <div class="thumb">
              <img :src="p.image" :alt="p.name" loading="lazy" @error="imgErr($event)" />
            </div>
            <div class="info">
              <p class="name">{{ p.name }}</p>
              <span class="model">型号：{{ p.model }}</span>
              <div class="bottom">
                <span class="price">¥{{ fmt(p.price) }}</span>
                <span class="ask">咨询 ›</span>
              </div>
            </div>
          </div>
          <div v-if="filterProducts.length === 0" class="empty">未找到相关商品</div>
        </main>
      </section>

      <!-- 聊天问答 -->
      <section class="chat-panel card">
        <header class="chat-header">
          <div class="header-left">
            <span class="avatar">购</span>
            <div class="header-info">
              <span class="agent-name">服满海知识库助手</span>
              <span class="status" :class="{ active: !loading }">
                {{ loading ? '查询中...' : '在线' }}
              </span>
            </div>
          </div>
          <button class="btn-line" @click="clearMessages">清空</button>
        </header>

        <main class="messages-wrap scroll-thin" ref="messagesRef">
          <div v-if="messages.length === 0" class="welcome">
            <span class="welcome-avatar">购</span>
            <p class="welcome-text">您好，我是服满海知识库助手。</p>
            <p class="welcome-sub">点击左侧商品即可向我提问，或直接输入关于海尔商品的任何问题。</p>
          </div>

          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message-row"
            :class="msg.role"
          >
            <div class="avatar-sm">{{ msg.role === 'user' ? '我' : '购' }}</div>
            <div class="message-content">
              <div v-if="msg.loading" class="bubble loading-bubble">
                <span class="dot" /><span class="dot" /><span class="dot" />
              </div>
              <div v-else class="bubble">{{ msg.content }}</div>
              <div v-if="msg.sources && msg.sources.length" class="sources-wrap">
                <span class="sources-label">参考来源</span>
                <span v-for="(src, si) in msg.sources" :key="si" class="source-tag">
                  {{ src.source }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="error" class="error-tip">{{ error }}</div>
        </main>

        <footer class="input-area">
          <textarea
            v-model="inputText"
            placeholder="输入问题，Enter 发送"
            :disabled="loading"
            @keydown.enter.exact.prevent="handleSend"
            rows="1"
          />
          <button
            class="send-btn"
            :disabled="loading || !inputText.trim()"
            @click="handleSend"
          >
            {{ loading ? '查询中...' : '发送' }}
          </button>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRag } from '../composables/useRag.js';
import { resolveImage } from '../utils/image.js';

const { messages, loading, error, ask, clearMessages } = useRag();

const inputText   = ref('');
const messagesRef = ref(null);

/* ─── 商品数据 ─── */
const products = ref([]);
const keyword  = ref('');
const activeCat = ref('all');

const categories = computed(() => {
  const def = [
    { key: 'all',  label: '全部',   icon: '全' },
    { key: 'tv',   label: '电视',   icon: '视' },
    { key: 'ac',   label: '空调',   icon: '空' },
    { key: 'fridge', label: '冰箱', icon: '冰' },
    { key: 'washer', label: '洗衣机', icon: '洗' },
    { key: 'freezer', label: '冷柜·酒柜', icon: '冷' },
    { key: 'kitchen', label: '厨卫', icon: '厨' },
    { key: 'water', label: '热水器', icon: '热' },
    { key: 'dish',  label: '洗碗机', icon: '碗' },
    { key: 'other', label: '其他',   icon: '品' },
  ];
  const names = categoriesNames.value;
  return def.map((c) => ({
    ...c,
    count: computed(() => filterByCat(c.key)).value.length,
    _names: names[c.key],
  }));
});

const categoriesNames = computed(() => {
  const map = { all: [], tv: [], ac: [], fridge: [], washer: [], freezer: [], kitchen: [], water: [], dish: [], other: [] };
  for (const p of products.value) {
    const key = catOf(p.name);
    map[key].push(p);
  }
  return map;
});

function catOf(name) {
  if (!name) return 'other';
  if (name.includes('电视') || name.includes('视') || name.includes('激光')) return 'tv';
  if (name.includes('空调') || name.includes('KFR')) return 'ac';
  if (name.includes('冰箱') || name.includes('BCD') || name.includes('冷藏')) return 'fridge';
  if (name.includes('洗衣机') || name.includes('滚筒') || name.includes('洗烘')) return 'washer';
  if (name.includes('冷柜') || name.includes('酒柜') || name.includes('冰吧') || name.includes('BD/BC')) return 'freezer';
  if (name.includes('油烟机') || name.includes('燃气灶') || name.includes('烟机') || name.includes('灶') || name.includes('蒸烤') || name.includes('烤箱')) return 'kitchen';
  if (name.includes('热水器') || name.includes('净水') || name.includes('壁挂炉')) return 'water';
  if (name.includes('洗碗机')) return 'dish';
  return 'other';
}

function filterByCat(key) {
  if (key === 'all') return products.value;
  return products.value.filter((p) => catOf(p.name) === key);
}

const filterProducts = computed(() => {
  const kw = keyword.value.trim().toLowerCase();
  let list = filterByCat(activeCat.value);
  if (kw) {
    list = list.filter(
      (p) =>
        p.name.toLowerCase().includes(kw) ||
        (p.model || '').toLowerCase().includes(kw),
    );
  }
  return list;
});

const fmt = (num) => {
  if (num == null) return '咨询';
  return num.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

const imgErr = (e) => {
  e.target.style.visibility = 'hidden';
};

/* ─── 交互 ─── */
const askProduct = (p) => {
  inputText.value = `我想了解海尔商品「${p.name}」，型号 ${p.model}，价格是多少？有什么特点？`;
  handleSend();
};

const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value)
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
};

const handleSend = async () => {
  const text = inputText.value.trim();
  if (!text || loading.value) return;
  inputText.value = '';
  await ask(text, scrollToBottom);
};

onMounted(async () => {
  try {
    const res = await fetch('/haier/products.json');
    const list = await res.json();
    products.value = list.map((p) => ({ ...p, image: resolveImage(p.image) }));
  } catch (e) {
    console.error('加载商品数据失败', e);
  }
});
</script>

<style scoped>
.rag-page {
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
  max-width: 1400px;
  margin: 0 auto;
  padding: 26px 24px;
  text-align: center;
}
.page-head h1 {
  font-size: 22px;
  font-weight: 700;
  color: var(--haier-text);
  letter-spacing: 2px;
}
.head-sub {
  margin-top: 10px;
  font-size: 13px;
  color: var(--haier-text-sub);
}

/* 横向主区域 */
.dialogue-stage {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 16px;
  min-height: 0;
  overflow: hidden;
  padding: 16px;
  background: var(--haier-bg);
}

/* 分类 */
.module-side {
  width: 150px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.side-heading {
  padding: 4px 4px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--haier-text-faint);
  letter-spacing: 2px;
}
.module-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.module-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 14px 8px;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius-sm);
  cursor: pointer;
  font-family: inherit;
  text-align: center;
  transition: all .2s;
}
.module-card:hover {
  box-shadow: var(--haier-shadow);
  border-color: var(--haier-primary);
}
.module-card.active {
  background: var(--haier-primary-tint);
  border-color: var(--haier-primary);
}
.module-icon {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: linear-gradient(135deg, #2f6bff, #5b8cff);
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 14px -4px rgba(47, 107, 255, 0.4);
}
.module-title { font-size: 13px; font-weight: 700; color: var(--haier-text); }
.module-desc { font-size: 11px; color: var(--haier-text-faint); }

/* 商品面板 */
.product-panel {
  width: 460px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  border-radius: var(--haier-radius);
  overflow: hidden;
}
.panel-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
}
.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid var(--haier-border-2);
  border-radius: 999px;
  background: var(--haier-bg);
  padding: 0 12px;
  transition: border-color .2s, box-shadow .2s;
}
.search-box:focus-within {
  border-color: var(--haier-primary);
  box-shadow: 0 0 0 3px rgba(47, 107, 255, 0.12);
}
.search-icon {
  width: 12px;
  height: 12px;
  border: 2px solid var(--haier-text-faint);
  border-radius: 50%;
  position: relative;
  flex-shrink: 0;
}
.search-icon::after {
  content: "";
  position: absolute;
  right: -5px;
  bottom: -3px;
  width: 5px;
  height: 2px;
  background: var(--haier-text-faint);
  transform: rotate(45deg);
}
.search-box input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 13px;
  font-family: inherit;
  color: var(--haier-text);
  padding: 8px 0;
}
.search-box input::placeholder { color: var(--haier-text-faint); }
.result-count { font-size: 12px; color: var(--haier-text-faint); flex-shrink: 0; }

.product-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: var(--haier-bg);
}
.product-card {
  display: flex;
  gap: 12px;
  padding: 10px;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius-sm);
  cursor: pointer;
  transition: box-shadow .2s, transform .2s, border-color .2s;
}
.product-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-2px);
  border-color: var(--haier-primary);
}
.thumb {
  width: 76px;
  height: 76px;
  flex-shrink: 0;
  border-radius: 10px;
  overflow: hidden;
  background: var(--haier-bg);
}
.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.name {
  font-size: 13px;
  font-weight: 600;
  color: var(--haier-text);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.model {
  margin-top: 4px;
  width: fit-content;
  padding: 2px 8px;
  border-radius: 999px;
  background: var(--haier-primary-tint);
  color: var(--haier-primary);
  font-size: 11px;
}
.bottom {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.price { font-size: 15px; font-weight: 700; color: var(--haier-primary); }
.ask { font-size: 12px; color: var(--haier-text-faint); }
.product-card:hover .ask { color: var(--haier-primary); }
.empty { text-align: center; padding: 40px 0; color: var(--haier-text-faint); font-size: 13px; }

/* 聊天面板 */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-radius: var(--haier-radius);
  overflow: hidden;
}
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 42px;
  height: 42px;
  border-radius: 14px;
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 14px -4px rgba(47, 107, 255, 0.5);
}
.header-info { display: flex; flex-direction: column; gap: 3px; }
.agent-name { font-size: 15px; font-weight: 700; color: var(--haier-text); }
.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--haier-text-faint);
}
.status::before {
  content: "";
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ccc;
}
.status.active { color: #0b9a66; }
.status.active::before { background: var(--haier-emerald); }

.messages-wrap {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 20px 18px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  background: var(--haier-bg);
}
.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 30px 20px 10px;
}
.welcome-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  font-size: 22px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px -6px rgba(47, 107, 255, 0.5);
}
.welcome-text { margin-top: 12px; font-size: 16px; font-weight: 600; color: var(--haier-text); }
.welcome-sub { margin-top: 8px; font-size: 13px; color: var(--haier-text-sub); }

.message-row { display: flex; gap: 8px; }
.message-row.user { justify-content: flex-end; flex-direction: row-reverse; }
.avatar-sm {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}
.message-row.user .avatar-sm { background: var(--haier-primary-tint); color: var(--haier-primary-d); }
.message-row.assistant .avatar-sm {
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  box-shadow: 0 6px 14px -4px rgba(47, 107, 255, 0.45);
}
.message-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  max-width: 82%;
}
.message-row.user .message-content { align-items: flex-end; }
.bubble {
  padding: 12px 16px;
  border-radius: 14px;
  font-size: 14px;
  line-height: 1.7;
  white-space: pre-wrap;
}
.message-row.user .bubble {
  background: var(--haier-primary);
  color: #fff;
  border-bottom-right-radius: 4px;
  box-shadow: 0 6px 16px -6px rgba(47, 107, 255, 0.5);
}
.message-row.assistant .bubble {
  background: #fff;
  color: var(--haier-text);
  border-bottom-left-radius: 4px;
  box-shadow: var(--haier-shadow);
}
.loading-bubble { display: flex; gap: 5px; align-items: center; min-width: 60px; }
.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--haier-primary);
  animation: dot-bounce 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
@keyframes dot-bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: .4; }
  40%           { transform: translateY(-5px); opacity: 1; }
}
.sources-wrap {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.sources-label { font-size: 11px; color: var(--haier-text-faint); }
.source-tag {
  font-size: 11px;
  padding: 3px 10px;
  border-radius: 999px;
  background: var(--haier-primary-tint);
  color: var(--haier-primary);
  border: 1px solid rgba(47, 107, 255, 0.25);
}

.error-tip {
  text-align: center;
  padding: 10px 16px;
  background: rgba(244, 63, 94, 0.1);
  color: var(--haier-red);
  border-radius: 10px;
  font-size: 13px;
}

.input-area {
  padding: 14px 16px;
  background: #fff;
  border-top: 1px solid var(--haier-border);
  display: flex;
  gap: 10px;
  align-items: flex-end;
}
textarea {
  flex: 1;
  resize: none;
  border: 1px solid var(--haier-border-2);
  border-radius: 12px;
  padding: 10px 14px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  background: var(--haier-bg);
  min-height: 42px;
  max-height: 120px;
  color: var(--haier-text);
}
textarea:focus {
  border-color: var(--haier-primary);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(47, 107, 255, 0.12);
}
textarea:disabled { opacity: 0.6; cursor: not-allowed; }
.send-btn {
  width: 88px;
  height: 42px;
  border-radius: 21px;
  flex-shrink: 0;
  border: none;
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all .2s;
}
.send-btn:hover:not(:disabled) { box-shadow: 0 6px 16px -4px rgba(47, 107, 255, 0.5); }
.send-btn:disabled { background: rgba(47, 107, 255, 0.35); cursor: not-allowed; }
</style>