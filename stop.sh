#!/usr/bin/env bash
# 服满海 AI 客服系统 —— 停止脚本
# 通过 ss 提取监听端口的 PID 后终止；不使用 fuser/lsof，不吞掉命令报错。
set -u

API_PORT=3000
WEB_PORT=5173
PORTS="$API_PORT $WEB_PORT"

# 输出监听指定端口的进程 PID（可能多个，按行输出）
port_pids() {
  ss -ltnp "sport = :$1" | sed -n 's/.*pid=\([0-9]\{1,\}\).*/\1/p' | sort -u
}

stopped=0
for port in $PORTS; do
  pids=$(port_pids "$port")
  if [ -z "$pids" ]; then
    echo "port $port: not listening"
    continue
  fi
  for pid in $pids; do
    echo "port $port: kill process $pid"
    kill "$pid"
    stopped=1
  done
done

if [ "$stopped" -eq 0 ]; then
  echo "no running service found"
  exit 0
fi

# 等待端口释放，未释放则强制终止
for port in $PORTS; do
  waited=0
  while [ "$waited" -lt 20 ]; do
    pids=$(port_pids "$port")
    [ -z "$pids" ] && break
    sleep 1
    waited=$((waited + 1))
  done
  pids=$(port_pids "$port")
  if [ -n "$pids" ]; then
    for pid in $pids; do
      echo "port $port: force kill process $pid"
      kill -9 "$pid"
    done
  fi
done

echo "service stopped"
exit 0
