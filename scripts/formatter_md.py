import os
import re
from bs4 import BeautifulSoup

# Diretório onde estão os arquivos Markdown
MD_DIR = "./v18/br"


def format_html_tables(text):
    """Localiza tabelas HTML no texto e aplica a formatação estrutural de indentação."""

    def replacer(match):
        soup = BeautifulSoup(match.group(0), 'html.parser')
        # prettify() ajusta quebras de linha e níveis de indentação automaticamente
        return soup.prettify()

    return re.sub(r'<table\b[^>]*>.*?</table>', replacer, text, flags=re.IGNORECASE | re.DOTALL)


def format_broken_links(text):
    """Corrige links quebrados que ficaram com formatação inválida após tradução."""
    # Regra original: [Texto][(url)] -> [Texto](url)
    text = re.sub(r'\[([^\]]+)\]\s*\[\(\s*([^)\s]+)[^)]*\)\]', r'[\1](\2)', text)

    # Regra 1: Falta de colchete fechando: [Texto(url "titulo") -> [Texto](url)
    # Ex: [`CREATE DATABASE`(sql-createdatabase.md "...") -> [`CREATE DATABASE`](sql-createdatabase.md)
    # Captura também links com âncoras (ex: .md#ancora)
    text = re.sub(r'\[([^\]\[(]+?)\(\s*([^)\s]+\.md(?:#[^)\s]*)?)[^)]*\)', r'[\1](\2)', text)

    # Padrão de prefixos de documentação
    doc_refs = r'(?:Seção|Capítulo|Section|Chapter|Tabela|Table|Figura|Figure|Apêndice|Appendix)\s+[\d\.A-Z]+'

    # Regra 2: Prefixo seguido de [(url "titulo")] -> [Prefixo](url)
    # Ex: Seção 32.15 [(libpq-envars.md "titulo")] -> [Seção 32.15](libpq-envars.md)
    text = re.sub(fr'({doc_refs})\s*\[\(\s*([^)\s]+\.md(?:#[^)\s]*)?)[^)]*\)\]', r'[\1](\2)', text)

    # Regra 3: Prefixo seguido de (url "titulo") -> [Prefixo](url)
    # Ex: Seção 32.15 (libpq-envars.md "titulo") -> [Seção 32.15](libpq-envars.md)
    # O (?<!\[) garante que a regra não mexa em textos que já estão corretos como [Seção 32.15](...)
    text = re.sub(fr'(?<!\[)({doc_refs})\s*\(\s*([^)\s]+\.md(?:#[^)\s]*)?)[^)]*\)', r'[\1](\2)', text)

    return text


def fix_unclosed_html_tags(text):
    """
    Identifica tags HTML comumente deixadas abertas pelo tradutor/markdownify
    e insere as tags de fechamento para evitar warnings do Pandoc (ex: Div unclosed).
    """
    lines = text.split('\n')
    in_code_block = False

    global_div_balance = 0
    out_lines = []

    # Tags inline ou parciais que devem ser fechadas estritamente antes do fim de um parágrafo
    inline_tags = ['code', 'span', 'p', 'a', 'strong', 'em', 'kbd', 'samp']
    inline_tags_balance = {tag: 0 for tag in inline_tags}

    for line in lines:
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            out_lines.append(line)
            continue

        if in_code_block:
            out_lines.append(line)
            continue

        # Cria uma versão limpa da linha para ignorar tags perfeitamente escapadas dentro de crases (`)
        # e também ignora tags self-closing completas como <br/> ou <img/>
        safe_line = re.sub(r'`[^`]*`', '', line)
        safe_line = re.sub(r'<[a-zA-Z0-9]+\b[^>]*/>', '', safe_line)

        # 1. Balanceamento global de DIVs
        open_divs = len(re.findall(r'<div\b[^>]*>', safe_line, re.IGNORECASE))
        close_divs = len(re.findall(r'</div>', safe_line, re.IGNORECASE))
        global_div_balance += (open_divs - close_divs)

        # 2. Balanceamento de tags inline (contagem e fechamento por parágrafo)
        for tag in inline_tags:
            open_tags = len(re.findall(fr'<{tag}\b[^>]*>', safe_line, re.IGNORECASE))
            close_tags = len(re.findall(fr'</{tag}>', safe_line, re.IGNORECASE))
            inline_tags_balance[tag] += (open_tags - close_tags)

        out_lines.append(line)

        # Ao encontrar uma linha em branco (fim do parágrafo atual)
        if not line.strip():
            for tag in inline_tags:
                count = inline_tags_balance[tag]
                if count > 0:
                    # Sobe no array procurando a última linha que continha texto e injeta o fechamento lá
                    for idx in range(len(out_lines) - 2, -1, -1):
                        if out_lines[idx].strip():
                            out_lines[idx] += f"</{tag}>" * count
                            break
            # Reseta o balanço de inline tags para limpar o estado antes do próximo parágrafo
            inline_tags_balance = {tag: 0 for tag in inline_tags}

    # Garantia de limpeza: fecha tags inline pendentes caso o arquivo acabe sem quebra de parágrafo
    for tag in inline_tags:
        count = inline_tags_balance[tag]
        if count > 0:
            for idx in range(len(out_lines) - 1, -1, -1):
                if out_lines[idx].strip():
                    out_lines[idx] += f"</{tag}>" * count
                    break

    final_text = '\n'.join(out_lines)

    # Adiciona no final do documento as tags de bloco que nunca foram fechadas
    if global_div_balance > 0:
        final_text += "\n\n" + "</div>\n" * global_div_balance

    return final_text


