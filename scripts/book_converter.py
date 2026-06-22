import subprocess
import re
import os
from pathlib import Path
import fitz  # PyMuPDF

PDF_FILE = "./books/postgresql-18-US.pdf"
OUTPUT_DIR = Path("./output")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text):
    """Remove caracteres especiais e espaços para criar nomes de pastas válidos."""
    text = str(text).strip()
    text = re.sub(r'[^\w\s-]', '', text).strip()
    text = re.sub(r'[\s-]+', '_', text)
    return text


# 1. Carregar o PDF com PyMuPDF
print(f"Lendo o PDF: {PDF_FILE}...")
doc = fitz.open(PDF_FILE)
total_pages = doc.page_count
print(f"Total de páginas: {total_pages}")

# 2. Obter capítulos (TOC - Table of Contents)
toc = doc.get_toc(simple=True)  # Retorna uma lista: [nivel, titulo, pagina]

if not toc:
    print("Aviso: Nenhum sumário (TOC) encontrado no PDF.")
    exit(1)

# Filtrar apenas o Nível 1 para pegar os capítulos principais.
nivel_maximo = 1
chapters = []
for level, title, page_num in toc:
    if level <= nivel_maximo:
        chapters.append({"title": title, "start_page": page_num - 1})

if not chapters:
    print("Nenhum capítulo de nível 1 encontrado. Tente aumentar 'nivel_maximo'.")
    exit(1)

# 3. Processar cada capítulo
for i, chapter in enumerate(chapters):
    chapter_title = chapter["title"]
    start_page = chapter["start_page"]

    if i + 1 < len(chapters):
        end_page = chapters[i + 1]["start_page"]
    else:
        end_page = total_pages

    if start_page >= end_page:
        continue

    safe_title = slugify(chapter_title)
    safe_title = (safe_title[:50] + '...') if len(safe_title) > 50 else safe_title
    chapter_folder_name = f"{i + 1:02d}_{safe_title}"

    chapter_dir = OUTPUT_DIR / chapter_folder_name
    chapter_dir.mkdir(parents=True, exist_ok=True)

    pdf_chunk_path = chapter_dir / f"{chapter_folder_name}.pdf"

    print(f"\nExtraindo capítulo {i + 1}: '{chapter_title}' (Páginas {start_page + 1} a {end_page})...")

    new_doc = fitz.open()
    new_doc.insert_pdf(doc, from_page=start_page, to_page=end_page - 1)
    new_doc.save(pdf_chunk_path)
    new_doc.close()

    print(f"PDF salvo em: {pdf_chunk_path}")

    # 5. Executar o marker-pdf no arquivo gerado (Forçando CPU)
    print(f"Executando marker-pdf (via CPU) para gerar o Markdown...")
    try:
        cmd = [
            "marker_single",
            str(pdf_chunk_path),
            "--output_dir", str(chapter_dir)
        ]

        # Força o uso da CPU
        env = os.environ.copy()
        env["CUDA_VISIBLE_DEVICES"] = "-1"
        env["TORCH_DEVICE"] = "cpu"

        subprocess.run(cmd, check=True, env=env)
        print(f"Markdown gerado com sucesso em: {chapter_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o marker-pdf no capítulo {i + 1}: {e}")
    except FileNotFoundError:
        print("Erro: O comando 'marker_single' não foi encontrado. Verifique a instalação do marker-pdf.")

doc.close()
print("\nProcesso concluído! Todos os capítulos foram processados.")