/**
 * ============================================================================
 * ITInfrastructureSidebar.tsx
 * ============================================================================
 *
 * Pannello laterale che mostra la timeline delle fasi IT e i progetti attivi.
 * Progettato per essere aperto come drawer laterale (simile a VaultHealthCheckDrawer
 * o DiagnosticDrawer già presenti nel Knowledge Vault).
 *
 * Da collocare in: src/components/itInfrastructure/ITInfrastructureSidebar.tsx
 *
 * Usage (in App.tsx o VaultModalsContainer.tsx dopo integrazione):
 *
 *   <ITInfrastructureSidebar
 *     isOpen={isITSidebarOpen}
 *     onClose={() => setIsITSidebarOpen(false)}
 *     allResources={allResources}
 *     onNavigate={onNavigateToResource}
 *   />
 *
 * ============================================================================
 */

import React, { useState, useMemo } from "react";
import {
  X,
  FolderKanban,
  Network,
  Layers,
  TrendingUp,
  ChevronDown,
  ChevronRight,
  FileText,
  Calendar,
  Search,
} from "lucide-react";
import { ResourceItem } from "../../types";
import { IT_DOC_TYPE_LIST } from "../../lib/okfItTemplates";
import { ITWorkflowTimeline } from "./ITWorkflowTimeline";

interface ITInfrastructureSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  allResources: ResourceItem[];
  onNavigate: (resource: ResourceItem) => void;
}

/**
 * Componente principale.
 */
