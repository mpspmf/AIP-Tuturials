"use client"

import * as React from "react"

import { ChapterContent } from "@/components/guide/chapter-content"
import { ChapterNavigation } from "@/components/guide/chapter-navigation"
import { FigureViewer } from "@/components/guide/figure-viewer"
import { SidebarProvider } from "@/components/ui/sidebar"
import { chapters } from "@/data/guide"

export function GuideApp() {
  const [chapterId, setChapterId] = React.useState("01")
  const [selectedFigureId, setSelectedFigureId] = React.useState<number>()
  const [requestedPlaying, setRequestedPlaying] = React.useState(false)
  const firstRender = React.useRef(true)
  const chapter = chapters.find((item) => item.id === chapterId) ?? chapters[0]

  React.useEffect(() => {
    if (firstRender.current) {
      firstRender.current = false
      setRequestedPlaying(!window.matchMedia("(prefers-reduced-motion: reduce)").matches)
    }
  }, [])

  const selectChapter = (id: string) => {
    setChapterId(id)
    setSelectedFigureId(undefined)
  }

  const selectFigureFromInstructions = React.useCallback((id: number) => {
    setRequestedPlaying(false)
    setSelectedFigureId(id)
  }, [])

  return (
    <SidebarProvider className="block" style={{ "--sidebar-width": "220px" } as React.CSSProperties}>
      <main className="guide-shell">
        <header className="guide-topbar">
          <p>AIP · Guia prático</p>
          <span>Instruções de trabalho</span>
        </header>
        <ChapterNavigation chapters={chapters} activeId={chapter.id} onSelect={selectChapter} />
        <div className={`guide-workspace ${chapter.figures.length ? "has-figures" : "is-text-only"}`}>
          <header className="guide-chapter-header">
            <p className="guide-eyebrow">Capítulo {chapter.id}</p>
            <h1 id="chapter-title">{chapter.title}</h1>
          </header>
          <div className="guide-workspace-body">
            {chapter.figures.length > 0 && (
              <FigureViewer
                key={chapter.id}
                figures={chapter.figures}
                selectedFigureId={selectedFigureId}
                onSelect={setSelectedFigureId}
                requestedPlaying={requestedPlaying}
                onRequestedPlayingChange={setRequestedPlaying}
              />
            )}
            <ChapterContent
              key={`instructions-${chapter.id}`}
              chapter={chapter}
              activeFigureId={selectedFigureId}
              onFigureSelect={selectFigureFromInstructions}
            />
          </div>
        </div>
      </main>
    </SidebarProvider>
  )
}
