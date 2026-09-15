---
okf_version: "0.2"
id: "patch-okf-parser-it-types"
title: "Patch 01 — Estensione di src/lib/okfParser.ts per tipi documentali IT"
type: "specification"
domain: "Knowledge Architecture & Parser Extensions"
tags: ["okf-v0.2", "patch", "parser", "it-infrastructure", "level-2"]
entities:
  - name: "OKF Parser Extension"
    type: "specification"
    description: "Estensione del parser OKF v0.2 per riconoscere 9 tipi documentali IT come alias canonici"
  - name: "IT Document Type Alias"
    type: "concept"
    description: "Mapping 9 tipi IT (rsd_urs, hld, lld, mop, rollback, as_built, atp, sop_runbook, handover_inventory) ai 6 tipi canonici OKF"
relations:
  - targetTitle: "Patch 02 — types.ts extension"
    targetId: "patch-okf-types-it-types"
    relationType: "depends_on"
    weight: 1.0
    description: "okfParser.ts dipende dai nuovi tipi ITProjectMetadata e ITDocType definiti in types.ts"
---

# Patch 01 — Estensione di `src/lib/okfParser.ts`

## File target
`src/lib/okfParser.ts`

## Strategia

Estendere il parser esistente **senza rompere la backward compatibility**:
1. Aggiungere 9 alias IT dei tipi canonici OKF
2. Aggiungere `IT_DOC_TYPE_ALIASES` map e `canonicalItTypeToOkf()` helper
3. Estendere `sanitizeDocType()` per riconoscere gli alias IT (preservando `originalDocType`)
4. Estendere `parseOKFDocument()` per estrarre i metadati IT estesi nel nuovo campo `itMetadata`
5. Aggiungere `OKF_IT_TEMPLATES` map importata da `./okfItTemplates`

---

## Modifica 1 — Aggiungere IT_DOC_TYPE_ALIASES in cima al file

### Posizione
Dopo `export const CANONICAL_OKF_TYPES` (riga ~10), prima di `export type CanonicalOKFType`.

### Codice da aggiungere

```typescript
// ============================================================================
// IT INFRASTRUCTURE DOCUMENT TYPES — Livello 2 extension
// 9 alias tipizzati che mappano ai 6 tipi canonici OKF v0.2.
// Questi alias preservano la semantica IT senza rompere la validità OKF.
// ============================================================================

export const IT_DOC_TYPE_ALIASES = {
  rsd_urs:           "specification",  // Requirements Specification Document
  hld:               "architecture",   // High-Level Design
  lld:               "architecture",   // Low-Level Design
  mop:               "guide",          // Method of Procedure
  rollback:          "guide",          // Rollback / Fallback Plan
  as_built:          "architecture",   // As-Built Documentation
  atp:               "specification",  // Acceptance Test Plan
  sop_runbook:       "guide",          // Standard Operating Procedures
  handover_inventory:"specification",  // Handover & Asset Inventory
} as const;

export type ITDocTypeAlias = keyof typeof IT_DOC_TYPE_ALIASES;

/**
 * Verifica se un tipo è un alias IT riconosciuto (case-insensitive, normalizzato).
 */
export function isITDocType(rawType: string): rawType is ITDocTypeAlias {
  const normalized = (rawType || "").trim().toLowerCase().replace(/[\s-]+/g, "_");
  return normalized in IT_DOC_TYPE_ALIASES;
}

/**
 * Mappa un alias IT al tipo canonico OKF corrispondente.
 * Restituisce undefined se l'input non è un alias IT.
 */
export function canonicalItTypeToOkf(rawType: string): CanonicalOKFType | undefined {
  if (!isITDocType(rawType)) return undefined;
  const normalized = (rawType as string).trim().toLowerCase().replace(/[\s-]+/g, "_") as ITDocTypeAlias;
  return IT_DOC_TYPE_ALIASES[normalized];
}
```

---

## Modifica 2 — Estendere `sanitizeDocType()` per riconoscere gli alias IT

### Posizione
Sostituire l'intera funzione `sanitizeDocType` (righe ~18-106).

### Vecchio codice (parziale, riga ~99-106)

```typescript
  // Default di sicurezza
  return {
    sanitized: "concept",
    wasRepaired: true,
    originalType: original,
    repairReason: `Re-indirizzato tipo sconosciuto '${original}' verso 'concept'`,
  };
}
```

