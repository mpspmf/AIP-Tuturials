# -*- coding: utf-8 -*-
"""Gera o manual PDF, a apresentação PowerPoint e o guião de vídeo (PT-PT)."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt
from reportlab.lib.colors import Color, HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(__file__).resolve().parent / "materiais"
OUT.mkdir(exist_ok=True)

NAVY = HexColor("#1B2A4A")
TEAMS = HexColor("#6264A7")
TEAMS_DARK = HexColor("#464EB8")
ACCENT = HexColor("#C4314B")
LIGHT = HexColor("#F4F5FB")
GREY = HexColor("#5B5FC7")
TEXT = HexColor("#1F2430")
MUTED = HexColor("#5C6370")
GREEN = HexColor("#237B4B")
AMBER = HexColor("#8A5A00")

PPT_NAVY = RGBColor(0x1B, 0x2A, 0x4A)
PPT_TEAMS = RGBColor(0x62, 0x64, 0xA7)
PPT_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PPT_TEXT = RGBColor(0x1F, 0x24, 0x30)
PPT_MUTED = RGBColor(0x5C, 0x63, 0x70)
PPT_LIGHT = RGBColor(0xF4, 0xF5, 0xFB)
PPT_GREEN = RGBColor(0x23, 0x7B, 0x4B)
PPT_AMBER = RGBColor(0x8A, 0x5A, 0x00)
PPT_RED = RGBColor(0xC4, 0x31, 0x4B)


def register_fonts():
    candidates = [
        (
            "Calibri",
            r"C:\Windows\Fonts\calibri.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
            r"C:\Windows\Fonts\calibrii.ttf",
        ),
        (
            "SegoeUI",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\segoeuii.ttf",
        ),
    ]
    for name, regular, bold, italic in candidates:
        r, b, i = Path(regular), Path(bold), Path(italic)
        if r.exists() and b.exists():
            pdfmetrics.registerFont(TTFont(name, str(r)))
            pdfmetrics.registerFont(TTFont(f"{name}-Bold", str(b)))
            if i.exists():
                pdfmetrics.registerFont(TTFont(f"{name}-Italic", str(i)))
            return name, f"{name}-Bold", f"{name}-Italic" if i.exists() else name
    return "Helvetica", "Helvetica-Bold", "Helvetica-Oblique"


FONT, FONT_B, FONT_I = register_fonts()


def styles():
    ss = getSampleStyleSheet()
    ss.add(
        ParagraphStyle(
            "CoverKicker",
            fontName=FONT_B,
            fontSize=11,
            textColor=TEAMS,
            tracking=1.2,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            "CoverTitle",
            fontName=FONT_B,
            fontSize=28,
            leading=34,
            textColor=NAVY,
            spaceAfter=12,
        )
    )
    ss.add(
        ParagraphStyle(
            "CoverSub",
            fontName=FONT,
            fontSize=13,
            leading=18,
            textColor=MUTED,
            spaceAfter=6,
        )
    )
    ss.add(
        ParagraphStyle(
            "H1",
            fontName=FONT_B,
            fontSize=16,
            leading=20,
            textColor=NAVY,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            "H2",
            fontName=FONT_B,
            fontSize=12.5,
            leading=16,
            textColor=TEAMS_DARK,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    ss.add(
        ParagraphStyle(
            "Body",
            fontName=FONT,
            fontSize=10.2,
            leading=14.4,
            textColor=TEXT,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
        )
    )
    ss.add(
        ParagraphStyle(
            "BodyLeft",
            parent=ss["Body"],
            alignment=TA_LEFT,
        )
    )
    ss.add(
        ParagraphStyle(
            "BulletBody",
            fontName=FONT,
            fontSize=10.2,
            leading=14.2,
            textColor=TEXT,
            leftIndent=4,
        )
    )
    ss.add(
        ParagraphStyle(
            "Caption",
            fontName=FONT_I,
            fontSize=8.5,
            leading=11,
            textColor=MUTED,
            spaceBefore=2,
            spaceAfter=10,
        )
    )
    ss.add(
        ParagraphStyle(
            "TOC",
            fontName=FONT,
            fontSize=11,
            leading=18,
            textColor=TEXT,
        )
    )
    ss.add(
        ParagraphStyle(
            "Footer",
            fontName=FONT,
            fontSize=8,
            textColor=MUTED,
        )
    )
    ss.add(
        ParagraphStyle(
            "Cell",
            fontName=FONT,
            fontSize=8.8,
            leading=12,
            textColor=TEXT,
        )
    )
    ss.add(
        ParagraphStyle(
            "CellHead",
            fontName=FONT_B,
            fontSize=9,
            leading=12,
            textColor=white,
        )
    )
    ss.add(
        ParagraphStyle(
            "Callout",
            fontName=FONT,
            fontSize=10,
            leading=14,
            textColor=NAVY,
            leftIndent=8,
            rightIndent=8,
        )
    )
    ss.add(
        ParagraphStyle(
            "SmallCenter",
            fontName=FONT,
            fontSize=9,
            leading=12,
            textColor=MUTED,
            alignment=TA_CENTER,
        )
    )
    return ss


S = styles()


def bullets(items):
    return ListFlowable(
        [ListItem(Paragraph(i, S["BulletBody"]), leftIndent=12, bulletColor=TEAMS) for i in items],
        bulletType="bullet",
        start="circle",
        leftIndent=16,
        bulletFontName=FONT,
        bulletFontSize=8,
        spaceBefore=2,
        spaceAfter=10,
    )


def table(headers, rows, col_widths):
    head = [Paragraph(h, S["CellHead"]) for h in headers]
    body = [[Paragraph(c, S["Cell"]) for c in row] for row in rows]
    data = [head] + body
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAMS_DARK),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("BACKGROUND", (0, 1), (-1, -1), white),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, LIGHT]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("GRID", (0, 0), (-1, -1), 0.3, HexColor("#D8DCE8")),
                ("BOX", (0, 0), (-1, -1), 0.6, TEAMS),
            ]
        )
    )
    return t


def callout(text):
    p = Paragraph(text, S["Callout"])
    t = Table([[p]], colWidths=[16.5 * cm])
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0, TEAMS),
                ("LINEBEFORE", (0, 0), (0, -1), 4, TEAMS),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return t


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 14 * mm, A4[0], 14 * mm, fill=1, stroke=0)
    canvas.setFillColor(TEAMS)
    canvas.rect(0, A4[1] - 16 * mm, A4[0], 2 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(FONT, 8)
    canvas.drawString(18 * mm, A4[1] - 10 * mm, "AIP  ·  Manual de comunicação interna")
    canvas.drawRightString(A4[0] - 18 * mm, A4[1] - 10 * mm, "Microsoft Teams")
    canvas.setFillColor(LIGHT)
    canvas.rect(0, 0, A4[0], 12 * mm, fill=1, stroke=0)
    canvas.setFillColor(MUTED)
    canvas.setFont(FONT, 8)
    canvas.drawString(18 * mm, 5 * mm, "Uso interno  ·  Português (Portugal)")
    canvas.drawRightString(A4[0] - 18 * mm, 5 * mm, f"{doc.page}")
    canvas.restoreState()


def cover_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, A4[0], A4[1], fill=1, stroke=0)
    canvas.setFillColor(TEAMS)
    canvas.rect(0, 0, 18 * mm, A4[1], fill=1, stroke=0)
    canvas.setFillColor(TEAMS_DARK)
    canvas.rect(0, A4[1] - 42 * mm, A4[0], 42 * mm, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont(FONT_B, 11)
    canvas.drawString(28 * mm, A4[1] - 22 * mm, "COMUNICAÇÃO INTERNA")
    canvas.setFont(FONT, 10)
    canvas.drawString(28 * mm, A4[1] - 32 * mm, "Guia de utilização  ·  Microsoft Teams")
    canvas.setFillColor(white)
    canvas.setFont(FONT_B, 26)
    y = A4[1] - 95 * mm
    for line in [
        "Do e-mail ao Teams:",
        "como comunicar mais",
        "depressa, sem perder",
        "o que é formal.",
    ]:
        canvas.drawString(28 * mm, y, line)
        y -= 12 * mm
    canvas.setFillColor(HexColor("#C9CCE8"))
    canvas.setFont(FONT, 12)
    canvas.drawString(
        28 * mm,
        70 * mm,
        "Manual de instruções para colaboradores e diretores de AO",
    )
    canvas.setFont(FONT, 10)
    canvas.drawString(28 * mm, 52 * mm, "AIP")
    canvas.drawString(28 * mm, 42 * mm, "Versão 1.0  ·  2026")
    canvas.restoreState()


def build_pdf():
    path = OUT / "Manual_Microsoft_Teams_AIP.pdf"
    doc = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=18 * mm,
        title="Manual Microsoft Teams — AIP",
        author="AIP",
        subject="Comunicação interna: Teams vs e-mail",
    )
    story = []
    story.append(Spacer(1, 16 * cm))
    story.append(PageBreak())

    story.append(Paragraph("Índice", S["H1"]))
    toc = [
        "1. Para que serve este manual",
        "2. Onde estamos hoje e para onde queremos ir",
        "3. Quando usar Teams e quando usar e-mail",
        "4. Organização: um Team por área operacional (AO)",
        "5. Canais sugeridos e nomenclatura",
        "6. Guia prático (o essencial em 15 minutos)",
        "7. A mesma mensagem no e-mail e no canal do Teams",
        "8. Porque o Teams é mais útil do que o e-mail no dia a dia",
        "9. Como incentivar quem só usa e-mail",
        "10. Boas práticas e etiqueta",
        "11. Notificações, telemóvel e disponibilidade",
        "12. Plano de adoção (90 dias)",
        "13. Perguntas frequentes",
        "14. Glossário rápido",
    ]
    for item in toc:
        story.append(Paragraph(item, S["TOC"]))
    story.append(PageBreak())

    story.append(Paragraph("1. Para que serve este manual", S["H1"]))
    story.append(
        Paragraph(
            "Este documento explica como a AIP passa a usar o <b>Microsoft Teams</b> "
            "como ferramenta principal de comunicação interna do dia a dia, "
            "reservando o <b>e-mail</b> para assuntos mais formais, externos ou com valor de arquivo.",
            S["Body"],
        )
    )
    story.append(
        Paragraph(
            "Não se trata de «proibir o e-mail». Trata-se de escolher o canal certo "
            "para cada tipo de conversa, para as respostas deixarem de demorar dias "
            "e a informação deixar de se perder em cadeias de mensagens.",
            S["Body"],
        )
    )
    story.append(Paragraph("Objetivos", S["H2"]))
    story.append(
        bullets(
            [
                "Acelerar a comunicação <b>dentro de cada área operacional (AO)</b>.",
                "Dar ao diretor de cada AO um espaço próprio para organizar canais de trabalho.",
                "Manter o e-mail para o que é sério: clientes, contratos, decisões formais e arquivo.",
                "Ajudar quem está habituado só ao Outlook a dar os primeiros passos sem pressão.",
            ]
        )
    )
    story.append(
        callout(
            "<b>Como ler este guia.</b> As secções 2 a 5 explicam a lógica da mudança. "
            "A secção 6 é o «como fazer» no ecrã. As secções 8 e 11 servem sobretudo "
            "a diretores e a quem vai liderar a adoção."
        )
    )

    story.append(Paragraph("2. Onde estamos hoje e para onde queremos ir", S["H1"]))
    story.append(Paragraph("Situação atual", S["H2"]))
    story.append(
        Paragraph(
            "O Teams <b>já existe</b> na empresa, mas está organizado como um único "
            "espaço para toda a gente: <b>um Team com dois canais</b>, com todos os "
            "colaboradores. Na prática, isso parece um quadro de avisos geral — "
            "útil para anúncios pontuais, pouco útil para o trabalho diário de cada AO. "
            "Resultado: a conversa continua no e-mail, que é lento, fragmentado e difícil de seguir.",
            S["Body"],
        )
    )
    story.append(Paragraph("O que queremos", S["H2"]))
    story.append(
        Paragraph(
            "Passar de «um Team da empresa» para <b>um Team por AO</b>. "
            "O diretor da AO cria os canais de que a equipa precisa (projetos, "
            "turnos, qualidade, dúvidas, etc.). O Team geral da empresa pode "
            "manter-se só para comunicados que realmente interessam a todos.",
            S["Body"],
        )
    )
    story.append(
        table(
            ["Hoje", "Amanhã"],
            [
                [
                    "1 Team para toda a empresa",
                    "1 Team por AO, gerido pelo diretor",
                ],
                [
                    "2 canais genéricos",
                    "Canais por tema, projeto ou processo",
                ],
                [
                    "Quase toda a conversa no e-mail",
                    "Dia a dia no Teams; e-mail para o formal",
                ],
                [
                    "Contexto perdido em cadeias e anexos",
                    "Histórico visível no canal certo",
                ],
                [
                    "Novos colegas começam «às escuras»",
                    "Onboarding: leem o canal e percebem o contexto",
                ],
            ],
            [8.2 * cm, 8.3 * cm],
        )
    )
    story.append(
        Paragraph(
            "Quadro 1 — Mudança de modelo de comunicação interna.",
            S["Caption"],
        )
    )

    story.append(Paragraph("3. Quando usar Teams e quando usar e-mail", S["H1"]))
    story.append(
        Paragraph(
            "A regra de ouro: <b>se a conversa é interna, operacional e precisa de "
            "resposta rápida, vai para o Teams</b>. Se precisa de formalidade, "
            "prova documental ou destinatários externos, fica no e-mail.",
            S["Body"],
        )
    )
    story.append(
        table(
            ["Situação", "Canal", "Porquê"],
            [
                [
                    "Dúvida rápida à equipa da AO",
                    "Teams — canal ou conversa",
                    "Resposta no contexto; todos os relevantes veem",
                ],
                [
                    "Acompanhar um projeto interno",
                    "Teams — canal do projeto",
                    "Histórico num só sítio; ficheiros partilhados",
                ],
                [
                    "Pedir um esclarecimento ao colega do lado",
                    "Teams — conversa (chat)",
                    "Substitui o «ping» por e-mail",
                ],
                [
                    "Reunião interna, alinhamento, ponto de situação",
                    "Teams — reunião",
                    "Convite, vídeo, gravação e notas no mesmo sítio",
                ],
                [
                    "Editar um Excel / Word em conjunto",
                    "Teams + ficheiro no SharePoint da equipa",
                    "Uma versão; acaba o «versão_final_v3»",
                ],
                [
                    "Comunicado a toda a empresa ou aviso crítico da AO",
                    "E-mail + canal (mesmo envio) ou Teams e e-mail à parte",
                    "Quem vive no Outlook e quem já está no canal vêem a mesma informação (secção 7)",
                ],
                [
                    "Cliente, fornecedor, entidade externa",
                    "E-mail",
                    "Canal profissional esperado no exterior",
                ],
                [
                    "Contrato, fatura, decisão formal, auditoria",
                    "E-mail (e repositório oficial, se existir)",
                    "Rasto formal e valor de arquivo",
                ],
                [
                    "Pedido disciplinar, RH sensível, dados pessoais delicados",
                    "E-mail / processo RH definido",
                    "Confidencialidade e formalismo",
                ],
                [
                    "Confirmar por escrito uma decisão já tomada no Teams",
                    "E-mail curto de síntese",
                    "O Teams discute; o e-mail fecha o assunto quando for preciso",
                ],
            ],
            [5.4 * cm, 4.6 * cm, 6.5 * cm],
        )
    )
    story.append(Paragraph("Quadro 2 — Matriz «quando usar o quê».", S["Caption"]))
    story.append(
        callout(
            "<b>Regra prática de 24 horas.</b> Se a pergunta for interna e espera "
            "resposta no próprio dia ou no dia seguinte, não comece um e-mail. "
            "Abra o canal da AO ou uma conversa no Teams. Se ao fim da discussão "
            "for preciso um comprovativo formal, envie um e-mail de 5 linhas a resumir o acordo."
        )
    )

    story.append(Paragraph("4. Organização: um Team por área operacional (AO)", S["H1"]))
    story.append(
        Paragraph(
            "Cada AO passa a ter o seu próprio Team no Microsoft Teams. "
            "É o espaço de trabalho daquela área — não um grupo de e-mail disfarçado.",
            S["Body"],
        )
    )
    story.append(Paragraph("Papéis", S["H2"]))
    story.append(
        bullets(
            [
                "<b>Diretor da AO:</b> é o «dono» do Team. Cria e arquiva canais, "
                "define quem entra, dá o exemplo (responde no Teams) e escolhe um embaixador.",
                "<b>Embaixador da AO (opcional, mas recomendado):</b> colega que ajuda "
                "os outros nos primeiros 30 dias e recolhe dúvidas.",
                "<b>Colaboradores da AO:</b> usam os canais para o trabalho do dia a dia; "
                "configuram notificações; não criam canais à revelia.",
                "<b>IT / administração M365:</b> cria os Teams iniciais (se necessário), "
                "garante licenças, e apoia permissões. Depois, o dia a dia é da AO.",
            ]
        )
    )
    story.append(Paragraph("O Team geral da empresa", S["H2"]))
    story.append(
        Paragraph(
            "O Team atual (toda a empresa, dois canais) <b>não precisa de desaparecer</b>. "
            "Passa a ter um papel estreito: avisos institucionais, campanhas internas, "
            "informações que realmente dizem respeito a todos. "
            "Deixa de ser o sítio para perguntar «quem pode ver isto no armazém?» "
            "ou discutir o planeamento de uma só AO.",
            S["Body"],
        )
    )
    story.append(
        Paragraph(
            "Se os dois canais atuais tiverem nomes genéricos, sugestão: "
            "um canal <b>Avisos</b> (só a direção / comunicação publica) e um canal "
            "<b>Geral</b> (conversa pontual de empresa). Tudo o resto migra para o Team da AO.",
            S["Body"],
        )
    )

    story.append(Paragraph("5. Canais sugeridos e nomenclatura", S["H1"]))
    story.append(
        Paragraph(
            "Nomes curtos, em minúsculas, com hífen, iguais em todas as AOs sempre que fizer sentido. "
            "Assim, um colaborador que mude de área reconhece a estrutura.",
            S["Body"],
        )
    )
    story.append(
        table(
            ["Canal", "Para que serve", "Quem escreve"],
            [
                [
                    "Geral",
                    "Canal predefinido da AO. Coordenação do dia a dia.",
                    "Toda a AO",
                ],
                [
                    "Avisos",
                    "Comunicados do diretor. Pouca conversa, muita clareza.",
                    "Diretor (e quem ele indicar)",
                ],
                [
                    "Dúvidas",
                    "Perguntas rápidas. Evita e-mails de «uma coisa rápida».",
                    "Toda a AO",
                ],
                [
                    "Projeto-[nome]",
                    "Um canal por iniciativa com início e fim.",
                    "Equipa do projeto",
                ],
                [
                    "Turnos / Operação",
                    "Passagem de testemunho, ocorrências, prioridades do dia.",
                    "Operação",
                ],
                [
                    "Qualidade / Segurança",
                    "Não conformidades ligeiras, lembretes, boas práticas.",
                    "Quem opera + qualidade",
                ],
            ],
            [4.2 * cm, 7.3 * cm, 5.0 * cm],
        )
    )
    story.append(Paragraph("Quadro 3 — Canais de partida (o diretor adapta à AO).", S["Caption"]))
    story.append(Paragraph("Regras de criação de canais", S["H2"]))
    story.append(
        bullets(
            [
                "Criar um canal só se o tema for <b>recorrente</b> ou um projeto com vida própria.",
                "Não criar um canal para um assunto de dois dias — usar uma conversa (thread) no canal Geral.",
                "Arquivar (não apagar de imediato) canais de projetos já fechados.",
                "Canais privados só quando houver confidencialidade real (não por hábito).",
            ]
        )
    )

    story.append(Paragraph("6. Guia prático (o essencial em 15 minutos)", S["H1"]))
    story.append(
        Paragraph(
            "O Teams já está disponível. Não é preciso «instalar uma ferramenta nova» "
            "para a maior parte das pessoas — é preciso <b>passar a abrir o sítio certo</b>.",
            S["Body"],
        )
    )
    story.append(Paragraph("6.1 Entrar e encontrar o Team da AO", S["H2"]))
    story.append(
        bullets(
            [
                "Abra o <b>Microsoft Teams</b> no computador (ou a aplicação no telemóvel).",
                "Inicie sessão com a <b>conta profissional</b> da AIP (a mesma do Outlook).",
                "No menu esquerdo, escolha <b>Equipas</b> (Teams).",
                "Procure o Team com o nome da sua AO. Se não aparecer, peça ao diretor ou ao IT para o adicionarem — não volte ao e-mail «porque não vejo o grupo».",
                "Abra o canal <b>Geral</b> e leia as últimas mensagens. Este é o novo «quadro» da área.",
            ]
        )
    )
    story.append(Paragraph("6.2 Escrever no canal (em vez de um e-mail à equipa)", S["H2"]))
    story.append(
        bullets(
            [
                "Clique na caixa de mensagem no fundo do canal.",
                "Escreva de forma direta: contexto + pedido + prazo, se existir.",
                "Use <b>@nome</b> para chamar uma pessoa. Use <b>@canal</b> só quando toda a gente precisa mesmo de ver (é barulhento — use com parcimónia).",
                "Para continuar o mesmo assunto, use <b>Responder</b> à mensagem original (thread). Não comece um recado novo sobre o mesmo tema.",
                "Anexe ou carregue o ficheiro no canal em vez de o mandar por e-mail. Fica uma versão, no sítio certo.",
            ]
        )
    )
    story.append(Paragraph("6.3 Conversa (chat) com uma pessoa ou um grupo pequeno", S["H2"]))
    story.append(
        Paragraph(
            "Use o chat para o que antes era um e-mail a uma ou duas pessoas: "
            "«tens 2 minutos?», «confirmas este número?», «podes ver o anexo no canal X?». "
            "Se a conversa passar a interessar à AO, <b>leve o assunto para o canal</b> "
            "com um resumo de três linhas — o chat privado não substitui o histórico da equipa.",
            S["Body"],
        )
    )
    story.append(Paragraph("6.4 Reuniões", S["H2"]))
    story.append(
        bullets(
            [
                "No canal ou no calendário do Teams, escolha <b>Reunir</b> / agendar.",
                "Pode continuar a criar o convite a partir do Outlook — a reunião abre no Teams.",
                "Partilhe o ecrã para mostrar um ficheiro em vez de o enviar «para verem antes».",
                "Se a reunião decidir alguma coisa importante, publique a decisão no canal (não só na cabeça de quem esteve presente).",
            ]
        )
    )
    story.append(Paragraph("6.5 Ficheiros", S["H2"]))
    story.append(
        Paragraph(
            "Cada Team tem uma biblioteca de ficheiros (SharePoint). "
            "Abrir no Teams → canal → separador <b>Ficheiros</b>. "
            "Trabalhar no documento online evita o ciclo "
            "«anexo → comentários → anexo novo → ninguém sabe qual é o certo».",
            S["Body"],
        )
    )
    story.append(Paragraph("6.6 Pesquisar", S["H2"]))
    story.append(
        Paragraph(
            "A barra de pesquisa no topo do Teams encontra mensagens, ficheiros e pessoas. "
            "Antes de perguntar «alguém tem o procedimento de…?», pesquise 10 segundos. "
            "Se mesmo assim não encontrar, pergunte no canal <b>Dúvidas</b> — a resposta fica para o próximo colega.",
            S["Body"],
        )
    )
    story.append(Paragraph("6.7 O que o diretor faz uma vez (e depois mantém)", S["H2"]))
    story.append(
        bullets(
            [
                "Confirmar com o IT que o Team da AO existe e que as pessoas certas estão lá (e só elas).",
                "Criar os canais iniciais (Geral, Avisos, Dúvidas + os da operação).",
                "Publicar no Geral uma mensagem de arranque: «A partir de [data], o dia a dia desta AO é aqui. E-mail fica para X, Y e Z.»",
                "Fixar (pin) essa mensagem ou o ficheiro deste manual no canal Avisos.",
                "Obter o <b>endereço de e-mail do canal Avisos</b> (secção 7) e guardá-lo nos contactos do Outlook, por exemplo «AO [nome] — Avisos Teams».",
                "Nomear o embaixador e indicar a quem se pede ajuda nos primeiros dias.",
            ]
        )
    )

    story.append(Paragraph("7. A mesma mensagem no e-mail e no canal do Teams", S["H1"]))
    story.append(
        Paragraph(
            "Durante a transição — e sempre que um aviso for importante o suficiente para "
            "não depender de a pessoa ter o Teams aberto — dá para <b>escrever uma vez e "
            "chegar aos dois sítios</b>: a caixa de entrada e o canal. "
            "Isto é especialmente útil para quem ainda só olha para o Outlook.",
            S["Body"],
        )
    )
    story.append(
        callout(
            "<b>Não use isto para tudo.</b> Se todas as dúvidas do dia forem em duplicado, "
            "a caixa de entrada continua cheia e o hábito não muda. Reserve o envio duplo "
            "para avisos, prazos, alterações de turno, segurança e comunicados da direção. "
            "A conversa do dia a dia fica só no canal."
        )
    )
    story.append(Paragraph("7.1 Método A — Um e-mail no Outlook que também aparece no canal", S["H2"]))
    story.append(
        Paragraph(
            "Cada canal do Teams tem um <b>endereço de e-mail próprio</b>. "
            "Se o colocar em <b>Para</b> ou em <b>Cc</b> ao enviar a mensagem no Outlook, "
            "os destinatários recebem o e-mail normalmente e a mesma mensagem é publicada no canal.",
            S["Body"],
        )
    )
    story.append(
        bullets(
            [
                "No Teams, abra o canal (por exemplo <b>Avisos</b>). Clique nos <b>três pontos</b> (…) junto ao nome do canal.",
                "Escolha <b>Obter endereço de e-mail</b> (em inglês: <i>Get email address</i>).",
                "Copie o endereço e, se quiser, <b>guarde-o como contacto</b> no Outlook com um nome claro.",
                "No Outlook, redija o e-mail como de costume. Em <b>Cc</b> (recomendado) acrescente esse endereço do canal, além das pessoas ou listas que devem receber o correio.",
                "Envie. No canal, a mensagem aparece como publicação (assunto + corpo; anexos, dentro dos limites da Microsoft).",
            ]
        )
    )
    story.append(
        Paragraph(
            "O diretor (ou o IT) pode restringir quem tem permissão para enviar e-mail "
            "para aquele canal — por exemplo, só membros da AO. Peça essa restrição nos "
            "canais de avisos, para um endereço perdido não se tornar uma porta de entrada de spam.",
            S["Body"],
        )
    )
    story.append(Paragraph("7.2 Método B — Partilhar no Teams um e-mail já existente", S["H2"]))
    story.append(
        Paragraph(
            "Se a mensagem <b>já está</b> no Outlook (recebida ou enviada) e quer que a AO "
            "a veja no canal, não precisa de a reescrever:",
            S["Body"],
        )
    )
    story.append(
        bullets(
            [
                "Abra o e-mail no Outlook (aplicação de ambiente de trabalho ou na web).",
                "Na faixa de opções, escolha <b>Partilhar no Teams</b> (ou <i>Share to Teams</i>). Se o botão não aparecer, o IT pode ter de o ativar na organização.",
                "Escolha o Team e o <b>canal</b> da AO (não o chat, se o objetivo for histórico da equipa).",
                "Acrescente uma linha de contexto («Para conhecimento da AO — prazo sexta») e partilhe.",
            ]
        )
    )
    story.append(Paragraph("7.3 Método C — Publicar no canal e avisar por e-mail quem ainda não olha para o Teams", S["H2"]))
    story.append(
        Paragraph(
            "O caminho inverso: escreve-se primeiro no canal (histórico no sítio certo) e, "
            "para as pessoas que ainda não abrem o Teams, reencaminha-se ou envia-se um e-mail "
            "curto com o link da conversa. No Teams, em qualquer mensagem: "
            "<b>Mais opções (…) → Copiar ligação</b>. Cole essa ligação no e-mail. "
            "Quem clicar abre o ponto exacto do canal (precisa de ter acesso ao Team).",
            S["Body"],
        )
    )
    story.append(Paragraph("7.4 O que isto não faz (importante)", S["H2"]))
    story.append(
        bullets(
            [
                "<b>Não é uma conversa sincronizada nos dois sentidos.</b> Quem responder no Outlook continua no fio de e-mail; quem responder no canal continua no Teams. Para o mesmo assunto, combine um sítio para as respostas (de preferência o canal).",
                "Há <b>limites de tamanho e de anexos</b> no e-mail para canal (definidos pela Microsoft e, por vezes, pela organização). Ficheiros grandes devem ir para a biblioteca do Team, não como anexo de 40 MB.",
                "Não envie para o endereço do canal <b>dados pessoais sensíveis, temas de RH ou informação de clientes</b> que não deveriam ficar visíveis a todos os membros daquele canal.",
                "Não reencaminhe o endereço do canal para fora da empresa nem o publique na internet.",
            ]
        )
    )
    story.append(
        table(
            ["Situação", "Método", "Notas"],
            [
                [
                    "Aviso da AO que toda a gente tem de ver, incluindo quem só abre o Outlook",
                    "A — e-mail com o canal em Cc",
                    "Um clique em Enviar; dois destinos",
                ],
                [
                    "E-mail de um cliente / fornecedor que a AO precisa de acompanhar",
                    "B — Partilhar no Teams",
                    "Não meta o cliente no canal; partilhe só o necessário",
                ],
                [
                    "Já publicou no canal e quer puxar um colega que ainda não olhou",
                    "C — e-mail curto com a ligação",
                    "Evita reescrever o texto",
                ],
                [
                    "Dúvida rápida do dia",
                    "Só Teams",
                    "Sem duplicar no correio",
                ],
            ],
            [5.2 * cm, 5.5 * cm, 5.8 * cm],
        )
    )
    story.append(Paragraph("Quadro 4 — Quando duplicar a mensagem e quando não duplicar.", S["Caption"]))

    story.append(Paragraph("8. Porque o Teams é mais útil do que o e-mail no dia a dia", S["H1"]))
    story.append(
        Paragraph(
            "O e-mail foi feito para correspondência: um remetente, destinatários, "
            "assunto, arquivo. O trabalho de uma AO parece-se mais com uma sala de operações: "
            "muitas conversas em paralelo, ficheiros vivos, decisões rápidas. "
            "O Teams encaixa nesse ritmo. Em concreto:",
            S["Body"],
        )
    )
    story.append(
        bullets(
            [
                "<b>Velocidade:</b> a pergunta aparece onde a equipa já está; não espera na caixa de entrada entre newsletters e fornecedores.",
                "<b>Contexto:</b> no canal do projeto, a conversa não se mistura com férias, faturas e CC desnecessários.",
                "<b>Menos «Responder a todos»:</b> quem precisa de ver está no canal; os outros não são copiados por hábito.",
                "<b>Uma versão do ficheiro:</b> edição em simultâneo; acaba a guerra de anexos.",
                "<b>Reuniões no mesmo sítio</b> onde depois fica o trabalho — não um convite órfão no Outlook.",
                "<b>Presença:</b> vê se a pessoa está disponível antes de ligar ou de insistir.",
                "<b>@menções:</b> chama quem tem de agir, sem mandar a mensagem a 20 pessoas «por se acaso».",
                "<b>Pesquisa:</b> mensagens e ficheiros da AO num só motor — não em pastas pessoais de Outlook diferentes.",
                "<b>Memória da equipa:</b> um colega novo lê o canal e percebe o que aconteceu na semana passada.",
                "<b>Telemóvel:</b> o mesmo espaço no bolso, com notificações que se podem afinar (ver secção 11).",
                "<b>Ligações úteis:</b> Planner, listas, aprovações e automatizações podem viver ao lado da conversa, quando a AO estiver pronta — não no dia um.",
            ]
        )
    )
    story.append(
        Paragraph(
            "O e-mail continua imbatível para o exterior e para o formal. "
            "A mudança não é «Teams é moderno, e-mail é antigo». "
            "É «cada ferramenta no ofício para que foi desenhada».",
            S["Body"],
        )
    )

    story.append(Paragraph("9. Como incentivar quem só usa e-mail", S["H1"]))
    story.append(
        Paragraph(
            "Habituar-se ao Outlook não é teimosia — é competência acumulada. "
            "A adoção falha quando se pede às pessoas que mudem de ferramenta "
            "sem mudar as regras do jogo. Se o diretor continuar a responder só por e-mail, "
            "o Teams morre em duas semanas.",
            S["Body"],
        )
    )
    story.append(Paragraph("O que funciona", S["H2"]))
    story.append(
        bullets(
            [
                "<b>Liderança no canal certo.</b> Se a pergunta chega no Teams, a resposta sai no Teams. "
                "Se alguém mandar por e-mail um assunto operacional, a resposta pode ser: "
                "«Vou responder no canal Dúvidas para ficar o histórico» — e responde-se lá. "
                "Nos primeiros 30 dias, avisos importantes podem ir <b>ao mesmo tempo</b> para o e-mail e para o canal (secção 7), para ninguém ficar de fora.",
                "<b>Uma página de regras, não um regulamento.</b> O quadro 2 deste manual, impresso ou fixado no canal Avisos.",
                "<b>Vitórias rápidas (primeiros 15 dias):</b> passar os «FYI» internos para Avisos; "
                "as dúvidas do dia para Dúvidas; uma reunião semanal da AO no Teams.",
                "<b>Formação curta:</b> 20 minutos por AO, no ecrã real, a fazer as ações da secção 6 e o envio duplo da secção 7. Gravar e pôr no canal.",
                "<b>Embaixador:</b> alguém paciente, não necessariamente o mais técnico.",
                "<b>Reduzir o ruído:</b> ensinar a silenciar canais irrelevantes e a ligar só o essencial. "
                "Quem é bombardeado de notificações volta ao e-mail.",
                "<b>Não ridicularizar o e-mail.</b> Respeitar quem precisa de tempo. Celebrar a primeira mensagem útil no canal, não a quantidade.",
                "<b>Piloto (recomendado):</b> uma AO durante 3–4 semanas, ajustar canais, depois replicar. "
                "O Team único atual continua para avisos de empresa.",
            ]
        )
    )
    story.append(Paragraph("Frases úteis (para diretores e embaixadores)", S["H2"]))
    story.append(
        bullets(
            [
                "«Isto é operacional da AO — mete no canal para o resto da equipa também ver.»",
                "«Se for para o cliente, mantém o e-mail. Se for para nós, Teams.»",
                "«Não precisas de ser rápido como no WhatsApp. Precisamos só de deixar o e-mail interno para o que é formal.»",
                "«Se não viste a notificação, o histórico está no canal. Não se perdeu na caixa de entrada.»",
            ]
        )
    )
    story.append(
        callout(
            "<b>O que evitar.</b> Obrigações vagas («usem mais o Teams»), grupos de WhatsApp a substituir o Teams, "
            "e canais onde só o diretor fala. O Teams só vale a pena se a conversa for a dois sentidos."
        )
    )

    story.append(Paragraph("10. Boas práticas e etiqueta", S["H1"]))
    story.append(
        bullets(
            [
                "Assunto claro na primeira linha. Trate o canal como um quadro, não como um café infinito.",
                "Uma ideia por mensagem quando pedir uma ação; evite romances.",
                "Responda na thread certa.",
                "Não use @canal para «bom dia» ou para partilhar um artigo.",
                "Se a conversa ficar sensível (pessoas, conflitos, dados), saia do canal aberto e use o canal formal / RH / e-mail.",
                "Fora do horário, não espere resposta imediata — o Teams não é um contrato de disponibilidade 24 horas (ver secção 11).",
                "Antes de criar um ficheiro novo, veja se já existe na pasta do canal.",
                "Quando um assunto ficar decidido, escreva a decisão em uma frase no canal. O futuro agradece.",
            ]
        )
    )

    story.append(Paragraph("11. Notificações, telemóvel e disponibilidade", S["H1"]))
    story.append(
        Paragraph(
            "O medo mais comum de quem vem do e-mail: «vou ficar a ser interrompido o dia todo». "
            "Isso só acontece se as notificações ficarem no padrão. Ajuste-as.",
            S["Body"],
        )
    )
    story.append(
        bullets(
            [
                "Definições → Notificações: mantenha alertas para <b>menções</b> e para o canal Avisos da sua AO.",
                "Silencie o Team geral da empresa se só precisar dos avisos pontuais — ou deixe só esse canal a notificar.",
                "No telemóvel, desligue o pré-visualizar de conteúdo em locais públicos; use PIN/biometria.",
                "Estado (Disponível, Ocupado, Não incomodar): use-o com honestidade. Não está «ausente» se está no escritório a trabalhar concentrado — está Ocupado.",
                "A AO pode definir um compromisso simples: «resposta no Teams em horário de expediente, sem obrigação fora de horas, salvo urgência verdadeira anunciada pelo diretor».",
            ]
        )
    )

    story.append(Paragraph("12. Plano de adoção (90 dias)", S["H1"]))
    story.append(
        table(
            ["Quando", "O quê", "Quem"],
            [
                [
                    "Semana 0",
                    "IT confirma licenças; cria os Teams por AO (ou o diretor, se tiver permissão); "
                    "copia este manual para o canal Avisos.",
                    "IT + diretores",
                ],
                [
                    "Semana 1",
                    "Sessão de 20 min por AO. Mensagem de arranque. Mostrar o endereço de e-mail do canal Avisos. "
                    "Piloto numa AO se a empresa for grande.",
                    "Diretor + embaixador",
                ],
                [
                    "Semanas 2–4",
                    "Dia a dia no Teams. E-mails operacionais internos são redirecionados com educação para o canal.",
                    "Toda a AO",
                ],
                [
                    "Dia 30",
                    "Retrospectiva: que canais sobram? que ruído há? o Team geral ainda está a ser usado para o que não deve?",
                    "Diretor",
                ],
                [
                    "Dia 90",
                    "Avaliar: menos e-mail interno de «uma coisa rápida»? reuniões da AO no Teams? "
                    "novos colegas encontram contexto sozinhos?",
                    "Direção + diretores de AO",
                ],
            ],
            [3.2 * cm, 9.3 * cm, 4.0 * cm],
        )
    )
    story.append(Paragraph("Quadro 5 — Calendário sugerido (adaptar à realidade da AIP).", S["Caption"]))
    story.append(
        Paragraph(
            "Indicadores simples (não são vigilância de pessoas): número de canais ativos com conversa útil; "
            "reuniões semanais da AO feitas no Teams; feedback qualitativo aos 30 e 90 dias. "
            "Evite rankings de «quem escreve mais».",
            S["Body"],
        )
    )

    story.append(Paragraph("13. Perguntas frequentes", S["H1"]))
    faqs = [
        (
            "E se eu não vir o Team da minha AO?",
            "Peça ao diretor ou ao IT para o adicionarem. Não recrie o hábito de mandar o mesmo por e-mail «entretanto» — "
            "exceto se for urgente e a pessoa certa não estiver no Teams.",
        ),
        (
            "Posso continuar a usar o e-mail com os colegas?",
            "Sim, para o que é formal, externo ou de arquivo. Para o operacional interno, o padrão passa a ser o Teams.",
        ),
        (
            "O Team antigo (toda a empresa) acaba?",
            "Não necessariamente. Fica para avisos de todos. O trabalho de cada AO sai de lá.",
        ),
        (
            "E o WhatsApp?",
            "Não é ferramenta da empresa para operação. Emergências pessoais à parte, o trabalho fica no Teams, "
            "onde há contas profissionais, ficheiros e histórico.",
        ),
        (
            "Tenho de ter o Teams no telemóvel?",
            "Não é obrigatório para toda a gente. É muito útil para quem se desloca. No escritório, o ambiente de trabalho no PC chega.",
        ),
        (
            "E se eu preferir o e-mail porque «fica prova»?",
            "As conversas e ficheiros do Teams também ficam registados na conta da organização. "
            "Quando a lei ou o processo exigirem um documento formal, usa-se o e-mail ou o sistema oficial — não se usa o e-mail para tudo «por precaução».",
        ),
        (
            "Posso criar eu um canal?",
            "Por defeito, peça ao diretor. Canais a mais matam a ferramenta tanto como canais a menos.",
        ),
        (
            "Como trato um cliente que me escreveu por e-mail?",
            "Responda por e-mail. Se internamente precisar da AO, use <b>Partilhar no Teams</b> para o canal certo "
            "(secção 7.2), sem reencaminhar cadeias enormes com dados a mais e sem meter o cliente no Team.",
        ),
        (
            "Como envio o mesmo aviso por e-mail e para o canal?",
            "No Outlook, coloque em Cc o endereço de e-mail do canal (secção 7.1). "
            "Se o e-mail já foi enviado, use Partilhar no Teams. Não duplique as conversas do dia a dia — só avisos que ninguém pode perder.",
        ),
        (
            "Se eu responder no Outlook a um e-mail que também foi para o canal, aparece no Teams?",
            "Em regra, não de forma fiável. As respostas no correio ficam no fio de e-mail; as do canal ficam no Teams. "
            "Combine à partida onde continua a conversa (de preferência no canal).",
        ),
    ]
    for q, a in faqs:
        story.append(Paragraph(q, S["H2"]))
        story.append(Paragraph(a, S["Body"]))

    story.append(Paragraph("14. Glossário rápido", S["H1"]))
    story.append(
        table(
            ["Termo", "Significado nesta empresa"],
            [
                ["Team (equipa)", "Espaço de trabalho. Na AIP, em regra: um por AO."],
                ["Canal", "Sala temática dentro do Team (Geral, Avisos, um projeto…)."],
                ["Conversa / chat", "Mensagem direta a uma pessoa ou grupo pequeno."],
                ["@menção", "Notificação a uma pessoa ou ao canal."],
                ["Thread / resposta", "Fio de mensagens sobre o mesmo assunto."],
                ["SharePoint", "Sítio onde os ficheiros do Team realmente vivem."],
                ["AO", "Área operacional — a unidade de organização deste modelo."],
                ["Embaixador", "Colega que apoia a adoção na AO."],
                [
                    "Endereço de e-mail do canal",
                    "Morada à qual se envia um e-mail para ele aparecer automaticamente nesse canal.",
                ],
                [
                    "Partilhar no Teams",
                    "Botão do Outlook que envia um e-mail já existente para um canal ou conversa.",
                ],
            ],
            [4.5 * cm, 12.0 * cm],
        )
    )
    story.append(Paragraph("Quadro 6 — Vocabulário mínimo.", S["Caption"]))
    story.append(Spacer(1, 8 * mm))
    story.append(
        callout(
            "<b>Próximo passo.</b> Diretor da AO: marcar a sessão de 20 minutos, publicar a mensagem de arranque "
            "e colar neste canal a regra «operacional → Teams; formal/externo → e-mail». "
            "O resto é hábito — e hábitos mudam-se com consistência, não com um anúncio único."
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "Documento interno. Conteúdo em português de Portugal. Ferramentas: Microsoft Teams e Outlook / Microsoft 365.",
            S["SmallCenter"],
        )
    )

    def first_page(canvas, doc_):
        cover_page(canvas, doc_)

    def later(canvas, doc_):
        header_footer(canvas, doc_)

    doc.build(story, onFirstPage=first_page, onLaterPages=later)
    return path


def build_docx():
    from manual_docx import build_docx as _build_docx

    return _build_docx()


def _set_run_font(run, name="Calibri", size=18, bold=False, color=PPT_TEXT):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    r = run._r
    rPr = r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    # latin already set via font.name


def add_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def rect(slide, l, t, w, h, color):
    sh = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    sh.fill.solid()
    sh.fill.fore_color.rgb = color
    sh.line.fill.background()
    return sh


def tb(slide, l, t, w, h, text, size=18, bold=False, color=PPT_TEXT, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    _set_run_font(run, size=size, bold=bold, color=color)
    return box


def bullets_box(slide, l, t, w, h, items, size=16):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.level = 0
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = "•  " + item
        _set_run_font(run, size=size, bold=False, color=PPT_TEXT)
    return box


def footer_bar(slide, page, total=12):
    rect(slide, Inches(0), Inches(7.15), Inches(13.333), Inches(0.35), PPT_NAVY)
    tb(
        slide,
        Inches(0.4),
        Inches(7.16),
        Inches(8),
        Inches(0.3),
        "AIP  ·  Comunicação interna  ·  Microsoft Teams",
        size=10,
        color=PPT_WHITE,
    )
    tb(
        slide,
        Inches(11.4),
        Inches(7.16),
        Inches(1.5),
        Inches(0.3),
        f"{page}  /  {total}",
        size=10,
        color=PPT_WHITE,
        align=PP_ALIGN.RIGHT,
    )


def title_block(slide, kicker, title, subtitle=None):
    rect(slide, Inches(0), Inches(0), Inches(0.18), Inches(7.5), PPT_TEAMS)
    tb(slide, Inches(0.5), Inches(0.28), Inches(12), Inches(0.3), kicker, size=12, bold=True, color=PPT_TEAMS)
    tb(slide, Inches(0.5), Inches(0.55), Inches(12.2), Inches(0.7), title, size=28, bold=True, color=PPT_NAVY)
    if subtitle:
        tb(slide, Inches(0.5), Inches(1.2), Inches(12.2), Inches(0.4), subtitle, size=14, color=PPT_MUTED)


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]
    total = 13

    # 1 cover
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_NAVY)
    rect(s, Inches(0), Inches(0), Inches(0.35), Inches(7.5), PPT_TEAMS)
    tb(s, Inches(0.7), Inches(1.5), Inches(11), Inches(0.4), "COMUNICAÇÃO INTERNA  ·  AIP", size=14, bold=True, color=PPT_TEAMS)
    tb(
        s,
        Inches(0.7),
        Inches(2.1),
        Inches(12),
        Inches(2.2),
        "Microsoft Teams e correio eletrónico:\nmodelo de comunicação interna\npor área operacional",
        size=32,
        bold=True,
        color=PPT_WHITE,
    )
    tb(
        s,
        Inches(0.7),
        Inches(5.0),
        Inches(11),
        Inches(0.8),
        "Apresentação institucional  ·  Português (Portugal)  ·  2026",
        size=16,
        color=RGBColor(0xC9, 0xCC, 0xE8),
    )

    # 2 problema
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "DIAGNÓSTICO", "Limitações do modelo atual")
    bullets_box(
        s,
        Inches(0.5),
        Inches(1.8),
        Inches(12.2),
        Inches(4.8),
        [
            "A comunicação interna operacional depende quase exclusivamente do e-mail.",
            "As cadeias de mensagens fragmentam-se; os anexos multiplicam-se; o contexto perde-se.",
            "O Microsoft Teams já se encontra disponível, mas organizado num único Team, com dois canais, para toda a organização.",
            "Essa estrutura é adequada a comunicados gerais, mas insuficiente para o trabalho quotidiano de cada área operacional (AO).",
        ],
        size=17,
    )
    footer_bar(s, 2, total)

    # 3 proposta
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "MODELO PROPOSTO", "Um Team por área operacional")
    cards = [
        ("1", "Team institucional", "Mantém-se para comunicados de interesse transversal. Deixa de ser o espaço do trabalho diário de cada AO."),
        ("2", "Team por AO", "Cada área dispõe do seu espaço de trabalho. O diretor define e gere os canais necessários."),
        ("3", "E-mail formal", "Clientes, contratos, decisões oficiais e arquivo documental continuam no correio eletrónico."),
    ]
    x = 0.5
    for n, title, body in cards:
        rect(s, Inches(x), Inches(1.85), Inches(3.9), Inches(4.6), PPT_LIGHT)
        tb(s, Inches(x + 0.25), Inches(2.05), Inches(3.4), Inches(0.5), n, size=28, bold=True, color=PPT_TEAMS)
        tb(s, Inches(x + 0.25), Inches(2.7), Inches(3.4), Inches(0.8), title, size=18, bold=True, color=PPT_NAVY)
        tb(s, Inches(x + 0.25), Inches(3.5), Inches(3.4), Inches(2.6), body, size=14, color=PPT_TEXT)
        x += 4.15
    footer_bar(s, 3, total)

    # 4 matriz
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "CRITÉRIO DE UTILIZAÇÃO", "Seleção do canal adequado")
    rect(s, Inches(0.5), Inches(1.85), Inches(6.0), Inches(4.7), PPT_LIGHT)
    tb(s, Inches(0.7), Inches(2.0), Inches(5.6), Inches(0.45), "MICROSOFT TEAMS", size=16, bold=True, color=PPT_TEAMS)
    bullets_box(
        s,
        Inches(0.7),
        Inches(2.5),
        Inches(5.6),
        Inches(3.8),
        [
            "Esclarecimentos e alinhamentos internos",
            "Gestão de projetos e operação corrente",
            "Colaboração em documentos",
            "Reuniões internas",
            "Assuntos que requerem resposta célere",
        ],
        size=15,
    )
    rect(s, Inches(6.8), Inches(1.85), Inches(6.0), Inches(4.7), PPT_LIGHT)
    tb(s, Inches(7.0), Inches(2.0), Inches(5.6), Inches(0.45), "CORREIO ELETRÓNICO", size=16, bold=True, color=PPT_RED)
    bullets_box(
        s,
        Inches(7.0),
        Inches(2.5),
        Inches(5.6),
        Inches(3.8),
        [
            "Clientes, fornecedores e entidades externas",
            "Contratos, faturação e auditoria",
            "Decisões formais sujeitas a arquivo",
            "Assuntos de RH e matérias sensíveis",
            "Síntese escrita após decisão no Teams",
            "Comunicados críticos: e-mail e canal em simultâneo (Cc)",
        ],
        size=14,
    )
    footer_bar(s, 4, total)

    # 5 canais
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(
        s,
        "ESTRUTURA DE CANAIS",
        "Canais recomendados por AO",
        "Recomenda-se uma estrutura simples. Criar canais apenas para temas recorrentes ou projetos autónomos.",
    )
    rows = [
        ("Geral", "Coordenação operacional quotidiana da AO"),
        ("Avisos", "Comunicados da direção da AO — informação unidirecional"),
        ("Dúvidas", "Pedidos de esclarecimento rápidos (substitui o e-mail operacional)"),
        ("Projeto-[nome]", "Iniciativas com calendário definido"),
        ("Operação / turnos", "Passagem de informação e prioridades do serviço"),
    ]
    y = 1.85
    for name, desc in rows:
        rect(s, Inches(0.5), Inches(y), Inches(12.3), Inches(0.85), PPT_LIGHT)
        tb(s, Inches(0.7), Inches(y + 0.18), Inches(3.5), Inches(0.5), name, size=16, bold=True, color=PPT_NAVY)
        tb(s, Inches(4.4), Inches(y + 0.18), Inches(8.2), Inches(0.5), desc, size=16, color=PPT_TEXT)
        y += 0.95
    footer_bar(s, 5, total)

    # 6 demo 5 passos
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "PROCEDIMENTO BÁSICO", "Cinco ações essenciais no Teams")
    steps = [
        ("1", "Abrir Equipas", "Identificar o Team da respetiva AO (e não o Team institucional)."),
        ("2", "Publicar no canal", "Contexto, pedido e prazo. Responder na conversa correspondente."),
        ("3", "@menção", "Identificar o responsável. Utilizar @canal apenas quando for indispensável."),
        ("4", "Partilhar ficheiros", "Carregar no canal. Manter uma única versão de trabalho."),
        ("5", "Agendar reunião", "Realizar a reunião no Teams e registar a decisão no canal."),
    ]
    x = 0.4
    for n, title, body in steps:
        rect(s, Inches(x), Inches(1.9), Inches(2.4), Inches(4.5), PPT_LIGHT)
        tb(s, Inches(x + 0.15), Inches(2.1), Inches(2.1), Inches(0.5), n, size=24, bold=True, color=PPT_TEAMS)
        tb(s, Inches(x + 0.15), Inches(2.7), Inches(2.1), Inches(1.0), title, size=14, bold=True, color=PPT_NAVY)
        tb(s, Inches(x + 0.15), Inches(3.8), Inches(2.1), Inches(2.3), body, size=12, color=PPT_TEXT)
        x += 2.55
    footer_bar(s, 6, total)

    # 7 mesma mensagem nos dois sítios
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(
        s,
        "INTEGRAÇÃO OUTLOOK–TEAMS",
        "Envio simultâneo para e-mail e canal",
        "Aplicável a comunicados relevantes. Não deve ser utilizado para a comunicação operacional corrente.",
    )
    methods = [
        ("A", "Cc do canal", "No Teams: opções do canal → Obter endereço de e-mail. No Outlook, incluir esse endereço em Cc. O conteúdo é entregue na caixa de entrada e publicado no canal."),
        ("B", "Partilhar no Teams", "Para mensagens já existentes no Outlook: Partilhar no Teams → selecionar o canal da AO. Adequado a correspondência externa que a equipa deve acompanhar."),
        ("C", "Ligação do canal", "Após publicação no Teams: copiar a ligação da mensagem e incluí-la num e-mail breve dirigido a quem ainda consulta sobretudo o Outlook."),
    ]
    x = 0.45
    for n, title, body in methods:
        rect(s, Inches(x), Inches(1.95), Inches(4.05), Inches(4.5), PPT_LIGHT)
        tb(s, Inches(x + 0.2), Inches(2.15), Inches(3.65), Inches(0.45), n, size=24, bold=True, color=PPT_TEAMS)
        tb(s, Inches(x + 0.2), Inches(2.65), Inches(3.65), Inches(0.7), title, size=16, bold=True, color=PPT_NAVY)
        tb(s, Inches(x + 0.2), Inches(3.4), Inches(3.65), Inches(2.8), body, size=13, color=PPT_TEXT)
        x += 4.2
    footer_bar(s, 7, total)

    # 8 vantagens
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "BENEFÍCIOS", "Vantagens do Teams na comunicação operacional")
    items = [
        "Respostas no contexto da AO, sem dispersão na caixa de entrada",
        "Redução de «Responder a todos» e de múltiplas versões de ficheiros",
        "Histórico acessível a novos colaboradores",
        "Reuniões, conversação e documentos na mesma plataforma",
        "Pesquisa centralizada de pessoas, mensagens e ficheiros",
        "E-mail reservado a assuntos formais e comunicação externa",
    ]
    bullets_box(s, Inches(0.5), Inches(1.85), Inches(12), Inches(4.8), items, size=18)
    footer_bar(s, 8, total)

    # 9 habitos
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "ADOÇÃO", "Orientações para colaboradores habituados ao e-mail")
    bullets_box(
        s,
        Inches(0.5),
        Inches(1.85),
        Inches(12.2),
        Inches(4.8),
        [
            "A liderança responde no Teams. O exemplo da direção é determinante.",
            "Critério simples: operacional → canal; formal ou externo → e-mail.",
            "Sessão prática de 20 minutos por AO, com demonstração no ecrã.",
            "Designação de um embaixador por área durante a fase inicial.",
            "Configuração de notificações: menções e avisos, sem excesso de alertas.",
            "Nos primeiros 30 dias, comunicados relevantes: e-mail e canal em simultâneo (Cc).",
            "Transição progressiva, com respeito pelos hábitos estabelecidos.",
        ],
        size=17,
    )
    footer_bar(s, 9, total)

    # 10 frase diretor
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "COMUNICADO DE ARRANQUE", "Texto recomendado para o canal Geral da AO")
    rect(s, Inches(0.5), Inches(1.95), Inches(12.3), Inches(4.5), PPT_LIGHT)
    tb(
        s,
        Inches(0.8),
        Inches(2.2),
        Inches(11.7),
        Inches(4.0),
        "«A partir de [data], a comunicação operacional desta AO passa a decorrer neste Team.\n\n"
        "Esclarecimentos, alinhamentos, ficheiros de trabalho e reuniões internas: Microsoft Teams.\n"
        "Clientes, contratos e documentação sujeita a arquivo formal: correio eletrónico.\n\n"
        "Assuntos operacionais recebidos por e-mail serão remetidos para este canal,\n"
        "a fim de preservar o histórico da equipa.\n\n"
        "Comunicados de caráter crítico: o mesmo texto no e-mail e neste canal\n"
        "(endereço do canal em Cc).»",
        size=14,
        color=PPT_NAVY,
    )
    footer_bar(s, 10, total)

    # 11 90 dias
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "PLANO DE IMPLEMENTAÇÃO", "Calendário de 90 dias")
    phases = [
        ("Semana 0–1", "Criação dos Teams por AO.\nSessão formativa de 20 min.\nComunicado de arranque."),
        ("Dia 15", "Esclarecimentos no canal.\nComunicados relevantes:\ne-mail e canal."),
        ("Dia 30", "Revisão da estrutura de canais.\nAjuste de notificações.\nRecolha de feedback."),
        ("Dia 90", "Reuniões da AO no Teams.\nRedução do e-mail operacional.\nIntegração de novos colaboradores."),
    ]
    x = 0.45
    for title, body in phases:
        rect(s, Inches(x), Inches(1.9), Inches(3.0), Inches(4.5), PPT_LIGHT)
        tb(s, Inches(x + 0.15), Inches(2.15), Inches(2.7), Inches(0.8), title, size=16, bold=True, color=PPT_TEAMS)
        tb(s, Inches(x + 0.15), Inches(3.1), Inches(2.7), Inches(3.0), body, size=14, color=PPT_TEXT)
        x += 3.2
    footer_bar(s, 11, total)

    # 12 o que nao muda
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_WHITE)
    title_block(s, "ÂMBITO E LIMITES", "O que esta mudança não implica")
    bullets_box(
        s,
        Inches(0.5),
        Inches(1.85),
        Inches(12.2),
        Inches(4.8),
        [
            "Não exige disponibilidade fora do horário de expediente.",
            "Não substitui o e-mail na comunicação com clientes e fornecedores.",
            "Não constitui instrumento de monitorização individual de atividade.",
            "Não obriga à duplicação sistemática de mensagens — apenas em comunicados críticos.",
            "Não elimina o Team institucional; restringe-o a avisos transversais.",
            "Não requer conhecimentos avançados: cinco ações essenciais são suficientes para iniciar.",
        ],
        size=17,
    )
    footer_bar(s, 12, total)

    # 13 close
    s = prs.slides.add_slide(blank)
    add_bg(s, PPT_NAVY)
    rect(s, Inches(0), Inches(0), Inches(0.35), Inches(7.5), PPT_TEAMS)
    tb(s, Inches(0.7), Inches(2.0), Inches(12), Inches(1.2), "Próximos passos", size=18, bold=True, color=PPT_TEAMS)
    tb(
        s,
        Inches(0.7),
        Inches(2.6),
        Inches(12),
        Inches(2.4),
        "Aceder ao Team da respetiva AO.\nUtilizar o canal adequado para a comunicação operacional.\nReservar o e-mail para assuntos formais e externos.",
        size=24,
        bold=True,
        color=PPT_WHITE,
    )
    tb(
        s,
        Inches(0.7),
        Inches(5.4),
        Inches(12),
        Inches(0.8),
        "Manual: Manual_Microsoft_Teams_AIP.pdf / .docx  ·  Apoio: diretor da AO ou embaixador",
        size=14,
        color=RGBColor(0xC9, 0xCC, 0xE8),
    )

    path = OUT / "Apresentacao_Microsoft_Teams_AIP.pptx"
    prs.save(str(path))
    return path


def build_guiao():
    path = OUT / "Guiao_Video_Microsoft_Teams_AIP.txt"
    path.write_text(
        """GUIÃO DE VÍDEO — Microsoft Teams na AIP
