# ItInfra — Template Documentali OKF v0.2 per Ciclo Lavorativo IT

[![Standard OKF](https://img.shields.io/badge/Standard-OKF%20v0.2-C5A059.svg)](https://github.com/matrixNeo76/KnowledgeVault/blob/main/docs/OKF_v0.2_SPECIFICATION.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Made for Knowledge Vault](https://img.shields.io/badge/Integrates%20with-Knowledge%20Vault-8E75B2.svg)](https://github.com/matrixNeo76/KnowledgeVault)
[![Italian](https://img.shields.io/badge/Language-Italiano-red.svg)]()

> **Repository di template documentali per infrastrutture IT complesse — dalla fase di Assessment al Go-Live, conformi allo standard OKF v0.2 (Open Knowledge Format).**
>
> Progettato per essere compilato da agenti AI (Claude, GPT, Gemini, Cursor, Copilot) tramite chat agentiche, e salvato in un knowledge vault dove i documenti vengono relazionati tra loro tramite `entities` e `relations` ontologiche.

---

## 🎯 A chi è rivolto

- **Integratori / System Engineer IT** che producono documentazione tecnica per progetti di infrastruttura
- **Team Operations** che devono gestire la documentazione post-rilascio
- **Agenti AI** che compilano template a partire da dati forniti in chat
- **Knowledge Engineers** che mantengono un knowledge vault ontologico

---

## 📦 Struttura del repository

```
ItInfra/
├── README.md                          ← Questo file (orientamento GitHub)
├── AGENTS.md                          ← Istruzioni auto-caricate da Cursor/Aider/Continue/Cline/Roo Code
├── CLAUDE.md                          ← Istruzioni auto-caricate da Claude Code (CLI Anthropic)
├── INTEGRAZIONE-REPO.md               ← Guida master in formato OKF v0.2: come integrare tutto nel Knowledge Vault
├── LICENSE                            ← MIT License
├── .gitignore
│
├── templates/                         ← 10 template documentali OKF v0.2 + 3 file orientamento
│   ├── 00-INDEX.md                    ← Indice navigazionale con link graph Mermaid
│   ├── 01-RSD-URS.md                  ← Fase 1 — Requirements Specification
│   ├── 02-HLD.md                      ← Fase 2 — High-Level Design
│   ├── 03-LLD.md                      ← Fase 2 — Low-Level Design (IP, VLAN, rack, ACL)
│   ├── 04-MOP.md                      ← Fase 3 — Method of Procedure
│   ├── 05-Rollback.md                 ← Fase 3 — Rollback / Fallback Plan
│   ├── 06-As-Built.md                 ← Fase 5-7 — As-Built Documentation
│   ├── 07-ATP.md                      ← Fase 6 — Acceptance Test Plan
│   ├── 08-SOP-Runbook.md              ← Fase 7 — Standard Operating Procedures
│   ├── 09-Handover-Inventory.md       ← Fase 7 — Handover & Asset Inventory
│   └── README.md                      ← Documentazione umana dei template
│
├── examples/                          ← 11 prompt di esempio per agenti AI
│   ├── README.md                      ← Indice esempi + workflow d'uso
│   ├── 00-prompt-master-template.md   ← Struttura generica di un prompt efficace
│   ├── 01-prompt-RSD-URS.md           ← 9 prompt completi e personalizzabili
│   ├── 02-prompt-HLD.md               ← Scenario coerente: Acme S.p.A. Milano
│   ├── 03-prompt-LLD.md
│   ├── 04-prompt-MOP.md
│   ├── 05-prompt-Rollback.md
│   ├── 06-prompt-As-Built.md
│   ├── 07-prompt-ATP.md
│   ├── 08-prompt-SOP-Runbook.md
│   └── 09-prompt-Handover-Inventory.md
│
└── integration/                       ← Estensioni per Knowledge Vault (https://github.com/matrixNeo76/KnowledgeVault)
    ├── level-2/                       ← Estensione parser OKF per 9 tipi documentali IT
    │   ├── README.md
    │   ├── 01-PATCH-okfParser.md      ← Modifica a src/lib/okfParser.ts
    │   ├── 02-PATCH-types.md          ← Modifica a src/types.ts
    │   ├── 03-NEW-okfItTemplates.ts  ← Nuovo file src/lib/okfItTemplates.ts
    │   ├── 04-PR-DESCRIPTION.md       ← PR description pronta per GitHub
    │   └── 05-MIGRATION-GUIDE.md      ← Guida migrazione 7-step
    │
    └── level-3/                       ← Modulo UI completo + API AI compiler
        ├── README.md
        ├── 01-NEW-ITProjectMetadataCard.tsx       ← Scheda metadata IT nel reader
        ├── 02-NEW-ITWorkflowTimeline.tsx          ← Timeline visuale 7 fasi
        ├── 03-NEW-ITInfrastructureSidebar.tsx      ← Drawer laterale con stats
        ├── 04-NEW-ITTemplateCompilerModal.tsx     ← Modale compilazione AI
        ├── 05-PATCH-KnowledgeReader.tsx.md         ← Patch: aggiungi tab "Ciclo IT"
        ├── 06-PATCH-Sidebar.tsx.md                 ← Patch: aggiungi voce "Ciclo IT"
        ├── 07-PATCH-CaptureBar.tsx.md              ← Patch: aggiungi pulsante "Template IT"
        ├── 08-PATCH-captureRoutes.ts.md            ← Patch: 2 nuovi endpoint API
        ├── 09-NEW-itInfrastructureService.ts        ← Servizio backend Gemini
        ├── 10-PR-DESCRIPTION.md                    ← PR description
        └── 11-MIGRATION-GUIDE.md                   ← Guida migrazione 11-step
```

---

## 🚀 Quick Start

### 1. Usare i template documentali (Livello 1)

Per usare solo i 10 template con un agente AI (Claude, Cursor, ecc.):

```bash
git clone https://github.com/matrixNeo76/ItInfra.git
cd ItInfra
cat templates/00-INDEX.md  # mappa delle 7 fasi e dei 9 tipi documentali
cat examples/01-prompt-RSD-URS.md  # prompt di esempio da personalizzare
```

Apri la chat del tuo agente AI e incolla il prompt personalizzato. L'agente leggerà `AGENTS.md` (o `CLAUDE.md` se usi Claude Code) automaticamente e compilerà il template rispettando lo standard OKF v0.2.

### 2. Integrare nel Knowledge Vault (Livello 2 + 3)

Per integrare il modulo completo nel tuo Knowledge Vault:

```bash
git clone https://github.com/matrixNeo76/ItInfra.git
git clone https://github.com/matrixNeo76/KnowledgeVault.git

cd KnowledgeVault
# Segui la guida master:
cat ../ItInfra/INTEGRAZIONE-REPO.md
```

La guida `INTEGRAZIONE-REPO.md` (in formato OKF v0.2 nativo) ti porta passo-passo attraverso i 3 livelli di integrazione.

---

## 🗺️ Le 7 fasi del ciclo lavorativo IT

| Fase | Denominazione | Documenti | Template |
|------|---------------|-----------|----------|
| 1. Analisi | Assessment & Site Survey | RSD/URS | `01-RSD-URS.md` |
| 2. Progettazione | Architectural Design | HLD, LLD | `02-HLD.md`, `03-LLD.md` |
| 3. Approvvigionamento | Procurement & Staging | MOP, Rollback | `04-MOP.md`, `05-Rollback.md` |
| 4. Posa e Montaggio | Racking & Cabling | (confluisce in As-Built) | `06-As-Built.md` |
| 5. Configurazione | Commissioning & Implementation | (confluisce in As-Built) | `06-As-Built.md` |
| 6. Collaudo | Testing & Validation | ATP | `07-ATP.md` |
| 7. Rilascio | Go-Live / Handover | As-Built, SOP/Runbook, Handover | `06-As-Built.md`, `08-SOP-Runbook.md`, `09-Handover-Inventory.md` |

---

## 🔗 Schema OKF v0.2

Tutti i template usano lo standard **OKF v0.2 (Open Knowledge Format)** nativo del [Knowledge Vault](https://github.com/matrixNeo76/KnowledgeVault). Il frontmatter YAML è composto da:

- **Campi canonici** (riconosciuti dal parser): `okf_version`, `id`, `title`, `type` (6 tipi canonici), `domain`, `tags`, `entities`, `relations`
- **Metadati estesi IT** (preservati in `rawFrontmatter`): `project_id`, `phase`, `related_docs`, `depends_on`, `status`, `version`, `author`, ecc.

### Mappatura 9 tipi IT → 6 tipi canonici OKF

| Tipo IT | Tipo canonico OKF |
|---------|-------------------|
| RSD/URS, ATP, Handover & Inventory | `specification` |
| HLD, LLD, As-Built | `architecture` |
| MOP, Rollback, SOP/Runbook | `guide` |

Vedi [`templates/00-INDEX.md`](./templates/00-INDEX.md) per dettagli completi.

---

## 🤖 Agenti AI supportati

I file `AGENTS.md` e `CLAUDE.md` vengono letti automaticamente da:

| Agente | File letto |
|--------|-----------|
| **Claude Code** (Anthropic CLI) | `CLAUDE.md` |
| **Cursor** | `AGENTS.md` |
| **Aider** | `AGENTS.md` |
| **Continue** | `AGENTS.md` |
| **Cline / Roo Code** | `AGENTS.md` |
| **Altri agenti** | Manualmente via prompt: "Prima di iniziare, leggi `AGENTS.md`" |

---

## 📊 Link Graph dei documenti

```mermaid
graph TD
    RSD[01-RSD/URS] --> HLD[02-HLD]
    RSD --> MOP[04-MOP]
    HLD --> LLD[03-LLD]
    LLD --> MOP
    MOP --> ROLL[05-Rollback]
    ROLL -.-> MOP
    LLD --> ASBUILT[06-As-Built]
    MOP --> ASBUILT
    LLD --> ATP[07-ATP]
    ASBUILT --> ATP
    ATP --> SOP[08-SOP/Runbook]
    ASBUILT --> SOP
    ASBUILT --> HAND[09-Handover-Inventory]
    SOP --> HAND
```

---

## 🛣️ Roadmap

### ✅ Completato
- [x] **Livello 1**: 10 template OKF v0.2 nativi
- [x] **Livello 2**: Estensione parser con 9 alias IT + 9 boilerplate
- [x] **Livello 3**: Modulo UI completo + API AI compiler (Gemini)
- [x] **Documentazione**: guide migrazione, PR descriptions, file integrazione repo

### 🔮 Candidati per Livello 4 (futuro)
- [ ] Colori D3 dedicati per i 9 tipi IT (patch a `KnowledgeGraph.tsx`)
- [ ] Export Excel/CSV degli asset inventariati
- [ ] Modifica inline dei metadati IT (estensione di `useVaultMutations.ts`)
- [ ] Integrazione con calendar per scadenze contratti
- [ ] Tool MCP per agenti AI esterni (estensione di `mcpRoutes.ts`)
- [ ] Auto-salvataggio diretto dei documenti compilati nel vault

---

## 🤝 Contribuire

Le contribuzioni sono benvenute! Apri una issue o una PR se:

- Trovi un bug in un template
- Vuoi aggiungere un nuovo tipo documentale IT
- Hai migliorato le AI-INSTRUCTIONS
- Vuoi tradurre i template in inglese o altre lingue
- Hai casi d'uso reali da condividere come esempi

### Standard per le PR

1. Mantieni lo schema OKF v0.2 nativo nel frontmatter
2. Aggiorna la checklist di validazione in fondo a ogni template
3. Verifica la coerenza `relations` vs `related_docs`
4. Testa con il parser: `python3 scripts/validate_okf_templates.py`

---

## 📚 Risorse correlate

- **Knowledge Vault** (repo principale): https://github.com/matrixNeo76/KnowledgeVault
- **Specifica OKF v0.2**: https://github.com/matrixNeo76/KnowledgeVault/blob/main/docs/OKF_v0.2_SPECIFICATION.md
- **Architettura del Vault**: https://github.com/matrixNeo76/KnowledgeVault/blob/main/docs/SYSTEM_ARCHITECTURE_OKF.md
- **Pipeline di ingestione**: https://github.com/matrixNeo76/KnowledgeVault/blob/main/docs/INGESTION_PIPELINE_SPEC.md

---

## 📄 Licenza

Distribuito sotto licenza MIT. Vedi [`LICENSE`](./LICENSE) per dettagli.

---

## 🙋 Supporto

- Apri una [issue](https://github.com/matrixNeo76/ItInfra/issues) per bug o richieste
- Consulta [`INTEGRAZIONE-REPO.md`](./INTEGRAZIONE-REPO.md) per la guida master
- Leggi [`AGENTS.md`](./AGENTS.md) prima di far compilare un template a un agente AI
