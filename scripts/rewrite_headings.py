import os
import re

# Diretório onde estão seus arquivos Markdown
MD_DIR = "./v18/br"

visitados = {}  # Dicionário: nome_do_arquivo -> nivel_alvo_na_hierarquia
ordem_arquivos = []


def rastrear_links(arquivo_md, level_atual):
    """
    Navega recursivamente (DFS) pelos links para descobrir a profundidade real de cada arquivo.
    """
    caminho_completo = os.path.join(MD_DIR, arquivo_md)

    # Evita loops infinitos e garante que o primeiro encontro (mais próximo da raiz) defina o nível
    if arquivo_md in visitados or not os.path.exists(caminho_completo):
        return

    visitados[arquivo_md] = level_atual
    ordem_arquivos.append(arquivo_md)

    with open(caminho_completo, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Regex aprimorada para capturar links de TOC:
    # Ignora espaços, aceita marcações opcionais de lista (*, +, 1.) ou de título (#)
    # Foca rigorosamente em capturar o nome do arquivo .md
    padrao_toc = r'^[ \t]*(?:#+\s+)?(?:(?:[\*\-\+]+|\d+(?:\.\d+)*\.?)\s*)?(?:[*_`]*|<[^>]+>)*\[.*?\]\(([\w\.-]+\.md)[^\)]*\)'
    links_no_toc = re.findall(padrao_toc, conteudo, flags=re.MULTILINE)

    # Mergulha em cada arquivo referenciado, empurrando-os um nível mais fundo (+1)
    for link in links_no_toc:
        rastrear_links(link, level_atual + 1)


def reescrever_titulos():
    """
    Abre cada arquivo mapeado, calcula o deslocamento necessário e reescreve os '#'
    """
    print(f"Iniciando a reescrita de {len(visitados)} arquivos...\n")
    arquivos_modificados = 0

    for arquivo_md, target_level in visitados.items():
        caminho_completo = os.path.join(MD_DIR, arquivo_md)

        with open(caminho_completo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        # 1. Descobre qual é o nível do título principal atual do arquivo
        highest_level = 99
        in_code_block = False

        for linha in linhas:
            # Ignora blocos de código para não confundir comentários (ex: # script bash) com títulos
            if linha.strip().startswith('```') or linha.strip().startswith('~~~'):
                in_code_block = not in_code_block
                continue

            if not in_code_block:
                match = re.match(r'^(#+)\s', linha)
                if match:
                    highest_level = min(highest_level, len(match.group(1)))

        # Se não tem nenhum título no arquivo, não há o que reescrever
        if highest_level == 99:
            continue

        # 2. Calcula o "Shift" (deslocamento).
        # Ex: Se o arquivo deveria ser Nível 4, mas começa com ## (2), o shift é +2.
        shift = target_level - highest_level

        if shift == 0:
            continue  # Já está perfeitamente alinhado com a hierarquia

        # 3. Reescreve as linhas aplicando o deslocamento a TODOS os títulos do arquivo
        novas_linhas = []
        in_code_block = False

        for linha in linhas:
            if linha.strip().startswith('```') or linha.strip().startswith('~~~'):
                in_code_block = not in_code_block
                novas_linhas.append(linha)
                continue

            if not in_code_block:
                match = re.match(r'^(#+)(\s.*)', linha)
                if match:
                    current_h = len(match.group(1))
                    new_h = current_h + shift

                    # Trava de segurança: impede que um título seja menor que H1
                    if new_h < 1:
                        new_h = 1

                    novas_linhas.append('#' * new_h + match.group(2) + '\n')
                else:
                    novas_linhas.append(linha)
            else:
                novas_linhas.append(linha)

        # 4. Salva as alterações de volta no arquivo
        with open(caminho_completo, 'w', encoding='utf-8') as f:
            f.writelines(novas_linhas)

        arquivos_modificados += 1

    print(f"Concluído! {arquivos_modificados} arquivos tiveram seus níveis de título ajustados.")


if __name__ == "__main__":
    print("Mapeando a árvore de documentos a partir do index.md...")
    # index.md é o Nível 1 (Raiz)
    rastrear_links("index.md", 1)

    # Processa os arquivos órfãos (que não foram linkados em nenhum TOC)
    todos_arquivos = [f for f in os.listdir(MD_DIR) if f.endswith('.md')]
    for arq in sorted(todos_arquivos):
        if arq not in visitados:
            visitados[arq] = 2  # Atribui Nível 2 por segurança (filhos diretos do índice)
            ordem_arquivos.append(arq)

    reescrever_titulos()

    # Opcional: Atualiza a sua lista ordenada se você ainda for concatenar depois
    with open("lista_ordenada.txt", 'w', encoding='utf-8') as f:
        for arq in ordem_arquivos:
            f.write(arq + '\n')