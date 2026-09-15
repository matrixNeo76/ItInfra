# Guida alla Migrazione — Livello 2

Questa guida ti accompagna passo-passo nell'applicazione delle patch del Livello 2 al tuo repo `KnowledgeVault` clonato localmente.

## Prerequisiti

- Repo clonato: `git clone https://github.com/matrixNeo76/KnowledgeVault.git`
- Node.js 22 LTS + bun installati
- Working directory pulita: `git status` non deve mostrare modifiche non committate
- Branch attivo: `git checkout -b feature/it-infrastructure-types`

## Step 1 — Backup preventivo

```bash
cd /path/to/KnowledgeVault

# Crea un branch di backup
git branch backup/pre-it-types

# Verifica di essere su un branch di lavoro pulito
git status
git log --oneline -3
```

## Step 2 — Applicare la patch a `src/types.ts`

### Opzione A — Applicazione manuale

Apri `src/types.ts` e applica le modifiche descritte in `02-PATCH-types.ts.md`:

1. Dopo l'interfaccia `OKFRelation` (riga ~19), aggiungi i nuovi tipi:
   - `ITDocType` (union di 9 valori stringa)
   - `ITProjectPhase` (1-7)
   - `ITDocStatus` (draft, in-review, approved, superseded)
   - `ITDocClassification` (public, internal, confidential, restricted)
   - `ITProjectMetadata` (interfaccia completa)

2. In fondo all'interfaccia `ResourceMetadata`, dopo `markdownContent?: string;`, aggiungi:
   - `itMetadata?: ITProjectMetadata;`
   - `isITAlias?: boolean;`

### Opzione B — Via sed (rapido)

```bash
# Aggiungi i nuovi tipi dopo OKFRelation
cat >> /tmp/it-types-snippet.ts << 'EOF'

// ============================================================================
// IT INFRASTRUCTURE DOCUMENT TYPES (Livello 2 extension)
// ============================================================================

export type ITDocType =
  | "rsd_urs"
  | "hld"
  | "lld"
  | "mop"
  | "rollback"
  | "as_built"
  | "atp"
  | "sop_runbook"
  | "handover_inventory";

export type ITProjectPhase = 1 | 2 | 3 | 4 | 5 | 6 | 7;

export type ITDocStatus = "draft" | "in-review" | "approved" | "superseded";

export type ITDocClassification = "public" | "internal" | "confidential" | "restricted";

export interface ITProjectMetadata {
  status?: ITDocStatus;
  version?: string;
  created_at?: string;
  updated_at?: string;
  project_id?: string;
  project_name?: string;
  site?: string;
  customer?: string;
  phase?: ITProjectPhase;
  author?: string;
  reviewer?: string;
  approver?: string;
  owner_team?: string;
  related_docs?: string[];
  depends_on?: string[];
  supersedes?: string | null;
  superseded_by?: string | null;
  classification?: ITDocClassification;
  retention?: string;
  lang?: string;
}
EOF

# Inserisci il snippet dopo la riga 19 (fine OKFRelation)
sed -i '19r /tmp/it-types-snippet.ts' src/types.ts

# Aggiungi itMetadata e isITAlias a ResourceMetadata (prima della chiusura dell'interfaccia)
# Questa modifica richiede edit manuale: cerca "keyConcepts?: string[];" e aggiungi sotto
```

### Verifica

```bash
npm run lint
# Deve passare senza errori
```

## Step 3 — Creare il nuovo file `src/lib/okfItTemplates.ts`

```bash
# Copia il file dalla cartella integration-livello-2
cp /path/to/integration-livello-2/03-NEW-okfItTemplates.ts src/lib/okfItTemplates.ts

# Verifica
ls -lh src/lib/okfItTemplates.ts
head -5 src/lib/okfItTemplates.ts
```

### Verifica

```bash
npm run lint
# Deve passare
```

## Step 4 — Applicare la patch a `src/lib/okfParser.ts`

### Attenzione
Questa è la patch più corposa. Leggi attentamente `01-PATCH-okfParser.ts.md` prima di applicare.

### Modifiche da applicare (in ordine)

1. **Aggiungi import** in cima al file:
   ```typescript
   import { ITProjectMetadata } from "../types";
   ```