### Nuovo codice (sostituisce l'intera funzione)

```typescript
export function sanitizeDocType(rawType: string): {
  sanitized: CanonicalOKFType;
  wasRepaired: boolean;
  originalType: string;
  repairReason?: string;
  isITAlias?: boolean;
} {
  const original = (rawType || "").trim();
  const normalized = original.toLowerCase().replace(/[\s-]+/g, "_");

  // 1. Tipo canonico OKF nativo (no repair)
  if (CANONICAL_OKF_TYPES.includes(normalized as CanonicalOKFType)) {
    return { sanitized: normalized as CanonicalOKFType, wasRepaired: false, originalType: original };
  }

  // 2. Alias IT riconosciuto (sanitizzazione SEMANTICA, preserva originalDocType)
  if (isITDocType(original)) {
    const canonical = canonicalItTypeToOkf(original)!;
    return {
      sanitized: canonical,
      wasRepaired: false,           // NON repaired: è un alias riconosciuto
      originalType: original,
      isITAlias: true,
    };
  }

  // 3. Heuristic fallback esistenti (invariati)
  if (normalized.includes("arch") || normalized.includes("infra") || normalized.includes("system") || normalized.includes("topology")) {
    return {
      sanitized: "architecture",
      wasRepaired: true,
      originalType: original,
      repairReason: `Re-indirizzato tipo non-standard '${original}' verso 'architecture'`,
    };
  }
  if (
    normalized.includes("guide") ||
    normalized.includes("tuto") ||
    normalized.includes("how") ||
    normalized.includes("walkthrough") ||
    normalized.includes("manual") ||
    normalized.includes("runbook")
  ) {
    return {
      sanitized: "guide",
      wasRepaired: true,
      originalType: original,
      repairReason: `Re-indirizzato tipo non-standard '${original}' verso 'guide'`,
    };
  }
  if (
    normalized.includes("spec") ||
    normalized.includes("rfc") ||
    normalized.includes("standard") ||
    normalized.includes("protocol") ||
    normalized.includes("contract")
  ) {
    return {
      sanitized: "specification",
      wasRepaired: true,
      originalType: original,
      repairReason: `Re-indirizzato tipo non-standard '${original}' verso 'specification'`,
    };
  }
  if (
    normalized.includes("tool") ||
    normalized.includes("mcp") ||
    normalized.includes("cli") ||
    normalized.includes("util") ||
    normalized.includes("script") ||
    normalized.includes("extension")
  ) {
    return {
      sanitized: "tool_description",
      wasRepaired: true,
      originalType: original,
      repairReason: `Re-indirizzato tipo non-standard '${original}' verso 'tool_description'`,
    };
  }
  if (
    normalized.includes("prompt") ||
    normalized.includes("skill") ||
    normalized.includes("agent") ||
    normalized.includes("instruction") ||
    normalized.includes("persona")
  ) {
    return {
      sanitized: "prompt_skill",
      wasRepaired: true,
      originalType: original,
      repairReason: `Re-indirizzato tipo non-standard '${original}' verso 'prompt_skill'`,
    };
  }

  // 4. Default di sicurezza
  return {
    sanitized: "concept",
    wasRepaired: true,
    originalType: original,
    repairReason: `Re-indirizzato tipo sconosciuto '${original}' verso 'concept'`,
  };
}
```

---

## Modifica 3 — Estendere `ParsedOKFDocument` con `itMetadata`

### Posizione
Modificare l'interfaccia `ParsedOKFDocument` (righe ~108-123).

### Vecchio codice

```typescript
export interface ParsedOKFDocument {
  isValidOKF: boolean;
  okfVersion?: string;
  title: string;
  docType: string;
  domain: string;
  tags: string[];
  entities: OKFEntity[];
  relations: OKFRelation[];
  bodyMarkdown: string;
  rawFrontmatter?: string;
  hasFrontmatter: boolean;
  wasAutoRepaired?: boolean;
  originalDocType?: string;
  autoRepairReason?: string;
}
```

### Nuovo codice