export const ITInfrastructureSidebar: React.FC<ITInfrastructureSidebarProps> = ({
  isOpen,
  onClose,
  allResources,
  onNavigate,
}) => {
  const [selectedProjectId, setSelectedProjectId] = useState<string | undefined>(undefined);
  const [showProjectList, setShowProjectList] = useState(true);

  // Estrae lista progetti IT unici dal vault
  const projects = useMemo(() => {
    const map = new Map<string, { id: string; name: string; count: number; latestUpdate?: string }>();
    allResources.forEach((r) => {
      const meta = r.metadata?.itMetadata;
      if (!meta?.project_id) return;
      const existing = map.get(meta.project_id);
      if (existing) {
        existing.count++;
        const updatedAt = meta.updated_at || meta.created_at;
        if (updatedAt && (!existing.latestUpdate || updatedAt > existing.latestUpdate)) {
          existing.latestUpdate = updatedAt;
        }
      } else {
        map.set(meta.project_id, {
          id: meta.project_id,
          name: meta.project_name || meta.project_id,
          count: 1,
          latestUpdate: meta.updated_at || meta.created_at,
        });
      }
    });
    return Array.from(map.values()).sort((a, b) => (b.latestUpdate || "").localeCompare(a.latestUpdate || ""));
  }, [allResources]);

  // Conteggio totale documenti IT
  const totalITDocs = useMemo(() => {
    return allResources.filter((r) => r.metadata?.isITAlias === true || r.metadata?.itMetadata).length;
  }, [allResources]);

  // Conteggio per tipo IT
  const docsByType = useMemo(() => {
    const map = new Map<string, number>();
    allResources.forEach((r) => {
      const t = r.metadata?.originalDocType;
      if (t) {
        map.set(t, (map.get(t) || 0) + 1);
      }
    });
    return map;
  }, [allResources]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-40 flex"
      role="dialog"
      aria-modal="true"
      aria-labelledby="it-sidebar-title"
    >
      {/* Overlay */}
      <div
        className="absolute inset-0 bg-black/60 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />

      {/* Drawer */}
      <div className="relative ml-auto w-full max-w-md sm:max-w-lg bg-[#0A0A0A] border-l border-[#1A1A1A] flex flex-col h-full shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-[#1A1A1A] bg-[#0F0F0F]">
          <div className="flex items-center gap-2">
            <Network className="w-5 h-5 text-[#C5A059]" />
            <h2 id="it-sidebar-title" className="text-sm font-semibold text-white">
              Ciclo Lavorativo IT
            </h2>
          </div>
          <button
            onClick={onClose}
            className="text-[#777] hover:text-white p-1 rounded transition-colors"
            aria-label="Chiudi"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body scrollable */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Stats summary */}
          <div className="grid grid-cols-3 gap-2">
            <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-2 text-center">
              <Layers className="w-4 h-4 text-[#C5A059] mx-auto mb-1" />
              <div className="text-lg font-semibold text-white">{projects.length}</div>
              <div className="text-[10px] text-[#777] uppercase tracking-wider">Progetti</div>
            </div>
            <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-2 text-center">
              <FileText className="w-4 h-4 text-[#C5A059] mx-auto mb-1" />
              <div className="text-lg font-semibold text-white">{totalITDocs}</div>
              <div className="text-[10px] text-[#777] uppercase tracking-wider">Documenti</div>
            </div>
            <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-2 text-center">
              <TrendingUp className="w-4 h-4 text-[#C5A059] mx-auto mb-1" />
              <div className="text-lg font-semibold text-white">
                {Math.round((projects.length > 0 ? totalITDocs / projects.length : 0) * 10) / 10}
              </div>
              <div className="text-[10px] text-[#777] uppercase tracking-wider">Doc/Progetto</div>
            </div>
          </div>

          {/* Selettore progetto */}
          <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-3">
            <button
              onClick={() => setShowProjectList(!showProjectList)}
              className="flex items-center justify-between w-full text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2"
            >
              <span className="flex items-center gap-1.5">
                <FolderKanban className="w-3.5 h-3.5" />
                Progetto attivo: {selectedProjectId || "Tutti"}
              </span>
              {showProjectList ? <ChevronDown className="w-3.5 h-3.5" /> : <ChevronRight className="w-3.5 h-3.5" />}
            </button>

            {showProjectList && (
              <div className="space-y-1">
                <button
                  onClick={() => setSelectedProjectId(undefined)}
                  className={`flex items-center justify-between w-full text-left text-xs px-2 py-1.5 rounded transition-colors ${
                    !selectedProjectId
                      ? "bg-[#C5A059]/10 text-[#C5A059]"
                      : "text-[#BBB] hover:bg-[#1A1A1A]"
                  }`}
                >
                  <span className="flex items-center gap-1.5">
                    <Layers className="w-3 h-3" />
                    Tutti i progetti
                  </span>
                  <span className="text-[10px] text-[#777]">{totalITDocs}</span>
                </button>

                {projects.map((p) => (
                  <button
                    key={p.id}
                    onClick={() => setSelectedProjectId(p.id)}
                    className={`flex items-center justify-between w-full text-left text-xs px-2 py-1.5 rounded transition-colors ${
                      selectedProjectId === p.id
                        ? "bg-[#C5A059]/10 text-[#C5A059]"
                        : "text-[#BBB] hover:bg-[#1A1A1A]"
                    }`}
                  >
                    <span className="flex items-center gap-1.5 min-w-0">
                      <FolderKanban className="w-3 h-3 shrink-0" />
                      <span className="truncate">{p.name}</span>
                    </span>
                    <span className="flex items-center gap-2 shrink-0">
                      {p.latestUpdate && (
                        <span className="text-[10px] text-[#777] flex items-center gap-0.5">
                          <Calendar className="w-2.5 h-2.5" />
                          {p.latestUpdate.slice(0, 10)}
                        </span>
                      )}
                      <span className="text-[10px] text-[#777]">{p.count}</span>
                    </span>
                  </button>
                ))}

                {projects.length === 0 && (
                  <p className="text-[10px] text-[#777] italic px-2 py-2">
                    Nessun progetto IT trovato. Crea un documento con{" "}
                    <code className="text-[#C5A059]">project_id</code> nel frontmatter.
                  </p>
                )}
              </div>
            )}
          </div>

          {/* Timeline */}
          <div>
            <h3 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-3 flex items-center gap-1.5">
              <Network className="w-3.5 h-3.5" />
              Timeline fasi
            </h3>
            <ITWorkflowTimeline
              allResources={allResources}
              projectId={selectedProjectId}
              onNavigate={onNavigate}
              compact={false}
            />
          </div>

          {/* Distribuzione tipi documentali */}
          <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-3">
            <h3 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2 flex items-center gap-1.5">
              <FileText className="w-3.5 h-3.5" />
              Distribuzione per tipo
            </h3>
            <div className="space-y-1">
              {IT_DOC_TYPE_LIST.map((t) => {
                const count = docsByType.get(t.type) || 0;
                const max = Math.max(...Array.from(docsByType.values()), 1);
                const width = (count / max) * 100;
                return (
                  <div key={t.type} className="flex items-center gap-2 text-xs">
                    <span className="text-[#999] w-32 truncate" title={t.label}>
                      {t.label}
                    </span>
                    <div className="flex-1 bg-[#1A1A1A] rounded h-3 overflow-hidden">
                      <div
                        className="bg-gradient-to-r from-[#60A5FA] to-[#C5A059] h-full transition-all duration-500"
                        style={{ width: `${width}%` }}
                      />
                    </div>
                    <span className="text-[#777] w-6 text-right tabular-nums">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-2 border-t border-[#1A1A1A] bg-[#0F0F0F]">
          <p className="text-[10px] text-[#555] text-center flex items-center justify-center gap-1">
            <Search className="w-3 h-3" />
            Documenti IT riconosciuti automaticamente dal parser OKF v0.2
          </p>
        </div>
      </div>
    </div>
  );
};

export default ITInfrastructureSidebar;
