#!/bin/bash

# Volta para a raiz do projeto baseando-se no local onde o script está salvo
cd "$(dirname "$0")/.." || exit 1

MD_DIR="./v18/br"
TMP_LIST="lista_ordenada.txt"
TMP_HTML="group_docs.html"
OUTPUT_EPUB="postgresql_18.4_docs.epub"

if [ ! -d "$MD_DIR" ]; then
    echo "Erro: Diretório $MD_DIR não encontrado."
    exit 1
fi

# 1. Executa o script de mapeamento estrutural
python3 scripts/mapping_toc.py

# Se falhou ao gerar a lista, aborta
if [ ! -f "$TMP_LIST" ]; then
    echo "Erro: Falha ao gerar $TMP_LIST"
    exit 1
fi

> "$TMP_HTML"

echo "Concatenando e blindando links internos..."

# 2. Lê a lista ordenada e converte
while IFS= read -r arquivo; do
    if [ -f "$arquivo" ]; then
        echo "Processando: $arquivo"
        nome_base=$(basename "$arquivo")

        # Injeta um ID com o nome original do arquivo para que links sem âncora funcionem
        echo "<div id=\"$nome_base\"></div>" >> "$TMP_HTML"

        # O `sed` converte links de arquivos isolados para âncoras locais do arquivo unificado.
        # Regra 1: [Texto](arquivo.md#ancora) vira [Texto](#ancora)
        # Regra 2: [Texto](arquivo.md) vira [Texto](#arquivo.md)
        sed -E 's/\]\([a-zA-Z0-9_-]+\.md#/\](#/g; s/\]\(([a-zA-Z0-9_-]+\.md)\)/\](#\1)/g' "$arquivo" | \
        pandoc -f markdown -t html >> "$TMP_HTML"

        echo -e "\n<div style='page-break-after: always;'></div>\n" >> "$TMP_HTML"
    fi
done < "$TMP_LIST"

# 3. Empacota com Calibre
echo "Empacotando e-book com o Calibre..."
ebook-convert "$TMP_HTML" "$OUTPUT_EPUB" \
    --chapter "//*[name()='h1' or name()='h2']" \
    --level1-toc "//*[name()='h1']" \
    --level2-toc "//*[name()='h2']" \
    --authors "PostgreSQL Global Development Group" \
    --title "PostgreSQL 18.4 Documentação"

echo "Concluído. E-book salvo em: $(pwd)/$OUTPUT_EPUB"

# Limpeza
rm "$TMP_LIST" "$TMP_HTML"