```typescript
export interface ParsedOKFDocument {
  isValidOKF: boolean;
  okfVersion?: string;
  title: string;
  docType: string;                   // Canonico OKF (sempre uno dei 6)
  domain: string;
  tags: string[];
  entities: OKFEntity[];
  relations: OKFRelation[];
  bodyMarkdown: string;
  rawFrontmatter?: string;
  hasFrontmatter: boolean;
  wasAutoRepaired?: boolean;
  originalDocType?: string;          // Popolato se type era alias IT o è stato repaired
  autoRepairReason?: string;
  isITAlias?: boolean;               // true se docType era un alias IT riconosciuto
  itMetadata?: ITProjectMetadata;    // Nuovo: metadati IT estesi estratti dal frontmatter
}
```

Aggiungere anche l'import in cima al file:

```typescript
import { ITProjectMetadata } from "../types";
```

---

## Modifica 4 — Estrarre `itMetadata` in `parseOKFDocument()`

### Posizione
All'interno di `parseOKFDocument`, nel loop che parsifica le chiavi top-level (riga ~202), aggiungere il riconoscimento dei campi IT estesi.

### Vecchio codice (riga ~202-217)

```typescript
    // Top-level scalar keys
    if (!line.startsWith(" ") && !line.startsWith("\t") && trimmed.includes(":")) {
      currentSection = "none";
      const [rawKey, ...valParts] = trimmed.split(":");
      const key = rawKey.trim();
      const val = valParts.join(":").trim().replace(/^["']|["']$/g, "");

      if (key === "okf_version" || key === "okfVersion") {
        okfVersion = val;
      } else if (key === "title") {
        title = val || title;
      } else if (key === "type" || key === "docType") {
        docType = val || docType;
      } else if (key === "domain") {
        domain = val || domain;
      }
      continue;
    }
```

### Nuovo codice

```typescript
    // Top-level scalar keys
    if (!line.startsWith(" ") && !line.startsWith("\t") && trimmed.includes(":")) {
      currentSection = "none";
      const [rawKey, ...valParts] = trimmed.split(":");
      const key = rawKey.trim();
      const val = valParts.join(":").trim().replace(/^["']|["']$/g, "");

      if (key === "okf_version" || key === "okfVersion") {
        okfVersion = val;
      } else if (key === "title") {
        title = val || title;
      } else if (key === "type" || key === "docType") {
        docType = val || docType;
      } else if (key === "domain") {
        domain = val || domain;
      }
      // === IT Metadata extraction (Livello 2) ===
      else if (key === "project_id") {
        itMeta.project_id = val;
      } else if (key === "project_name") {
        itMeta.project_name = val;
      } else if (key === "site") {
        itMeta.site = val;
      } else if (key === "customer") {
        itMeta.customer = val;
      } else if (key === "phase") {
        const phaseNum = parseInt(val, 10);
        if (!isNaN(phaseNum) && phaseNum >= 1 && phaseNum <= 7) {
          itMeta.phase = phaseNum as 1|2|3|4|5|6|7;
        }
      } else if (key === "author") {
        itMeta.author = val;
      } else if (key === "reviewer") {
        itMeta.reviewer = val;
      } else if (key === "approver") {
        itMeta.approver = val;
      } else if (key === "owner_team") {
        itMeta.owner_team = val;
      } else if (key === "status") {
        itMeta.status = val as any;
      } else if (key === "version" || key === "docVersion") {
        itMeta.version = val;
      } else if (key === "created_at") {
        itMeta.created_at = val;
      } else if (key === "updated_at") {
        itMeta.updated_at = val;
      } else if (key === "classification") {
        itMeta.classification = val;
      } else if (key === "retention") {
        itMeta.retention = val;
      } else if (key === "lang") {
        itMeta.lang = val;
      } else if (key === "supersedes") {
        itMeta.supersedes = val || null;
      } else if (key === "superseded_by") {
        itMeta.superseded_by = val || null;
      }
      continue;
    }
```

E aggiungere l'inizializzazione di `itMeta` prima del loop:

```typescript
  const itMeta: ITProjectMetadata = {
    related_docs: [],
    depends_on: [],
  };

  let currentRelatedDocs = false;
  let currentDependsOn = false;
```

E nel riconoscimento delle section headers (riga ~191), aggiungere:

```typescript
    if (trimmed.startsWith("related_docs:")) {
      currentSection = "related_docs";
      currentRelatedDocs = true;
      continue;
    }

    if (trimmed.startsWith("depends_on:")) {
      currentSection = "depends_on";
      currentDependsOn = true;
      continue;
    }
```

E nel blocco che gestisce gli array items (riga ~221), aggiungere:

