/**
 * ============================================================================
 * ITWorkflowTimeline.tsx
 * ============================================================================
 *
 * Timeline visuale delle 7 fasi del ciclo lavorativo IT. Mostra per ciascuna
 * fase i documenti prodotti e lo stato di avanzamento (completato / in corso /
 * da iniziare) in base ai documenti presenti nel vault.
 *
 * Da collocare in: src/components/itInfrastructure/ITWorkflowTimeline.tsx
 *
 * Usage (in ITInfrastructureSidebar o in una pagina dedicata):
 *
 *   <ITWorkflowTimeline
 *     allResources={allResources}
 *     projectId="acme-milano-2026"
 *     onNavigate={onNavigateToResource}
 *   />
 *
 * ============================================================================
 */

import React, { useMemo } from "react";
import {
  Search,
  PenTool,
  Package,
  Server,
  Settings,
  TestTube,
  Rocket,
  CheckCircle2,
  Clock,
  Circle,
  ChevronRight,
  FileText,
  AlertTriangle,
} from "lucide-react";
import { ResourceItem, ITDocType } from "../../types";
import { IT_DOC_TYPES, IT_DOC_TYPE_LIST } from "../../lib/okfItTemplates";

interface ITWorkflowTimelineProps {
  allResources: ResourceItem[];
  projectId?: string; // se omesso, mostra tutti i progetti
  onNavigate: (resource: ResourceItem) => void;
  compact?: boolean; // modalità compatta per sidebar
}

interface PhaseInfo {
  phase: number;
  name: string;
  description: string;
  icon: React.ElementType;
  color: string;
  expectedDocTypes: ITDocType[];
}

const PHASES: PhaseInfo[] = [
  {
    phase: 1,
    name: "Assessment",
    description: "Rilevamento requisiti e site survey",
    icon: Search,
    color: "#60A5FA",
    expectedDocTypes: ["rsd_urs"],
  },
  {
    phase: 2,
    name: "Design",
    description: "Progettazione architetturale HLD + LLD",
    icon: PenTool,
    color: "#A78BFA",
    expectedDocTypes: ["hld", "lld"],
  },
  {
    phase: 3,
    name: "Procurement & Staging",
    description: "Approvvigionamento e pre-assemblaggio",
    icon: Package,
    color: "#F472B6",
    expectedDocTypes: ["mop", "rollback"],
  },
  {
    phase: 4,
    name: "Racking & Cabling",
    description: "Installazione fisica e cablaggio certificato",
    icon: Server,
    color: "#FB923C",
    expectedDocTypes: [], // confluisce in as_built
  },
  {
    phase: 5,
    name: "Commissioning",
    description: "Configurazione apparati e servizi base",
    icon: Settings,
    color: "#FBBF24",
    expectedDocTypes: [], // confluisce in as_built
  },
  {
    phase: 6,
    name: "Testing",
    description: "Collaudo funzionale, performance, failover",
    icon: TestTube,
    color: "#34D399",
    expectedDocTypes: ["atp"],
  },
  {
    phase: 7,
    name: "Go-Live / Handover",
    description: "Cutover, handover e documentazione finale",
    icon: Rocket,
    color: "#C5A059",
    expectedDocTypes: ["as_built", "sop_runbook", "handover_inventory"],
  },
];

/**
 * Determina lo stato di una fase in base ai documenti prodotti.
 */
function getPhaseStatus(
  phase: PhaseInfo,
  docsInPhase: ResourceItem[]
): "completed" | "in_progress" | "pending" {
  if (phase.expectedDocTypes.length === 0) {
    // Fasi senza documenti diretti (4, 5) — considerate "pending" finché as_built non esiste
    return "pending";
  }
  const total = phase.expectedDocTypes.length;
  const found = docsInPhase.length;
  if (found === 0) return "pending";
  if (found >= total) return "completed";
  return "in_progress";
}

/**
 * Componente principale.
 */
