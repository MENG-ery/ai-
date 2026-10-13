/**
 * useProducts — 家电产品数据层（列表 / 详情）
 */
import { ref } from 'vue';

const API_BASE = '/api';

export function useProducts() {
  const products = ref([]);
  const loading = ref(false);
  const error = ref('');

  const fetchProducts = async () => {
    loading.value = true;
    error.value = '';
    try {
      const res = await fetch(`${API_BASE}/products`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      products.value = data.products || [];
    } catch (err) {
      error.value = `产品加载失败：${err.message}`;
    } finally {
      loading.value = false;
    }
  };

  const getProduct = (id) =>
    products.value.find((p) => p.id === id) || null;

  return { products, loading, error, fetchProducts, getProduct };
}