```typescript
    if (currentSection === "related_docs" && trimmed.startsWith("-")) {
      const docId = trimmed.replace(/^-\s*/, "").replace(/^["']|["']$/g, "").trim();
      if (docId) itMeta.related_docs!.push(docId);
      continue;
    }

    if (currentSection === "depends_on" && trimmed.startsWith("-")) {
      const depId = trimmed.replace(/^-\s*/, "").replace(/^["']|["']$/g, "").trim();
      if (depId) itMeta.depends_on!.push(depId);
      continue;
    }
```

### Posizione
Alla fine della funzione, prima del `return`, aggiungere il merge:

```typescript
  // === IT Metadata finalizzazione (Livello 2) ===
  const finalItMeta: ITProjectMetadata | undefined =
    itMeta.project_id || itMeta.project_name || itMeta.phase || itMeta.author
      ? itMeta
      : undefined;

  const { sanitized: finalDocType, wasRepaired: wasAutoRepaired, originalType: originalDocType, repairReason: autoRepairReason, isITAlias } = sanitizeDocType(docType);

  const isValidOKF = Boolean(
    okfVersion &&
    okfVersion.includes("0.2") &&
    title &&
    CANONICAL_OKF_TYPES.includes(finalDocType)
  );

  return {
    isValidOKF,
    okfVersion: okfVersion || "0.2",
    title,
    docType: finalDocType,
    domain,
    tags: tags.length > 0 ? Array.from(new Set(tags)) : ["knowledge", "okf-v0.2"],
    entities,
    relations,
    bodyMarkdown,
    rawFrontmatter: rawYaml,
    hasFrontmatter: true,
    wasAutoRepaired,
    originalDocType: wasAutoRepaired || isITAlias ? originalDocType : undefined,
    autoRepairReason,
    isITAlias,
    itMetadata: finalItMeta,
  };
}
```

---

## Modifica 5 — Aggiungere import di `OKF_IT_TEMPLATES`

### Posizione
In fondo al file, dopo `OKF_TEMPLATES` e prima di `VALID_OKF_DOC_TYPES`.

### Codice da aggiungere

```typescript
// ============================================================================
// IT INFRASTRUCTURE BOILERPLATE TEMPLATES (Livello 2)
// 9 boilerplate predefiniti per authoring immediato di documenti IT.
// Importati da file separato per separazione delle responsabilità.
// ============================================================================

export { OKF_IT_TEMPLATES, IT_DOC_TYPES } from "./okfItTemplates";
```

---

## Verifica post-modifica

Dopo aver applicato tutte le modifiche, il parser deve:

1. ✅ Continuare a riconoscere documenti OKF v0.2 esistenti (backward compat)
2. ✅ Riconoscere `type: "rsd_urs"` come alias IT → `docType: "specification"`, `originalDocType: "rsd_urs"`, `isITAlias: true`
3. ✅ Estrarre `project_id`, `phase`, `related_docs`, `depends_on` in `itMetadata`
4. ✅ Validare come OKF valido anche i documenti con alias IT
5. ✅ Passare i test esistenti senza modifiche

## Esempio di output atteso

Per un documento con frontmatter:
```yaml
---
okf_version: "0.2"
id: "architecture-acme-milano-lld-01"
title: "LLD — DC Milano"
type: "lld"
domain: "IT Infrastructure"
tags: ["okf-v0.2", "lld"]
project_id: "acme-milano-2026"
phase: 2
related_docs:
  - "architecture-acme-milano-hld-01"
entities:
  - name: "Cisco Nexus 9300"
    type: "technology"
    description: "Switch core L3"
---
```

Il `parseOKFDocument` deve restituire:

```typescript
{
  isValidOKF: true,
  okfVersion: "0.2",
  title: "LLD — DC Milano",
  docType: "architecture",           // ← canonico OKF
  originalDocType: "lld",            // ← preservato (nuovo!)
  isITAlias: true,                   // ← nuovo!
  domain: "IT Infrastructure",
  tags: ["okf-v0.2", "lld"],
  entities: [{ name: "Cisco Nexus 9300", type: "technology", description: "..." }],
  relations: [],
  itMetadata: {                     // ← nuovo!
    project_id: "acme-milano-2026",
    phase: 2,
    related_docs: ["architecture-acme-milano-hld-01"],
    depends_on: [],
  },
  // ... altri campi
}
```