Duração alvo: 7 a 9 minutos
Língua: português de Portugal
Formato: gravar o ecrã (Teams aberto) + narração. Webcam opcional nos 20 segundos iniciais.

────────────────────────────────────────
ANTES DE GRAVAR
────────────────────────────────────────
- Abrir o Teams já autenticado com conta da empresa.
- Ter visível: Team da empresa (2 canais) E um Team de AO de exemplo
  (mesmo que ainda seja de teste, com canais Geral / Avisos / Dúvidas).
- Ter o Outlook aberto para mostrar «Obter endereço de e-mail» e Cc (rascunho).
- Se possível, ter o botão Partilhar no Teams visível no Outlook.
- Desligar notificações durante a gravação.
- Resolução 1920×1080; não mostrar dados pessoais reais de clientes.
- Tom: calmo, direto, sem jargão. Não ridicularizar quem usa e-mail.

────────────────────────────────────────
0:00–0:25  ABERTURA (pode ser cara + nome)
────────────────────────────────────────
NARRAÇÃO:
«Olá. Este vídeo explica como vamos passar a comunicar melhor dentro da AIP:
o dia a dia no Microsoft Teams, por área operacional, e o e-mail para o que é
formal ou externo. Dura menos de dez minutos e mostra o ecrã real.»