2. **Aggiungi IT_DOC_TYPE_ALIASES** dopo `CANONICAL_OKF_TYPES` (riga ~10):
   - Copia il blocco `IT_DOC_TYPE_ALIASES`, `ITDocTypeAlias`, `isITDocType()`, `canonicalItTypeToOkf()` dal file `01-PATCH-okfParser.ts.md` sezione "Modifica 1"

3. **Sostituisci `sanitizeDocType()`** con la nuova versione (sezione "Modifica 2")

4. **Estendi l'interfaccia `ParsedOKFDocument`** con i nuovi campi (sezione "Modifica 3"):
   - `originalDocType?: string;` (già esiste, resta invariato)
   - `isITAlias?: boolean;` (NUOVO)
   - `itMetadata?: ITProjectMetadata;` (NUOVO)

5. **Modifica `parseOKFDocument()`**:
   - Inizializza `itMeta` prima del loop (sezione "Modifica 4")
   - Aggiungi riconoscimento section headers per `related_docs:` e `depends_on:`
   - Aggiungi riconoscimento delle chiavi IT estese nel blocco top-level
   - Aggiungi gestione array items per `related_docs` e `depends_on`
   - Aggiungi `finalItMeta` e `isITAlias` nel return finale

6. **Aggiungi export** in fondo al file (sezione "Modifica 5"):
   ```typescript
   export { OKF_IT_TEMPLATES, IT_DOC_TYPES } from "./okfItTemplates";
   ```

### Verifica

```bash
npm run lint
# Deve passare senza errori TypeScript
```

## Step 5 — Verifica funzionale

### Test 1: documento OKF canonico (backward compat)

Crea un file di test `/tmp/test-canonical.md`:

```yaml
---
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
# Body content
```

Lancia uno script di test rapido:

```bash
cat > /tmp/test-parser.ts << 'EOF'
import { parseOKFDocument } from "./src/lib/okfParser";
import { readFileSync } from "fs";

const doc = readFileSync("/tmp/test-canonical.md", "utf-8");
const parsed = parseOKFDocument(doc);

console.log("isValidOKF:", parsed.isValidOKF);
console.log("docType:", parsed.docType);
console.log("originalDocType:", parsed.originalDocType);
console.log("isITAlias:", parsed.isITAlias);
console.log("itMetadata:", parsed.itMetadata);
EOF

npx tsx /tmp/test-parser.ts
```

**Output atteso**:
```
isValidOKF: true
docType: architecture
originalDocType: architecture   # uguale a docType, non è alias IT
isITAlias: undefined            # non è alias IT
itMetadata: undefined           # nessun metadato IT
```

### Test 2: documento IT alias

Crea `/tmp/test-it-alias.md`:

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
# Body
```

Aggiorna lo script di test per leggere questo file:

```bash
cat > /tmp/test-parser-it.ts << 'EOF'
import { parseOKFDocument } from "./src/lib/okfParser";
import { readFileSync } from "fs";

const doc = readFileSync("/tmp/test-it-alias.md", "utf-8");
const parsed = parseOKFDocument(doc);

console.log("isValidOKF:", parsed.isValidOKF);
console.log("docType:", parsed.docType);
console.log("originalDocType:", parsed.originalDocType);
console.log("isITAlias:", parsed.isITAlias);
console.log("itMetadata.project_id:", parsed.itMetadata?.project_id);
console.log("itMetadata.phase:", parsed.itMetadata?.phase);
console.log("itMetadata.related_docs:", parsed.itMetadata?.related_docs);
EOF

npx tsx /tmp/test-parser-it.ts
```

**Output atteso**:
```
isValidOKF: true
docType: architecture              # canonico OKF (per D3)
originalDocType: lld               # preservato!
isITAlias: true                    # nuovo!
itMetadata.project_id: acme-milano-2026
itMetadata.phase: 2
itMetadata.related_docs: [ 'architecture-acme-milano-hld-01' ]
```

### Test 3: boilerplate OKF_IT_TEMPLATES

```bash
cat > /tmp/test-templates.ts << 'EOF'
import { OKF_IT_TEMPLATES, IT_DOC_TYPE_LIST, getITBoilerplate } from "./src/lib/okfItTemplates";

console.log("=== Lista tipi IT (ordinati per fase) ===");
IT_DOC_TYPE_LIST.forEach(t => {
  console.log(`Fase ${t.phase} | ${t.type.padEnd(20)} → ${t.canonical.padEnd(14)} | ${t.label}`);
});

