---
okf_version: "0.2"
id: "guide-repo-integration-complete"
title: "Guida Integrazione Repo — Come accogliere tutto quanto sviluppato nel Knowledge Vault"
type: "guide"
domain: "Knowledge Architecture & Repository Integration"
tags: ["okf-v0.2", "integration-guide", "knowledge-vault", "level-1", "level-2", "level-3", "migration"]
project_id: "templates-ciclo-it"
phase: 7
status: "approved"
version: "1.0"
created_at: "2026-09-15"
updated_at: "2026-09-15"
lang: "it"

entities:
  - name: "Knowledge Vault Repository"
    type: "organization"
    description: "Repo GitHub matrixNeo76/KnowledgeVault che accoglierà le estensioni dei 3 livelli"
  - name: "OKF v0.2 Standard"
    type: "specification"
    description: "Standard di serializzazione già nativo nel parser del repo (src/lib/okfParser.ts)"
  - name: "Livello 1 — Schema Template"
    type: "concept"
    description: "10 template documentali IT con schema YAML OKF v0.2 nativo"
  - name: "Livello 2 — Parser Extension"
    type: "specification"
    description: "Estensione del parser per riconoscere 9 alias IT come tipi canonici OKF"
  - name: "Livello 3 — UI Module"
    type: "concept"
    description: "Modulo UI completo con sidebar, timeline, reader tab, template compiler AI"
  - name: "Migration Workflow"
    type: "pattern"
    description: "Sequenza ordinata di applicazione dei 3 livelli nel repo Knowledge Vault"

relations:
  - targetTitle: "Specifica Formale OKF v0.2"
    targetId: "spec-okf-v02-formal"
    relationType: "implements"
    weight: 1.0
    description: "Questa guida rispetta lo standard OKF v0.2 e viene riconosciuta nativamente dal parser del repo"
  - targetTitle: "Architettura di Sistema del Knowledge Vault"
    targetId: "arch-vault-root-summary"
    relationType: "extends"
    weight: 0.95
    description: "Estende l'architettura del Knowledge Vault con il modulo IT infrastructure"
  - targetTitle: "Livello 1 — Template documentali OKF v0.2"
    targetId: "index-ciclo-lavorativo-it"
    relationType: "documents"
    weight: 1.0
    description: "Guida l'integrazione dei 10 template documentali nel repo"
  - targetTitle: "Livello 2 — Estensione parser"
    targetId: "patch-okf-parser-it-types"
    relationType: "documents"
    weight: 1.0
    description: "Guida l'applicazione delle patch al parser OKF"
  - targetTitle: "Livello 3 — Modulo UI"
    targetId: "guide-repo-integration-complete"
    relationType: "extends"
    weight: 0.9
    description: "Guida l'integrazione del modulo UI completo"
---

# Guida Integrazione Repo — Come accogliere tutto quanto sviluppato

> **Documento di integrazione finale**: spiega come modificare il repo https://github.com/matrixNeo76/KnowledgeVault per accogliere i 10 template documentali IT (Livello 1), l'estensione del parser OKF (Livello 2) e il modulo UI completo (Livello 3).
>
> **Formato**: questo documento è conforme allo standard OKF v0.2 nativo e viene riconosciuto dal parser `src/lib/okfParser.ts` del Knowledge Vault. Una volta caricato nel vault, apparirà come nodo nel grafo D3 con relazioni verso gli altri documenti di integrazione.

---

## 1. Panoramica dell'integrazione

Il presente documento guida l'integrazione nel repo `matrixNeo76/KnowledgeVault` di **3 livelli progressivi** di estensione per supportare il ciclo lavorativo IT (Assessment → Design → Procurement → Racking → Commissioning → Testing → Go-Live).

| Livello | Cosa aggiunge | Complessità | Tempo stimato | Breaking changes |
|---------|--------------|-------------|----------------|-------------------|
| **Livello 1** | 11 template documentali .md (10 template + 1 indice) con schema OKF v0.2 nativo | Bassa | 30 min | Nessuno |
| **Livello 2** | Estensione parser (`okfParser.ts`, `types.ts`) + nuovo file `okfItTemplates.ts` | Media | 2-3 ore | Nessuno (additivo) |
| **Livello 3** | 4 componenti React + 1 servizio backend + 4 patch a file esistenti | Alta | 4-6 ore | Nessuno (additivo) |

