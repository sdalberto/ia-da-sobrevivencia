#!/bin/sh
# macOS: clique duas vezes para preparar o kit (precisa de internet).
cd "$(dirname "$0")" || exit 1
sh ./iniciar.sh prepare "$@"
echo
echo "Pressione Enter para fechar."
read _
