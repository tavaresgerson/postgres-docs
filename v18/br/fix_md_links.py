#!/usr/bin/env python3
"""Corrige links internos quebrados em arquivos Markdown.

O script cria um mapa de arquivos Markdown baseado em nomes originais sem
prefixos numéricos do tipo "N-" e atualiza links Markdown que referenciam
arquivos pelo nome antigo.

Modo dry-run pode ser ativado no topo do arquivo.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Ative o dry-run definindo como True.
DRY_RUN = False

LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PREFIX_PATTERN = re.compile(r"^(\d+)-(.+\.md)$")


def build_lookup(root: Path) -> Dict[str, str]:
    """Constrói o mapa de nome_original.md => caminho/relativo/do/arquivo."""
    lookup: Dict[str, str] = {}

    for path in sorted(root.rglob("*.md")):
        if path.is_file():
            relative_path = path.relative_to(root).as_posix()
            match = PREFIX_PATTERN.match(path.name)
            if match:
                original_name = match.group(2)
            else:
                original_name = path.name

            if original_name in lookup:
                print(
                    f"Aviso: nome duplicado encontrado para '{original_name}'."
                    f" Mantendo '{lookup[original_name]}' e ignorando '{relative_path}'."
                )
            else:
                lookup[original_name] = relative_path
    return lookup


def should_ignore_target(target: str) -> bool:
    """Retorna True para links que não devem ser corrigidos."""
    target = target.strip()
    if target.startswith("http://") or target.startswith("https://"):
        return True
    if target.startswith("#"):
        return True
    return False


def replace_links_in_text(text: str, lookup: Dict[str, str]) -> Tuple[str, int]:
    """Substitui links no texto e retorna o texto atualizado e o número de alterações."""
    replacements = 0

    def replace(match: re.Match) -> str:
        nonlocal replacements
        label = match.group(1)
        target = match.group(2).strip()

        if should_ignore_target(target):
            return match.group(0)

        # Extrai apenas o nome do arquivo sem diretório.
        target_basename = Path(target).name
        if target_basename in lookup:
            new_target = lookup[target_basename]
            if new_target != target:
                replacements += 1
                return f"[{label}]({new_target})"

        return match.group(0)

    updated_text = LINK_PATTERN.sub(replace, text)
    return updated_text, replacements


def update_files(root: Path, lookup: Dict[str, str], dry_run: bool) -> Tuple[int, int]:
    """Varre os arquivos Markdown e corrige links internos."""
    files_scanned = 0
    total_replacements = 0

    for path in sorted(root.rglob("*.md")):
        if not path.is_file():
            continue

        files_scanned += 1
        original_text = path.read_text(encoding="utf-8")
        updated_text, replacements = replace_links_in_text(original_text, lookup)

        if replacements > 0:
            total_replacements += replacements
            print(f"{path.relative_to(root)}: {replacements} link(s) atualizados")
            if not dry_run:
                path.write_text(updated_text, encoding="utf-8")

    return files_scanned, total_replacements


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Corrige links internos quebrados em Markdown usando um mapa de arquivos renomeados."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Caminho para a raiz do projeto onde estão os arquivos Markdown.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Exibe as alterações que seriam feitas, sem gravar arquivos.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.root).resolve()
    dry_run = args.dry_run or DRY_RUN

    print(f"Raiz do projeto: {root}")
    print(f"Modo dry-run: {'sim' if dry_run else 'não'}")

    lookup = build_lookup(root)
    print(f"Mapa de nomes originais carregado: {len(lookup)} arquivo(s) Markdown")

    files_scanned, total_replacements = update_files(root, lookup, dry_run)
    print("\nResumo final:")
    print(f"  Arquivos varridos: {files_scanned}")
    print(f"  Links corrigidos: {total_replacements}")


if __name__ == "__main__":
    main()