### Strategia generale

Tutte le modifiche sono **additive**: nessun documento OKF esistente viene rotto, nessuna API esistente cambia firma, nessuna UI esistente perde funzionalità. I 3 livelli sono applicabili progressivamente — anche solo il Livello 1 rende il sistema già utilizzabile.

---

## 2. Prerequisiti

### Versioni software
- **Node.js**: 22 LTS (già richiesto dal repo)
- **Bun**: installato (già richiesto dal repo)
- **Git**: 2.30+ per `git apply` delle patch

### Variabili d'ambiente
- `GEMINI_API_KEY` o `GOOGLE_API_KEY` — già richiesta dal Knowledge Vault base
- `GEMINI_MODEL=gemini-2.5-flash` (opzionale, default `gemini-2.5-flash`) — solo per Livello 3

### Backup preventivo (consigliato)

```bash
cd /path/to/KnowledgeVault
git checkout -b backup/pre-it-infrastructure
git checkout -b feature/it-infrastructure-complete
```

---

## 3. Livello 1 — Template documentali OKF v0.2

### Obiettivo
Aggiungere 11 file `.md` (10 template + 1 indice) + cartella `examples/` con 12 file di prompt + 3 file di orientamento (`README.md`, `AGENTS.md`, `CLAUDE.md`).

### Origine dei file
I file sono già pronti nel pacchetto `templates.zip` scaricato da `/home/z/my-project/download/templates.zip`. Estrai lo zip in una directory temporanea:

```bash
mkdir -p /tmp/it-templates
cd /tmp/it-templates
unzip /path/to/templates.zip
ls templates/
```

### Posizione consigliata nel repo

Opzione A — **Sottocartella `docs/it-infrastructure/`** (consigliata, preserva la struttura del repo):
```
docs/
├── OKF_v0.2_SPECIFICATION.md           ← esistente
├── SYSTEM_ARCHITECTURE_OKF.md          ← esistente
├── INGESTION_PIPELINE_SPEC.md          ← esistente
├── SYSTEM_REPLICATION_GUIDE.md         ← esistente
├── PROJECT_STRUCTURE.md                ← esistente
├── SPEC_PIANO_MITIGAZIONE_CRITICITA_OKF.md  ← esistente
└── it-infrastructure/                   ← NUOVA cartella
    ├── README.md
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── 00-INDEX.md
    ├── 01-RSD-URS.md
    ├── 02-HLD.md
    ├── 03-LLD.md
    ├── 04-MOP.md
    ├── 05-Rollback.md
    ├── 06-As-Built.md
    ├── 07-ATP.md
    ├── 08-SOP-Runbook.md
    ├── 09-Handover-Inventory.md
    ├── 10-RCA-Troubleshooting.md
    └── examples/
        ├── README.md
        ├── 00-prompt-master-template.md
        ├── 01-prompt-RSD-URS.md
        ├── 02-prompt-HLD.md
        ├── 03-prompt-LLD.md
        ├── 04-prompt-MOP.md
        ├── 05-prompt-Rollback.md
        ├── 06-prompt-As-Built.md
        ├── 07-prompt-ATP.md
        ├── 08-prompt-SOP-Runbook.md
        ├── 09-prompt-Handover-Inventory.md
        └── 10-prompt-RCA-Troubleshooting.md
```

### Comandi

```bash
cd /path/to/KnowledgeVault

# Copia i template nella cartella docs/it-infrastructure/
mkdir -p docs/it-infrastructure/examples
cp /tmp/it-templates/templates/[0-9][0-9]-*.md docs/it-infrastructure/
cp /tmp/it-templates/templates/README.md docs/it-infrastructure/
cp /tmp/it-templates/templates/AGENTS.md docs/it-infrastructure/
cp /tmp/it-templates/templates/CLAUDE.md docs/it-infrastructure/
cp /tmp/it-templates/templates/examples/*.md docs/it-infrastructure/examples/

# Verifica
ls -lh docs/it-infrastructure/
```

