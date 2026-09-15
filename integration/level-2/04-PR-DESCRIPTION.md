# PR — Estensione parser OKF v0.2 con tipi documentali IT (Livello 2)

## Titolo

`feat(parser): riconoscimento 9 tipi documentali IT come alias canonici OKF v0.2`

## Descrizione

Questa PR estende il parser OKF v0.2 per riconoscere esplicitamente i 9 tipi documentali del ciclo lavorativo IT (RSD/URS, HLD, LLD, MOP, Rollback, As-Built, ATP, SOP/Runbook, Handover & Inventory) senza rompere la backward compatibility con i documenti OKF esistenti.

## Cosa cambia

### Estensioni additive (no breaking changes)

1. **`src/lib/okfParser.ts`** — Aggiunto `IT_DOC_TYPE_ALIASES` map + helper `isITDocType()` / `canonicalItTypeToOkf()`. Estesa `sanitizeDocType()` per riconoscere i 9 alias IT preservando `originalDocType` e flag `isITAlias`. Esteso `ParsedOKFDocument` con campo opzionale `itMetadata`. Il parser estrae ora i metadati IT estesi (`project_id`, `phase`, `related_docs`, `depends_on`, ecc.) dal frontmatter.

2. **`src/types.ts`** — Aggiunti nuovi tipi: `ITDocType` (union di 9 valori), `ITProjectPhase` (1-7), `ITDocStatus`, `ITDocClassification`, `ITProjectMetadata` (interfaccia completa). Estesa `ResourceMetadata` con campi opzionali `itMetadata` e `isITAlias`.

3. **`src/lib/okfItTemplates.ts`** (NUOVO file) — Esporta `IT_DOC_TYPES` (map metadata), `OKF_IT_TEMPLATES` (9 boilerplate YAML minimi), `IT_DOC_TYPE_LIST` (per UI), `getITBoilerplate()`, `getITDocTypeInfo()`.

## Strategia di integrazione

Per evitare di rompere la backward compatibility:

| Aspetto | Prima | Dopo |
|---------|-------|------|
| `type: "lld"` | Sanitizzato a `"architecture"` con `wasRepaired: true` (perdita semantica) | Riconosciuto come alias IT → `docType: "architecture"`, `originalDocType: "lld"`, `isITAlias: true` |
| Metadati IT estesi | Persi nel `rawFrontmatter` opaco | Estratti in `parsedDocument.itMetadata` tipizzato |
| Boilerplate | Solo 6 `OKF_TEMPLATES` canonici | + 9 `OKF_IT_TEMPLATES` specifici per IT |

## Mappatura tipi IT → tipi canonici OKF

| Tipo IT | Tipo canonico OKF | Fase |
|---------|-------------------|------|
| `rsd_urs` | `specification` | 1 |
| `hld` | `architecture` | 2 |
| `lld` | `architecture` | 2 |
| `mop` | `guide` | 3 |
| `rollback` | `guide` | 3 |
| `as_built` | `architecture` | 5-7 |
| `atp` | `specification` | 6 |
| `sop_runbook` | `guide` | 7 |
| `handover_inventory` | `specification` | 7 |

## Test di regressione

### Pre-condizioni
- [ ] I documenti OKF v0.2 esistenti nel vault continuano a passare la validazione `validateOKFDocumentSchema()`
- [ ] I 6 tipi canonici OKF (`concept`, `architecture`, `guide`, `specification`, `tool_description`, `prompt_skill`) restano validi invariat

### Nuovi test da aggiungere

```typescript
// test/okfParser.itTypes.test.ts (nuovo file)

import { parseOKFDocument, isITDocType, canonicalItTypeToOkf } from "../src/lib/okfParser";

describe("IT Doc Type Aliases", () => {
  test("isITDocType riconosce i 9 alias", () => {
    expect(isITDocType("rsd_urs")).toBe(true);
    expect(isITDocType("lld")).toBe(true);
    expect(isITDocType("sop_runbook")).toBe(true);
    expect(isITDocType("handover_inventory")).toBe(true);
  });

  test("isITDocType case-insensitive e normalizzato", () => {
    expect(isITDocType("RSD-URS")).toBe(true);
    expect(isITDocType("SOP Runbook")).toBe(true);
    expect(isITDocType("Handover-Inventory")).toBe(true);
  });

  test("canonicalItTypeToOkf mappa correttamente", () => {
    expect(canonicalItTypeToOkf("lld")).toBe("architecture");
    expect(canonicalItTypeToOkf("mop")).toBe("guide");
    expect(canonicalItTypeToOkf("atp")).toBe("specification");
  });

  test("Documenti IT alias sono validi OKF", () => {
    const doc = `---
okf_version: "0.2"
title: "Test LLD"
type: "lld"
domain: "IT Infrastructure"
tags: ["okf-v0.2", "lld"]
project_id: "test-proj"
phase: 2
related_docs:
  - "architecture-test-hld-01"