def format_markdown_definitions(text):
    lines = text.split('\n')

    # PASSO 1: Achatar (Flatten) as listas de definição e remover a indentação fantasma
    pass1_lines = []
    i = 0
    in_def = False
    while i < len(lines):
        line = lines[i]

        m = re.match(r'^:\s+(.*)', line)
        if m and pass1_lines and pass1_lines[-1].strip() and not pass1_lines[-1].strip().startswith('|'):
            term = pass1_lines.pop().strip()
            def_text = m.group(1).strip()
            pass1_lines.append(f"{term}: {def_text}" if def_text else f"{term}:")
            in_def = True
            i += 1
            continue

        if in_def:
            if not line.strip():
                pass1_lines.append(line)
                i += 1
                continue

            if line.strip().startswith('```'):
                in_def = False
                pass1_lines.append(line)
                i += 1
                continue

            # Se for texto dentro da definição, remove até 4 espaços de indentação do DocBook
            indent_m = re.match(r'^ {1,4}(.*)', line)
            if indent_m:
                pass1_lines.append(indent_m.group(1))
                i += 1
                continue
            elif line.startswith('\t'):
                pass1_lines.append(line[1:])
                i += 1
                continue
            else:
                in_def = False  # Acabou a indentação, acabou o bloco

        pass1_lines.append(line)
        i += 1

    # PASSO 2: Limpar os blocos de código (alinhar cercas à esquerda e corrigir código na mesma linha)
    pass2_lines = []
    in_code_block = False
    fence_indent = 0
    lang_list = ['sql', 'c', 'python', 'bash', 'sh', 'json', 'yaml', 'html', 'xml', 'text', 'console', 'plpgsql',
                 'postgres', 'postgresql']

    for line in pass1_lines:
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            if in_code_block:  # Cerca de abertura
                fence_indent = len(line) - len(line.lstrip('\t '))
                code_content = stripped[3:].strip()

                # Se há texto colado na cerca e não é um marcador de linguagem, empurra para a próxima linha
                if code_content and code_content.lower() not in lang_list:
                    pass2_lines.append('```')
                    pass2_lines.append(code_content)
                else:
                    pass2_lines.append('```' + code_content)
            else:  # Cerca de fechamento
                pass2_lines.append('```')
            continue

        if in_code_block:
            # Subtrai do código a mesma quantidade de espaços que a cerca tinha, mantendo a indentação relativa intacta
            fixed_line = re.sub(f'^ {{0,{fence_indent}}}', '', line)
            pass2_lines.append(fixed_line)
            continue

        pass2_lines.append(line)

    # PASSO 3: Desembrulhar texto normal (remover hard wraps) e isolar notas parentéticas
    pass3_lines = []
    in_code_block = False

    for line in pass2_lines:
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            pass3_lines.append(line)
            continue

        if in_code_block:
            pass3_lines.append(line)
            continue

        is_normal_line = bool(stripped) and not stripped.startswith(('|', '#', '>', '<'))

        if is_normal_line and pass3_lines:
            prev_line = pass3_lines[-1]
            prev_stripped = prev_line.strip()

            is_prev_normal = bool(prev_stripped) and not prev_stripped.startswith(('|', '#', '>', '```', '<'))
            is_current_list_marker = re.match(r'^(\*|-|\+|\d+\.)\s', stripped)

            if is_prev_normal and not is_current_list_marker:
                # Regra de ouro: se a linha anterior terminou em ponto e a atual começa com parênteses, é um novo parágrafo.
                if prev_stripped.endswith('.') and stripped.startswith('('):
                    pass3_lines.append('')
                    pass3_lines.append(line.rstrip())
                else:
                    # Concatena fundindo os hard wraps
                    pass3_lines[-1] = pass3_lines[-1].rstrip() + " " + stripped
                continue

        pass3_lines.append(line.rstrip())

    return '\n'.join(pass3_lines)


def process_markdown_files():
    if not os.path.exists(MD_DIR):
        print(f"Diretório '{MD_DIR}' não encontrado. Execute o conversor original primeiro.")
        return

    md_files = [f for f in os.listdir(MD_DIR) if f.endswith('.md')]
    print(f"Formatando {len(md_files)} arquivos. Aguarde...\n")

    count = 0
    for filename in md_files:
        filepath = os.path.join(MD_DIR, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Aplica a formatação de definições de parágrafos
        new_content = format_markdown_definitions(content)
        # Aplica a indentação no HTML das tabelas preservadas
        new_content = format_html_tables(new_content)
        # Corrige links malformados
        new_content = format_broken_links(new_content)
        # Tenta reparar a perda de fechamento de tags do HTML que restou
        new_content = fix_unclosed_html_tags(new_content)

        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1

    print(f"Formatação concluída. {count} arquivos foram modificados.")


if __name__ == "__main__":
    process_markdown_files()