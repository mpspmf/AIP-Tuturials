"use client"

import { Lightbulb } from "lucide-react"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import type { GuideBlock, GuideChapter } from "@/data/guide"

type ChapterContentProps = {
  chapter: GuideChapter
  activeFigureId?: number
  onFigureSelect: (id: number) => void
}

function FigureReferences({ ids, onSelect }: { ids?: number[]; onSelect: (id: number) => void }) {
  if (!ids?.length) return null
  return (
    <span className="guide-figure-refs" aria-label="Figuras relacionadas">
      {ids.map((id) => (
        <button key={id} type="button" onClick={() => onSelect(id)}>
          Figura {id}
        </button>
      ))}
    </span>
  )
}

function StepBlock({
  block,
  className,
  onFigureSelect,
}: {
  block: Extract<GuideBlock, { kind: "step" }>
  className: string
  onFigureSelect: (id: number) => void
}) {
  const firstFigureId = block.figureIds?.[0]
  const stepContents = (
    <>
      <span className="guide-step-number">{String(block.number).padStart(2, "0")}</span>
      <span className="guide-step-text">{block.text}</span>
    </>
  )

  return (
    <section
      className={`${className} guide-step ${firstFigureId !== undefined ? "has-figure" : ""}`}
      aria-label={`Passo ${block.number}`}
    >
      {firstFigureId !== undefined ? (
        <button
          type="button"
          className="guide-step-main is-interactive"
          onClick={() => onFigureSelect(firstFigureId)}
        >
          {stepContents}
        </button>
      ) : (
        <div className="guide-step-main">{stepContents}</div>
      )}
      <FigureReferences ids={block.figureIds} onSelect={onFigureSelect} />
    </section>
  )
}

function ParagraphBlock({
  block,
  className,
  onFigureSelect,
}: {
  block: Extract<GuideBlock, { kind: "paragraph" }>
  className: string
  onFigureSelect: (id: number) => void
}) {
  const firstFigureId = block.figureIds?.[0]

  if (firstFigureId === undefined) return <p className={className}>{block.text}</p>

  return (
    <p className={`${className} guide-paragraph has-figure`}>
      <button
        type="button"
        className="guide-paragraph-main is-interactive"
        onClick={() => onFigureSelect(firstFigureId)}
      >
        {block.text}
      </button>
      <FigureReferences ids={block.figureIds} onSelect={onFigureSelect} />
    </p>
  )
}

function Block({ block, activeFigureId, onFigureSelect }: { block: GuideBlock; activeFigureId?: number; onFigureSelect: (id: number) => void }) {
  const related = "figureIds" in block && block.figureIds?.includes(activeFigureId ?? -1)
  const className = `guide-block ${related ? "is-linked" : ""}`
  const references = "figureIds" in block ? block.figureIds : undefined

  switch (block.kind) {
    case "heading":
      return <h2 className="guide-section-heading">{block.text}</h2>
    case "paragraph":
      return <ParagraphBlock block={block} className={className} onFigureSelect={onFigureSelect} />
    case "step":
      return <StepBlock block={block} className={className} onFigureSelect={onFigureSelect} />
    case "callout":
      return (
        <aside className={`${className} guide-callout`}>
          <Lightbulb aria-hidden="true" size={18} />
          <div><h3>{block.title}</h3><p>{block.text}<FigureReferences ids={references} onSelect={onFigureSelect} /></p></div>
        </aside>
      )
    case "example":
      return <aside className="guide-example"><h3>{block.title}</h3><p>{block.text}</p></aside>
    case "table":
      return (
        <div className="guide-table-wrap">
          <Table>
            <TableHeader>
              <TableRow>
                {block.headers.map((header) => <TableHead key={header}>{header}</TableHead>)}
              </TableRow>
            </TableHeader>
            <TableBody>
              {block.rows.map((row, index) => (
                <TableRow key={`${row.join("-")}-${index}`}>
                  {row.map((cell, cellIndex) => <TableCell key={`${cell}-${cellIndex}`}>{cell}</TableCell>)}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </div>
      )
  }
}

export function ChapterContent({ chapter, activeFigureId, onFigureSelect }: ChapterContentProps) {
  return (
    <article
      className="guide-content"
      aria-labelledby="chapter-title"
      tabIndex={0}
    >
      <p className="guide-intro">{chapter.intro}</p>
      <div className="guide-rule" />
      <div className="guide-blocks">
        {chapter.blocks.map((block) => <Block key={block.id} block={block} activeFigureId={activeFigureId} onFigureSelect={onFigureSelect} />)}
      </div>
    </article>
  )
}
