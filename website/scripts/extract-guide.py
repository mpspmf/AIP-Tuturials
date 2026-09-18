"""Extrai o guia AIP para dados TypeScript e imagens PNG.

O script lê os ficheiros originais sem os alterar. A lista Excel é incluída
apenas como exemplo pedagógico, substituindo os endereços reais por endereços
fictícios no domínio example.com. O modelo Word é apresentado com a duplicação
do campo Nome corrigida.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from zipfile import ZipFile
import json
import re
import struct
import unicodedata
import xml.etree.ElementTree as ET

import openpyxl


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
W = f"{{{NS['w']}}}"
R = f"{{{NS['r']}}}"
A = f"{{{NS['a']}}}"

TYPE_DECLARATIONS = """export interface GuideFigure {
  id: number;
  src: string;
  width: number;
  height: number;
  caption: string;
}

export type GuideBlock =
  | { id: string; kind: 'paragraph'; text: string; figureIds?: number[] }
  | { id: string; kind: 'heading'; text: string }
  | { id: string; kind: 'step'; number: number; text: string; figureIds?: number[] }
  | { id: string; kind: 'table'; headers: string[]; rows: string[][] }
  | { id: string; kind: 'callout'; title: string; text: string; figureIds?: number[] }
  | { id: string; kind: 'example'; title: string; text: string };

