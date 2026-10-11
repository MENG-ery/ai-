<!-- client/src/views/AgentView.vue（海尔官网风格：横幅 + 面包屑 + 横向功能模块 + 聊天面板） -->
<template>
  <div class="haier-page">
    <!-- Hero 横幅 -->
    <div class="hero-banner">
      <div class="hero-inner">
        <span class="hero-line"></span>
        <h1>极速购智能客服 · 订单查询</h1>
        <p class="hero-sub">输入订单号即可查询订单状态与物流信息</p>
      </div>
    </div>

    <!-- 面包屑 -->
    <div class="crumbs">
      <router-link to="/">首页</router-link>
      <span class="sep">&gt;</span>
      <span class="cur">订单查询</span>
    </div>

    <!-- 横向主区域 -->
    <div class="page-main">
      <!-- 功能模块卡片 -->
      <aside class="module-grid">
        <button
          v-for="m in modules"
          :key="m.title"
          class="module-card"
          @click="handleQuick(m.question)"
        >
          <span class="module-icon">{{ m.icon }}</span>
          <span class="module-title">{{ m.title }}</span>
          <span class="module-desc">{{ m.desc }}</span>
        </button>
      </aside>

      <!-- 聊天面板 -->
      <section class="chat-panel">
        <header class="chat-header">
          <div class="header-left">
            <div class="avatar">购</div>
            <div>
              <h1>极速购智能客服（Agent 模式）</h1>
              <span :class="['status', { active: !loading }]">
                {{ loading ? '思考中...' : '在线' }}
              </span>
            </div>
          </div>
          <button class="haier-pill-btn" @click="clearMessages">清空对话</button>
        </header>

        <main class="messages-wrap" ref="messagesRef">
          <div v-if="messages.length === 0" class="welcome">
            <p>您好，我是极速购智能客服小购。</p>
            <p class="sub">我可以帮您查询订单状态和物流信息，请提供您的订单号。</p>
          </div>

          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message-row"
            :class="msg.role"
          >
            <div class="avatar-sm">{{ msg.role === 'user' ? '我' : '购' }}</div>
            <div class="message-content">
              <div v-if="msg.steps && msg.steps.length" class="steps-wrap">
                <div v-for="(step, si) in msg.steps" :key="si" class="step-item">
                  <span class="step-label">调用工具</span>
                  <span class="step-tool">{{ step.tool }}</span>
                  <span class="step-input">{{ formatInput(step.toolInput) }}</span>
                </div>
              </div>
              <div v-if="msg.thinking" class="thinking">
                <span class="dot-1">.</span>
                <span class="dot-2">.</span>
                <span class="dot-3">.</span>
              </div>
              <div v-else class="bubble">{{ msg.content }}</div>
            </div>
          </div>

          <div v-if="loading && steps.length" class="message-row assistant">
            <div class="avatar-sm">购</div>
            <div class="message-content">
              <div class="steps-wrap">
                <div v-for="(step, si) in steps" :key="si" class="step-item">
                  <span class="step-label">调用工具</span>
                  <span class="step-tool">{{ step.tool }}</span>
                  <span class="step-input">{{ formatInput(step.toolInput) }}</span>
                </div>
              </div>
              <div class="thinking">
                <span class="dot-1">.</span>
                <span class="dot-2">.</span>
                <span class="dot-3">.</span>
              </div>
            </div>
          </div>

          <div v-if="error" class="error-tip">{{ error }}</div>
        </main>

        <footer class="input-area">
          <textarea
            v-model="inputText"
            placeholder="输入消息，Enter 发送，Shift+Enter 换行"
            :disabled="loading"
            @keydown.enter.exact.prevent="handleSend"
            rows="1"
          />
          <button
            class="send-btn"
            :disabled="loading || !inputText.trim()"
            @click="handleSend"
          >
            {{ loading ? '思考中...' : '发送' }}
          </button>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useAgent } from '../composables/useAgent.js';

const { messages, loading, steps, error, sendMessage, clearMessages } = useAgent();

const inputText   = ref('');
const messagesRef = ref(null);

const modules = [
  { icon: '状', title: '订单状态',   desc: '查询订单 ORD-001 当前状态', question: '查一下订单 ORD-001 的状态' },
  { icon: '物', title: '物流跟踪',   desc: '查看快递配送进度',         question: '订单 ORD-001 的快递到哪了？' },
  { icon: '单', title: '我的订单',   desc: '获取最近订单列表',         question: '我有哪些订单？' },
];

const scrollToBottom = async () => {
  await nextTick();
  if (messagesRef.value)
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
};

const handleSend = async () => {
  const text = inputText.value.trim();
  if (!text || loading.value) return;
  inputText.value = '';
  await sendMessage(text, scrollToBottom);
};

const handleQuick = (q) => {
  inputText.value = q;
  handleSend();
};

const formatInput = (input) => {
  if (!input) return '';
  return Object.values(input).join(' · ');
};
</script>

<style scoped>
/* ─── 页面骨架：全宽横幅 + 面包屑 + 横向主区域 ─── */
.haier-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  font-family: "Helvetica Neue", Helvetica, Arial, "Microsoft YaHei", sans-serif;
}