entities:
  - name: "Test Entity"
    type: "technology"
    description: "test"
---
# Body
Test content with sufficient length.`;

    const parsed = parseOKFDocument(doc);
    expect(parsed.isValidOKF).toBe(true);
    expect(parsed.docType).toBe("architecture");
    expect(parsed.originalDocType).toBe("lld");
    expect(parsed.isITAlias).toBe(true);
    expect(parsed.itMetadata).toBeDefined();
    expect(parsed.itMetadata?.project_id).toBe("test-proj");
    expect(parsed.itMetadata?.phase).toBe(2);
    expect(parsed.itMetadata?.related_docs).toEqual(["architecture-test-hld-01"]);
  });

  test("Documenti OKF canonici esistenti non sono influenzati", () => {
    const doc = `---
okf_version: "0.2"
title: "Test Architecture"
type: "architecture"
domain: "Systems"
tags: ["okf-v0.2", "test"]
entities:
  - name: "X"
    type: "concept"
    description: "y"
---
# Body`;

    const parsed = parseOKFDocument(doc);
    expect(parsed.isValidOKF).toBe(true);
    expect(parsed.docType).toBe("architecture");
    expect(parsed.isITAlias).toBeUndefined();
    expect(parsed.originalDocType).toBe("architecture");
    expect(parsed.itMetadata).toBeUndefined();
  });
});
```

## Esempio di output atteso

### Documento input
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

### Output `parseOKFDocument`
```typescript
{
  isValidOKF: true,
  okfVersion: "0.2",
  title: "LLD — DC Milano",
  docType: "architecture",           // ← canonico OKF (per D3)
  originalDocType: "lld",            // ← preservato (nuovo!)
  isITAlias: true,                   // ← nuovo!
  domain: "IT Infrastructure",
  tags: ["okf-v0.2", "lld"],
  entities: [{ name: "Cisco Nexus 9300", ... }],
  relations: [],
  itMetadata: {                     // ← nuovo!
    project_id: "acme-milano-2026",
    phase: 2,
    related_docs: ["architecture-acme-milano-hld-01"],
    depends_on: [],
  },
  // ... altri campi invariati
}
```

## Limiti noti (fuori scope di questa PR)

1. **KnowledgeGraph.tsx**: il grafo D3 continua a visualizzare i 6 colori dei tipi canonici. I 9 tipi IT non avranno colore distinto. (Candidato per Livello 3.)

2. **KnowledgeReader.tsx**: la scheda "Grafo & Relazioni" non mostra ancora i metadati IT estesi (project_id, phase, related_docs). Serve un nuovo componente `ITProjectMetadataCard.tsx`. (Candidato per Livello 3.)

3. **okfSerializer.ts**: la serializzazione (output) continua a usare solo i 6 tipi canonici. L'authoring automatico di documenti IT tipizzati richiede l'uso manuale dei boilerplate `OKF_IT_TEMPLATES`.

## Checklist

- [ ] Codice compilato senza errori TypeScript (`npm run lint`)
- [ ] Test esistenti passano (`npm run test:cekikj`)
- [ ] Nuovi test per alias IT aggiunti e passano
- [ ] Backward compatibility verificata su un sample di documenti OKF esistenti
- [ ] `OKF_IT_TEMPLATES` esporta tutti i 9 boilerplate con frontmatter valido
- [ ] `IT_DOC_TYPE_LIST` ha 9 entry ordinate per fase
- [ ] Helper `getITBoilerplate()` e `getITDocTypeInfo()` funzionano
- [ ] Documentazione aggiornata: `docs/OKF_v0.2_SPECIFICATION.md` con sezione "IT Aliases"
- [ ] `AGENTS.md` del Knowledge Vault menziona i 9 tipi IT

## File modificati

```
src/lib/okfParser.ts        | +120 righe (IT_DOC_TYPE_ALIASES, helpers, sanitizeDocType estesa, itMetadata extraction)
src/types.ts                | +85 righe  (ITDocType, ITProjectPhase, ITDocStatus, ITDocClassification, ITProjectMetadata, ResourceMetadata esteso)
src/lib/okfItTemplates.ts   | +250 righe (NUOVO file)
```

## File NON modificati (per design)

- `src/lib/okfSerializer.ts` — serializzazione resta solo canonica OKF
- `src/components/KnowledgeGraph.tsx` — grafo D3 invariato
- `src/components/KnowledgeReader.tsx` — reader invariato
- `src/components/CaptureBar.tsx` — capture UI invariata
- `server/routes/captureRoutes.ts` — API invariata
- `firestore.rules` — regole DB invariate

## Refman

- Spec OKF v0.2: `docs/OKF_v0.2_SPECIFICATION.md`
- Architettura: `docs/SYSTEM_ARCHITECTURE_OKF.md`
- Pipeline ingestione: `docs/INGESTION_PIPELINE_SPEC.md`
- Template IT esterni: https://github.com/matrixNeo76/KnowledgeVault/tree/main (cartella `/download/templates/`)
