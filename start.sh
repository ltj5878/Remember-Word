#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
RUN_DIR="$ROOT_DIR/.run"
LOG_DIR="$ROOT_DIR/logs"

BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-localhost}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

BACKEND_PID_FILE="$RUN_DIR/backend.pid"
FRONTEND_PID_FILE="$RUN_DIR/frontend.pid"
BACKEND_LOG="$LOG_DIR/backend.log"
FRONTEND_LOG="$LOG_DIR/frontend.log"

mkdir -p "$RUN_DIR" "$LOG_DIR"

pid_is_running() {
  local pid="$1"
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

pid_from_file() {
  local pid_file="$1"
  if [[ -f "$pid_file" ]]; then
    tr -d '[:space:]' < "$pid_file"
  fi
}

port_pid() {
  local port="$1"
  lsof -tiTCP:"$port" -sTCP:LISTEN 2>/dev/null | head -n 1 || true
}

service_running() {
  local pid_file="$1"
  local port="$2"
  local pid
  pid="$(pid_from_file "$pid_file")"

  if pid_is_running "$pid"; then
    return 0
  fi

  [[ -n "$(port_pid "$port")" ]]
}

install_backend_deps() {
  if [[ ! -x "$BACKEND_DIR/venv/bin/uvicorn" ]]; then
    echo "Installing backend dependencies..."
    python3 -m venv "$BACKEND_DIR/venv"
    "$BACKEND_DIR/venv/bin/pip" install -r "$BACKEND_DIR/requirements.txt"
  fi
}

install_frontend_deps() {
  if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
    echo "Installing frontend dependencies..."
    (cd "$FRONTEND_DIR" && npm install)
  fi
}

start_backend() {
  if service_running "$BACKEND_PID_FILE" "$BACKEND_PORT"; then
    echo "Backend already running on port $BACKEND_PORT."
    return
  fi

  install_backend_deps
  echo "Starting backend on http://$BACKEND_HOST:$BACKEND_PORT ..."
  (
    cd "$BACKEND_DIR"
    BACKEND_HOST="$BACKEND_HOST" BACKEND_PORT="$BACKEND_PORT" \
      "$BACKEND_DIR/venv/bin/uvicorn" main:app --reload --host "$BACKEND_HOST" --port "$BACKEND_PORT"
  ) >"$BACKEND_LOG" 2>&1 &
  echo $! > "$BACKEND_PID_FILE"
}

start_frontend() {
  if service_running "$FRONTEND_PID_FILE" "$FRONTEND_PORT"; then
    echo "Frontend already running on port $FRONTEND_PORT."
    return
  fi

  install_frontend_deps
  echo "Starting frontend on http://$FRONTEND_HOST:$FRONTEND_PORT ..."
  (
    cd "$FRONTEND_DIR"
    npm run dev -- --host "$FRONTEND_HOST" --port "$FRONTEND_PORT"
  ) >"$FRONTEND_LOG" 2>&1 &
  echo $! > "$FRONTEND_PID_FILE"
}

stop_service() {
  local name="$1"
  local pid_file="$2"
  local port="$3"
  local pid
  pid="$(pid_from_file "$pid_file")"

  if pid_is_running "$pid"; then
    echo "Stopping $name process $pid ..."
    kill "$pid" 2>/dev/null || true
    for _ in {1..20}; do
      if ! pid_is_running "$pid"; then
        break
      fi
      sleep 0.2
    done
    if pid_is_running "$pid"; then
      echo "$name process $pid did not exit; sending TERM again."
      kill "$pid" 2>/dev/null || true
    fi
  fi

  pid="$(port_pid "$port")"
  if pid_is_running "$pid"; then
    echo "Stopping $name listener $pid on port $port ..."
    kill "$pid" 2>/dev/null || true
  fi

  rm -f "$pid_file"
}

start() {
  start_backend
  start_frontend
  echo "Logs:"
  echo "  backend:  $BACKEND_LOG"
  echo "  frontend: $FRONTEND_LOG"
}

stop() {
  stop_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT"
  stop_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT"
}

status_service() {
  local name="$1"
  local pid_file="$2"
  local port="$3"
  local pid
  pid="$(pid_from_file "$pid_file")"

  if pid_is_running "$pid"; then
    echo "$name: running (pid $pid, port $port)"
    return
  fi

  pid="$(port_pid "$port")"
  if pid_is_running "$pid"; then
    echo "$name: running (pid $pid, port $port; no matching PID file)"
    return
  fi

  echo "$name: stopped (port $port)"
}

status() {
  status_service "backend" "$BACKEND_PID_FILE" "$BACKEND_PORT"
  status_service "frontend" "$FRONTEND_PID_FILE" "$FRONTEND_PORT"
}

case "${1:-start}" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  restart)
    stop
    start
    ;;
  status)
    status
    ;;
  *)
    echo "Usage: $0 [start|stop|restart|status]" >&2
    exit 2
    ;;
esac