────────────────────────────────────────
0:25–1:10  O PROBLEMA
────────────────────────────────────────
ECRÃ: caixa de entrada do Outlook (pode ser desfocada) ou o Team único atual.
NARRAÇÃO:
«Hoje quase tudo vai por e-mail. É lento, as conversas perdem-se e os ficheiros
andam em anexos com três versões. Já temos Teams — mas está um único Team,
com dois canais, para toda a gente. Isso serve para avisos gerais.
Não serve para o trabalho de cada área operacional.»

────────────────────────────────────────
1:10–2:00  A PROPOSTA
────────────────────────────────────────
ECRÃ: lista de Equipas — apontar o Team da empresa e o Team da AO.
NARRAÇÃO:
«A proposta é simples. Um Team por AO. O diretor cria os canais de que a
equipa precisa. O Team de toda a empresa fica para comunicados que interessam
a todos. O e-mail não desaparece: clientes, contratos, decisões formais e
arquivo continuam no correio eletrónico.»

────────────────────────────────────────
2:00–2:40  REGRA DE OURO
────────────────────────────────────────
ECRÃ: slide 4 da apresentação, ou um papel com duas colunas Teams / E-mail.
NARRAÇÃO:
«Regra de ouro: se a conversa é interna, operacional e precisa de resposta
rápida, vai para o Teams. Se precisa de formalidade, destinatário externo
ou prova de arquivo, fica no e-mail. Se discutimos no Teams e no fim for
preciso um comprovativo, manda-se um e-mail curto a resumir o acordo.»