export interface GuideChapter {
  id: string;
  title: string;
  shortTitle: string;
  intro: string;
  blocks: GuideBlock[];
  figures: GuideFigure[];
}
"""

SHORT_TITLES = {
    "01": "Como utilizar",
    "02": "Escolher a ferramenta",
    "03": "Conversar no Teams",
    "04": "Normas de utilização",
    "05": "Criar equipa e canais",
    "06": "Utilizar canais",
    "07": "Calendário do Teams",
    "08": "Calendário do canal",
    "09": "Planner no Teams",
    "10": "Emails em série",
}


def normalize_text(node: ET.Element) -> str:
    """Extrai texto OOXML, preservando quebras explícitas e normalizando espaços."""
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


def embedded_rel_ids(paragraph: ET.Element) -> list[str]:
    return [item.get(R + "embed", "") for item in paragraph.findall(".//a:blip", NS)]


def png_dimensions(data: bytes) -> tuple[int, int]:
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise ValueError("A imagem incorporada não é PNG e não pode ser copiada diretamente.")
    return struct.unpack(">II", data[16:24])


def make_block(chapter: dict, kind: str, **fields) -> dict:
    number = len(chapter["blocks"]) + 1
    block = {"id": f"{chapter['id']}-{kind}-{number:02d}", "kind": kind, **fields}
    chapter["blocks"].append(block)
    return block


def table_data(table: ET.Element) -> tuple[list[str], list[list[str]]]:
    rows = []
    for row in table.findall("w:tr", NS):
        rows.append([normalize_text(cell) for cell in row.findall("w:tc", NS)])
    if not rows:
        raise ValueError("Tabela vazia no guia.")
    return rows[0], rows[1:]


def extract_docx_paragraphs(path: Path) -> list[str]:
    with ZipFile(path) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    return [normalize_text(p) for p in root.findall(".//w:body/w:p", NS) if normalize_text(p)]


def sanitized_recipients(recipients_xlsx: Path) -> tuple[list[str], list[list[str]]]:
    workbook = openpyxl.load_workbook(recipients_xlsx, read_only=True, data_only=True)
    sheet = workbook.active
    values = [["" if value is None else str(value) for value in row] for row in sheet.iter_rows(values_only=True)]
    workbook.close()
    headers, rows = values[0], values[1:]
    expected = ["Email", "Nome", "Empresa", "Saudacao"]
    if headers != expected:
        raise ValueError(f"Cabeçalhos inesperados na lista: {headers!r}")

    sanitized: list[list[str]] = []
    for _, name, company, greeting in rows:
        slug = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", ".", slug.lower()).strip(".")
        sanitized.append([f"{slug}@example.com", name, company, greeting])
    return headers, sanitized


def corrected_invite_example(invite_docx: Path) -> str:
    paragraphs = extract_docx_paragraphs(invite_docx)
    if not paragraphs or paragraphs[0].count("«Nome»") != 2:
        raise ValueError("O modelo de convite já não contém a duplicação esperada do campo Nome.")
    paragraphs[0] = "«Saudacao» «Nome»,"
    return "\n\n".join(paragraphs)


def add_chapter_10_examples(chapter: dict, recipients_xlsx: Path, invite_docx: Path) -> None:
    headers, rows = sanitized_recipients(recipients_xlsx)
    list_index = next(
        index for index, block in enumerate(chapter["blocks"])
        if block.get("figureIds") == [37]
    )
    table_block = {
        "id": f"{chapter['id']}-table-example",
        "kind": "table",
        "headers": headers,
        "rows": rows,
    }
    chapter["blocks"].insert(list_index + 1, table_block)

    word_index = next(
        index for index, block in enumerate(chapter["blocks"])
        if block["kind"] == "paragraph" and block["text"].startswith("Use o Word para preparar")
    )
    example_block = {
        "id": f"{chapter['id']}-example-invite",
        "kind": "example",
        "title": "Exemplo corrigido do modelo no Word",
        "text": corrected_invite_example(invite_docx),
    }
    chapter["blocks"].insert(word_index + 1, example_block)


def extract(
    guide_docx: Path,
    recipients_xlsx: Path,
    invite_docx: Path,
    image_dir: Path,
) -> list[dict]:
    image_dir.mkdir(parents=True, exist_ok=True)

    chapters: list[dict] = []
    chapter: dict | None = None
    last_text_block: dict | None = None
    pending_image: tuple[str, bytes] | None = None

    with ZipFile(guide_docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
        rel_root = ET.fromstring(archive.read("word/_rels/document.xml.rels"))
        rels = {rel.get("Id", ""): rel.get("Target", "") for rel in rel_root}
        body = root.find("w:body", NS)
        if body is None:
            raise ValueError("O documento não contém um corpo OOXML.")

        for element in body:
            if element.tag == W + "tbl":
                if chapter is not None:
                    headers, rows = table_data(element)
                    make_block(chapter, "table", headers=headers, rows=rows)
                    last_text_block = None
                continue
            if element.tag != W + "p":
                continue

            style = paragraph_style(element)
            text = normalize_text(element)
            rel_ids = embedded_rel_ids(element)

            if style == "Ttulo1":
                match = re.fullmatch(r"(\d{2})\s+(.+)", text)
                if not match:
                    raise ValueError(f"Título de capítulo inesperado: {text!r}")
                chapter_id, title = match.groups()
                chapter = {
                    "id": chapter_id,
                    "title": title,
                    "shortTitle": SHORT_TITLES[chapter_id],
                    "intro": "",
                    "blocks": [],
                    "figures": [],
                }
                chapters.append(chapter)
                last_text_block = None
                continue

            if chapter is None:
                continue

            if rel_ids:
                if len(rel_ids) != 1:
                    raise ValueError(f"Parágrafo com {len(rel_ids)} imagens; era esperada uma.")
                target = rels[rel_ids[0]]
                source_name = "word/" + target.lstrip("/")
                pending_image = (target, archive.read(source_name))
                continue

            if style == "Legenda1":
                match = re.fullmatch(r"Figura\s+(\d+)\s+—\s+(.+)", text)
                if not match or pending_image is None:
                    raise ValueError(f"Legenda sem imagem ou formato inesperado: {text!r}")
                figure_id = int(match.group(1))
                caption = match.group(2)
                target, image_data = pending_image
                if not target.lower().endswith(".png"):
                    raise ValueError(f"A Figura {figure_id} não está armazenada como PNG: {target}")
                width, height = png_dimensions(image_data)
                output_image = image_dir / f"figure-{figure_id:02d}.png"
                output_image.write_bytes(image_data)
                chapter["figures"].append({
                    "id": figure_id,
                    "src": f"/images/figure-{figure_id:02d}.png",
                    "width": width,
                    "height": height,
                    "caption": caption,
                })
                if last_text_block is not None:
                    last_text_block.setdefault("figureIds", []).append(figure_id)
                pending_image = None
                continue

            if not text:
                continue
            if not chapter["intro"]:
                chapter["intro"] = text
                last_text_block = None
                continue
            if style == "Ttulo2":
                make_block(chapter, "heading", text=text)
                last_text_block = None
                continue

            step_match = re.fullmatch(r"(\d+)\.\s+(.+)", text, flags=re.DOTALL)
            if step_match:
                last_text_block = make_block(
                    chapter,
                    "step",
                    number=int(step_match.group(1)),
                    text=step_match.group(2),
                )
            else:
                last_text_block = make_block(chapter, "paragraph", text=text)

    if pending_image is not None:
        raise ValueError("Ficou uma imagem sem legenda no fim do documento.")
    if [chapter["id"] for chapter in chapters] != [f"{n:02d}" for n in range(1, 11)]:
        raise ValueError("A sequência de capítulos não corresponde a 01–10.")

    add_chapter_10_examples(chapters[-1], recipients_xlsx, invite_docx)
    return chapters


def write_typescript(chapters: list[dict], output_ts: Path) -> None:
    payload = json.dumps(chapters, ensure_ascii=False, indent=2)
    output_ts.parent.mkdir(parents=True, exist_ok=True)
    output_ts.write_text(
        TYPE_DECLARATIONS + "\nexport const chapters: GuideChapter[] = " + payload + ";\n",
        encoding="utf-8",
        newline="\n",
    )


def verify(chapters: list[dict], image_dir: Path) -> None:
    figures = [figure for chapter in chapters for figure in chapter["figures"]]
    if [figure["id"] for figure in figures] != list(range(1, 41)):
        raise ValueError("A sequência de figuras extraídas não corresponde a 1–40.")
    if any(not (image_dir / f"figure-{number:02d}.png").is_file() for number in range(1, 41)):
        raise ValueError("Faltam ficheiros de imagem na pasta de saída.")
    if chapters[0]["figures"] or chapters[1]["figures"]:
        raise ValueError("Os capítulos 01 e 02 não deveriam conter figuras.")
    chapter_02_tables = [block for block in chapters[1]["blocks"] if block["kind"] == "table"]
    if len(chapter_02_tables) != 1 or len(chapter_02_tables[0]["headers"]) != 3:
        raise ValueError("A tabela do capítulo 02 não tem as três colunas esperadas.")
    if not any(block.get("figureIds") == [5, 6] for block in chapters[3]["blocks"]):
        raise ValueError("As figuras 5 e 6 não estão associadas ao bloco de notificações.")
    if not any(block.get("figureIds") == [37] for block in chapters[9]["blocks"]):
        raise ValueError("A Figura 37 não está associada ao parágrafo de preparação da lista.")
    planner_steps = [block["number"] for block in chapters[8]["blocks"] if block["kind"] == "step"]
    if planner_steps != [1, 2, 3, 4, 5, 6, 1, 2]:
        raise ValueError(f"Numeração inesperada nos procedimentos do Planner: {planner_steps}")
    serialized = json.dumps(chapters, ensure_ascii=False)
    if "gmail.com" in serialized:
        raise ValueError("Foi encontrado um endereço Gmail nos dados de saída.")
    block_ids = [block["id"] for chapter in chapters for block in chapter["blocks"]]
    if len(block_ids) != len(set(block_ids)):
        raise ValueError("Existem ids de blocos repetidos.")


def resolve_project_dir(value: str | None) -> Path:
    """Resolve a raiz do website; quando instalado, é a pasta pai de scripts/."""
    return Path(value).resolve() if value else Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrai o guia AIP para o website.")
    parser.add_argument(
        "--project-dir",
        help="Raiz do website; por omissão usa a pasta pai de scripts/.",
    )
    args = parser.parse_args()

    project_dir = resolve_project_dir(args.project_dir)
    source_dir = project_dir.parent
    guide_docx = source_dir / "AIP_GUIA.docx"
    recipients_xlsx = source_dir / "Lista_Demonstracao_AIP.xlsx"
    invite_docx = source_dir / "Modelo_Convite_AIP.docx"
    output_ts = project_dir / "data" / "guide.ts"
    image_dir = project_dir / "public" / "images"

    chapters = extract(guide_docx, recipients_xlsx, invite_docx, image_dir)
    verify(chapters, image_dir)
    write_typescript(chapters, output_ts)
    block_count = sum(len(chapter["blocks"]) for chapter in chapters)
    figure_count = sum(len(chapter["figures"]) for chapter in chapters)
    print(
        f"Gerados {len(chapters)} capítulos, {block_count} blocos e {figure_count} figuras "
        f"em {project_dir}."
    )


if __name__ == "__main__":
    main()
