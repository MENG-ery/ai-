#!/usr/bin/env bash
# 服满海 AI 客服系统 —— 启动脚本（生产模式）
# 端口固定：前端 5173、后端 3000
# 退出码：已启动 / 启动成功 -> 0；启动失败 -> 2
set -u

ROOT="$(cd "$(dirname "$0")" && pwd)"
API_PORT=3000
WEB_PORT=5173
LOG_DIR="$ROOT/logs"
mkdir -p "$LOG_DIR"

# 端口是否有监听（返回 0/1）
port_listening() {
  ss -ltn "sport = :$1" | grep -q ":$1"
}

# 等待端口就绪，$1=端口 $2=超时秒数
wait_port() {
  local port="$1" waited=0
  while [ "$waited" -lt "$2" ]; do
    if port_listening "$port"; then
      return 0
    fi
    sleep 1
    waited=$((waited + 1))
  done
  return 1
}

# ── 1. 校验是否已启动：前后端都在监听则直接返回 0 ──
if port_listening "$WEB_PORT" && port_listening "$API_PORT"; then
  echo "service already running (web:$WEB_PORT api:$API_PORT)"
  exit 0
fi

# ── 2. 清理残留进程：统一交给 stop.sh，避免 kill 残留子进程占用端口 ──
bash "$ROOT/stop.sh"

# ── 3. 构建前端（生产模式）。vite build 会先清空 dist，避免旧构建缓存 ──
echo "building frontend..."
export NODE_OPTIONS="--max-old-space-size=384"
if ! (cd "$ROOT/client" && npm run build > "$LOG_DIR/build.log" 2>&1); then
  echo "frontend build failed, see $LOG_DIR/build.log"
  exit 2
fi

# ── 4. 启动后端（生产模式，不开 --reload 热重载，降低内存峰值）──
echo "starting backend on $API_PORT..."
cd "$ROOT/server-py"
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port "$API_PORT" > "$LOG_DIR/api.log" 2>&1 &
if ! wait_port "$API_PORT" 60; then
  echo "backend failed to start, see $LOG_DIR/api.log"
  exit 2
fi

# ── 5. 启动前端（生产预览，serve 构建产物；根路径即首页）──
echo "starting frontend on $WEB_PORT..."
cd "$ROOT/client"
nohup node_modules/.bin/vite preview --port "$WEB_PORT" --host 0.0.0.0 --strictPort > "$LOG_DIR/web.log" 2>&1 &
if ! wait_port "$WEB_PORT" 60; then
  echo "frontend failed to start, see $LOG_DIR/web.log"
  exit 2
fi

# ── 6. 校验 Web 页面可访问 ──
if ! curl -fsS "http://127.0.0.1:$WEB_PORT/" > /dev/null; then
  echo "web root not accessible"
  exit 2
fi

echo "service started (web:$WEB_PORT api:$API_PORT)"
exit 0
