<!-- client/src/views/SettingsView.vue 设置：大模型配置 -->
<template>
  <div class="settings-page scroll-thin">
    <div class="settings-main">
      <p class="heading">设置</p>
      <p class="sub">配置对话使用的大模型，保存后即时生效，未配置的字段使用后端默认模型</p>

      <!-- 预设模板 -->
      <section class="card preset-card">
        <p class="card-title">常用模型模板</p>
        <div class="preset-grid">
          <button
            v-for="p in PROVIDERS"
            :key="p.name"
            class="preset-btn"
            @click="apply(p)"
          >
            <span class="preset-name">{{ p.name }}</span>
            <span class="preset-model">{{ p.model }}</span>
          </button>
        </div>
      </section>

      <!-- 配置表单 -->
      <section class="card form-card">
        <p class="card-title">自定义配置</p>
        <div class="field">
          <label class="label">API Key</label>
          <input
            v-model.trim="form.apiKey"
            class="input"
            type="password"
            placeholder="sk-..."
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label class="label">接口地址 Base URL</label>
          <input
            v-model.trim="form.baseUrl"
            class="input"
            placeholder="https://api.example.com/v1"
          />
        </div>
        <div class="field">
          <label class="label">模型名称 Model</label>
          <input
            v-model.trim="form.model"
            class="input"
            placeholder="deepseek-chat"
          />
        </div>
        <p class="field-hint">留空表示使用后端默认大模型，不会覆盖已保存的选择。</p>

        <div class="actions">
          <button class="btn-primary" :disabled="!dirty" @click="save">
            保存配置
          </button>
          <button class="btn-ghost" @click="reset">恢复默认</button>
        </div>
      </section>

      <!-- 当前状态 -->
      <section class="card status-card">
        <p class="card-title">当前生效模型</p>
        <div class="status-row">
          <span class="dot-online"></span>
          <span class="current-model">{{ currentModelDisplay() }}</span>
        </div>
        <p v-if="saved.apiKey" class="status-note">已启用前端自定义配置</p>
        <p v-else class="status-note">使用后端默认配置</p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useModel } from '../composables/useModel.js';

const { PROVIDERS, saved, applyProvider, setConfig, resetConfig, currentModelDisplay, defaultModel } = useModel();

const form = ref({ ...saved.value });

const dirty = computed(
  () =>
    form.value.apiKey !== saved.value.apiKey ||
    form.value.baseUrl !== saved.value.baseUrl ||
    form.value.model !== saved.value.model,
);

const apply = (p) => {
  applyProvider(p);
  form.value = { ...saved.value };
};

const save = () => {
  setConfig({
    apiKey: form.value.apiKey,
    baseUrl: form.value.baseUrl,
    model: form.value.model,
    display: form.value.model || form.value.display,
  });
  form.value = { ...saved.value };
};

const reset = () => {
  resetConfig();
  form.value = { ...saved.value };
};
</script>

<style scoped>
.settings-page {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  background: var(--haier-bg);
}
.settings-main {
  max-width: 720px;
  margin: 0 auto;
  padding: 28px 20px 48px;
}
.heading { font-size: 24px; font-weight: 700; color: var(--haier-text); letter-spacing: 1px; }
.sub { margin-top: 8px; font-size: 13px; color: var(--haier-text-sub); }

.card {
  margin-top: 22px;
  padding: 20px;
  border-radius: var(--haier-radius);
}
.card-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--haier-text);
  margin-bottom: 14px;
}

.preset-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.preset-btn {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  padding: 12px 14px;
  background: var(--haier-bg);
  border: 1px solid var(--haier-border);
  border-radius: var(--haier-radius-sm);
  cursor: pointer;
  font-family: inherit;
  text-align: left;
  transition: all .2s;
}
.preset-btn:hover { border-color: var(--haier-primary); background: var(--haier-primary-tint); }
.preset-name { font-size: 14px; font-weight: 700; color: var(--haier-text); }
.preset-model { font-size: 12px; color: var(--haier-text-faint); }

.field { margin-bottom: 16px; }
.field-hint { margin: -6px 0 16px; font-size: 12px; color: var(--haier-text-faint); }
.actions { display: flex; gap: 10px; }

.status-row { display: flex; align-items: center; gap: 10px; }
.current-model { font-size: 16px; font-weight: 700; color: var(--haier-primary); }
.status-note { margin-top: 10px; font-size: 12px; color: var(--haier-text-faint); }
</style>