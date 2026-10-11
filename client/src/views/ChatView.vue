<!--
  智能客服对话界面（海尔官网风格）
  首页：大搜索框 + 提示词 → 搜索后进入对话模式
  Hero：加宽风景图轮播，文字不变
-->
<template>
  <div class="haier-page">
    <!-- Hero 横幅：加宽风景图轮播 -->
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

    <!-- 面包屑 -->
    <div class="crumbs">
      <router-link to="/">首页</router-link>
      <span class="sep">&gt;</span>
      <span class="cur">智能客服</span>
    </div>

    <!-- 搜索入口（默认首页，下滑展示热门家电） -->
    <div v-if="mode === 'home'" class="home-stage">
      <div class="search-stage">
        <div class="search-box">
          <span class="search-icon"></span>
          <input
            v-model="searchText"
            placeholder="请输入您的问题，如：我的订单到哪了？"
            @keydown.enter="handleSearch"
          />
          <button class="search-btn" @click="handleSearch">
            <span class="btn-ico"></span>搜索
          </button>
        </div>
        <div class="hot-section">
          <p class="hot-label">热门问题</p>
          <div class="hot-words">
            <button
              v-for="q in hotWords"
              :key="q"
              class="haier-chip"
              @click="handleQuick(q)"
            >
              {{ q }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 对话模式 -->
    <div v-else class="page-main">
      <!-- 功能模块卡片 -->
      <aside class="module-side">
        <div class="module-grid">
          <button
            v-for="m in modules"
            :key="m.title"
            class="module-card"
            @click="handleQuickQuestion(m.question)"
          >
            <span class="module-icon">{{ m.icon }}</span>
            <span class="module-title">{{ m.title }}</span>
            <span class="module-desc">{{ m.desc }}</span>
          </button>
        </div>
      </aside>

      <!-- 聊天面板 -->
      <section class="chat-panel">
        <header class="chat-header">
          <div class="header-left">
            <button class="back-btn" title="返回搜索首页" @click="goHome">‹</button>
            <div class="avatar">购</div>
            <div class="header-info">
              <span class="status" :class="{ active: !streaming }">
                <i class="status-dot"></i>
                {{ streaming ? '回复中...' : '在线' }}
              </span>
            </div>
          </div>
        </header>

        <main class="messages-wrap" ref="messagesRef">
          <!-- 欢迎卡片 -->
          <div v-if="messages.length === 0" class="welcome">
            <div class="welcome-card">
              <div class="welcome-avatar">购</div>
              <p class="welcome-title">您好！我是极速购智能客服小购</p>
              <p class="welcome-sub">点击左侧功能卡片，或直接输入您的购物、订单、物流问题～</p>
            </div>
          </div>

          <!-- 历史消息 -->
          <div
            v-for="(msg, index) in messages"
            :key="index"
            class="message-row"
            :class="msg.role"
          >
            <div class="bubble-wrap">
              <div class="avatar-sm">
                {{ msg.role === 'user' ? '我' : '购' }}
              </div>
              <div class="bubble-col">
                <div class="bubble">
                  <p>{{ msg.content }}</p>
                </div>
                <span class="msg-time">{{ msg.time }}</span>
              </div>
            </div>
          </div>

          <!-- 流式输出中的消息 -->
          <div v-if="streaming" class="message-row assistant">
            <div class="bubble-wrap">
              <div class="avatar-sm">购</div>
              <div class="bubble-col">
                <div class="bubble streaming">
                  <p>{{ streamText || '&nbsp;' }}<span class="cursor">▋</span></p>
                </div>
              </div>
            </div>
          </div>

          <!-- 错误提示 -->
          <div v-if="error" class="error-tip">
            ⚠️ {{ error }}
          </div>
        </main>

        <footer class="input-area">
          <div class="input-wrap">
            <textarea
              v-model="inputText"
              ref="inputRef"
              placeholder="输入消息，Enter 发送，Shift+Enter 换行"
              :disabled="streaming"
              @keydown.enter.exact.prevent="handleSend"
              rows="1"
              @input="autoResize"
            />
            <button
              class="send-btn"
              :class="{ loading: streaming }"
              :disabled="streaming || !inputText.trim()"
              @click="handleSend"
            >
              <span v-if="!streaming">发送</span>
              <span v-else class="dot-loading">
                <i /><i /><i />
              </span>
            </button>
          </div>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { useChat } from '../composables/useChat.js';

const route = useRoute();
const { messages, streaming, streamText, error, sendMessage, clearMessages } =
  useChat();

const inputText = ref('');
const messagesRef = ref(null);
const inputRef = ref(null);

/* ─── 模式：home = 搜索入口，chat = 对话界面 ─── */
const mode = ref('home');
const searchText = ref('');

const modules = [
  { icon: '订', title: '订单查询',   desc: '查订单状态与物流信息', question: '我的订单在哪里？' },
  { icon: '退', title: '退款咨询',   desc: '了解退款政策与到账时间', question: '如何申请退款？' },
  { icon: '物', title: '物流跟踪',   desc: '快递在途与预计到达时间', question: '物流多久到？' },
  { icon: '客', title: '联系客服',   desc: '获取人工客服支持',     question: '如何联系客服？' },
];

const hotWords = [
  '推荐一款性价比高的冰箱？',
  '空调怎么选？新一级能效有什么好处？',
  '洗衣机洗烘一体值得买吗？',
  '想买一台观影效果好的电视',
  '家电保修政策是怎样的？',
  '如何选择适合自己的家电？',
];

/* ─── Hero 风景图轮播 ─── */
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
  const ask = route.query.ask;
  if (ask) {
    mode.value = 'chat';
    inputText.value = ask;
    handleSend();
  }
});
onUnmounted(() => {
  if (heroTimer) clearInterval(heroTimer);
});

