"""Valida, sem escrever ficheiros, o guia AIP instalado no website."""

from __future__ import annotations

import argparse
from hashlib import sha256
from pathlib import Path
from zipfile import ZipFile
import json
import re
import struct
import xml.etree.ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
W = f"{{{NS['w']}}}"

EXPECTED_LINKS = {
    3: [(1, [1]), (2, [2]), (3, [3]), (4, []), (5, [4])],
    5: [(1, [7]), (2, [8]), (3, [9]), (4, [10]), (5, [11]), (6, [12]), (7, [])],
    6: [(1, [13, 14]), (2, [15]), (3, [16]), (4, [17]), (5, [18])],
    7: [(1, [19]), (2, [20, 21]), (3, [22]), (4, [])],
    8: [(1, [23, 24]), (2, [25]), (3, [26, 27])],
    10: [(1, []), (2, [38]), (3, [39]), (4, []), (5, []), (6, [40]), (7, [])],
}


def resolve_project_dir(value: str | None) -> Path:
    """Resolve a raiz do website; quando instalado, é a pasta pai de scripts/."""
    return Path(value).resolve() if value else Path(__file__).resolve().parents[1]


def normalize_text(node: ET.Element) -> str:
    parts: list[str] = []
    for item in node.iter():
        if item.tag == W + "t":
            parts.append(item.text or "")
        elif item.tag == W + "tab":
            parts.append("\t")
        elif item.tag in {W + "br", W + "cr"}:
            parts.append("\n")
    raw = "".join(parts).replace("\u00a0", " ")
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in raw.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return "\n".join(lines)


def paragraph_style(paragraph: ET.Element) -> str:
    style = paragraph.find("w:pPr/w:pStyle", NS)
    return style.get(W + "val", "") if style is not None else ""


def table_data(table: ET.Element) -> tuple[list[str], list[list[str]]]:
    rows = [
        [normalize_text(cell) for cell in row.findall("w:tc", NS)]
        for row in table.findall("w:tr", NS)
    ]
    assert rows
    return rows[0], rows[1:]


def load_chapters(guide_ts: Path) -> list[dict]:
    source = guide_ts.read_text(encoding="utf-8")
    marker = "export const chapters: GuideChapter[] = "
    payload = source.split(marker, 1)[1].rsplit(";", 1)[0]
    return json.loads(payload)