### Verifica

1. Apri `docs/it-infrastructure/00-INDEX.md` in un editor Markdown — deve visualizzare correttamente tabelle e diagramma Mermaid
2. Carica `docs/it-infrastructure/03-LLD.md` nel Knowledge Vault (incolla il contenuto nella CaptureBar) — il parser deve riconoscerlo come documento OKF v0.2 valido con `type: "architecture"` e visualizzarlo nel grafo D3
3. Verifica che le `entities` e `relations` nel frontmatter vengano parseate correttamente

### Commit

```bash
git add docs/it-infrastructure/
git commit -m "docs(it-infrastructure): aggiunti 10 template documentali OKF v0.2 per ciclo lavorativo IT

- 00-INDEX.md con mappa fasi, link graph, schema frontmatter
- 9 template: RSD/URS, HLD, LLD, MOP, Rollback, As-Built, ATP, SOP/Runbook, Handover
- 11 esempi di prompt per agenti AI in examples/
- README.md, AGENTS.md, CLAUDE.md per orientamento umano + agenti AI
- Schema OKF v0.2 nativo compatibile col parser src/lib/okfParser.ts

Vedi docs/it-infrastructure/README.md per dettagli."
```

---

## 4. Livello 2 — Estensione del parser OKF

### Obiettivo
Estendere `src/lib/okfParser.ts` per riconoscere esplicitamente i 9 tipi documentali IT come alias canonici OKF, preservando la semantica IT originale.

### File da modificare/creare

| File | Azione | Fonte |
|------|--------|-------|
| `src/lib/okfParser.ts` | Modifica | `integration-livello-2/01-PATCH-okfParser.ts.md` |
| `src/types.ts` | Modifica | `integration-livello-2/02-PATCH-types.ts.md` |
| `src/lib/okfItTemplates.ts` | NUOVO file | `integration-livello-2/03-NEW-okfItTemplates.ts` |

### Comandi

```bash
cd /path/to/KnowledgeVault

# 1. Copia il nuovo file okfItTemplates.ts
cp /tmp/it-templates/templates/integration-livello-2/03-NEW-okfItTemplates.ts \
   src/lib/okfItTemplates.ts

# 2. Applica le modifiche a okfParser.ts (manuale, vedi 01-PATCH-okfParser.ts.md)
#    Apri il file PATCH e segui le 5 modifiche descritte

# 3. Applica le modifiche a types.ts (manuale, vedi 02-PATCH-types.ts.md)
#    Apri il file PATCH e segui le 3 modifiche descritte

# 4. Verifica
npm run lint
```

### Verifica funzionale

```bash
# Test 1: documento OKF canonico esistente continua a funzionare
cat > /tmp/test-canonical.md << 'EOF'
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
# Body
EOF

# Crea uno script di test rapido
cat > /tmp/test-parser.ts << 'EOF'
import { parseOKFDocument } from "./src/lib/okfParser";
import { readFileSync } from "fs";
const doc = readFileSync(process.argv[2], "utf-8");
const parsed = parseOKFDocument(doc);
console.log(JSON.stringify({
  isValidOKF: parsed.isValidOKF,
  docType: parsed.docType,
  isITAlias: parsed.isITAlias,
  itMetadata: parsed.itMetadata,
}, null, 2));
EOF

npx tsx /tmp/test-parser.ts /tmp/test-canonical.md
# Output atteso: isValidOKF: true, isITAlias: undefined, itMetadata: undefined

# Test 2: documento IT alias viene riconosciuto
cat > /tmp/test-it-alias.md << 'EOF'
---
okf_version: "0.2"
id: "architecture-test-lld-01"
title: "LLD Test"
type: "lld"
domain: "IT Infrastructure"
tags: ["okf-v0.2", "lld"]
project_id: "test-proj"
phase: 2
entities:
  - name: "Test"
    type: "technology"
    description: "test"
---
# Body
EOF

npx tsx /tmp/test-parser.ts /tmp/test-it-alias.md
# Output atteso: isValidOKF: true, docType: "architecture", isITAlias: true,
#                itMetadata: { project_id: "test-proj", phase: 2, related_docs: [], depends_on: [] }
```

