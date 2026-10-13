// client/src/composables/useModel.js
/** 大模型配置管理：从 localStorage 读取/保存，供请求与 UI 使用 */
import { ref } from 'vue';

const STORAGE_KEY = 'kaos.llm.config';

// 预设模板（真实可用：token.sensenova.cn 网关已核验）
const PROVIDERS = [
  { name: 'DeepSeek V4 Flash', baseUrl: 'https://token.sensenova.cn/v1', model: 'deepseek-v4-flash' },
  { name: 'GLM-5.2',           baseUrl: 'https://token.sensenova.cn/v1', model: 'glm-5.2' },
  { name: 'DeepSeek Flash',    baseUrl: 'https://token.sensenova.cn/v1', model: 'deepseek-flash' },
  { name: 'Sensenova U1.5',    baseUrl: 'https://token.sensenova.cn/v1', model: 'sensenova-u1.5-lite' },
];

const emptyConfig = () => ({ apiKey: '', baseUrl: '', model: '', display: '' });

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) {
      const cfg = JSON.parse(raw);
      return { ...emptyConfig(), ...cfg };
    }
  } catch (e) {
    console.warn('读取模型配置失败', e);
  }
  return emptyConfig();
}

const saved = ref(load());
const defaultModel = ref('');

function persist() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(saved.value));
}

// 从后端 health 获取默认模型名
async function initDefaultModel() {
  try {
    const res = await fetch('http://localhost:3000/api/chat/health');
    const data = await res.json();
    defaultModel.value = data.model_display || data.model || '';
  } catch (e) {
    defaultModel.value = '';
  }
}

// 当前实际使用的模型显示名：优先用户配置，否则后端默认
const currentModelDisplay = () =>
  saved.value.display || saved.value.model || defaultModel.value || '默认模型';

// 传给后端接口的模型配置（空字段去掉，让后端回落默认）
const requestModel = () => {
  const cfg = saved.value;
  const out = {};
  if (cfg.apiKey) out.apiKey = cfg.apiKey;
  if (cfg.baseUrl) out.baseUrl = cfg.baseUrl;
  if (cfg.model) out.model = cfg.model;
  return Object.keys(out).length ? out : null;
};

function setConfig(cfg) {
  saved.value = { ...saved.value, ...cfg };
  persist();
}

function applyProvider(p) {
  saved.value = { ...saved.value, baseUrl: p.baseUrl, model: p.model, display: p.name };
  persist();
}

function resetConfig() {
  saved.value = emptyConfig();
  persist();
}

initDefaultModel();

export function useModel() {
  return {
    PROVIDERS,
    currentModelDisplay,
    requestModel,
    setConfig,
    applyProvider,
    resetConfig,
    saved,
    defaultModel,
  };
}