/**
 * ============================================================================
 * ITTemplateCompilerModal.tsx
 * ============================================================================
 *
 * Modale per compilare un template IT tramite Gemini AI a partire dai dati
 * forniti dall'utente. Usa l'endpoint POST /api/it-infrastructure/compile-template
 * (definito in 08-PATCH-captureRoutes.ts.md + 09-NEW-itInfrastructureService.ts).
 *
 * Da collocare in: src/components/itInfrastructure/ITTemplateCompilerModal.tsx
 *
 * Usage (in CaptureBar.tsx dopo integrazione):
 *
 *   <ITTemplateCompilerModal
 *     isOpen={isITCompilerOpen}
 *     onClose={() => setIsITCompilerOpen(false)}
 *     onResourceCompiled={(resource) => handleNewResource(resource)}
 *   />
 *
 * ============================================================================
 */

import React, { useState, useMemo } from "react";
import {
  X,
  FileText,
  Loader2,
  Sparkles,
  AlertCircle,
  CheckCircle2,
  Copy,
  Download,
  ChevronRight,
} from "lucide-react";
import { ResourceItem, ITDocType } from "../../types";
import { IT_DOC_TYPE_LIST, getITBoilerplate, getITDocTypeInfo } from "../../lib/okfItTemplates";

interface ITTemplateCompilerModalProps {
  isOpen: boolean;
  onClose: () => void;
  onResourceCompiled?: (resource: ResourceItem) => void;
}

type CompilerStage = "form" | "compiling" | "success" | "error";