### Commit

```bash
git add src/lib/okfParser.ts src/lib/okfItTemplates.ts src/types.ts
git commit -m "feat(parser): riconoscimento 9 tipi documentali IT come alias canonici OKF v0.2

- Aggiunto IT_DOC_TYPE_ALIASES map e helpers isITDocType/canonicalItTypeToOkf
- Estesa sanitizeDocType() per riconoscere alias IT (preserva originalDocType)
- Esteso ParsedOKFDocument con itMetadata e isITAlias (opzionali)
- Aggiunti tipi ITDocType, ITProjectMetadata, ITProjectPhase, ITDocStatus, ITDocClassification
- Esteso ResourceMetadata con itMetadata e isITAlias (opzionali)
- Creato okfItTemplates.ts con 9 boilerplate YAML + metadata
- Backward compatibility: documenti OKF esistenti non sono influenzati

Vedi integration-livello-2/README.md per dettagli."
```

---

## 5. Livello 3 — Modulo UI completo

### Obiettivo
Aggiungere 4 nuovi componenti React, 1 servizio backend, 4 patch a file esistenti per integrare il ciclo IT nella UI del Knowledge Vault.

### File da modificare/creare

| File | Azione | Fonte |
|------|--------|-------|
| `src/components/itInfrastructure/ITProjectMetadataCard.tsx` | NUOVO | `integration-livello-3/01-NEW-ITProjectMetadataCard.tsx` |
| `src/components/itInfrastructure/ITWorkflowTimeline.tsx` | NUOVO | `integration-livello-3/02-NEW-ITWorkflowTimeline.tsx` |
| `src/components/itInfrastructure/ITInfrastructureSidebar.tsx` | NUOVO | `integration-livello-3/03-NEW-ITInfrastructureSidebar.tsx` |
| `src/components/itInfrastructure/ITTemplateCompilerModal.tsx` | NUOVO | `integration-livello-3/04-NEW-ITTemplateCompilerModal.tsx` |
| `src/components/KnowledgeReader.tsx` | Modifica | `integration-livello-3/05-PATCH-KnowledgeReader.tsx.md` |
| `src/components/Sidebar.tsx` | Modifica | `integration-livello-3/06-PATCH-Sidebar.tsx.md` |
| `src/components/CaptureBar.tsx` | Modifica | `integration-livello-3/07-PATCH-CaptureBar.tsx.md` |
| `server/routes/captureRoutes.ts` | Modifica | `integration-livello-3/08-PATCH-captureRoutes.ts.md` |
| `server/services/itInfrastructureService.ts` | NUOVO | `integration-livello-3/09-NEW-itInfrastructureService.ts` |

### Comandi

```bash
cd /path/to/KnowledgeVault

# 1. Crea la cartella e copia i 4 componenti React
mkdir -p src/components/itInfrastructure

cp /tmp/it-templates/templates/integration-livello-3/01-NEW-ITProjectMetadataCard.tsx \
   src/components/itInfrastructure/ITProjectMetadataCard.tsx

cp /tmp/it-templates/templates/integration-livello-3/02-NEW-ITWorkflowTimeline.tsx \
   src/components/itInfrastructure/ITWorkflowTimeline.tsx

cp /tmp/it-templates/templates/integration-livello-3/03-NEW-ITInfrastructureSidebar.tsx \
   src/components/itInfrastructure/ITInfrastructureSidebar.tsx

cp /tmp/it-templates/templates/integration-livello-3/04-NEW-ITTemplateCompilerModal.tsx \
   src/components/itInfrastructure/ITTemplateCompilerModal.tsx

# 2. Copia il servizio backend
cp /tmp/it-templates/templates/integration-livello-3/09-NEW-itInfrastructureService.ts \
   server/services/itInfrastructureService.ts

# 3. Applica le 4 patch ai file esistenti (manuale)
#    Apri i file 05-PATCH-*, 06-PATCH-*, 07-PATCH-*, 08-PATCH-* e segui le istruzioni

# 4. Aggiorna .env.example
echo '
# IT Infrastructure Module (Livello 3)
GEMINI_MODEL=gemini-2.5-flash' >> .env.example

# 5. Verifica
npm run lint
```