console.log("\n=== Boilerplate LLD ===");
const boilerplate = getITBoilerplate("lld");
console.log(boilerplate);
EOF

npx tsx /tmp/test-templates.ts
```

**Output atteso**: lista dei 9 tipi IT con fase e tipo canonico + boilerplate LLD completo.

## Step 6 — Commit e push

```bash
# Verifica modifiche
git status
git diff --stat

# Commit
git add src/types.ts src/lib/okfParser.ts src/lib/okfItTemplates.ts
git commit -m "feat(parser): riconoscimento 9 tipi documentali IT come alias canonici OKF v0.2

- Aggiunto IT_DOC_TYPE_ALIASES map e helpers isITDocType/canonicalItTypeToOkf
- Estesa sanitizeDocType() per riconoscere alias IT (preserva originalDocType)
- Esteso ParsedOKFDocument con itMetadata e isITAlias (opzionali)
- Aggiunti tipi ITDocType, ITProjectMetadata, ITProjectPhase, ITDocStatus, ITDocClassification
- Esteso ResourceMetadata con itMetadata e isITAlias (opzionali)
- Creato okfItTemplates.ts con 9 boilerplate YAML + metadata
- Backward compatibility: documenti OKF esistenti non sono influenzati

Vedi integration-livello-2/README.md per dettagli."

# Push (se hai un fork o un branch remoto)
git push origin feature/it-infrastructure-types
```

## Step 7 — Aprire la PR su GitHub

1. Vai su https://github.com/matrixNeo76/KnowledgeVault
2. Clicca "Compare & pull request" per il branch `feature/it-infrastructure-types`
3. Usa il titolo e la descrizione da `04-PR-DESCRIPTION.md`
4. Aggiungi label `enhancement`, `parser`, `okf-v0.2`, `it-infrastructure`
5. Se hai test, assicurati che passino in CI

## Rollback in caso di problemi

```bash
# Ripristina il branch di backup
git checkout backup/pre-it-types

# Oppure resetta le modifiche
git checkout main
git branch -D feature/it-infrastructure-types
```

## Troubleshooting

### Errore: "Cannot find module './okfItTemplates'"

**Causa**: il file `src/lib/okfItTemplates.ts` non è stato creato o è in posizione sbagliata.

**Fix**:
```bash
ls src/lib/okfItTemplates.ts
# Se non esiste:
cp /path/to/integration-livello-2/03-NEW-okfItTemplates.ts src/lib/okfItTemplates.ts
```

### Errore TypeScript: "Property 'itMetadata' does not exist on type 'ResourceMetadata'"

**Causa**: la patch a `src/types.ts` non è stata applicata completamente.

**Fix**: verifica che l'interfaccia `ResourceMetadata` contenga `itMetadata?: ITProjectMetadata;` e `isITAlias?: boolean;` in fondo, prima della parentesi graffa di chiusura.

### Errore: "isITDocType is not a function"

**Causa**: la funzione `isITDocType` non è stata esportata da `okfParser.ts`.

**Fix**: verifica che il blocco `export function isITDocType(...)` sia presente dopo `IT_DOC_TYPE_ALIASES` in `src/lib/okfParser.ts`.

### I test esistenti falliscono

**Causa probabile**: la nuova `sanitizeDocType()` ha cambiato comportamento per qualche tipo non standard.

**Fix**: confronta il vecchio e nuovo `sanitizeDocType()`. La differenza dovrebbe essere solo l'aggiunta del branch `isITDocType(original)` prima delle euristiche esistenti. Tutti gli altri branch devono restare invariati.

## Conclusione

Dopo aver completato gli Step 1-6, il tuo Knowledge Vault riconosce nativamente i 9 tipi documentali IT del ciclo lavorativo. I documenti caricati tramite CaptureBar con `type: "lld"` (o qualsiasi altro alias IT) saranno:

1. ✅ Validati come OKF v0.2 (isValidOKF: true)
2. ✅ Visualizzati nel grafo D3 con il tipo canonico corretto
3. ✅ Riconoscibili come IT via `isITAlias: true` e `originalDocType: "lld"`
4. ✅ Arricchiti con `itMetadata` tipizzato per uso futuro in UI custom

Per il Livello 3 (modulo UI completo per IT infrastructure), apri una nuova richiesta.
