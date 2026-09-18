"use client"

import * as React from "react"
import { ChevronLeft, ChevronRight, Expand, Pause, Play, X } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Carousel, CarouselContent, CarouselItem, type CarouselApi } from "@/components/ui/carousel"
import { Dialog, DialogClose, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import type { GuideFigure } from "@/data/guide"

type FigureViewerProps = {
  figures: GuideFigure[]
  selectedFigureId?: number
  onSelect: (id: number) => void
  requestedPlaying: boolean
  onRequestedPlayingChange: (playing: boolean) => void
}

export function FigureViewer({
  figures,
  selectedFigureId,
  onSelect,
  requestedPlaying,
  onRequestedPlayingChange,
}: FigureViewerProps) {
  const [api, setApi] = React.useState<CarouselApi>()
  const [index, setIndex] = React.useState(0)
  const [hovered, setHovered] = React.useState(false)
  const [focused, setFocused] = React.useState(false)
  const [dialogOpen, setDialogOpen] = React.useState(false)
  const [fitToWindow, setFitToWindow] = React.useState(true)
  const [hidden, setHidden] = React.useState(false)
  const [reducedMotion, setReducedMotion] = React.useState(false)
  const openerRef = React.useRef<HTMLElement | null>(null)

  const temporaryPause = hovered || focused || dialogOpen || hidden
  const playing = requestedPlaying && !temporaryPause
  const figure = figures[index]

  React.useEffect(() => {
    const setVisibility = () => setHidden(document.hidden)

    setVisibility()
    document.addEventListener("visibilitychange", setVisibility)
    return () => document.removeEventListener("visibilitychange", setVisibility)
  }, [])

  React.useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)")
    const sync = () => setReducedMotion(media.matches)

    sync()
    media.addEventListener("change", sync)
    return () => media.removeEventListener("change", sync)
  }, [])

  React.useEffect(() => {
    if (!api) return

    const syncSelectedFigure = () => {
      const nextIndex = api.selectedScrollSnap()
      const nextFigure = figures[nextIndex]

      if (!nextFigure) return
      setIndex(nextIndex)
      onSelect(nextFigure.id)
    }

    api.on("select", syncSelectedFigure)
    syncSelectedFigure()

    return () => {
      api.off("select", syncSelectedFigure)
    }
  }, [api, figures, onSelect])

  React.useEffect(() => {
    if (!api) return

    const pauseForManualDrag = () => onRequestedPlayingChange(false)

    api.on("pointerDown", pauseForManualDrag)
    return () => {
      api.off("pointerDown", pauseForManualDrag)
    }
  }, [api, onRequestedPlayingChange])

  React.useEffect(() => {
    if (!api) return

    const foundIndex = selectedFigureId === undefined
      ? 0
      : figures.findIndex((item) => item.id === selectedFigureId)
    const nextIndex = foundIndex < 0 ? 0 : foundIndex

    if (api.selectedScrollSnap() !== nextIndex) api.scrollTo(nextIndex)
  }, [api, figures, selectedFigureId])

  React.useEffect(() => {
    if (!playing || figures.length < 2) return

    const timer = window.setInterval(() => api?.scrollNext(), 8000)
    return () => window.clearInterval(timer)
  }, [api, figures.length, playing])

  const goTo = (target: number) => {
    onRequestedPlayingChange(false)
    api?.scrollTo(target)
  }

  const previous = () => {
    onRequestedPlayingChange(false)
    api?.scrollPrev()
  }

  const next = () => {
    onRequestedPlayingChange(false)
    api?.scrollNext()
  }

  const openDialog = (event: React.MouseEvent<HTMLElement>) => {
    openerRef.current = event.currentTarget
    setDialogOpen(true)
  }

  const handleKeyDown = (event: React.KeyboardEvent<HTMLDivElement>) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault()
      previous()
    }

    if (event.key === "ArrowRight") {
      event.preventDefault()
      next()
    }
  }

  if (!figure) return null

  return (
    <section className="guide-viewer-column" aria-label="Visualizador de figuras">
      <div className="guide-viewer-sticky">
        <div
          className="guide-viewer"
          onMouseEnter={() => setHovered(true)}
          onMouseLeave={() => setHovered(false)}
          onFocusCapture={() => setFocused(true)}
          onBlurCapture={(event) => {
            if (!event.currentTarget.contains(event.relatedTarget as Node)) {
              setFocused(false)
            }
          }}
        >
          <div className="guide-viewer-bar">
            <span>Figura {figure.id}</span>
            <span>Imagem {index + 1} de {figures.length}</span>
          </div>

          <Carousel
            opts={{ loop: true, duration: reducedMotion ? 0 : 25 }}
            setApi={setApi}
            onKeyDownCapture={handleKeyDown}
            className="guide-carousel"
            tabIndex={0}
            aria-label={`Figura ${figure.id}, imagem ${index + 1} de ${figures.length}`}
          >
            <CarouselContent className="ml-0">
              {figures.map((item, itemIndex) => {
                const isCurrent = itemIndex === index

                return (
                  <CarouselItem
                    className="pl-0"
                    key={item.id}
                    aria-hidden={!isCurrent}
                    inert={!isCurrent || undefined}
                  >
                    <button
                      type="button"
                      className="guide-image-button"
                      onClick={openDialog}
                      aria-label={`Ampliar figura ${item.id}`}
                      tabIndex={isCurrent ? 0 : -1}
                    >
                      <img
                        src={item.src}
                        width={item.width}
                        height={item.height}
                        alt={item.caption}
                        loading={itemIndex === 0 ? "eager" : "lazy"}
                        fetchPriority={itemIndex === 0 ? "high" : "auto"}
                      />
                    </button>
                  </CarouselItem>
                )
              })}
            </CarouselContent>
          </Carousel>

          <div className="guide-viewer-controls">
            <Button size="icon-sm" variant="outline" onClick={previous} aria-label="Figura anterior">
              <ChevronLeft />
            </Button>
            <div className="guide-figure-picker" aria-label="Selecionar figura">
              {figures.map((item, itemIndex) => (
                <button
                  key={item.id}
                  type="button"
                  aria-label={`Ver figura ${item.id}`}
                  aria-current={itemIndex === index ? "true" : undefined}
                  onClick={() => goTo(itemIndex)}
                >
                  {item.id}
                </button>
              ))}
            </div>
            <Button size="icon-sm" variant="outline" onClick={next} aria-label="Figura seguinte">
              <ChevronRight />
            </Button>
            <div className="guide-play-actions">
              <Button size="sm" variant="ghost" onClick={() => onRequestedPlayingChange(!requestedPlaying)} aria-pressed={requestedPlaying}>
                {requestedPlaying ? <Pause /> : <Play />}
                {requestedPlaying ? "Pausa" : "Reproduzir"}
              </Button>
            <Button size="icon-sm" variant="ghost" onClick={openDialog} aria-label="Ampliar figura">
                <Expand />
              </Button>
            </div>
          </div>
        </div>
        <p className="guide-caption">{figure.caption}</p>
      </div>

      <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
        <DialogContent
          showCloseButton={false}
          className="guide-figure-dialog max-w-[min(96vw,1400px)] p-4 sm:max-w-[min(96vw,1400px)]"
          onCloseAutoFocus={(event) => {
            event.preventDefault()
            if (openerRef.current?.isConnected) openerRef.current.focus()
          }}
        >
          <DialogClose asChild>
            <Button size="icon-sm" variant="ghost" className="guide-dialog-close" aria-label="Fechar ampliação">
              <X />
            </Button>
          </DialogClose>
          <DialogHeader>
            <DialogTitle>Figura {figure.id}</DialogTitle>
            <DialogDescription>{figure.caption}</DialogDescription>
          </DialogHeader>
          <div className={`guide-dialog-image ${fitToWindow ? "is-fit" : "is-full"}`}>
            <img src={figure.src} width={figure.width} height={figure.height} alt={figure.caption} />
          </div>
          <Button size="sm" variant="outline" onClick={() => setFitToWindow((current) => !current)}>
            {fitToWindow ? "Ver resolução completa" : "Ajustar à janela"}
          </Button>
        </DialogContent>
      </Dialog>
    </section>
  )
}
