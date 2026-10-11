<!-- client/src/views/GraphView.vue（海尔官网风格：横幅 + 面包屑 + 横向功能模块 + 聊天面板） -->
<template>
  <div class="haier-page">
    <!-- Hero 横幅 -->
    <div class="hero-banner">
      <div class="hero-inner">
        <span class="hero-line"></span>
        <h1>极速购智能客服中枢</h1>
        <p class="hero-sub">自动识别问题类型，调度最合适的模块为您服务</p>
      </div>
    </div>

    <!-- 面包屑 -->
    <div class="crumbs">
      <router-link to="/">首页</router-link>
      <span class="sep">&gt;</span>
      <span class="cur">智能中枢</span>
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
              <h1>极速购智能客服中枢</h1>
              <span class="subtitle">
                {{ loading ? currentNode || '处理中...' : '多 Agent 协作模式' }}
              </span>
            </div>
          </div>
          <button class="haier-pill-btn" @click="clearMessages">清空</button>
        </header>

        <main class="messages-wrap" ref="messagesRef">
          <div v-if="messages.length === 0" class="welcome">
            <p>您好，我是极速购智能客服中枢。</p>
            <p class="sub">我会自动判断您的问题类型，调用最合适的模块为您服务。</p>
          </div>

          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message-row"
            :class="msg.role"
          >
            <div class="avatar-sm">{{ msg.role === 'user' ? '我' : '购' }}</div>
            <div class="message-content">
              <!-- 工作流执行轨迹 -->
              <div v-if="msg.nodes && msg.nodes.length" class="flow-trace">
                <template v-for="(node, ni) in msg.nodes" :key="ni">
                  <span class="node-name">{{ NODE_DISPLAY[node] || node }}</span>
                  <span v-if="ni < msg.nodes.length - 1" class="arrow">→</span>
                </template>
                <span v-if="msg.intent" class="intent-tag">{{ msg.intent }}</span>
              </div>

              <!-- 工具调用步骤 -->
              <div v-if="msg.steps && msg.steps.length" class="steps-wrap">
                <div v-for="(step, si) in msg.steps" :key="si" class="step-item">
                  <span class="step-tool">{{ step.tool }}</span>
                  <span class="step-sep">·</span>
                  <span class="step-input">{{ formatStepInput(step.input) }}</span>
                </div>
              </div>

              <div v-if="msg.loading" class="bubble loading-bubble">
                <span class="dot" /><span class="dot" /><span class="dot" />
              </div>
              <div v-else class="bubble">{{ msg.content }}</div>
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
            {{ loading ? '处理中...' : '发送' }}
          </button>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import { useGraph, NODE_LABELS } from '../composables/useGraph.js';

const { messages, loading, currentNode, error, sendMessage, clearMessages } = useGraph();

const inputText   = ref('');
const messagesRef = ref(null);

const NODE_DISPLAY = NODE_LABELS;

const modules = [
  { icon: '订', title: '订单问题',   desc: '订单状态、物流与配送', question: '订单 ORD-001 发货了吗？' },
  { icon: '知', title: '知识库问答', desc: '商品规格、保修与售后', question: '蓝牙耳机怎么保修？' },
  { icon: '退', title: '退款咨询',   desc: '退款政策与到账时间',   question: '退款需要多少天？' },
  { icon: '聊', title: '日常闲聊',   desc: '问候与日常对话',       question: '你好' },
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

const formatStepInput = (input) => {
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
  display: flex; align-items: center;
  justify-content: space-between;
  padding: 14px 20px; background: #fff;
  border-bottom: 2px solid var(--haier-primary);
}
.header-left { display: flex; align-items: center; gap: 12px; }
.avatar {
  width: 42px; height: 42px; border-radius: 8px;
  background: var(--haier-primary); color: #fff;
  font-size: 18px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.header-left h1      { font-size: 16px; font-weight: 700; margin: 0; color: var(--haier-text); }
.header-left .subtitle { font-size: 12px; color: var(--haier-text-weak); transition: color .2s; }
.chat-header .haier-pill-btn { height: 30px; }

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

.message-content {
  display: flex; flex-direction: column; gap: 6px; max-width: 78%;
}
.message-row.user .message-content { align-items: flex-end; }

.flow-trace {
  display: flex; align-items: center;
  flex-wrap: wrap; gap: 4px; font-size: 11px;
}
.node-name {
  padding: 2px 8px; border-radius: 4px;
  background: var(--haier-blue-tint); color: var(--haier-primary);
  border: 1px solid #9cc8f0;
}
.arrow { color: var(--haier-text-faint); font-size: 10px; }
.intent-tag {
  padding: 2px 8px; border-radius: 4px;
  background: #fff; color: var(--haier-primary);
  border: 1px solid var(--haier-primary); margin-left: 4px;
}

.steps-wrap { display: flex; flex-direction: column; gap: 3px; }
.step-item {
  display: flex; align-items: center; gap: 6px;
  font-size: 12px; padding: 4px 10px;
  background: #fff; border-radius: 6px;
  border: 1px solid var(--haier-border);
}
.step-tool  { font-weight: 600; color: var(--haier-text-sub); }
.step-sep   { color: var(--haier-text-faint); }
.step-input { color: var(--haier-text-weak); }

.bubble {
  padding: 12px 16px; border-radius: 10px;
  font-size: 14px; line-height: 1.7; white-space: pre-wrap;
}
.message-row.user .bubble {
  background: var(--haier-primary); color: #fff; border-bottom-right-radius: 2px;
}
.message-row.assistant .bubble {
  background: var(--haier-bg); color: var(--haier-text);
  border-bottom-left-radius: 2px;
}

.loading-bubble {
  display: flex; gap: 5px; align-items: center;
  padding: 12px 16px; background: var(--haier-bg); border-radius: 10px;
  border-bottom-left-radius: 2px;
  min-width: 60px;
}
.dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: var(--haier-text-weak); animation: bounce 1.2s infinite;
}
.dot:nth-child(2) { animation-delay: .2s; }
.dot:nth-child(3) { animation-delay: .4s; }
@keyframes bounce {
  0%, 80%, 100% { transform: translateY(0); opacity: .4; }
  40%           { transform: translateY(-5px); opacity: 1; }
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
  display: flex; gap: 10px; align-items: flex-end;
}
textarea {
  flex: 1; resize: none; border: 1px solid var(--haier-border-2);
  border-radius: 8px; padding: 10px 14px;
  font-size: 14px; font-family: inherit;
  outline: none; background: #fafafa;
  min-height: 42px; max-height: 120px;
}
textarea:focus    { border-color: var(--haier-primary); background: #fff; }
textarea:disabled { opacity: 0.6; }

.send-btn {
  width: 80px; height: 42px; border-radius: 8px;
  border: none; background: var(--haier-primary); color: #fff;
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: background .2s;
}
.send-btn:hover:not(:disabled) { background: var(--haier-primary-d); }
.send-btn:disabled { background: var(--haier-blue-tint); color: #fff; cursor: not-allowed; }
</style>