### Verifica funzionale end-to-end

```bash
# Avvia il server
npm run dev

# Test 1: endpoint lista tipi IT
curl http://localhost:3000/api/it-infrastructure/types | python3 -m json.tool
# Deve restituire 9 tipi

# Test 2: endpoint compilazione (richiede GEMINI_API_KEY)
curl -X POST http://localhost:3000/api/it-infrastructure/compile-template \
  -H "Content-Type: application/json" \
  -d '{
    "docType": "rsd_urs",
    "project_id": "test-proj-2026",
    "project_name": "Test Project"
  }' | python3 -c "import sys,json; d=json.load(sys.stdin); print('OK' if d.get('success') else 'ERR:', d.get('error',''))"

# Test 3: UI
# Apri http://localhost:5173 nel browser
# - CaptureBar deve mostrare pulsante "Template IT"
# - Carica un documento IT nel vault → Sidebar deve mostrare voce "Ciclo IT" con badge
# - Click sulla voce → drawer laterale con timeline
# - Click su un documento nella timeline → KnowledgeReader con tab "Ciclo IT"
```

### Commit

```bash
git add src/components/itInfrastructure/ \
        server/services/itInfrastructureService.ts \
        src/components/KnowledgeReader.tsx \
        src/components/Sidebar.tsx \
        src/components/CaptureBar.tsx \
        server/routes/captureRoutes.ts \
        .env.example

git commit -m "feat(ui): modulo IT infrastructure completo — sidebar, timeline, reader tab, template compiler AI

- 4 nuovi componenti React in src/components/itInfrastructure/
- 1 nuovo servizio backend in server/services/
- 2 nuovi endpoint API (POST compile-template, GET types)
- Patch a KnowledgeReader (4° tab 'Ciclo IT')
- Patch a Sidebar (voce 'Ciclo IT' con badge contatore)
- Patch a CaptureBar (pulsante 'Template IT')
- Patch a captureRoutes (endpoint API)
- Documentazione: PR description + migration guide incluse

Vedi integration-livello-3/README.md per dettagli."
```

---

## 6. Verifica finale integrata

Dopo aver applicato tutti i 3 livelli, esegui una verifica end-to-end completa:

### 6.1 — Compilazione TypeScript

```bash
npm run lint
# Output atteso: nessun errore
```

### 6.2 — Test esistenti

```bash
npm run test:cekikj
# Output atteso: tutti i test passano (backward compatibility)
```

### 6.3 — Caricamento documento IT di test

```bash
# Genera un documento LLD con l'endpoint AI
curl -X POST http://localhost:3000/api/it-infrastructure/compile-template \
  -H "Content-Type: application/json" \
  -d '{
    "docType": "lld",
    "project_id": "acme-milano-2026",
    "project_name": "Sostituzione Infrastruttura DC Milano",
    "site": "MIL-01",
    "customer": "Acme S.p.A.",
    "author": "Mario Rossi",
    "owner_team": "Acme Operations",
    "custom_data": "3x Dell R750, 1x NetApp FAS8700, 2x Cisco Nexus 9300, 2x Fortinet FG-200F"
  }' > /tmp/lld-test.json

# Estrai il markdown
python3 -c "import json; d=json.load(open('/tmp/lld-test.json')); print(d.get('markdown',''))" > /tmp/lld-test.md

# Verifica che sia OKF v0.2 valido
head -30 /tmp/lld-test.md
# Deve iniziare con ---
# okf_version: "0.2"
# type: "architecture"  (canonico)
# originalDocType: "lld" (preservato)
# itMetadata con project_id, phase, related_docs, depends_on
```

### 6.4 — Caricamento nel vault