────────────────────────────────────────
2:40–4:00  DEMO NO ECRÃ (o miolo)
────────────────────────────────────────
Ações a mostrar, sem pressa:

1) Menu Equipas → abrir o Team da AO → canal Geral.
   «Aqui vive o dia a dia da área. Não no Team de toda a empresa.»

2) Escrever uma mensagem de exemplo:
   «Boa tarde. Preciso de confirmar o prazo X até amanhã às 12h. @Nome.»
   Mostrar a menção.
   «Usem o @nome para chamar quem tem de agir. O @canal só quando for mesmo
   para toda a gente — faz muito barulho.»

3) Responder na thread a essa mensagem.
   «Continuem o mesmo assunto aqui. Não comecem um recado novo.»

4) Separador Ficheiros → carregar um documento inofensivo (ex.: este manual).
   «Uma versão, no sítio certo. Acaba o anexo versão_final_v3.»

5) Botão Reunir / agendar (não é preciso entrar numa chamada real).
   «As reuniões da AO também nascem daqui. Depois da reunião, publiquem a
   decisão no canal. Quem faltou fica a saber.»

────────────────────────────────────────
4:00–5:20  A MESMA MENSAGEM NO E-MAIL E NO CANAL
────────────────────────────────────────
ECRÃ: canal Avisos → três pontos (…) → Obter endereço de e-mail.
Depois Outlook: novo e-mail com o endereço em Cc (pode ser um rascunho, sem enviar
se não quiser poluir o canal de produção).