def source_chapters(guide_docx: Path) -> list[dict]:
    """Extrai a sequência semântica da fonte para detetar qualquer parágrafo omitido."""
    with ZipFile(guide_docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    body = root.find("w:body", NS)
    assert body is not None

    chapters: list[dict] = []
    chapter: dict | None = None
    for element in body:
        if element.tag == W + "tbl":
            if chapter is not None:
                headers, rows = table_data(element)
                chapter["blocks"].append({"kind": "table", "headers": headers, "rows": rows})
            continue
        if element.tag != W + "p":
            continue

        style = paragraph_style(element)
        text = normalize_text(element)
        if style == "Ttulo1":
            match = re.fullmatch(r"(\d{2})\s+(.+)", text)
            assert match
            chapter = {
                "id": match.group(1),
                "title": match.group(2),
                "intro": "",
                "blocks": [],
            }
            chapters.append(chapter)
            continue
        if chapter is None or not text or element.findall(".//a:blip", NS) or style == "Legenda1":
            continue
        if not chapter["intro"]:
            chapter["intro"] = text
            continue
        if style == "Ttulo2":
            chapter["blocks"].append({"kind": "heading", "text": text})
            continue
        step_match = re.fullmatch(r"(\d+)\.\s+(.+)", text, flags=re.DOTALL)
        if step_match:
            chapter["blocks"].append({
                "kind": "step",
                "number": int(step_match.group(1)),
                "text": step_match.group(2),
            })
        else:
            chapter["blocks"].append({"kind": "paragraph", "text": text})
    return chapters


def source_invite_example(invite_docx: Path) -> str:
    with ZipFile(invite_docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs = [
        normalize_text(paragraph)
        for paragraph in root.findall(".//w:body/w:p", NS)
        if normalize_text(paragraph)
    ]
    assert paragraphs and paragraphs[0].count("«Nome»") == 2
    paragraphs[0] = "«Saudacao» «Nome»,"
    return "\n\n".join(paragraphs)


def source_block_view(block: dict) -> dict:
    if block["kind"] in {"heading", "paragraph"}:
        return {"kind": block["kind"], "text": block["text"]}
    if block["kind"] == "step":
        return {"kind": "step", "number": block["number"], "text": block["text"]}
    if block["kind"] == "table":
        return {"kind": "table", "headers": block["headers"], "rows": block["rows"]}
    raise AssertionError(f"Bloco de fonte inesperado: {block['kind']}")


def png_dimensions(data: bytes) -> tuple[int, int]:
    assert data[:8] == b"\x89PNG\r\n\x1a\n" and data[12:16] == b"IHDR"
    return struct.unpack(">II", data[16:24])


def step_links(chapter: dict) -> list[tuple[int, list[int]]]:
    return [
        (block["number"], block.get("figureIds", []))
        for block in chapter["blocks"]
        if block["kind"] == "step"
    ]


def validate(project_dir: Path) -> tuple[int, int, int]:
    source_dir = project_dir.parent
    guide_docx = source_dir / "AIP_GUIA.docx"
    invite_docx = source_dir / "Modelo_Convite_AIP.docx"
    guide_ts = project_dir / "data" / "guide.ts"
    image_dir = project_dir / "public" / "images"

    chapters = load_chapters(guide_ts)
    expected_source = source_chapters(guide_docx)
    assert [item["id"] for item in chapters] == [f"{number:02d}" for number in range(1, 11)]
    assert len(expected_source) == len(chapters)

    for expected, actual in zip(expected_source, chapters, strict=True):
        assert (expected["id"], expected["title"], expected["intro"]) == (
            actual["id"], actual["title"], actual["intro"]
        )
        actual_source_blocks = [
            source_block_view(block)
            for block in actual["blocks"]
            if block["id"] not in {"10-table-example", "10-example-invite"}
        ]
        assert expected["blocks"] == actual_source_blocks, f"Cobertura incompleta no capítulo {actual['id']}"

    all_figures = [figure for chapter in chapters for figure in chapter["figures"]]
    assert [figure["id"] for figure in all_figures] == list(range(1, 41))
    assert all(figure["src"] == f"/images/figure-{figure['id']:02d}.png" for figure in all_figures)
    assert all(not re.match(r"Figura\s+\d+", figure["caption"]) for figure in all_figures)

    with ZipFile(guide_docx) as archive:
        for figure in all_figures:
            number = figure["id"]
            source_data = archive.read(f"word/media/image{number}.png")
            output_data = (image_dir / f"figure-{number:02d}.png").read_bytes()
            assert sha256(source_data).digest() == sha256(output_data).digest()
            assert png_dimensions(output_data) == (figure["width"], figure["height"])

    for chapter in chapters:
        block_ids = [block["id"] for block in chapter["blocks"]]
        assert len(block_ids) == len(set(block_ids))
        assert not any(
            block["kind"] == "paragraph" and block["text"] == chapter["intro"]
            for block in chapter["blocks"]
        )
        chapter_figure_ids = {figure["id"] for figure in chapter["figures"]}
        for block in chapter["blocks"]:
            assert set(block.get("figureIds", [])).issubset(chapter_figure_ids)

    chapter_02_table = next(block for block in chapters[1]["blocks"] if block["kind"] == "table")
    assert chapter_02_table["headers"] == ["Necessidade", "Onde trabalhar", "Exemplo"]
    assert all(len(row) == 3 for row in chapter_02_table["rows"])
    assert any(block.get("figureIds") == [5, 6] for block in chapters[3]["blocks"])
    assert any(block.get("figureIds") == [37] for block in chapters[9]["blocks"])

    for chapter_number, expected in EXPECTED_LINKS.items():
        assert step_links(chapters[chapter_number - 1]) == expected
    assert step_links(chapters[8]) == [
        (1, [28]), (2, [29]), (3, [30]), (4, [31]),
        (5, [32, 33]), (6, [34]), (1, [35]), (2, [36]),
    ]

    example_table = next(block for block in chapters[9]["blocks"] if block["id"] == "10-table-example")
    assert example_table["headers"] == ["Email", "Nome", "Empresa", "Saudacao"]
    assert len(example_table["rows"]) == 3
    assert all(
        len(row) == 4 and row[0].endswith("@example.com") and row[1] and row[2] and row[3]
        for row in example_table["rows"]
    )
    invite_example = next(block for block in chapters[9]["blocks"] if block["id"] == "10-example-invite")
    assert invite_example["text"] == source_invite_example(invite_docx)
    assert invite_example["text"].count("«Nome»") == 1
    assert all(field in invite_example["text"] for field in ("«Saudacao»", "«Nome»", "«Empresa»"))

    text = guide_ts.read_text(encoding="utf-8")
    assert "gmail.com" not in text.lower()
    assert text.count("@example.com") == 3
    assert not list(project_dir.rglob("*.docx"))
    assert not list(project_dir.rglob("*.xlsx"))
    return len(chapters), sum(len(chapter["blocks"]) for chapter in chapters), len(all_figures)


def main() -> None:
    parser = argparse.ArgumentParser(description="Valida o guia AIP instalado no website.")
    parser.add_argument(
        "--project-dir",
        help="Raiz do website; por omissão usa a pasta pai de scripts/.",
    )
    args = parser.parse_args()
    project_dir = resolve_project_dir(args.project_dir)
    chapter_count, block_count, figure_count = validate(project_dir)
    print(
        f"Validação concluída em {project_dir}: {chapter_count} capítulos, "
        f"{block_count} blocos, cobertura integral da fonte e "
        f"{figure_count} imagens com hash idêntico à fonte."
    )


if __name__ == "__main__":
    main()
