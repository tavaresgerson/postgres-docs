#!/usr/bin/env python3
"""Formata células HTML de tabelas em arquivos Markdown.

O script localiza blocos <td>...</td> e <th>...</th> em um arquivo e
normaliza o conteúdo interno para um formato mais legível, mantendo os
parágrafos em linhas separadas e compactando espaços em branco entre tags.
"""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import List

CELL_TAG_PATTERN = re.compile(r"(?P<indent>[ \t]*)<(?P<tag>td|th)\b(?P<attrs>[^>]*)>(?P<inner>.*?)</(?P=tag)>", re.S)


class _Node:
    def __init__(self, name: str, attrs: dict[str, str] | None = None, children: List[object] | None = None):
        self.name = name
        self.attrs = attrs or {}
        self.children: List[object] = children or []


class _HTMLTreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = _Node("document")
        self.stack: List[_Node] = [self.root]

    def handle_starttag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        node = _Node(tag, {k: (v or "") for k, v in attrs})
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: List[tuple[str, str | None]]) -> None:
        node = _Node(tag, {k: (v or "") for k, v in attrs})
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].name == tag:
                self.stack = self.stack[:index]
                break

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.stack[-1].children.append(data)


def _collapse_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _render_attrs(attrs: dict[str, str]) -> str:
    if not attrs:
        return ""
    parts = []
    for name, value in attrs.items():
        if value is None:
            value = ""
        parts.append(f'{name}="{value}"')
    return " " + " ".join(parts)


def _render_children(children: List[object], level: int) -> List[str]:
    lines: List[str] = []
    for child in children:
        if isinstance(child, str):
            text = _collapse_ws(child)
            if text:
                lines.append(" " * level + text)
            continue

        if child.name in {"p", "div", "li"}:
            inner_lines = _render_children(child.children, level + 1)
            if inner_lines:
                lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}>")
                lines.extend(inner_lines)
                lines.append(" " * level + f"</{child.name}>")
            else:
                lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}></{child.name}>")
            continue

        if child.name in {"code", "em", "strong", "a", "span", "sup", "sub"}:
            inner = _render_inline(child.children)
            lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}>{inner}</{child.name}>")
            continue

        if child.name in {"br"}:
            lines.append(" " * level + "<br />")
            continue

        if child.name in {"td", "th", "tr", "tbody", "thead", "table"}:
            inner_lines = _render_children(child.children, level + 1)
            if inner_lines:
                lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}>")
                lines.extend(inner_lines)
                lines.append(" " * level + f"</{child.name}>")
            else:
                lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}></{child.name}>")
            continue

        # Preserve any remaining tag names inline when possible.
        inner = _render_inline(child.children)
        if inner:
            lines.append(" " * level + f"<{child.name}{_render_attrs(child.attrs)}>{inner}</{child.name}>")

    return lines


def _render_inline(children: List[object]) -> str:
    parts: List[str] = []
    for child in children:
        if isinstance(child, str):
            parts.append(_collapse_ws(child))
        else:
            body = _render_inline(child.children)
            if child.name in {"code", "em", "strong", "a", "span", "sup", "sub"}:
                parts.append(f"<{child.name}{_render_attrs(child.attrs)}>{body}</{child.name}>")
            elif child.name in {"br"}:
                parts.append("<br />")
            else:
                parts.append(body)

    return " ".join([part for part in parts if part]).strip()


def _format_cell(match: re.Match[str]) -> str:
    indent = match.group("indent")
    tag = match.group("tag")
    attrs = match.group("attrs")
    inner_html = match.group("inner")

    parser = _HTMLTreeBuilder()
    parser.feed(inner_html)
    parser.close()

    body_lines = _render_children(parser.root.children, 1)
    body = "\n".join(body_lines).strip()

    if not body:
        return f"{indent}<{tag}{attrs}></{tag}>"

    lines = [f"{indent}<{tag}{attrs}>", *[f"{indent} {line}" if line else f"{indent}" for line in body.splitlines()], f"{indent}</{tag}>"]
    return "\n".join(lines)


def format_html_tables(text: str) -> str:
    return CELL_TAG_PATTERN.sub(_format_cell, text)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Formata células HTML de tabelas em arquivos Markdown.")
    parser.add_argument("path", nargs="?", default=".", help="Caminho para o arquivo Markdown (ou diretório).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    path = Path(args.path)

    if path.is_dir():
        files = sorted(path.rglob("*.md"))
    else:
        files = [path]

    for file_path in files:
        original_text = file_path.read_text(encoding="utf-8")
        updated_text = format_html_tables(original_text)
        if updated_text != original_text:
            file_path.write_text(updated_text, encoding="utf-8")
            print(f"Atualizado: {file_path}")
        else:
            print(f"Sem mudanças: {file_path}")


if __name__ == "__main__":
    main()
