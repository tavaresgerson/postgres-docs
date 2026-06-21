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

        if content != new_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            count += 1

    print(f"Formatação concluída. {count} arquivos foram modificados.")


if __name__ == "__main__":
    process_markdown_files()