1. Apri il browser su `http://localhost:5173`
2. Clicca "Template IT" nella CaptureBar (oppure incolla direttamente il markdown)
3. Compila un documento di test
4. Verifica:
   - Il documento appare nel vault con il tipo IT riconosciuto
   - La sidebar mostra la voce "Ciclo IT" con badge
   - Il grafo D3 mostra il documento con archi verso le entità
   - Aprendo il documento, il tab "Ciclo IT" mostra i metadati

---

## 7. Struttura finale del repo dopo integrazione

```
KnowledgeVault/
├── docs/
│   ├── OKF_v0.2_SPECIFICATION.md                ← esistente
│   ├── SYSTEM_ARCHITECTURE_OKF.md               ← esistente
│   ├── INGESTION_PIPELINE_SPEC.md               ← esistente
│   ├── SYSTEM_REPLICATION_GUIDE.md              ← esistente
│   ├── PROJECT_STRUCTURE.md                     ← esistente
│   ├── SPEC_PIANO_MITIGAZIONE_CRITICITA_OKF.md  ← esistente
│   └── it-infrastructure/                       ← NUOVO (Livello 1)
│       ├── README.md
│       ├── AGENTS.md
│       ├── CLAUDE.md
│       ├── 00-INDEX.md
│       ├── 01-RSD-URS.md ... 09-Handover-Inventory.md
│       ├── examples/...
│       ├── integration-livello-2/...            ← patch Livello 2
│       ├── integration-livello-3/...            ← patch Livello 3
│       └── INTEGRAZIONE-REPO.md                 ← questo file
│
├── src/
│   ├── lib/
│   │   ├── okfParser.ts                         ← MODIFICATO (Livello 2)
│   │   ├── okfSerializer.ts                    ← invariato
│   │   └── okfItTemplates.ts                   ← NUOVO (Livello 2)
│   ├── types.ts                                 ← MODIFICATO (Livello 2)
│   └── components/
│       ├── KnowledgeReader.tsx                  ← MODIFICATO (Livello 3)
│       ├── Sidebar.tsx                          ← MODIFICATO (Livello 3)
│       ├── CaptureBar.tsx                       ← MODIFICATO (Livello 3)
│       └── itInfrastructure/                   ← NUOVO (Livello 3)
│           ├── ITProjectMetadataCard.tsx
│           ├── ITWorkflowTimeline.tsx
│           ├── ITInfrastructureSidebar.tsx
│           └── ITTemplateCompilerModal.tsx
│
├── server/
│   ├── routes/
│   │   └── captureRoutes.ts                    ← MODIFICATO (Livello 3)
│   └── services/
│       └── itInfrastructureService.ts           ← NUOVO (Livello 3)
│
└── .env.example                                 ← MODIFICATO (Livello 3)
```

---

## 8. Rollback graduale

Se incontri problemi, puoi fare rollback a qualsiasi livello:

### Rollback solo Livello 3
```bash
git revert <commit-livello-3>
# Oppure rimuovi manualmente i file nuovi e ripristina i 4 file patchati
rm -rf src/components/itInfrastructure/
rm server/services/itInfrastructureService.ts
git checkout HEAD~1 -- src/components/KnowledgeReader.tsx src/components/Sidebar.tsx \
                       src/components/CaptureBar.tsx server/routes/captureRoutes.ts .env.example
```

### Rollback Livello 2 + 3
```bash
git revert <commit-livello-3> <commit-livello-2>
rm src/lib/okfItTemplates.ts
git checkout HEAD~2 -- src/lib/okfParser.ts src/types.ts
```

### Rollback completo (ritorno al pre-Livello 1)
```bash
git checkout backup/pre-it-infrastructure
# Oppure
git reset --hard <commit-pre-livello-1>
```

---

## 9. Limiti noti e prossimi passi

### Limiti noti

1. **Grafo D3 non distingue i 9 tipi IT**: il `KnowledgeGraph.tsx` continua a usare i 6 colori dei tipi canonici OKF. I 9 tipi IT avranno lo stesso colore del tipo canonico corrispondente (es. `lld` avrà il colore di `architecture`).

