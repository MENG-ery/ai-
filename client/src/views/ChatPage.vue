<!--
  服满海 AI 客服 · 对话页
  独立新界面，顶部返回首页，支持流式对话
-->
<template>
  <div class="chat-page">
    <div class="chat-inner">
      <section class="chat-panel card">
        <header class="chat-header">
          <div class="header-left">
            <router-link to="/" class="back-btn" title="返回首页">‹</router-link>
            <div class="avatar">
              <span class="avatar-ico">购</span>
              <i class="dot-online"></i>
            </div>
            <div class="header-info">
              <span class="agent-name">服满海智能客服</span>
              <span class="status" :class="{ active: !streaming }">
                {{ streaming ? '回复中...' : '在线' }}
              </span>
            </div>
          </div>
        </header>

        <main class="messages-wrap scroll-thin" ref="messagesRef">
          <!-- 欢迎卡片 -->
          <div v-if="messages.length === 0" class="welcome">
            <div class="welcome-avatar">购</div>
            <p class="welcome-title">您好！我是服满海智能客服小购</p>
            <p class="welcome-sub">直接输入您的购物、订单、物流问题，我会耐心为您解答～</p>
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
          <div v-if="error" class="error-tip">⚠️ {{ error }}</div>
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
              <span v-else class="dot-loading"><i /><i /><i /></span>
            </button>
          </div>
        </footer>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useChat } from '../composables/useChat.js';

const route = useRoute();
const { messages, streaming, streamText, error, sendMessage } = useChat();

const inputText = ref('');
const messagesRef = ref(null);
const inputRef = ref(null);

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

onMounted(() => {
  const q = route.query.q;
  if (q) {
    inputText.value = q;
    handleSend();
  }
});
</script>

<style scoped>
.chat-page {
  flex: 1;
  min-height: 0;
  display: flex;
  background: var(--haier-bg);
  overflow: hidden;
}
.chat-inner {
  flex: 1;
  display: flex;
  max-width: 1080px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 20px;
}

.chat-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-radius: var(--haier-radius);
  overflow: hidden;
}

/* Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: #fff;
  border-bottom: 1px solid var(--haier-border);
}
.header-left { display: flex; align-items: center; gap: 14px; }
.back-btn {
  width: 34px;
  height: 34px;
  border: 1px solid var(--haier-border-2);
  border-radius: 50%;
  background: #fff;
  color: var(--haier-primary);
  font-size: 20px;
  line-height: 1;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all .2s;
}
.back-btn:hover { background: var(--haier-primary-tint); border-color: var(--haier-primary); }
.avatar {
  position: relative;
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}
.avatar-ico {
  width: 44px;
  height: 44px;
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
.avatar .dot-online {
  position: absolute;
  right: -2px;
  bottom: -2px;
  border: 2px solid #fff;
  width: 12px;
  height: 12px;
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

/* Messages */
.messages-wrap {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 24px 22px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  background: var(--haier-bg);
}
.welcome { display: flex; flex-direction: column; align-items: center; gap: 12px; padding: 40px 20px 16px; text-align: center; }
.welcome-avatar {
  width: 58px;
  height: 58px;
  border-radius: 50%;
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  font-size: 24px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px -6px rgba(47, 107, 255, 0.5);
}
.welcome-title { font-size: 16px; font-weight: 700; color: var(--haier-text); }
.welcome-sub { font-size: 13px; color: var(--haier-text-sub); line-height: 1.6; }

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
  width: 34px;
  height: 34px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
}
.message-row.user .avatar-sm {
  background: var(--haier-primary-tint);
  color: var(--haier-primary-d);
}
.message-row.assistant .avatar-sm {
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  box-shadow: 0 6px 14px -4px rgba(47, 107, 255, 0.45);
}

.bubble {
  padding: 12px 18px;
  border-radius: 16px;
  line-height: 1.75;
  font-size: 14px;
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
.bubble p { margin: 0; white-space: pre-wrap; }

.msg-time { font-size: 11px; color: var(--haier-text-faint); padding: 0 4px; }

.cursor {
  display: inline-block;
  animation: blink 1s step-end infinite;
  color: var(--haier-primary);
  font-weight: 700;
}
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }

.error-tip {
  text-align: center;
  padding: 10px 16px;
  border-radius: 10px;
  background: rgba(244, 63, 94, 0.1);
  color: var(--haier-red);
  font-size: 13px;
}

/* Input area */
.input-area {
  padding: 14px 18px;
  background: #fff;
  border-top: 1px solid var(--haier-border);
}
.input-wrap { display: flex; gap: 10px; align-items: flex-end; }
textarea {
  flex: 1;
  resize: none;
  border: 1px solid var(--haier-border-2);
  border-radius: 12px;
  padding: 11px 16px;
  font-size: 14px;
  font-family: inherit;
  line-height: 1.6;
  outline: none;
  transition: border-color .2s, box-shadow .2s;
  background: var(--haier-bg);
  min-height: 44px;
  max-height: 120px;
  overflow-y: auto;
  color: var(--haier-text);
}
textarea:focus {
  border-color: var(--haier-primary);
  background: #fff;
  box-shadow: 0 0 0 3px rgba(47, 107, 255, 0.12);
}
textarea:disabled { opacity: 0.6; cursor: not-allowed; }

.send-btn {
  width: 84px;
  height: 44px;
  border-radius: 22px;
  flex-shrink: 0;
  border: none;
  background: linear-gradient(135deg, #2f6bff, #1e52e0);
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all .2s;
  display: flex;
  align-items: center;
  justify-content: center;
}
.send-btn:hover:not(:disabled) { background: var(--haier-primary-d); box-shadow: 0 6px 16px -4px rgba(47, 107, 255, 0.5); }
.send-btn:disabled { background: rgba(47, 107, 255, 0.35); cursor: not-allowed; box-shadow: none; }

/* Loading dots */
.dot-loading { display: flex; gap: 4px; }
.dot-loading i {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #fff;
  animation: dot 1.2s ease-in-out infinite;
}
.dot-loading i:nth-child(2) { animation-delay: .2s; }
.dot-loading i:nth-child(3) { animation-delay: .4s; }
@keyframes dot { 0%, 80%, 100% { opacity: .2; transform: scale(.8); } 40% { opacity: 1; transform: scale(1); } }
</style>