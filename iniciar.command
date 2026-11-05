#!/bin/sh
# macOS: clique duas vezes neste arquivo para abrir a IA da Sobrevivência.
# (Na primeira vez: clique com o botão direito > Abrir, para liberar no Gatekeeper.)
cd "$(dirname "$0")" || exit 1
# Remove a "quarentena" do macOS dos binários do kit (copiados de pendrive/zip baixado).
xattr -dr com.apple.quarantine runtime 2>/dev/null
exec sh ./iniciar.sh "$@"
