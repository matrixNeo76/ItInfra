/**
 * ============================================================================
 * ITProjectMetadataCard.tsx
 * ============================================================================
 *
 * Scheda dedicata per la visualizzazione dei metadati IT estesi nel
 * KnowledgeReader. Mostra project_id, phase, owner_team, related_docs,
 * depends_on e altre informazioni del ciclo lavorativo IT.
 *
 * Da collocare in: src/components/itInfrastructure/ITProjectMetadataCard.tsx
 *
 * Dipendenze:
 * - React 19 + lucide-react (già presenti nel Knowledge Vault)
 * - Tipi ITDocType, ITProjectMetadata da ../../types (richiede Livello 2 applicato)
 * - Helper getITDocTypeInfo, IT_DOC_TYPES da ../../lib/okfItTemplates (richiede Livello 2)
 *
 * Usage (in KnowledgeReader.tsx dopo integrazione):
 *
 *   {activeTab === "it_metadata" && (
 *     <ITProjectMetadataCard resource={resource} onNavigate={onNavigateToResource} allResources={allResources} />
 *   )}
 *
 * ============================================================================
 */

import React from "react";
import {
  FolderKanban,
  MapPin,
  Building2,
  Calendar,
  User,
  Users,
  GitBranch,
  ArrowRight,
  AlertCircle,
  Clock,
  Shield,
  Tag,
  FileText,
  Layers,
  CheckCircle2,
  XCircle,
  Info,
} from "lucide-react";
import { ResourceItem, ITProjectMetadata, ITDocType } from "../../types";
import { getITDocTypeInfo } from "../../lib/okfItTemplates";

interface ITProjectMetadataCardProps {
  resource: ResourceItem;
  allResources: ResourceItem[];
  onNavigate: (resource: ResourceItem) => void;
}

/**
 * Rende una singola riga "label : value" con icona.
 */
function MetaRow({
  icon: Icon,
  label,
  value,
  highlight = false,
}: {
  icon: React.ElementType;
  label: string;
  value: React.ReactNode;
  highlight?: boolean;
}) {
  if (!value || (Array.isArray(value) && value.length === 0)) return null;
  return (
    <div className="flex items-start gap-3 py-2 border-b border-[#1A1A1A] last:border-b-0">
      <Icon className={`w-4 h-4 mt-0.5 shrink-0 ${highlight ? "text-[#C5A059]" : "text-[#777]"}`} />
      <div className="flex-1 min-w-0">
        <div className="text-[10px] uppercase tracking-wider text-[#777] mb-0.5">{label}</div>
        <div className={`text-sm ${highlight ? "text-[#C5A059] font-medium" : "text-[#DDD]"}`}>
          {value}
        </div>
      </div>
    </div>
  );
}

/**
 * Rende un badge per lo stato del documento.
 */
function StatusBadge({ status }: { status: ITProjectMetadata["status"] }) {
  if (!status) return null;
  const config: Record<string, { color: string; bg: string; icon: React.ElementType }> = {
    draft:       { color: "#BBB", bg: "#1A1A1A", icon: FileText },
    "in-review": { color: "#C5A059", bg: "rgba(197,160,89,0.1)", icon: Clock },
    approved:    { color: "#4ADE80", bg: "rgba(74,222,128,0.1)", icon: CheckCircle2 },
    superseded:  { color: "#F87171", bg: "rgba(248,113,113,0.1)", icon: XCircle },
  };
  const c = config[status] || config.draft;
  const Icon = c.icon;
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] uppercase tracking-wider font-medium"
      style={{ color: c.color, background: c.bg }}
    >
      <Icon className="w-3 h-3" />
      {status}
    </span>
  );
}

/**
 * Rende un badge per la fase (1-7) con colore progressivo.
 */