NARRAÇÃO:
«Quem ainda só abre o Outlook não precisa de ficar de fora nos avisos importantes.
Cada canal tem um endereço de e-mail. Copiamos, pomos em Cc no Outlook, e a
mesma mensagem chega à caixa de entrada e ao canal. Um envio, dois sítios.
Se o e-mail já existe — por exemplo de um cliente — usamos Partilhar no Teams
e escolhemos o canal da AO, sem meter o cliente dentro do Team.
Atenção: as respostas no Outlook e as respostas no canal não são a mesma
conversa. Para avisos está bem. Para o vai-e-vem do dia, fiquem só no Teams,
senão voltamos a ter duas discussões em paralelo.»

────────────────────────────────────────
5:20–6:00  QUEM SÓ USA E-MAIL
────────────────────────────────────────
ECRÃ: voltar ao canal Avisos / Geral.
NARRAÇÃO:
«Se está habituado só ao Outlook, não precisa de se tornar especialista.
Cinco gestos chegam: abrir o Team da AO, escrever no canal, mencionar quem
interessa, pôr o ficheiro ali, reunir quando for preciso.
O diretor dá o exemplo: se a pergunta vem no Teams, a resposta sai no Teams.
Se mandarem um assunto operacional por e-mail, vamos responder no canal,
com educação, para ficar o histórico. Ninguém é avaliado por quantas
mensagens escreve.»

