#!/usr/bin/env sh
# IA da Sobrevivência — iniciar no Linux/macOS:  ./iniciar.sh   (opções: --lang en | --lang es)
# Subcomandos: ./iniciar.sh chat | ask "pergunta" | status | prepare
cd "$(dirname "$0")" || exit 1

case "$(uname -s)" in
  Darwin) OS=macos ;;
  *) OS=linux ;;
esac
case "$(uname -m)" in
  x86_64|amd64) ARCH=x86_64 ;;
  arm64|aarch64) ARCH=arm64 ;;
  *) ARCH="$(uname -m)" ;;
esac

PY=""
if [ -x "runtime/python/$OS-$ARCH/python/bin/python3" ]; then
  PY="runtime/python/$OS-$ARCH/python/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
  PY="python3"
elif command -v python >/dev/null 2>&1; then
  PY="python"
fi
if [ -z "$PY" ]; then
  echo "Python 3 não encontrado. Rode ./preparar-kit.sh com internet (ou instale python3)."
  exit 1
fi

# Sem subcomando => interface web
case "$1" in
  start|chat|ask|search|status|prepare) exec "$PY" sobrevivencia.py "$@" ;;
  *) exec "$PY" sobrevivencia.py "$@" start ;;
esac
