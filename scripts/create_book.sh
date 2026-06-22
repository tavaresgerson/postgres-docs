#!/bin/bash

# Volta para a raiz do projeto baseando-se no local onde o script está salvo
cd "$(dirname "$0")/.." || exit 1

MD_DIR="./v18/br"
TMP_LIST="lista_ordenada.txt"
TMP_MD="unified_docs.md"
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

> "$TMP_MD"
echo "Concatenando arquivos Markdown..."

# 2. Aglutina todos os Markdowns em um único arquivo base
while IFS= read -r arquivo; do
    if [ -f "$arquivo" ]; then
        nome_base=$(basename "$arquivo")

        # Injeta um ID com o nome original do arquivo para que links sem âncora funcionem
        echo "<div id=\"$nome_base\"></div>" >> "$TMP_MD"
        
        # Anexa o conteúdo do markdown
        cat "$arquivo" >> "$TMP_MD"
        
        # Garante espaçamento e quebra de página (usando sintaxe que o pandoc entende)
        echo -e "\n\n<div style='page-break-after: always;'></div>\n\n" >> "$TMP_MD"
    fi
done < "$TMP_LIST"

echo "Blindando links internos..."

# 3. Corrige os links no arquivo Markdown unificado
# Regra 1: [Texto](arquivo.md#ancora "Titulo") vira [Texto](#ancora "Titulo")
sed -E -i 's/\]\([a-zA-Z0-9_-]+\.md#([^)]*)\)/\](#\1)/g' "$TMP_MD"

# Regra 2: [Texto](arquivo.md "Titulo") vira [Texto](#arquivo.md "Titulo")
sed -E -i 's/\]\(([a-zA-Z0-9_-]+\.md)([^)]*)\)/\](#\1\2)/g' "$TMP_MD"

echo "Convertendo para HTML Standalone..."

# 4. Processamento em Lote Único (Pandoc)
# O parâmetro -s (standalone) garante um cabeçalho HTML e DOM perfeitamente formados
pandoc "$TMP_MD" -f markdown -t html -s -o "$TMP_HTML"

echo "Empacotando e-book com o Calibre..."

# 5. Empacotamento usando local-name() para evitar falhas de namespace no XML
ebook-convert "$TMP_HTML" "$OUTPUT_EPUB" \
    --chapter "//*[local-name()='h1' or local-name()='h2']" \
    --level1-toc "//*[local-name()='h1']" \
    --level2-toc "//*[local-name()='h2']" \
    --level3-toc "//*[local-name()='h3']" \
    --authors "PostgreSQL Global Development Group" \
    --title "PostgreSQL 18.4 Documentação"

echo "Concluído. E-book salvo em: $(pwd)/$OUTPUT_EPUB"

# Limpeza
rm "$TMP_LIST" "$TMP_MD" "$TMP_HTML"