2. **Modifica inline dei metadati IT non supportata**: il modulo IT è read-only per i metadati. Per modificarli, l'utente deve editare il frontmatter manualmente e ri-caricare il documento.

3. **Compilazione AI non salva direttamente nel vault**: l'endpoint `/api/it-infrastructure/compile-template` è stateless. L'utente deve copiare il markdown e salvarlo tramite CaptureBar.

4. **Quota Gemini**: la compilazione AI consuma quota Gemini (modello `gemini-2.5-flash`). In caso di rate limit, il servizio restituisce errore.

### Candidati per Livello 4 (futuro)

- Colori D3 dedicati per i 9 tipi IT (patch a `KnowledgeGraph.tsx`)
- Export Excel/CSV degli asset inventariati
- Modifica inline dei metadati IT (estensione di `useVaultMutations.ts`)
- Integrazione con calendar per scadenze contratti (nuovo endpoint)
- Tool MCP per agenti AI esterni (estensione di `mcpRoutes.ts`)
- Auto-salvataggio diretto dei documenti compilati nel vault

---

## 10. Note finali

### Perché il formato OKF v0.2 per questo documento

Ho scelto di scrivere questa guida in formato OKF v0.2 nativo (con frontmatter YAML conforme al parser `src/lib/okfParser.ts`) perché:

1. **Compatibilità automatica**: una volta caricato nel Knowledge Vault, questo documento viene riconosciuto come `type: "guide"` (canonico OKF) e visualizzato nel grafo D3
2. **Tracciabilità relazionale**: le `relations` nel frontmatter collegano questa guida agli altri documenti di integrazione (`patch-okf-parser-it-types`, `index-ciclo-lavorativo-it`, ecc.) creando automaticamente archi nel grafo
3. **Coerenza con il repo**: il Knowledge Vault usa già OKF v0.2 per tutti i suoi documenti canonici (`docs/OKF_v0.2_SPECIFICATION.md`, `AGENTS.md`, `README.md`). Una guida di integrazione non in OKF sarebbe un'anomalia
4. **Riconoscimento da parte di agenti AI**: agenti Claude Code, Cursor, ecc. che operano nel repo troveranno questo documento automaticamente parsabile e comprensibile

### Perché non un file `.md` "semplice"

Un file `.md` senza frontmatter OKF v0.2 verrebbe comunque riconosciuto dal parser (fallback a `type: "concept"`), ma:
- Perderebbe le relazioni ontologiche con gli altri documenti di integrazione
- Non avrebbe entità estratte automaticamente
- Non sarebbe visualizzato come nodo "di primo livello" nel grafo D3

Per questi motivi, il formato OKF v0.2 è la scelta ottimale per documenti destinati a vivere nel Knowledge Vault.

### Licenza e attribuzione

Tutte le estensioni sviluppate (Livelli 1, 2, 3) sono rilasciate come contributo al progetto Knowledge Vault. Adattale liberamente al tuo contesto. Nessuna attribuzione richiesta, ma feedback e miglioramenti sono benvenuti.

---

## Riferimenti rapidi

- **Repo target**: https://github.com/matrixNeo76/KnowledgeVault
- **Standard OKF v0.2**: `docs/OKF_v0.2_SPECIFICATION.md` nel repo
- **Architettura sistema**: `docs/SYSTEM_ARCHITECTURE_OKF.md` nel repo
- **Parser YAML**: `src/lib/okfParser.ts` (esteso nel Livello 2)
- **Tipi TypeScript**: `src/types.ts` (esteso nel Livello 2)
- **Boilerplate IT**: `src/lib/okfItTemplates.ts` (NUOVO nel Livello 2)
- **Modulo UI IT**: `src/components/itInfrastructure/` (NUOVO nel Livello 3)
- **Servizio backend IT**: `server/services/itInfrastructureService.ts` (NUOVO nel Livello 3)

Per domande o chiarimenti sull'integrazione, consulta le migration guide specifiche:
- `integration-livello-2/05-MIGRATION-GUIDE.md`
- `integration-livello-3/11-MIGRATION-GUIDE.md`
