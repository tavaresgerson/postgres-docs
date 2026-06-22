import os
import re

MD_DIR = "./v18/br"
OUTPUT_LIST = "lista_ordenada.txt"

visitados = set()
ordem_arquivos = []


def rastrear_links(arquivo_md):
    caminho_completo = os.path.join(MD_DIR, arquivo_md)

    # Previne loops infinitos e arquivos inexistentes
    if arquivo_md in visitados or not os.path.exists(caminho_completo):
        return

    visitados.add(arquivo_md)
    ordem_arquivos.append(caminho_completo)

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # REGEX CORRIGIDA:
    # 1. ^[ \t]* : Aceita indentação inicial.
    # 2. (?:(?:[\*\-\+]+|\d+(?:\.\d+)*\.?)\s*)? : Torna marcadores de lista (*, -, 1., 1.2., etc) opcionais.
    # 3. (?:[*_`]*|<[^>]+>)* : Aceita formatação (negrito, itálico) ou HTML envolvendo o link.
    # 4. \[.*?\] : Lê o texto visível do link.
    # 5. \(([\w\.-]+\.md)[^\)]*\) : Captura rigorosamente apenas o arquivo .md, ignorando tudo o que vier depois (âncoras e títulos) até fechar o parêntese.
    padrao_toc = r'^[ \t]*(?:(?:[\*\-\+]+|\d+(?:\.\d+)*\.?)\s*)?(?:[*_`]*|<[^>]+>)*\[.*?\]\(([\w\.-]+\.md)[^\)]*\)'

    links_no_toc = re.findall(padrao_toc, conteudo, flags=re.MULTILINE)

    # Entra recursivamente em cada arquivo referenciado no sumário local
    for link in links_no_toc:
        rastrear_links(link)


if __name__ == "__main__":
    print("Mapeando a estrutura do livro a partir do index.md...")
    rastrear_links("index.md")

    # Garante que nenhum arquivo fique de fora (órfãos que não estão em nenhum TOC)
    todos = [f for f in os.listdir(MD_DIR) if f.endswith('.md')]
    for arq in sorted(todos):
        if arq not in visitados:
            ordem_arquivos.append(os.path.join(MD_DIR, arq))
            visitados.add(arq)

    # Salva na raiz do projeto
    with open(OUTPUT_LIST, 'w', encoding='utf-8') as f:
        for arq in ordem_arquivos:
            f.write(arq + '\n')

    print(f"Mapeamento concluído. {len(ordem_arquivos)} arquivos ordenados logicamente.")