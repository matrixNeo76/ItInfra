---
okf_version: "0.2"
id: "patch-okf-types-it-types"
title: "Patch 02 — Estensione di src/types.ts con tipi IT"
type: "specification"
domain: "Knowledge Architecture & TypeScript Types"
tags: ["okf-v0.2", "patch", "types", "it-infrastructure", "level-2"]
entities:
  - name: "ITProjectMetadata"
    type: "specification"
    description: "Interfaccia TypeScript per metadati IT estesi estratti dal frontmatter OKF"
  - name: "ITDocType"
    type: "specification"
    description: "Union type dei 9 tipi documentali IT canonici"
relations:
  - targetTitle: "Patch 01 — okfParser.ts extension"
    targetId: "patch-okf-parser-it-types"
    relationType: "extends"
    weight: 1.0
    description: "okfParser.ts consuma i nuovi tipi definiti qui"
  - targetTitle: "Patch 03 — okfItTemplates.ts (new file)"
    targetId: "patch-okf-it-templates"
    relationType: "references"
    weight: 0.9
    description: "okfItTemplates.ts usa ITDocType per tipizzare i boilerplate"
---

# Patch 02 — Estensione di `src/types.ts`

## File target
`src/types.ts`

## Strategia

Aggiungere nuove interfacce TypeScript per i tipi IT estesi, **senza modificare** i tipi esistenti (`OKFEntity`, `OKFRelation`, `ResourceMetadata`, `ResourceItem`). I nuovi tipi sono **additivi** e opzionali.

---

## Modifica 1 — Aggiungere `ITDocType` union type

### Posizione
Dopo `export interface OKFRelation` (riga ~19), prima di `export type TagCategory`.

### Codice da aggiungere

```typescript
// ============================================================================
// IT INFRASTRUCTURE DOCUMENT TYPES (Livello 2 extension)
// ============================================================================

/**
 * 9 tipi documentali IT canonici del ciclo lavorativo.
 * Mappano ai 6 tipi canonici OKF v0.2 tramite IT_DOC_TYPE_ALIASES (vedi okfParser.ts).
 */
export type ITDocType =
  | "rsd_urs"             // Requirements Specification Document (Fase 1)
  | "hld"                 // High-Level Design (Fase 2)
  | "lld"                 // Low-Level Design (Fase 2)
  | "mop"                 // Method of Procedure (Fase 3)
  | "rollback"            // Rollback / Fallback Plan (Fase 3)
  | "as_built"            // As-Built Documentation (Fase 5-7)
  | "atp"                 // Acceptance Test Plan (Fase 6)
  | "sop_runbook"         // Standard Operating Procedures (Fase 7)
  | "handover_inventory"; // Handover & Asset Inventory (Fase 7)

/**
 * Fasi del ciclo lavorativo IT (1-7).
 */
export type ITProjectPhase = 1 | 2 | 3 | 4 | 5 | 6 | 7;

/**
 * Stati del documento nel ciclo di vita.
 */
export type ITDocStatus =
  | "draft"
  | "in-review"
  | "approved"
  | "superseded";

/**
 * Livello di classificazione del documento.
 */
export type ITDocClassification =
  | "public"
  | "internal"
  | "confidential"
  | "restricted";
```

---

## Modifica 2 — Aggiungere `ITProjectMetadata` interface

### Posizione
Subito dopo il blocco `ITDocType` aggiunto sopra.

### Codice da aggiungere

```typescript
/**
 * Metadati IT estesi estratti dal frontmatter OKF v0.2.
 *
 * Questi campi NON sono canonici OKF v0.2, ma vengono preservati
 * nel `rawFrontmatter` del parser e resi disponibili come tipizzazione
 * strutturata per documenti del ciclo lavorativo IT.
 *
 * Sono OPZIONALI: un documento OKF può avere solo alcuni di questi campi,
 * oppure nessuno (se è un documento generico non IT).
 */
export interface ITProjectMetadata {
  // === Identità estesa ===
  status?: ITDocStatus;
  version?: string;
  created_at?: string;        // ISO 8601 (YYYY-MM-DD)
  updated_at?: string;        // ISO 8601 (YYYY-MM-DD)

  // === Progetto ===
  project_id?: string;        // es. "acme-milano-2026"
  project_name?: string;
  site?: string;              // SITE_CODE es. "MIL-01"
  customer?: string;
  phase?: ITProjectPhase;     // 1-7

  // === Persone ===
  author?: string;
  reviewer?: string;
  approver?: string;
  owner_team?: string;

  // === Relazioni estese (complementari a `relations` canonico OKF) ===
  /**
   * Array di ID (non titoli) dei documenti correlati nel ciclo lavorativo.
   * Per ogni ID qui presente, dovrebbe esistere una corrispondente entry
   * in `relations` (canonico OKF) con `targetId` uguale.
   */
  related_docs?: string[];

  /**
   * Array di ID dei documenti che sono prerequisito (input) per questo.
   * Subset di `related_docs` con semantica "dipende da".
   */
  depends_on?: string[];

  // === Versioning ===
  supersedes?: string | null;     // ID del documento sostituito da questo
  superseded_by?: string | null;  // ID del documento che sostituisce questo

  // === Governance ===
  classification?: ITDocClassification;
  retention?: string;              // es. "7y", "10y", "indefinite"
  lang?: string;                   // es. "it", "en"
}
```

---

## Modifica 3 — Estendere `ResourceMetadata` con `itMetadata` (opzionale)

### Posizione
In fondo all'interfaccia `ResourceMetadata` (riga ~170), dopo `markdownContent?: string;`.

### Codice da aggiungere

```typescript
  // === IT Infrastructure Metadata (Livello 2) ===
  /**
   * Metadati IT estesi estratti dal frontmatter OKF v0.2.
   * Presente solo se il documento è stato riconosciuto come parte del
   * ciclo lavorativo IT (alias type o metadati IT nel frontmatter).
   */
  itMetadata?: ITProjectMetadata;

  /**
   * True se il documento usa un alias IT come `type` (es. "lld" invece di "architecture").
   * Preserva la semantica IT pur mantenendo la validità OKF v0.2.
   */
  isITAlias?: boolean;
```

---

## Verifica post-modifica

Dopo aver applicato le modifiche, il `npm run lint` deve passare senza errori.

I nuovi tipi sono utilizzabili in tutto il codebase:

```typescript
import { ITProjectMetadata, ITDocType, ITProjectPhase } from "./types";

const meta: ITProjectMetadata = {
  project_id: "acme-milano-2026",
  phase: 2,
  status: "draft",
  related_docs: ["architecture-acme-milano-hld-01"],
};

const docType: ITDocType = "lld";
const phase: ITProjectPhase = 3;
```

## Backward compatibility

Tutti i tipi esistenti restano invariati. Le modifiche sono **additive**:
- ✅ `OKFEntity`, `OKFRelation` invariati
- ✅ `ResourceMetadata` esteso con 2 campi OPZIONALI (`itMetadata`, `isITAlias`)
- ✅ `ResourceItem` invariato
- ✅ Nuovi tipi `ITDocType`, `ITProjectPhase`, `ITDocStatus`, `ITDocClassification`, `ITProjectMetadata` — tutti nuovi, non sostituiscono nulla