export const ITWorkflowTimeline: React.FC<ITWorkflowTimelineProps> = ({
  allResources,
  projectId,
  onNavigate,
  compact = false,
}) => {
  // Filtra le risorse IT del progetto specificato
  const itResources = useMemo(() => {
    return allResources.filter((r) => {
      const meta = r.metadata?.itMetadata;
      const isIT = r.metadata?.isITAlias === true || !!meta;
      if (!isIT) return false;
      if (projectId && meta?.project_id !== projectId) return false;
      return true;
    });
  }, [allResources, projectId]);

  // Raggruppa per fase
  const docsByPhase = useMemo(() => {
    const map = new Map<number, ResourceItem[]>();
    PHASES.forEach((p) => map.set(p.phase, []));
    itResources.forEach((r) => {
      const phase = r.metadata?.itMetadata?.phase;
      if (phase && map.has(phase)) {
        map.get(phase)!.push(r);
      }
    });
    return map;
  }, [itResources]);

  // Calcola progresso globale
  const progress = useMemo(() => {
    let completed = 0;
    let inProgress = 0;
    PHASES.forEach((p) => {
      const status = getPhaseStatus(p, docsByPhase.get(p.phase) || []);
      if (status === "completed") completed++;
      else if (status === "in_progress") inProgress++;
    });
    return {
      completed,
      inProgress,
      pending: 7 - completed - inProgress,
      percent: Math.round((completed / 7) * 100),
    };
  }, [docsByPhase]);

  if (itResources.length === 0) {
    return (
      <div className={`text-center ${compact ? "p-4" : "p-8"}`}>
        <AlertTriangle className="w-8 h-8 text-[#555] mx-auto mb-3" />
        <p className="text-sm text-[#BBB] mb-2">
          {projectId ? `Nessun documento IT trovato per il progetto "${projectId}"` : "Nessun documento IT nel vault"}
        </p>
        {!compact && (
          <p className="text-xs text-[#777]">
            I documenti del ciclo IT vengono riconosciuti quando contengono metadati come{" "}
            <code className="text-[#C5A059]">project_id</code>, <code className="text-[#C5A059]">phase</code> o
            usano un alias type IT nel frontmatter.
          </p>
        )}
      </div>
    );
  }

  return (
    <div className={compact ? "space-y-2" : "space-y-4"}>
      {/* Header progresso (solo modalità estesa) */}
      {!compact && (
        <div className="bg-[#0A0A0A] border border-[#1A1A1A] rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-sm font-semibold text-[#C5A059] flex items-center gap-2">
              <FileText className="w-4 h-4" />
              Avanzamento ciclo IT
              {projectId && <span className="text-[#777] text-xs font-normal">— {projectId}</span>}
            </h3>
            <span className="text-xs text-[#999]">
              {progress.completed}/7 fasi completate · {itResources.length} documenti
            </span>
          </div>
          <div className="w-full bg-[#1A1A1A] rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-[#60A5FA] via-[#A78BFA] to-[#C5A059] h-full transition-all duration-500"
              style={{ width: `${progress.percent}%` }}
            />
          </div>
          <div className="flex justify-between mt-1 text-[10px] text-[#777]">
            <span>Fase 1</span>
            <span>{progress.percent}%</span>
            <span>Fase 7</span>
          </div>
        </div>
      )}

      {/* Timeline verticale */}
      <div className="relative">
        {/* Linea verticale di sfondo */}
        <div
          className="absolute left-3 sm:left-4 top-0 bottom-0 w-px bg-[#1A1A1A]"
          aria-hidden="true"
        />

        <div className="space-y-3">
          {PHASES.map((phase) => {
            const docsInPhase = docsByPhase.get(phase.phase) || [];
            const status = getPhaseStatus(phase, docsInPhase);
            const Icon = phase.icon;

            const StatusIcon = status === "completed" ? CheckCircle2 : status === "in_progress" ? Clock : Circle;
            const statusColor =
              status === "completed" ? "#4ADE80" : status === "in_progress" ? "#FBBF24" : "#555";

            return (
              <div key={phase.phase} className="relative flex gap-3 sm:gap-4">
                {/* Nodo fase */}
                <div className="relative shrink-0 z-10">
                  <div
                    className={`w-6 h-6 sm:w-8 sm:h-8 rounded-full flex items-center justify-center border-2 transition-colors ${
                      status === "completed"
                        ? "bg-[#0A0A0A] border-[#4ADE80]"
                        : status === "in_progress"
                        ? "bg-[#0A0A0A] border-[#FBBF24]"
                        : "bg-[#0A0A0A] border-[#333]"
                    }`}
                    style={{ boxShadow: status !== "pending" ? `0 0 12px ${statusColor}40` : "none" }}
                  >
                    <Icon
                      className={`w-3 h-3 sm:w-4 sm:h-4 ${status !== "pending" ? "" : "text-[#555]"}`}
                      style={{ color: status !== "pending" ? phase.color : "#555" }}
                    />
                  </div>
                </div>

                {/* Contenuto fase */}
                <div className="flex-1 min-w-0 pb-4">
                  <div className="flex items-center gap-2 mb-1 flex-wrap">
                    <h4 className={`font-medium ${compact ? "text-xs" : "text-sm"} text-white`}>
                      Fase {phase.phase} — {phase.name}
                    </h4>
                    <StatusIcon
                      className="w-3 h-3 shrink-0"
                      style={{ color: statusColor }}
                    />
                    {docsInPhase.length > 0 && (
                      <span className="text-[10px] text-[#777] bg-[#1A1A1A] px-1.5 py-0.5 rounded">
                        {docsInPhase.length} doc{docsInPhase.length > 1 ? "s" : ""}
                      </span>
                    )}
                  </div>
                  {!compact && (
                    <p className="text-xs text-[#999] mb-2">{phase.description}</p>
                  )}

                  {/* Lista documenti nella fase */}
                  {docsInPhase.length > 0 ? (
                    <div className="space-y-1">
                      {docsInPhase.map((doc) => {
                        const docMeta = doc.metadata?.itMetadata;
                        const originalType = doc.metadata?.originalDocType as ITDocType | undefined;
                        const itInfo = originalType ? IT_DOC_TYPES[originalType] : null;
                        const docStatus = docMeta?.status;
                        return (
                          <button
                            key={doc.id}
                            onClick={() => onNavigate(doc)}
                            className="flex items-center gap-2 w-full text-left bg-[#0A0A0A] hover:bg-[#111] border border-[#1A1A1A] hover:border-[#C5A059]/30 rounded px-2 py-1.5 transition-colors group"
                          >
                            <ChevronRight className="w-3 h-3 text-[#555] group-hover:text-[#C5A059] transition-colors" />
                            <span className="text-xs text-[#DDD] group-hover:text-white transition-colors truncate flex-1">
                              {doc.title}
                            </span>
                            {itInfo && (
                              <span
                                className="text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded font-medium"
                                style={{ color: phase.color, background: `${phase.color}1A` }}
                              >
                                {originalType}
                              </span>
                            )}
                            {docStatus && (
                              <span
                                className="text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded font-medium"
                                style={{
                                  color: docStatus === "approved" ? "#4ADE80" : docStatus === "draft" ? "#BBB" : "#C5A059",
                                  background:
                                    docStatus === "approved"
                                      ? "rgba(74,222,128,0.1)"
                                      : docStatus === "draft"
                                      ? "#1A1A1A"
                                      : "rgba(197,160,89,0.1)",
                                }}
                              >
                                {docStatus}
                              </span>
                            )}
                          </button>
                        );
                      })}
                    </div>
                  ) : (
                    !compact && (
                      <p className="text-[10px] text-[#555] italic">
                        {phase.expectedDocTypes.length === 0
                          ? "Nessun documento diretto — confluisce nella fase successiva"
                          : `Documenti attesi: ${phase.expectedDocTypes.join(", ")}`}
                      </p>
                    )
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default ITWorkflowTimeline;

/**
 * Esporta la lista delle fasi per uso in altri componenti.
 */
export { PHASES as IT_WORKFLOW_PHASES };
