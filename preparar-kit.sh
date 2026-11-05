#!/usr/bin/env sh
# IA da Sobrevivência — preparar o kit (PRECISA DE INTERNET, rode uma vez)
# Exemplos sem perguntas:
#   ./preparar-kit.sh --model padrao --zims recomendado --os all --python
#   ./preparar-kit.sh --search medicine          # procurar outras bases no catálogo Kiwix
cd "$(dirname "$0")" || exit 1
exec sh ./iniciar.sh prepare "$@"