function PhaseBadge({ phase }: { phase: number }) {
  const phaseColors: Record<number, string> = {
    1: "#60A5FA", // blu
    2: "#A78BFA", // viola
    3: "#F472B6", // rosa
    4: "#FB923C", // arancione
    5: "#FBBF24", // giallo
    6: "#34D399", // verde
    7: "#C5A059", // gold
  };
  const color = phaseColors[phase] || "#777";
  const phaseLabels: Record<number, string> = {
    1: "Assessment",
    2: "Design",
    3: "Procurement",
    4: "Racking",
    5: "Commissioning",
    6: "Testing",
    7: "Go-Live",
  };
  return (
    <span
      className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] uppercase tracking-wider font-medium"
      style={{ color, background: `${color}1A` }}
    >
      <Layers className="w-3 h-3" />
      Fase {phase} — {phaseLabels[phase] || "—"}
    </span>
  );
}

/**
 * Rende un link cliccabile a un documento correlato.
 */
function RelatedDocLink({
  docId,
  allResources,
  onNavigate,
}: {
  docId: string;
  allResources: ResourceItem[];
  onNavigate: (r: ResourceItem) => void;
}) {
  // Cerca il documento nel vault per ID
  const target = allResources.find(
    (r) => r.id === docId || r.metadata?.id === docId || r.title === docId
  );

  if (target) {
    return (
      <button
        onClick={() => onNavigate(target)}
        className="inline-flex items-center gap-1 text-xs text-[#C5A059] hover:text-[#D9B870] hover:underline transition-colors"
      >
        <ArrowRight className="w-3 h-3" />
        {target.title}
      </button>
    );
  }

  // Documento non trovato nel vault (placeholder)
  return (
    <span className="inline-flex items-center gap-1 text-xs text-[#777] italic">
      <AlertCircle className="w-3 h-3" />
      {docId} <span className="text-[10px]">(da compilare)</span>
    </span>
  );
}

/**
 * Componente principale.
 */