.hero-banner {
  width: 100%;
  background: linear-gradient(135deg, #0c5ca8, #005aaa);
  padding: 34px 0 30px;
  flex-shrink: 0;
}
.hero-inner {
  max-width: 1230px;
  margin: 0 auto;
  padding: 0 15px;
  text-align: center;
}
.hero-line {
  display: block;
  width: 34px; height: 5px;
  margin: 0 auto 16px;
  background: #fff;
  border-radius: 2px;
}
.hero-inner h1 { font-size: 26px; font-weight: 700; color: #fff; letter-spacing: 2px; }
.hero-sub { margin-top: 10px; font-size: 14px; color: #dbe9f7; letter-spacing: 1px; }

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

.page-main {
  flex: 1;
  display: flex;
  align-items: stretch;
  gap: 20px;
  max-width: 1230px;
  width: 100%;
  margin: 0 auto;
  padding: 16px 15px;
  overflow: hidden;
}

/* ─── 左侧功能模块卡片 ─── */
.module-grid {
  width: 320px;
  flex-shrink: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  align-content: start;
  overflow-y: auto;
}
.module-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px 12px;
  background: var(--haier-bg-card);
  border: 1px solid var(--haier-border);
  border-radius: 6px;
  cursor: pointer;
  font-family: inherit;
  text-align: center;
  transition: box-shadow .2s, transform .2s;
}
.module-card:hover {
  box-shadow: var(--haier-shadow-hover);
  transform: translateY(-2px);
}
.module-icon {
  width: 44px; height: 44px;
  border-radius: 8px;
  background: var(--haier-primary);
  color: #fff;
  font-size: 18px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.module-title { font-size: 14px; font-weight: 700; color: var(--haier-text); }
.module-desc { font-size: 12px; color: var(--haier-text-weak); line-height: 1.5; }

/* ─── 右侧聊天面板 ─── */
.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: 8px;
  overflow: hidden;
  min-width: 0;
}
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: #fff;
  border-bottom: 2px solid var(--haier-primary);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 42px; height: 42px; border-radius: 8px;
  background: var(--haier-primary); color: #fff;
  font-size: 18px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.header-left h1 { font-size: 16px; font-weight: 700; margin: 0; color: var(--haier-text); }
.status { font-size: 12px; color: var(--haier-text-weak); }
.status.active { color: #22c55e; }

.messages-wrap {
  flex: 1; overflow-y: auto;
  padding: 20px 16px;
  display: flex; flex-direction: column; gap: 16px;
}

.welcome { text-align: center; padding: 30px 20px; color: var(--haier-text-sub); }
.welcome p { font-size: 16px; font-weight: 600; color: var(--haier-text); }
.welcome .sub { margin-top: 8px; font-size: 13px; font-weight: 400; color: var(--haier-text-weak); }

.message-row { display: flex; gap: 8px; }
.message-row.user { justify-content: flex-end; flex-direction: row-reverse; }

.avatar-sm {
  width: 32px; height: 32px; border-radius: 8px; flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 12px; font-weight: 700;
}
.message-row.user .avatar-sm      { background: var(--haier-primary); color: #fff; }
.message-row.assistant .avatar-sm { background: var(--haier-blue-tint); color: var(--haier-primary); }

.message-content { display: flex; flex-direction: column; gap: 6px; max-width: 75%; }
.message-row.user .message-content { align-items: flex-end; }

.bubble {
  padding: 12px 16px; border-radius: 10px;
  font-size: 14px; line-height: 1.7; white-space: pre-wrap;
}
.message-row.user .bubble {
  background: var(--haier-primary); color: #fff;
  border-bottom-right-radius: 2px;
}
.message-row.assistant .bubble {
  background: var(--haier-bg); color: var(--haier-text);
  border-bottom-left-radius: 2px;
}

.steps-wrap { display: flex; flex-direction: column; gap: 4px; }
.step-item {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; background: #fff;
  border: 1px solid var(--haier-border);
  border-radius: 6px; padding: 5px 10px; color: var(--haier-text-sub);
}
.step-label { color: var(--haier-text-weak); }
.step-tool  { font-weight: 600; color: var(--haier-primary); }
.step-input { color: var(--haier-text-weak); }

.thinking {
  display: flex; gap: 2px;
  padding: 10px 16px;
  background: var(--haier-bg); border-radius: 10px;
  font-size: 22px; color: var(--haier-text-weak);
  width: fit-content;
}
.thinking span { animation: bounce 1.2s infinite; }
.dot-2 { animation-delay: .2s; }
.dot-3 { animation-delay: .4s; }
@keyframes bounce {
  0%, 80%, 100% { opacity: .3; transform: translateY(0); }
  40%           { opacity: 1;  transform: translateY(-4px); }
}

.error-tip {
  text-align: center; padding: 10px 16px;
  background: #fef2f2; color: var(--haier-red);
  border: 1px solid #f5c2c2;
  border-radius: 8px; font-size: 13px;
}

.input-area {
  padding: 14px 16px; background: #fff;
  border-top: 1px solid var(--haier-border);
}
.input-area { display: flex; gap: 10px; align-items: flex-end; }
textarea {
  flex: 1; resize: none; border: 1px solid var(--haier-border-2);
  border-radius: 8px; padding: 10px 14px;
  font-size: 14px; font-family: inherit; line-height: 1.6;
  outline: none; background: #fafafa;
  min-height: 42px; max-height: 120px;
}
textarea:focus   { border-color: var(--haier-primary); background: #fff; }
textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.send-btn {
  width: 80px; height: 42px; border-radius: 8px; flex-shrink: 0;
  border: none; background: var(--haier-primary); color: #fff;
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: background .2s;
}
.send-btn:hover:not(:disabled) { background: var(--haier-primary-d); }
.send-btn:disabled { background: var(--haier-blue-tint); cursor: not-allowed; }
</style>