export const ITTemplateCompilerModal: React.FC<ITTemplateCompilerModalProps> = ({
  isOpen,
  onClose,
  onResourceCompiled,
}) => {
  const [stage, setStage] = useState<CompilerStage>("form");
  const [selectedType, setSelectedType] = useState<ITDocType | "">("");
  const [projectId, setProjectId] = useState("");
  const [projectName, setProjectName] = useState("");
  const [site, setSite] = useState("");
  const [customer, setCustomer] = useState("");
  const [author, setAuthor] = useState("");
  const [ownerTeam, setOwnerTeam] = useState("");
  const [customData, setCustomData] = useState("");
  const [compiledDoc, setCompiledDoc] = useState<string>("");
  const [errorMessage, setErrorMessage] = useState<string>("");
  const [copied, setCopied] = useState(false);

  // Lista tipi raggruppati per fase
  const typesByPhase = useMemo(() => {
    const map = new Map<number, typeof IT_DOC_TYPE_LIST>();
    IT_DOC_TYPE_LIST.forEach((t) => {
      if (!map.has(t.phase)) map.set(t.phase, []);
      map.get(t.phase)!.push(t);
    });
    return Array.from(map.entries()).sort((a, b) => a[0] - b[0]);
  }, []);

  if (!isOpen) return null;

  // Validazione form
  const canCompile = selectedType && projectId && projectName;

  const handleCompile = async () => {
    if (!canCompile) return;
    setStage("compiling");
    setErrorMessage("");

    try {
      const response = await fetch("/api/it-infrastructure/compile-template", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          docType: selectedType,
          project_id: projectId,
          project_name: projectName,
          site: site || undefined,
          customer: customer || undefined,
          author: author || undefined,
          owner_team: ownerTeam || undefined,
          custom_data: customData || undefined,
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({ error: "Errore generico" }));
        throw new Error(err.error || `HTTP ${response.status}`);
      }

      const data = await response.json();
      setCompiledDoc(data.markdown);
      setStage("success");
    } catch (err: any) {
      setErrorMessage(err.message || "Errore sconosciuto durante la compilazione");
      setStage("error");
    }
  };

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(compiledDoc);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Errore copia:", err);
    }
  };

  const handleDownload = () => {
    const typeInfo = getITDocTypeInfo(selectedType as ITDocType);
    const filename = `${selectedType}-${projectId}-${new Date().toISOString().slice(0, 10)}.md`;
    const blob = new Blob([compiledDoc], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleClose = () => {
    // Reset state quando si chiude
    setStage("form");
    setSelectedType("");
    setProjectId("");
    setProjectName("");
    setSite("");
    setCustomer("");
    setAuthor("");
    setOwnerTeam("");
    setCustomData("");
    setCompiledDoc("");
    setErrorMessage("");
    onClose();
  };

  const selectedTypeInfo = selectedType ? getITDocTypeInfo(selectedType as ITDocType) : null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
      aria-labelledby="it-compiler-title"
    >
      <div className="absolute inset-0 bg-black/70 backdrop-blur-sm" onClick={handleClose} />

      <div className="relative bg-[#0A0A0A] border border-[#1A1A1A] rounded-lg shadow-2xl w-full max-w-3xl max-h-[90vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-[#1A1A1A] bg-[#0F0F0F]">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-[#C5A059]" />
            <h2 id="it-compiler-title" className="text-sm font-semibold text-white">
              Compila Template IT con AI
            </h2>
          </div>
          <button
            onClick={handleClose}
            className="text-[#777] hover:text-white p-1 rounded transition-colors"
            aria-label="Chiudi"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6">
          {stage === "form" && (
            <div className="space-y-5">
              {/* Selezione tipo documento */}
              <div>
                <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-2">
                  Tipo documento
                </label>
                <div className="space-y-2">
                  {typesByPhase.map(([phase, types]) => (
                    <div key={phase}>
                      <div className="text-[10px] uppercase tracking-wider text-[#555] mb-1 mt-2">
                        Fase {phase}
                      </div>
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {types.map((t) => (
                          <button
                            key={t.type}
                            onClick={() => setSelectedType(t.type)}
                            className={`flex items-start gap-2 p-2 rounded border text-left transition-colors ${
                              selectedType === t.type
                                ? "border-[#C5A059] bg-[#C5A059]/10"
                                : "border-[#1A1A1A] bg-[#0F0F0F] hover:border-[#C5A059]/50"
                            }`}
                          >
                            <FileText
                              className={`w-4 h-4 mt-0.5 shrink-0 ${selectedType === t.type ? "text-[#C5A059]" : "text-[#555]"}`}
                            />
                            <div className="min-w-0">
                              <div className={`text-xs font-medium ${selectedType === t.type ? "text-[#C5A059]" : "text-[#DDD]"}`}>
                                {t.label}
                              </div>
                              <div className="text-[10px] text-[#777] truncate">{t.description}</div>
                            </div>
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Dati progetto */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Project ID *
                  </label>
                  <input
                    type="text"
                    value={projectId}
                    onChange={(e) => setProjectId(e.target.value)}
                    placeholder="es. acme-milano-2026"
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Nome progetto *
                  </label>
                  <input
                    type="text"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="es. Sostituzione Infrastruttura DC Milano"
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Sito
                  </label>
                  <input
                    type="text"
                    value={site}
                    onChange={(e) => setSite(e.target.value)}
                    placeholder="es. MIL-01"
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Cliente
                  </label>
                  <input
                    type="text"
                    value={customer}
                    onChange={(e) => setCustomer(e.target.value)}
                    placeholder="es. Acme S.p.A."
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Autore
                  </label>
                  <input
                    type="text"
                    value={author}
                    onChange={(e) => setAuthor(e.target.value)}
                    placeholder="Nome autore documento"
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
                <div>
                  <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                    Team responsabile
                  </label>
                  <input
                    type="text"
                    value={ownerTeam}
                    onChange={(e) => setOwnerTeam(e.target.value)}
                    placeholder="es. Acme Operations"
                    className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-sm text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none"
                  />
                </div>
              </div>

              {/* Dati custom */}
              <div>
                <label className="block text-xs uppercase tracking-wider text-[#C5A059] font-semibold mb-1">
                  Dati specifici (textarea libera)
                </label>
                <textarea
                  value={customData}
                  onChange={(e) => setCustomData(e.target.value)}
                  placeholder={`Incolla qui i dati specifici per il documento ${selectedTypeInfo?.label || ""}.\n\nEs. per LLD:\n- Subnet: 10.10.10.0/24 DMZ, ...\n- VLAN: 10 DMZ, 20 PROD, ...\n- Server: 3x Dell R750\n- Storage: NetApp FAS8700\n- ...`}
                  rows={8}
                  className="w-full bg-[#0F0F0F] border border-[#1A1A1A] rounded px-3 py-2 text-xs text-white placeholder-[#555] focus:border-[#C5A059] focus:outline-none font-mono"
                />
                <p className="text-[10px] text-[#777] mt-1">
                  Più dati strutturati fornisci, migliore sarà la compilazione. L'agente AI rispetta
                  le AI-INSTRUCTIONS del template e la coerenza con OKF v0.2.
                </p>
              </div>

              {/* Anteprima boilerplate */}
              {selectedType && (
                <details className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-3">
                  <summary className="text-xs text-[#C5A059] cursor-pointer flex items-center gap-1.5">
                    <ChevronRight className="w-3 h-3" />
                    Anteprima boilerplate YAML (template base)
                  </summary>
                  <pre className="mt-2 text-[10px] text-[#999] overflow-x-auto bg-[#0A0A0A] p-2 rounded">
                    {getITBoilerplate(selectedType as ITDocType)}
                  </pre>
                </details>
              )}
            </div>
          )}

          {stage === "compiling" && (
            <div className="flex flex-col items-center justify-center py-12">
              <Loader2 className="w-10 h-10 text-[#C5A059] animate-spin mb-4" />
              <p className="text-sm text-white mb-1">Compilazione in corso...</p>
              <p className="text-xs text-[#777]">
                Gemini 3.7 Flash sta generando il documento {selectedTypeInfo?.label}
              </p>
            </div>
          )}

          {stage === "success" && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-[#4ADE80]">
                <CheckCircle2 className="w-5 h-5" />
                <span className="text-sm font-medium">Documento compilato con successo</span>
              </div>
              <div className="bg-[#0F0F0F] border border-[#1A1A1A] rounded p-3">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs uppercase tracking-wider text-[#C5A059] font-semibold">
                    Documento OKF v0.2 generato
                  </span>
                  <div className="flex gap-1">
                    <button
                      onClick={handleCopy}
                      className="flex items-center gap-1 text-xs text-[#999] hover:text-[#C5A059] px-2 py-1 rounded hover:bg-[#1A1A1A] transition-colors"
                    >
                      <Copy className="w-3 h-3" />
                      {copied ? "Copiato!" : "Copia"}
                    </button>
                    <button
                      onClick={handleDownload}
                      className="flex items-center gap-1 text-xs text-[#999] hover:text-[#C5A059] px-2 py-1 rounded hover:bg-[#1A1A1A] transition-colors"
                    >
                      <Download className="w-3 h-3" />
                      Download
                    </button>
                  </div>
                </div>
                <pre className="text-[10px] text-[#DDD] overflow-auto max-h-96 bg-[#0A0A0A] p-3 rounded border border-[#1A1A1A]">
                  {compiledDoc}
                </pre>
              </div>
              <p className="text-[10px] text-[#777]">
                Il documento è pronto per essere caricato nel vault tramite CaptureBar (incolla il testo)
                o salvato su file e importato in seguito.
              </p>
            </div>
          )}

          {stage === "error" && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-[#F87171]">
                <AlertCircle className="w-5 h-5" />
                <span className="text-sm font-medium">Errore compilazione</span>
              </div>
              <div className="bg-[rgba(248,113,113,0.05)] border border-[rgba(248,113,113,0.3)] rounded p-3">
                <p className="text-xs text-[#F87171] font-mono">{errorMessage}</p>
              </div>
              <button
                onClick={() => setStage("form")}
                className="text-xs text-[#C5A059] hover:underline"
              >
                ← Torna al form
              </button>
            </div>
          )}
        </div>

        {/* Footer con azioni */}
        {stage === "form" && (
          <div className="flex items-center justify-between gap-2 px-4 py-3 border-t border-[#1A1A1A] bg-[#0F0F0F]">
            <p className="text-[10px] text-[#777]">
              {canCompile ? "Pronto per la compilazione" : "Compila i campi obbligatori (*)"}
            </p>
            <div className="flex gap-2">
              <button
                onClick={handleClose}
                className="text-xs text-[#999] hover:text-white px-3 py-1.5 rounded transition-colors"
              >
                Annulla
              </button>
              <button
                onClick={handleCompile}
                disabled={!canCompile}
                className="flex items-center gap-1.5 text-xs font-medium bg-[#C5A059] text-[#0A0A0A] px-4 py-1.5 rounded hover:bg-[#D9B870] transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
              >
                <Sparkles className="w-3.5 h-3.5" />
                Compila con AI
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ITTemplateCompilerModal;