export const ITProjectMetadataCard: React.FC<ITProjectMetadataCardProps> = ({
  resource,
  allResources,
  onNavigate,
}) => {
  const meta: ITProjectMetadata | undefined = resource.metadata?.itMetadata;
  const isITAlias = resource.metadata?.isITAlias;
  const originalDocType = resource.metadata?.originalDocType;

  // Se il documento non ha metadati IT, mostra empty state informativo
  if (!meta && !isITAlias) {
    return (
      <div className="p-6 text-center">
        <Info className="w-8 h-8 text-[#555] mx-auto mb-3" />
        <p className="text-sm text-[#BBB] mb-2">Questo documento non fa parte del ciclo lavorativo IT</p>
        <p className="text-xs text-[#777]">
          I documenti del ciclo IT vengono riconosciuti automaticamente quando contengono
          metadati come <code className="text-[#C5A059]">project_id</code>,{" "}
          <code className="text-[#C5A059]">phase</code>, o usano un alias type IT (es.{" "}
          <code className="text-[#C5A059]">lld</code> invece di{" "}
          <code className="text-[#C5A059]">architecture</code>).
        </p>
      </div>
    );
  }

  // Recupera info del tipo IT (se è alias)
  const itTypeInfo = originalDocType ? getITDocTypeInfo(originalDocType as ITDocType) : null;

  return (
    <div className="p-4 sm:p-6 space-y-6">
      {/* Header del documento IT */}
      <div className="space-y-3">
        <div className="flex items-center gap-2 flex-wrap">
          {itTypeInfo && (
            <span
              className="inline-flex items-center gap-1.5 px-2 py-1 rounded text-[10px] uppercase tracking-wider font-semibold"
              style={{ color: "#C5A059", background: "rgba(197,160,89,0.1)" }}
            >
              <FileText className="w-3 h-3" />
              {itTypeInfo.label}
            </span>
          )}
          {meta?.phase && <PhaseBadge phase={meta.phase} />}
          {meta?.status && <StatusBadge status={meta.status} />}
          {meta?.classification && (
            <span className="inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] uppercase tracking-wider font-medium text-[#F87171] bg-[rgba(248,113,113,0.1)]">
              <Shield className="w-3 h-3" />
              {meta.classification}
            </span>
          )}
        </div>
        {itTypeInfo?.description && (
          <p className="text-xs text-[#999] italic">{itTypeInfo.description}</p>
        )}
      </div>

      {/* Griglia metadati */}
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
        {/* Identità estesa */}
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2 flex items-center gap-1.5">
            <FolderKanban className="w-3.5 h-3.5" /> Identità
          </h4>
          <MetaRow icon={Tag} label="ID Documento" value={resource.metadata?.id || resource.id} highlight />
          <MetaRow icon={GitBranch} label="Versione" value={meta?.version} />
          {meta?.created_at && (
            <MetaRow icon={Calendar} label="Creato il" value={meta.created_at} />
          )}
          {meta?.updated_at && (
            <MetaRow icon={Calendar} label="Aggiornato il" value={meta.updated_at} />
          )}
        </div>

        {/* Progetto */}
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2 flex items-center gap-1.5">
            <FolderKanban className="w-3.5 h-3.5" /> Progetto
          </h4>
          <MetaRow icon={FolderKanban} label="Project ID" value={meta?.project_id} highlight />
          <MetaRow icon={FolderKanban} label="Nome progetto" value={meta?.project_name} />
          <MetaRow icon={MapPin} label="Sito" value={meta?.site} />
          <MetaRow icon={Building2} label="Cliente" value={meta?.customer} />
        </div>

        {/* Persone */}
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2 flex items-center gap-1.5">
            <Users className="w-3.5 h-3.5" /> Persone
          </h4>
          <MetaRow icon={User} label="Autore" value={meta?.author} />
          <MetaRow icon={User} label="Revisore" value={meta?.reviewer} />
          <MetaRow icon={User} label="Approvatore" value={meta?.approver} />
          <MetaRow icon={Users} label="Team responsabile" value={meta?.owner_team} />
        </div>

        {/* Governance */}
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2 flex items-center gap-1.5">
            <Shield className="w-3.5 h-3.5" /> Governance
          </h4>
          <MetaRow icon={Shield} label="Classificazione" value={meta?.classification} />
          <MetaRow icon={Clock} label="Retention" value={meta?.retention} />
          <MetaRow icon={Tag} label="Lingua" value={meta?.lang} />
          {meta?.supersedes && (
            <MetaRow icon={GitBranch} label="Sostituisce" value={meta.supersedes} />
          )}
          {meta?.superseded_by && (
            <MetaRow icon={GitBranch} label="Sostituito da" value={meta.superseded_by} />
          )}
        </div>
      </div>

      {/* Documenti correlati */}
      {meta?.related_docs && meta.related_docs.length > 0 && (
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-3 flex items-center gap-1.5">
            <ArrowRight className="w-3.5 h-3.5" /> Documenti correlati ({meta.related_docs.length})
          </h4>
          <div className="space-y-2 bg-[#0A0A0A] border border-[#1A1A1A] rounded p-3">
            {meta.related_docs.map((docId, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-[10px] text-[#555] mt-0.5 font-mono">{String(i + 1).padStart(2, "0")}</span>
                <RelatedDocLink docId={docId} allResources={allResources} onNavigate={onNavigate} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dipendenze (depends_on) */}
      {meta?.depends_on && meta.depends_on.length > 0 && (
        <div>
          <h4 className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-3 flex items-center gap-1.5">
            <AlertCircle className="w-3.5 h-3.5" /> Dipendenze ({meta.depends_on.length})
          </h4>
          <div className="space-y-2 bg-[#0A0A0A] border border-[rgba(197,160,89,0.3)] rounded p-3">
            <p className="text-xs text-[#999] mb-2 italic">
              Documenti che devono essere già compilati prima di questo:
            </p>
            {meta.depends_on.map((docId, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="text-[10px] text-[#C5A059] mt-0.5 font-mono">→</span>
                <RelatedDocLink docId={docId} allResources={allResources} onNavigate={onNavigate} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Footer informativo */}
      <div className="text-[10px] text-[#555] border-t border-[#1A1A1A] pt-3 flex items-center gap-1.5">
        <Info className="w-3 h-3" />
        <span>
          Metadati estratti dal frontmatter OKF v0.2 dal parser nativo. Tipo IT originale:{" "}
          <code className="text-[#C5A059]">{originalDocType || "—"}</code>
          {isITAlias && <span className="ml-1 text-[#4ADE80]">(alias riconosciuto)</span>}
        </span>
      </div>
    </div>
  );
};

export default ITProjectMetadataCard;
