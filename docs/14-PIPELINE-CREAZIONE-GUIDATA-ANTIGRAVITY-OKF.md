---
okf_version: "0.2"
id: "guide-pipeline-creazione-guidata-antigravity-01"
title: "Guida Operativa — Pipeline di Creazione Guidata OKF v0.2 con Antigravity"
type: "guide"
domain: "IT Infrastructure & Agentic Documentation Pipeline"
tags: ["okf-v0.2", "pipeline", "antigravity", "automation", "scaffolding", "generative-ui", "zero-hallucination", "drift-guard", "reconciliation", "mermaid-linter"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Automation Suite"
phase: 0
author: "matrixNeo76"
reviewer: "System Architects & DevOps Team"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture & Knowledge Engineering"
status: "approved"
version: "1.1.0"
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
    description: "Motore scripts/itinfra_scaffold.py per propagazione automatica e supporto phased scaffolding"
  - name: "Reverse Reconciliation Engine"
    type: "toolchain"
    description: "Motore scripts/itinfra_reconcile.py per allineamento a ritroso da As-Built verso il manifesto"
  - name: "Checkpointed Modular Interview"
    type: "pattern"
    description: "Pattern di raccolta requisiti a checkpoint atomici per prevenire saturazione del contesto LLM"
  - name: "Generative UI Cockpit"
    type: "toolchain"
    description: "Cruscotto esecutivo offline per visualizzazione telemetrica e matrice dei 10 documenti"
  - name: "Local Encrypted Vault"
    type: "toolchain"
    description: "Gestore crittografico AES-256-GCM con input mascherato anti-leak e team bundling (.vbundle)"
  - name: "Zero-Hallucination Policy"
    type: "pattern"
    description: "Politica che vieta dati tecnici inventati, forzando tag DA-RICHIEDERE e grounding rigoroso"
  - name: "Remote Drift & Conflict Guard"
    type: "pattern"
    description: "Meccanismo di protezione da sovrascritture su storage SMB tramite lock distribuito e manifest SHA-256"

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
    weight: 0.9
    description: "Architettura di staging locale e sincronizzazione centrale con lock distribuito e drift detection"
---

# Guida Operativa — Pipeline di Creazione Guidata OKF v0.2 con Antigravity

## 1. Visione d'Insieme & Filosofia Architetturale

La pipeline di gestione della creazione guidata documentale di **ITInfra** trasforma il processo tradizionale di redazione tecnica — spesso disorganizzato, frammentato, soggetto a errori e allucinazioni — in un **flusso ingegneristico deterministico, atomico, resiliente e a zero attrito**.

### 🌟 Principi Guida del Design Ingegneristico:
1. **100% Offline-First & Zero-Dipendenze Esterne**: Nessun server MCP esterno, demone in background o microservizio REST API da manutenere. Tutta la suite opera esclusivamente su **Python standard, file system locale su SSD, Git e share SMB aziendale**.
2. **Sinergia Bimodale (UI Visiva + Chat Agentica)**: 
   - La **Generative UI** funge da cabina di pilotaggio e telemetria visiva (*"Cosa c'è e cosa manca?"*).
   - L'**Agente AI** opera come architetto tecnico ed esecutore (*"Come progettare la rete e redigere i documenti?"*).
3. **Politica Rigorosa Zero-Hallucination & Strict Grounding**: È severamente vietato inventare subnet, IP, VLAN, MAC address, seriali o configurazioni hardware non dichiarate. I dati mancanti vengono tassativamente etichettati con `<DA-RICHIEDERE>` e tracciati come Open Issues.
4. **Resilienza Trasparente (Auto-Healing & Typo Guard)**: Se un operatore lancia lo scaffolding su un progetto non inizializzato, il motore crea automaticamente il manifesto con parametri di default e procede senza errori bloccanti. La Typo Guard integrata (`difflib`) intercetta refusi su progetti esistenti prevenendo cartelle orfane.
5. **Anti-Leak & Zero Secret Exposure**: Le credenziali non transitano mai in chiaro nella chat o nei log della shell CLI (`--value` deprecato a favore di input mascherato da `getpass`, standard input e variabile d'ambiente). Nei documenti Markdown sono ammessi unicamente URI sicuri `vault://it/projects/<slug>/...`.
6. **Protezione da Drift e Conflitti su Storage Remoto**: La pubblicazione centrale è protetta da lock atomico O_CREAT|O_EXCL (`.publish_<slug>.lock`) e tracciata tramite impronta SHA-256 (`.publish_manifest.json`), impedendo sovrascritture accidentali di modifiche effettuate direttamente sulla share di rete.

---

## 2. Diagramma di Flusso della Pipeline End-to-End

```text
========================================================================================================
             PIPELINE DI CREAZIONE GUIDATA OKF v0.2 CON GOOGLE ANTIGRAVITY (ITINFRA)
========================================================================================================

   INGEGNERE IT / TECNICO                            GOOGLE ANTIGRAVITY / CLAUDE CODE
  +----------------------+                          +-----------------------------------+
  |   Chat Antigravity   | <--- Zero-Search ------> | Fast-Path Rule (00-fastpath.md)   |
  |   o Terminale CMD    |      Deterministic       | Trigger: "start <slug>", "ui", ecc|
  +----------+-----------+                          +-----------------+-----------------+
             |                                                        |
             | Invoca il comando (es. 'start demo-aure')              | Delega a scripts/itinfra.py
             v                                                        v
  +-------------------------------------------------------------------------------------+
  |                             ITINFRA CORE CLI ENGINE                                  |
  |                           (scripts/itinfra.py start)                                |
  |              - Typo Guard Integrato: intercetta errori di digitazione               |
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
                   v [FASE 3: AUTO-SCAFFOLDING A MILESTONE]            | - Matrice 10 Doc a colori
  +--------------------------------------------------+                 | - Telemetria Share Master
  |      ProjectScaffolder (itinfra_scaffold.py)     |                 | - Click-to-Action comandi
  |   Propaga Ground Truth (Subnet, AD, HW, SLA)     |                 |
  |   Supporto Milestone: --phase [assessment|...|all|                 |
  |   Applica Zero-Hallucination: <DA-RICHIEDERE>    | <---------------+
  +------------------------+-------------------------+
                           |
                           v [FASE 4: INTERVISTA A CHECKPOINT ATOMICI]
  +-------------------------------------------------------------------------------------+
  |                 CHECKPOINTED MODULAR INTERVIEW (scripts/itinfra_interview.py)       |
  |  Previene saturazione contesto LLM salvando lo stato incrementale su disco:         |
  |  - Blocco 1: Scope, Stakeholder e Target SLA (RTO / RPO)                            |
  |  - Blocco 2: Topologia, Supernetting IPv4, VLAN e Gateway (Diagrammi Mermaid)       |
  |  - Blocco 3: Compute, Storage e Hypervisor (Core, RAM, Datastore ZFS/Ceph)          |
  |  - Blocco 4: Sicurezza, Matrice Accessi & Local AES-256 Vault (vault://...)         |
  |  - Blocco 5: Metodi Operativi MOP, Piano Rollback e Test ATP                        |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 5: CRITTOGRAFIA DEI SEGRETI & ANTI-LEAK]
  +-------------------------------------------------------------------------------------+
  |                    LOCAL ENCRYPTED SECRET VAULT (AES-256-GCM)                       |
  |  - Zero Cleartext nella Chat & Shell: input mascherato da getpass, stdin sicuro     |
  |  - Team Bundling (.vbundle) con PBKDF2 per scambio protetto multi-operatore         |
  |  - Solo URI vault://it/projects/<slug>/... nei documenti Markdown                   |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 6: QUALITY GATE LOCALE & LINTER]
  +-------------------------------------------------------------------------------------+
  |                     OKF v0.2 FORMAL VALIDATOR, MERMAID LINTER & AUDIT               |
  |  - it validate: Schema OKF v0.2, frontmatter canonico, entita' e relazioni D3       |
  |  - Mermaid Syntax Linter: validazione 24 tipi di diagramma e bilanciamento parentesi|
  |  - Blocchi Canonici YAML: ```yaml:inventory e ```yaml:network senza fragilita' regex|
  |  - it audit-consistency: Coerenza semantica incrociata tra Manifest, LLD e As-Built|
  |  - it test-suite: Collaudo Enterprise 15 moduli (100% Pass Rate)                   |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 7: PUBBLICAZIONE MASTER CON DRIFT GUARD]
  +-------------------------------------------------------------------------------------+
  |                     CENTRAL PUBLISH & CONCURRENCY-SAFE DISTRIBUTION                 |
  |  - it publish <slug>: Staging-then-swap atomico e Lock Remoto (.publish_<slug>.lock)|
  |  - Remote Drift Detection: impronta crittografica SHA-256 (.publish_manifest.json) |
  |  - git commit & push: Versionamento permanente tracciato su branch main             |
  +------------------------------------------+------------------------------------------+
                                             |
                                             v [FASE 8: RICONCILIAZIONE INVERSA SUL CAMPO]
  +-------------------------------------------------------------------------------------+
  |                REVERSE RECONCILIATION ENGINE (scripts/itinfra_reconcile.py)         |
  |  - it reconcile <slug>: Estrae variazioni da 06-As-Built.md (Deviazioni §3, HW, IP) |
  |  - Genera il Drift Report rispetto al manifesto di progetto                         |
  |  - Propaga a ritroso i parametri verificati dal collaudo reale (Backporting sicuro) |
  +-------------------------------------------------------------------------------------+
```

---

## 3. Le 8 Fasi Dettagliate della Pipeline

### Fase 1: Innesco Zero-Search, Typo Guard & Onboarding All-in-One
- **Trigger Rapido**: L'ingegnere scrive in chat `start <slug>` (es. `start demo-aure`) oppure lancia dal terminale `it start demo-aure`.
- **Fast-Path Deterministico**: Le regole di sistema in `.agents/rules/00-fastpath.md` vietano all'agente di eseguire ricerche esplorative su disco (`find_by_name`, `grep_search`), avviando in 0 secondi `python scripts/itinfra.py start <slug>`.
- **Typo Guard Integrata**: Se l'operatore digita per errore un nome errato (es. `demo-auire`), il modulo `difflib` intercetta la somiglianza (>= 0.70), blocca la creazione di cartelle orfane e suggerisce il progetto corretto (`demo-aure`). Il flag `--force` permette di forzare la creazione.
- **Auto-Healing**:
  - Se la cartella `projects/<slug>/` o il file `project-manifest.yaml` non esistono, vengono generati istantaneamente a partire dal template master con valori sanitizzati.
  - Viene inizializzato `projects/<slug>/_scratchpad.md` per la memoria di staging locale anti-inquinamento.

### Fase 2: Visualizzazione nel Cruscotto Esecutivo (Generative UI)
- Viene generato il file autonomo `projects/enterprise_dashboard.html` e iniettato nella chat tramite il tag `<agent-embed src="file:///...">`.
- **Matrice dei 10 Documenti**: Mostra istantaneamente lo stato di ciascuna tipologia documentale (`Approved` in verde, `In-Review` in ciano, `Draft` in giallo, `Missing` in grigio).
- **Click-to-Action**: L'ingegnere non deve memorizzare la sintassi CLI: la UI fornisce pulsanti interattivi che copiano i comandi precisi negli appunti.

### Fase 3: Auto-Scaffolding Deterministico & Supporto Phased Milestones
- Il modulo `scripts/itinfra_scaffold.py` estrae il **Ground Truth** dal manifesto di progetto:
  - Identificativi: `project_id`, `project_name`, `customer`, `lead_architect`, `created_at`.
  - Parametri di rete: `supernet_ipv4`, `active_directory_domain`, `dc_ip`, `core_switch_model`.
  - Infrastruttura e SLA: `hypervisor_host`, `tier1_rto`, `tier1_rpo`, prefisso vault.
- **Phased Scaffolding (`--phase`)**: Per progetti complessi, l'ingegnere può evitare il rumore documentale precoce (Day-1 clutter) generando solo i documenti pertinenti alla milestone corrente:
  - `assessment`: genera solo `01-RSD-URS.md`.
  - `design`: genera i documenti 01, 02 (`HLD`), 03 (`LLD`).
  - `staging`: aggiunge 04 (`MOP`) e 05 (`Rollback`).
  - `deployment`: aggiunge 06 (`As-Built`).
  - `testing`: aggiunge 07 (`ATP`).
  - `handover`: aggiunge 08 (`SOP-Runbook`) e 09 (`Handover-Inventory`).
  - `all`: genera l'intero ciclo a 10 documenti (incluso 10 `RCA-Troubleshooting`).
- I campi non desumibili dal manifesto vengono contrassegnati con `<DA-RICHIEDERE>`, azzerando ogni rischio di allucinazione.

### Fase 4: Intervista Guidata a Checkpoint Atomici (Chat Agentica)
Per prevenire la saturazione del contesto dell'LLM (Context Window Saturation) causata da prompt monolitici, l'intervista tecnica viene condotta a **blocchi modulari salvati su disco** (`scripts/itinfra_interview.py`):
- **Blocco 1 — Scope & SLA**: Definizione obiettivi, stakeholder, vincoli di progetto e target RTO/RPO.
- **Blocco 2 — Rete & Topologia**: Calcolo supernetting (/24, /27), gateway, VLAN ID (Mgmt, Server, Client, iSCSI, DMZ) e generazione schemi Mermaid logici.
- **Blocco 3 — Compute & Storage**: Dimensionamento host fisici (Dell/HPE), socket vCPU, RAM, datastore ZFS/Ceph e storage repository.
- **Blocco 4 — Sicurezza & Matrice Accessi**: Regole firewall di inter-VLAN routing, segmentazione NIS2 e credenziali amministrative.
- **Blocco 5 — Operations & ATP**: Cronoprogramma di rollout (MOP), piano di ripristino di emergenza (Rollback) e casi di test di collaudo e accettazione.
Ogni blocco salva lo stato in `_interview_state.json` e aggiorna direttamente `project-manifest.yaml`.

### Fase 5: Gestione Sicura Credenziali (Local Secret Vault & Anti-Leak)
- **Direttiva Tassativa Anti-Leak**: È severamente vietato incollare password o secret in chiaro nella chat o utilizzare l'argomento `--value "<secret>"` nella shell.
- L'ingegnere e l'agente archiviano i secret nel vault locale cifrato AES-256-GCM tramite prompt mascherato o stdin sicuro:
  ```powershell
  # Input mascherato da getpass:
  it vault set <slug> fw/admin

  # Input da pipeline PowerShell (senza traccia nella shell history):
  Get-Content secret.txt | it vault set <slug> fw/admin
  ```
- Nei documenti OKF v0.2 viene registrato esclusivamente il puntatore URI:
  `admin_password_ref: "vault://it/projects/<slug>/fw/admin"`
- **Team Bundling (`.vbundle`)**: I secret possono essere trasferiti in modo cifrato tra workstation dei tecnici tramite `it vault export-bundle` e `it vault import-bundle` protetti da passphrase di team (PBKDF2).

### Fase 6: Quality Gate Formale, Fenced YAML & Linter Mermaid
Prima di promuovere un documento a `status: in-review` o `approved`:
1. **Linter OKF v0.2 & Mermaid Syntax Linter**: `it validate projects/<slug>/<file>.md`
   - Valida la presenza dei campi canonici OKF v0.2 (`okf_version`, `entities`, `relations`).
   - Verifica la conformità sintattica dei diagrammi ```mermaid (24 tipi canonici), il bilanciamento delle parentesi `[ ]`, `( )`, `{ }` e le best practice di escaping delle label.
2. **Audit Coerenza Semantica & Semantic Drift Guard**: `it audit-consistency <slug>`
   - Parsing prioritario dei blocchi ```yaml:inventory e ```yaml:network che eliminano la fragilità delle regex sulle tabelle Markdown.
   - Controlla che le subnet dichiarate nel manifesto coincidano con l'LLD e l'As-Built.
   - **D3 Semantic Drift Check**: Rileva dispositivi nei blocchi YAML non ancora censiti nel grafo OKF v0.2 ed emette `[WARN: Unmapped Entity in OKF Graph]`.
3. **Enterprise Test Suite**: `it test-suite`
   - Esegue tutti i **16 moduli di collaudo del sistema** garantendo il 100% di conformità.

### Fase 7: Pubblicazione Master Centrale, Lock Resiliente & VPN Fast Path
Quando il progetto è completato e validato:
- L'operatore lancia `it publish <slug>`.
- **Remote Lock Distribuito con Auto-Break**: Il publisher acquisisce un lock atomico `O_CREAT | O_EXCL` (`.publish_<slug>.lock`) sulla share SMB con TTL di 300s. Se un processo concorrente precedente è crashato lasciando un lock orfano, il publisher lo rimuove automaticamente; in casi straordinari, l'operatore può forzare la rimozione con `--break-lock`.
- **Stat-First Fast Path per VPN/SMB**: Il motore archivia `size` e timestamp `mtime_epoch` in `.publish_manifest.json`. Se il file remoto coincide in dimensioni e timestamp, evita il ricalcolo SHA-256 byte-a-byte, garantendo pubblicazioni istantanee anche su connessioni geografiche lente.
- **Remote Drift Detection**: Il motore confronta i file remoti con l'impronta registrata in `.publish_manifest.json` (SHA-256). Se rileva modifiche manuali o non coordinate sulla share master, **blocca la pubblicazione** con `[CONFLITTO REMOTO RILEVATO]` a tutela del lavoro svolto, a meno del flag esplicito `--force`.
- **Staging-then-Swap Atomico**: I file vengono copiati in una cartella di staging temporanea remota e spostati in blocco nella cartella definitiva, azzerando il rischio di corruzione da disconnessioni di rete.
- **Vault Team Bundling & TTL**: I secret possono essere scambiati via `.vbundle` con scadenza temporale (default 168h / 7 giorni) conforme a NIS2/ISO 27001 (`--ttl-hours`, bypass con `--force-expired`) e ri-cifrati atomicamente con `it vault rotate-key <slug>`.

### Fase 8: Riconciliazione Inversa da As-Built a Manifesto
Durante o dopo l'installazione sul campo (Fasi 4 e 5), le configurazioni reali possono divergere dal design iniziale:
- L'ingegnere esegue il motore di riconciliazione inversa:
  ```bash
  it reconcile <slug> [--dry-run]
  ```
- Il modulo `scripts/itinfra_reconcile.py` analizza `06-As-Built.md` (§3 Tabella Deviazioni, §4 Apparati Hardware, §5 Indirizzamento IP e blocchi ```yaml:inventory).
- Calcola il **Drift Report** dettagliato e aggiorna automaticamente `project-manifest.yaml`, garantendo che il manifesto rimanga la sorgente di verità assoluta (*Single Source of Truth*) per tutta la vita utile dell'infrastruttura.

---

## 4. Matrice delle 7 Fasi e dei 10 Documenti OKF v0.2

| Fase Ciclo IT | Codice Documento | Tipo Canonico OKF | Scopo Ingegneristico | Milestone Scaffolding |
| :--- | :--- | :--- | :--- | :--- |
| **1. Assessment** | `01-RSD-URS.md` | `specification` | Analisi preliminare, requisiti utente e vincoli di business | `--phase assessment` |
| **2. Design** | `02-HLD.md` | `architecture` | Architettura concettuale ad alto livello e principi guida | `--phase design` |
| **2. Design** | `03-LLD.md` | `architecture` | Design esecutivo: IPAM, VLAN, elevazioni rack, ACL firewall | `--phase design` |
| **3. Procurement** | `04-MOP.md` | `guide` | Metodo di procedura passo-passo per il rollout sul campo | `--phase staging` |
| **3. Procurement** | `05-Rollback.md` | `guide` | Piano di ripristino di emergenza e fallback procedurale | `--phase staging` |
| **4-5. Implementation** | `06-As-Built.md` | `architecture` | Configurazione reale installata, cablaggi, seriali e MAC | `--phase deployment` |
| **6. Testing** | `07-ATP.md` | `specification` | Piano di collaudo, checklist funzionali e accettazione cliente | `--phase testing` |
| **7. Go-Live** | `08-SOP-Runbook.md` | `guide` | Procedure operative standard, gestione backup e manutenzione | `--phase handover` |
| **7. Go-Live** | `09-Handover-Inventory.md` | `specification` | Passaggio di consegne, inventario cespiti e garanzie hardware | `--phase handover` |
| **Post-Go-Live** | `10-RCA-Troubleshooting.md` | `guide` | Root Cause Analysis per incidenti operativi e correttivi CAPA | `--phase all` |

---

## 5. Sintesi Operativa & Benefici Ingegneristici

Grazie a questa pipeline integrata e blindata, Google Antigravity e l'infrastruttura ITInfra garantiscono:
- **Zero Attrito**: Creazione di un nuovo cliente in **meno di 1 secondo** con auto-scaffolding progressivo e cruscotto visuale immediato.
- **Zero Allucinazioni**: Grounding rigoroso dal manifesto condiviso e divieto assoluto di inventare dati tecnici non forniti.
- **Zero Secret Leaks**: Politica anti-leak rigorosa con cifratura AES-256-GCM, input mascherato e team bundles protetti.
- **Zero Concorrenza Silenziosa**: Lock atomici distribuiti su share SMB e fingerprinting crittografico SHA-256 contro il remote drift.
- **Piena Tracciabilità**: Ciclo chiuso con riconciliazione inversa continua da As-Built verso il manifesto di progetto.