────────────────────────────────────────
6:00–6:35  NOTIFICAÇÕES E HORÁRIO
────────────────────────────────────────
ECRÃ: Definições → Notificações (mesmo que seja um zoom rápido).
NARRAÇÃO:
«Afinem as notificações. Deixem alertas para menções e para o canal de avisos.
Silenciem o resto. O Teams não é um contrato de disponibilidade à noite.
Em horário de expediente, sim: olhem o canal da AO como olhariam para a
caixa de entrada — com a vantagem de a conversa já estar no sítio certo.»

────────────────────────────────────────
6:35–7:10  FECHO
────────────────────────────────────────
ECRÃ: mensagem de arranque no canal (texto do slide 10) ou capa do manual.
NARRAÇÃO:
«O manual em PDF tem a matriz completa, os três métodos para a mesma mensagem
chegar ao e-mail e ao canal, e as perguntas frequentes. O próximo passo é
concreto: abrir o Team da vossa AO e escrever a primeira dúvida no canal certo.
Deixem o e-mail para o que é sério — e, nos avisos que ninguém pode perder,
usem o Cc do canal. Obrigado.»

────────────────────────────────────────
VERSÃO CURTA (2 min, se precisarem de um «teaser»)
────────────────────────────────────────
1. Problema: e-mail lento + um Team único inútil para o dia a dia.
2. Proposta: Team por AO; e-mail para o formal.
3. Ponte: avisos importantes em Cc para o endereço do canal.
4. Um gesto: abrir o canal Geral e @mencionar.
5. Convite: ler o manual / ir à sessão de 20 minutos.

────────────────────────────────────────
PÓS-PRODUÇÃO
────────────────────────────────────────
- Título sugerido: «AIP | Do e-mail ao Teams (guia de 7 minutos)»
- Colocar o ficheiro no Team geral (canal Avisos) E no canal Avisos de cada AO.
- Legendas em PT-PT (o Teams e o Clipchamp geram legendas; rever «ficheiro»,
  «telemóvel», «e-mail»).
""",
        encoding="utf-8",
    )
    return path


if __name__ == "__main__":
    pdf = build_pdf()
    pptx = build_pptx()
    guiao = build_guiao()
    docx = build_docx()
    print(pdf)
    print(pptx)
    print(guiao)
    print(docx)
