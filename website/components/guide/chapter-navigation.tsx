"use client"

import { BookOpen } from "lucide-react"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"
import type { GuideChapter } from "@/data/guide"

type ChapterNavigationProps = {
  chapters: GuideChapter[]
  activeId: string
  onSelect: (id: string) => void
}

export function ChapterNavigation({ chapters, activeId, onSelect }: ChapterNavigationProps) {
  return (
    <Sidebar collapsible="none" className="guide-sidebar-primitive">
      <SidebarContent>
        <SidebarGroup>
          <div className="guide-chapter-select">
            <label className="guide-select-label" htmlFor="chapter-select">Capítulo</label>
            <Select value={activeId} onValueChange={onSelect}>
              <SelectTrigger id="chapter-select" className="w-full border-slate-300 bg-white text-left text-slate-900">
                <SelectValue />
              </SelectTrigger>
              <SelectContent position="popper">
                {chapters.map((chapter) => (
                  <SelectItem key={chapter.id} value={chapter.id}>
                    {chapter.id}. {chapter.shortTitle}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <nav className="guide-navigation" aria-label="Capítulos do guia">
            <div className="guide-navigation-heading">
              <BookOpen aria-hidden="true" size={16} /> Guia AIP
            </div>
            <p className="guide-navigation-kicker">Índice</p>
            <SidebarGroupContent>
              <SidebarMenu>
                {chapters.map((chapter) => {
                  const active = chapter.id === activeId

                  return (
                    <SidebarMenuItem key={chapter.id}>
                      <SidebarMenuButton
                        aria-current={active ? "page" : undefined}
                        isActive={active}
                        className={`guide-chapter-link ${active ? "is-active" : ""}`}
                        onClick={() => onSelect(chapter.id)}
                      >
                        <span>{chapter.id}</span>
                        <span>{chapter.shortTitle}</span>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </nav>
        </SidebarGroup>
      </SidebarContent>
    </Sidebar>
  )
}