/* ─── 搜索入口逻辑 ─── */
const handleSearch = () => {
  const text = searchText.value.trim();
  if (!text) return;
  mode.value = 'chat';
  searchText.value = '';
  inputText.value = text;
  handleSend();
};

const handleQuick = (q) => {
  mode.value = 'chat';
  inputText.value = q;
  handleSend();
};

const goHome = () => {
  if (streaming.value) return;
  mode.value = 'home';
  clearMessages();
};

/* ─── 对话逻辑 ─── */
const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
  }
};

const autoResize = () => {
  const el = inputRef.value;
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 120) + 'px';
};

const handleSend = async () => {
  const text = inputText.value.trim();
  if (!text || streaming.value) return;
  inputText.value = '';
  if (inputRef.value) inputRef.value.style.height = 'auto';
  await sendMessage(text, scrollToBottom);
};

const handleQuickQuestion = (q) => {
  inputText.value = q;
  handleSend();
};
</script>

<style scoped>
/* ─── 页面骨架 ─── */
.haier-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", sans-serif;
}

/* ─── Hero 横幅：加宽风景图轮播 ─── */
.hero-banner {
  position: relative;
  width: 100%;
  padding: 104px 0 92px;
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
  background: linear-gradient(90deg, rgba(8, 62, 130, 0.72), rgba(12, 92, 168, 0.45));
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
  font-size: 32px;
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

/* ─── 面包屑 ─── */
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

/* ─── 首页（搜索入口，空白浅灰白背景，居中） ─── */
.home-stage {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #f6f7f9;
}
.search-stage {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 20px 15px;
}
.search-box {
  display: flex;
  align-items: center;
  width: 100%;
  max-width: 780px;
  background: #fff;
  border: 2px solid var(--haier-primary);
  border-radius: 999px;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(12, 92, 168, 0.14);
  transition: box-shadow .25s;
}
.search-box:focus-within {
  box-shadow: 0 12px 32px rgba(12, 92, 168, 0.22);
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
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 6px;
  padding: 0 32px;
  height: 48px;
  border: none;
  border-radius: 999px;
  background: var(--haier-primary);
  color: #fff;
  font-size: 15px;
  font-weight: 600;
  letter-spacing: 2px;
  cursor: pointer;
  transition: background .2s, box-shadow .2s;
}
.search-btn:hover { background: var(--haier-primary-d); box-shadow: 0 6px 16px rgba(12, 92, 168, 0.35); }
.btn-ico {
  width: 8px;
  height: 8px;
  border: 2px solid #fff;
  border-left: none;
  border-bottom: none;
  transform: rotate(45deg);
}

.hot-section {
  width: 100%;
  max-width: 880px;
  text-align: center;
}
.hot-label {
  position: relative;
  display: inline-block;
  padding-top: 12px;
  margin-bottom: 16px;
  font-size: 15px;
  font-weight: 700;
  color: var(--haier-text);
  letter-spacing: 3px;
}
.hot-label::before {
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
.hot-words {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}
.hot-words .haier-chip {
  padding: 9px 18px;
  font-size: 13px;
}

/* ─── 对话主区域 ─── */
.page-main {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 20px;
  max-width: 1280px;
  width: 100%;
  margin: 0 auto;
  padding: 18px 16px;
  overflow: hidden;
}

/* 左侧功能模块 */
.module-side {
  width: 330px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.module-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  align-content: start;
}
.module-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 9px;
  padding: 24px 14px 20px;
  background: var(--haier-bg-card);
  border: 1px solid var(--haier-border);
  border-radius: 8px;
  cursor: pointer;
  font-family: inherit;
  text-align: center;
  overflow: hidden;
  transition: box-shadow .25s, transform .25s, border-color .25s;
}
.module-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--haier-primary), var(--haier-blue-light));
  opacity: 0;
  transition: opacity .25s;
}
.module-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-3px);
  border-color: #bcd8f2;
}
.module-card:hover::before { opacity: 1; }
.module-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #0c5ca8, #45a0de);
  color: #fff;
  font-size: 19px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(12, 92, 168, 0.3);
}
.module-title { font-size: 14px; font-weight: 700; color: var(--haier-text); }
.module-desc { font-size: 12px; color: var(--haier-text-weak); line-height: 1.5; }

/* 聊天面板 */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: 10px;
  overflow: hidden;
  min-width: 0;
  box-shadow: var(--haier-shadow);
}

/* Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: #fff;
  border-bottom: 2px solid var(--haier-primary);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.back-btn {
  width: 32px;
  height: 32px;
  border: 1px solid var(--haier-border-2);
  border-radius: 50%;
  background: #fff;
  color: var(--haier-primary);
  font-size: 19px;
  line-height: 1;
  cursor: pointer;
  transition: all .2s;
}
.back-btn:hover { background: var(--haier-blue-tint); border-color: var(--haier-blue-light); }
.avatar {
  width: 44px; height: 44px; border-radius: 12px;
  background: linear-gradient(135deg, #0c5ca8, #45a0de);
  color: #fff; font-size: 19px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 4px 10px rgba(12, 92, 168, 0.28);
}
.status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: var(--haier-text-sub);
}
.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #ccc;
}
.status.active .status-dot {
  background: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.18);
}

/* Messages */
.messages-wrap {
  flex: 1; overflow-y: auto; padding: 22px 20px;
  display: flex; flex-direction: column; gap: 18px;
  background: #fafbfc;
}
.welcome { display: flex; justify-content: center; }
.welcome-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
  max-width: 520px;
  padding: 36px 24px;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: 12px;
  box-shadow: var(--haier-shadow);
  text-align: center;
}
.welcome-avatar {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #0c5ca8, #45a0de);
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 16px rgba(12, 92, 168, 0.3);
}
.welcome-title { font-size: 16px; font-weight: 700; color: var(--haier-text); }
.welcome-sub { font-size: 13px; color: var(--haier-text-weak); line-height: 1.6; }

.message-row { display: flex; }
.message-row.user { justify-content: flex-end; }
.message-row.assistant { justify-content: flex-start; }
.bubble-wrap { display: flex; align-items: flex-end; gap: 10px; max-width: 78%; }
.message-row.user .bubble-wrap { flex-direction: row-reverse; }

.bubble-col {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  max-width: 100%;
}
.message-row.user .bubble-col { align-items: flex-end; }

.avatar-sm {
  width: 34px; height: 34px; border-radius: 10px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700;
}
.message-row.user .avatar-sm {
  background: var(--haier-primary); color: #fff;
  box-shadow: 0 3px 8px rgba(12, 92, 168, 0.3);
}
.message-row.assistant .avatar-sm {
  background: var(--haier-blue-tint); color: var(--haier-primary);
}

.bubble {
  padding: 12px 18px; border-radius: 14px;
  line-height: 1.75; font-size: 14px;
}
.message-row.user .bubble {
  background: linear-gradient(135deg, #0c5ca8, #1a6fb8);
  color: #fff;
  border-bottom-right-radius: 4px;
  box-shadow: 0 4px 12px rgba(12, 92, 168, 0.25);
}
.message-row.assistant .bubble {
  background: #fff;
  color: var(--haier-text);
  border-bottom-left-radius: 4px;
  border: 1px solid var(--haier-border);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}
.bubble p { margin: 0; white-space: pre-wrap; }

.msg-time {
  font-size: 11px;
  color: var(--haier-text-faint);
  padding: 0 4px;
}

.cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
  color: var(--haier-primary); font-weight: 700;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

.error-tip {
  text-align: center; padding: 10px 16px; border-radius: 8px;
  background: #fef2f2; color: var(--haier-red); font-size: 13px;
  border: 1px solid #f5c2c2;
}

/* Input area */
.input-area {
  padding: 14px 18px;
  background: #fff;
  border-top: 1px solid var(--haier-border);
}
.input-wrap { display: flex; gap: 10px; align-items: flex-end; }
textarea {
  flex: 1; resize: none; border: 1px solid var(--haier-border-2);
  border-radius: 10px; padding: 11px 16px;
  font-size: 14px; font-family: inherit; line-height: 1.6;
  outline: none; transition: border-color .2s, box-shadow .2s;
  background: #fafbfc; min-height: 44px; max-height: 120px;
  overflow-y: auto;
}
textarea:focus {
  border-color: var(--haier-primary);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(12, 92, 168, 0.12);
}
textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.send-btn {
  width: 84px; height: 44px; border-radius: 22px; flex-shrink: 0;
  border: none; background: linear-gradient(135deg, #0c5ca8, #1a6fb8); color: #fff;
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: all .2s; display: flex; align-items: center; justify-content: center;
}
.send-btn:hover:not(:disabled) {
  background: var(--haier-primary-d);
  box-shadow: 0 5px 14px rgba(12, 92, 168, 0.35);
}
.send-btn:disabled { background: #c6d8ee; cursor: not-allowed; }

/* Loading dots */
.dot-loading { display: flex; gap: 4px; }
.dot-loading i {
  width: 5px; height: 5px; border-radius: 50%;
  background: #fff; animation: dot 1.2s ease-in-out infinite;
}
.dot-loading i:nth-child(2) { animation-delay: .2s; }
.dot-loading i:nth-child(3) { animation-delay: .4s; }
@keyframes dot { 0%, 80%, 100% { opacity: .2; transform: scale(.8); } 40% { opacity: 1; transform: scale(1); } }
</style>
