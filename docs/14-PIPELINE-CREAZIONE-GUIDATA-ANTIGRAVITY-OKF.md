---
okf_version: "0.2"
id: "guide-pipeline-creazione-guidata-antigravity-01"
title: "Guida Operativa — Pipeline di Creazione Guidata OKF v0.2 con Antigravity"
type: "guide"
domain: "IT Infrastructure & Agentic Documentation Pipeline"
tags: ["okf-v0.2", "pipeline", "antigravity", "automation", "scaffolding", "generative-ui", "zero-hallucination"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Automation Suite"
phase: 0
author: "matrixNeo76"
reviewer: "System Architects & DevOps Team"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture & Knowledge Engineering"
status: "approved"
version: "1.0.0"
created_at: "2026-09-17"
updated_at: "2026-09-17"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "guide-itinfra-agentic-assistant-01"
  - "guide-itinfra-cli-manual-01"
  - "specification-itinfra-assistant-v02"
  - "guide-local-workspace-central-publish-01"
depends_on:
  - "architecture-itinfra-docs-index-01"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "Antigravity Agentic IDE"
    type: "framework"
    description: "Ambiente di sviluppo e pair-programming assistito da agenti AI autonomi"
  - name: "OKF v0.2 Documentation Pipeline"
    type: "specification"
    description: "Pipeline deterministica end-to-end per la redazione documentale IT a 7 fasi"
  - name: "Auto-Scaffolding Engine"
    type: "toolchain"
    description: "Motore scripts/itinfra_scaffold.py per propagazione automatica e auto-healing del manifesto"
  - name: "Generative UI Cockpit"
    type: "toolchain"
    description: "Cruscotto esecutivo offline per visualizzazione telemetrica e matrice dei 10 documenti"
  - name: "Local Encrypted Vault"
    type: "toolchain"
    description: "Gestore crittografico AES-256-GCM per secret aziendali e URI vault://"
  - name: "Zero-Hallucination Policy"
    type: "pattern"
    description: "Politica che vieta dati tecnici inventati, forzando tag DA-RICHIEDERE e grounding rigoroso"

relations:
  - targetTitle: "Indice Generale della Documentazione ITInfra"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.95
    description: "Indice master navigazionale della suite documentale"
  - targetTitle: "Guida all'Uso con Agenti AI e Framework Agentici"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "extends"
    weight: 1.0
    description: "Estensione procedurale del workflow di intervista a turni con l'assistente agentico"
  - targetTitle: "Manuale Operativo CLI ITInfra"
    targetId: "guide-itinfra-cli-manual-01"
    relationType: "references"
    weight: 0.9
    description: "Manuale di riferimento per i comandi CLI scripts/itinfra.py"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 0.95
    description: "Attuazione operativa della specifica architetturale dell'assistente"
  - targetTitle: "Guida all'Architettura Local Workspace & Central Publish"
    targetId: "guide-local-workspace-central-publish-01"
    relationType: "depends_on"
    weight: 0.85
    description: "Architettura di staging locale e sincronizzazione centrale"
---

# Guida Operativa — Pipeline di Creazione Guidata OKF v0.2 con Antigravity

## 1. Visione d'Insieme & Filosofia Architetturale

La pipeline di gestione della creazione guidata documentale di **ITInfra** trasforma il processo tradizionale di redazione tecnica — spesso disorganizzato, soggetto a errori e allucinazioni — in un **flusso ingegneristico deterministico, atomico e a zero attrito**.

### 🌟 Principi Guida del Design:
1. **100% Offline-First & Zero-Dipendenze**: Nessun server MCP esterno, demone in background o microservizio REST API. Tutta la suite opera su **Python nativo standard, file Markdown su filesystem locale, Git e share SMB aziendale**.
2. **Sinergia Bimodale (UI Visiva + Chat Agentica)**: 
   - La **Generative UI** funge da cabina di pilotaggio e telemetria visiva (*"Cosa c'è e cosa manca?"*).
   - L'**Agente AI** opera come architetto tecnico ed esecutore (*"Come progettare la rete e redigere i documenti?"*).
3. **Politica Rigorosa Zero-Hallucination**: È severamente vietato inventare subnet, IP, VLAN, MAC address o configurazioni hardware non dichiarate. I dati mancanti vengono tassativamente etichettati con `<DA-RICHIEDERE>` e tracciati come Open Issues.
4. **Resilienza Trasparente (Auto-Healing)**: Se un operatore lancia lo scaffolding su un progetto non inizializzato, il motore crea automaticamente il manifesto con parametri di default e procede senza sollevare eccezioni bloccanti.

---

## 2. Diagramma di Flusso della Pipeline End-to-End

```text
========================================================================================================
             PIPELINE DI CREAZIONE GUIDATA OKF v0.2 CON GOOGLE ANTIGRAVITY (ITINFRA)
========================================================================================================

   INGEGNERE IT / TECNICO                            GOOGLE ANTIGRAVITY / CLAUDE CODE
  +----------------------+                          +-----------------------------------+
  |   Chat Antigravity   | <--- Zero-Search ------> | Fast-Path Rule (00-fastpath.md)   |
  |   o Terminale CMD    |      Deterministic       | Trigger: "start <slug>", "ui", ecc.|
  +----------+-----------+                          +-----------------+-----------------+
             |                                                        |
             | Invoca il comando (es. 'start demo-aure')              | Delega a scripts/itinfra.py
             v                                                        v
  +-------------------------------------------------------------------------------------+
  |                             ITINFRA CORE CLI ENGINE                                  |
  |                           (scripts/itinfra.py start)                                |
  +------------------------------------------+------------------------------------------+
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
                   v [FASE 1: ONBOARDING & AUTO-HEALING]               v [FASE 2: CRUSCOTTO UI]
  +----------------------------------+               +----------------------------------+
  |    Auto-Init Project Manifest    |               | Generative UI Cockpit (Zero-CDN) |
  | projects/<slug>/manifest.yaml    |               | enterprise_dashboard.html        |
  | _scratchpad.md (Staging Memory)  |               | <agent-embed src="...">          |
  +----------------+-----------------+               +-----------------+----------------+
                   |                                                   |
                   v [FASE 3: AUTO-SCAFFOLDING ATOMICO]                | - Matrice 10 Doc a colori
  +--------------------------------------------------+                 | - Telemetria Share Master
  |      ProjectScaffolder (itinfra_scaffold.py)     |                 | - Click-to-Action comandi
  |   Propaga Ground Truth (Subnet, AD, HW, SLA)     |                 |
  |   Genera i 10 Documenti OKF v0.2 in projects/    |                 |
  |   Applica Zero-Hallucination: <DA-RICHIEDERE>    | <---------------+
  +------------------------+-------------------------+
                           |
                           v [FASE 4: INTERVISTA GUIDATA A BLOCCHI IN CHAT]
  +-------------------------------------------------------------------------------------+
  |                       AGENTIC INTERVIEW WIZARD (Chat AI)                            |
  |  - Blocco 1: Scope, Stakeholder e Target SLA (RTO / RPO)                            |
  |  - Blocco 2: Topologia, Supernetting IPv4, VLAN e Gateway (Diagrammi Mermaid)       |
  |  - Blocco 3: Compute, Storage e Hypervisor (Core, RAM, Datastore)                   |
  |  - Blocco 4: Sicurezza, Matrice Accessi & Local AES-256 Vault (vault://...)         |
  |  - Blocco 5: Metodi Operativi MOP, Piano Rollback e Test ATP                        |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 5: CRITTOGRAFIA DEI SEGRETI]
  +-------------------------------------------------------------------------------------+
  |                    LOCAL ENCRYPTED SECRET VAULT (AES-256-GCM)                       |
  |              Zero Secrets in Chiaro: solo URI vault://it/projects/...               |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 6: QUALITY GATE LOCALE & LINTER]
  +-------------------------------------------------------------------------------------+
  |                        OKF v0.2 FORMAL VALIDATOR & AUDIT                            |
  |  - it validate: Schema OKF v0.2, frontmatter canonico, entita' e relazioni D3       |
  |  - it audit-consistency: Coerenza semantica incrociata tra Manifest, LLD e As-Built|
  |  - it test-suite: Collaudo Enterprise 13 moduli (100% Pass Rate)                   |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 7: PUBBLICAZIONE MASTER CENTRALE]
  +-------------------------------------------------------------------------------------+
  |                          CENTRAL PUBLISH & DISTRIBUTION                             |
  |  - it publish <slug>: Quality Gate convalidato -> Sync su \fileserv01\dati01\...    |
  |  - git commit & push: Versionamento permanente tracciato su branch main             |
  +-------------------------------------------------------------------------------------+
```

---

## 3. Le 7 Fasi Dettagliate della Pipeline

### Fase 1: Innesco Zero-Search & Auto-Healing Onboarding
- **Trigger**: L'ingegnere scrive in chat `start <slug>` (es. `start demo-aure`) oppure lancia dal terminale `it start demo-aure`.
- **Fast-Path**: Le direttive in `.agents/rules/00-fastpath.md` impongono all'agente di non eseguire ricerche su disco (`find_by_name`, `grep_search`), avviando direttamente in 0 secondi `python scripts/itinfra.py start <slug>`.
- **Auto-Healing**:
  - Se la cartella `projects/<slug>/` o il file `project-manifest.yaml` non esistono, vengono generati istantaneamente a partire dal template master con valori sanitizzati.
  - Viene inizializzato `projects/<slug>/_scratchpad.md` per la memoria di staging locale anti-inquinamento.

### Fase 2: Visualizzazione nel Cruscotto Esecutivo (Generative UI)
- Viene generato il file autonomo `projects/enterprise_dashboard.html` e iniettato nella chat tramite il tag `<agent-embed src="file:///...">`.
- **Matrice dei 10 Documenti**: Mostra istantaneamente lo stato di ciascuna tipologia documentale (`Approved` in verde, `In-Review` in ciano, `Draft` in giallo, `Missing` in grigio).
- **Click-to-Action**: L'ingegnere non deve memorizzare la sintassi CLI: la UI fornisce pulsanti che copiano i comandi precisi negli appunti.

### Fase 3: Auto-Scaffolding Deterministico
- Il modulo `scripts/itinfra_scaffold.py` legge il **Ground Truth** dal manifesto di progetto:
  - Identificativi: `project_id`, `project_name`, `customer`, `lead_architect`, `created_at`.
  - Parametri di rete: `supernet_ipv4`, `active_directory_domain`, `dc_ip`, `core_switch_model`.
  - Infrastruttura e SLA: `hypervisor_host`, `tier1_rto`, `tier1_rpo`, prefisso vault.
- I 10 template conformi OKF v0.2 vengono istanziati nella cartella del cliente con la sostituzione atomica di oltre 250 variabili.
- Tutti i campi non desumibili dal manifesto vengono contrassegnati con `<DA-RICHIEDERE>`, azzerando ogni rischio di allucinazione.

### Fase 4: Intervista Guidata a Blocchi Tematici (Chat Agentica)
L'ingegnere apre la chat per completare i documenti specifici (es. `01-RSD-URS.md` o `03-LLD.md`). L'agente AI segue rigorosamente l'intervista per blocchi tematici:
- **Blocco 1 — Scope & SLA**: Definizione obiettivi, vincoli di progetto e target RTO/RPO.
- **Blocco 2 — Rete & Topologia**: Calcolo delle subnet (/24, /27), gateway, VLAN ID (Mgmt, Server, Client, iSCSI, DMZ) e generazione diagrammi Mermaid logici.
- **Blocco 3 — Compute & Storage**: Dimensionamento host fisici (Dell/HPE), vCPU, allocazione RAM, datastore ZFS/Ceph e storage repository.
- **Blocco 4 — Sicurezza & Matrice Accessi**: Regole firewall di inter-VLAN routing, segmentazione NIS2 e credenziali amministrative.
- **Blocco 5 — Operations & ATP**: Cronoprogramma di rollout (MOP), piano di ripristino in caso di fallimento (Rollback) e casi di test di collaudo.

### Fase 5: Gestione Sicura Credenziali (Local Secret Vault)
- È severamente vietato inserire password in chiaro nei documenti Markdown o nei commit Git.
- L'ingegnere e l'agente archiviano i secret nel vault locale AES-256-GCM:
  ```bash
  it vault set <slug> fw/admin --value "SegretoSicuro2026!"
  ```
- Nei documenti OKF v0.2 viene registrato esclusivamente il puntatore:
  `admin_password_ref: "vault://it/projects/<slug>/fw/admin"`

### Fase 6: Quality Gate Formale & Linter OKF v0.2
Prima di promuovere un documento a `status: in-review` o `approved`:
1. **Linter OKF v0.2**: `it validate projects/<slug>/<file>.md`
   - Valida la presenza di tutti i campi canonici (`okf_version`, `entities`, `relations`).
   - Verifica la coerenza tra `related_docs` e gli archi del grafo D3.
2. **Audit Coerenza Semantica**: `it audit-consistency <slug>`
   - Controlla che le subnet dichiarate nel manifesto coincidano con l'LLD e l'As-Built.
3. **Enterprise Test Suite**: `it test-suite`
   - Esegue tutti i 13 moduli di collaudo del sistema, garantendo il 100% di conformità.

### Fase 7: Pubblicazione Master Centrale & Git Sync
Quando il progetto è completato e validato:
- L'operatore lancia `it publish <slug>`.
- Il Quality Gate verifica l'assenza di errori bloccanti e sincronizza in modo differenziale la cartella del progetto verso la share master centrale (`\\fileserv01\dati01\workaure\projects\<slug>`).
- L'ingegnere effettua il commit e push Git per il tracciamento permanente della release.

---

## 4. Matrice delle 7 Fasi e dei 10 Documenti OKF v0.2

| Fase Ciclo IT | Codice Documento | Tipo Canonico OKF | Scopo Ingegneristico |
| :--- | :--- | :--- | :--- |
| **1. Assessment** | `01-RSD-URS.md` | `specification` | Analisi preliminare, requisiti utente e vincoli di business |
| **2. Design** | `02-HLD.md` | `architecture` | Architettura concettuale ad alto livello e principi guida |
| **2. Design** | `03-LLD.md` | `architecture` | Design esecutivo: IPAM, VLAN, elevazioni rack, ACL firewall |
| **3. Procurement** | `04-MOP.md` | `guide` | Metodo di procedura passo-passo per il rollout sul campo |
| **3. Procurement** | `05-Rollback.md` | `guide` | Piano di ripristino di emergenza e fallback procedurale |
| **4-5. Implementation** | `06-As-Built.md` | `architecture` | Configurazione reale installata, cablaggi, seriali e MAC |
| **6. Testing** | `07-ATP.md` | `specification` | Piano di collaudo, checklist funzionali e accettazione cliente |
| **7. Go-Live** | `08-SOP-Runbook.md` | `guide` | Procedure operative standard, gestione backup e manutenzione |
| **7. Go-Live** | `09-Handover-Inventory.md` | `specification` | Passaggio di consegne, inventario cespiti e garanzie hardware |
| **Post-Go-Live** | `10-RCA-Troubleshooting.md` | `guide` | Root Cause Analysis per incidenti operativi e correttivi CAPA |

---

## 5. Sintesi Operativa

Grazie a questa pipeline integrata, Google Antigravity e l'infrastruttura ITInfra offrono:
- **Velocità**: Creazione di un nuovo cliente in **meno di 1 secondo** con tutti i 10 template precompilati.
- **Affidabilità**: Eliminazione delle allucinazioni grazie all'ereditarietà deterministica dal manifesto.
- **Governance**: Piena tracciabilità ontologica D3, crittografia AES-256 dei secret e conformità agli standard NIS2 e ISO 27001.
