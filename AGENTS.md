# AGENTS.md — Istruzioni per agenti AI

> Questo file è letto automaticamente da Google Antigravity, Cursor, Aider, Continue, Cline, Roo Code e altri agenti che seguono la convenzione `AGENTS.md`. Per Claude Code vedere `CLAUDE.md` (contenuto equivalente).

---

## ⚡ 0. REGOLA FONDAMENTALE: ZERO-SEARCH FAST-PATH & COMANDI DETERMINISTICI

> 🛑 **DIRETTIVA DI SISTEMA CRITICA PER L'AGENTE AI:**
> Se l'utente ti saluta (`ciao`, `buongiorno`), ti chiede **puoi aiutarmi ad utilizzare il nostro applicativo itinfra**, **cosa fa questo applicativo**, **come visualizzare i comandi**, **quali comandi sono disponibili**, o **come usare ITInfra**:
> ❌ **È SEVERAMENTE VIETATO usare tool di ricerca file (`find_by_name`, `grep_search`, `list_dir`, scansioni generiche).** Tu conosci già perfettamente questo applicativo, non hai bisogno di cercare tra i file per orientarti.
> ✅ **Rispondi ALL'ISTANTE (0 secondi) e in modo DETERMINISTICO** presentando la Scheda Operativa ITInfra qui sotto.

### 📋 Scheda Operativa di Risposta Immediata

Restituisci all'istante questo schema chiaro ed esaustivo:

👋 **Benvenuto in ITInfra!**
Questo è l'ambiente di lavoro per la documentazione tecnica, governance, automazione e collaudo di infrastrutture IT complesse su standard OKF v0.2.

### 🚀 Comandi Rapidi Disponibili (Zero Attrito)

| Azione Desiderata | Da Chat Antigravity (Scrivi semplicemente) | Da Terminale (Prompt / PowerShell) |
| :--- | :--- | :--- |
| **All-in-One: Avvia Progetto (Init+Scaffold+UI)** | `start <slug>` *(o `avvia <slug>`)* | `it start <slug>` |
| **Allineare Template e Motore** | `aggiorna` *(o `update`)* | `it update` *(oppure solo `update`)* |
| **Verificare Rete e Permessi** | `controlla` *(o `check`)* | `it check` |
| **Pubblicare Progetto su Server** | `pubblica <slug>` | `it publish <slug>` |
| **Inizializzare Nuovo Cliente** | `inizializza <slug>` | `it init <slug> --client "Nome" --name "Titolo"` |
| **Auto-Scaffold Template da Manifest** | `scaffold <slug>` | `it scaffold <slug>` |
| **Verificare Stato 7 Fasi** | `stato <slug>` | `it status <slug>` |
| **Valida Documento Attivo** | `valida` *(o tasto `Ctrl+Shift+B`)* | `it validate <percorso_file>` |
| **Ingestione Documenti Tecnici (OKF v0.2)** | `ingest <file>` | `it ingest <file> [--slug <slug>] [--apply]` |
| **Cruscotto Grafico Esecutivo** | `ui` *(o `dashboard`)* | `it ui` |
| **Collaudo Completo Sistema** | `test-suite` | `it test-suite` |
| **Avvio Quotidiano "1-Clic"** | *Doppio clic sull'icona Desktop:*<br>**`ITInfra - Aggiorna e Avvia`** | `it start` |

🖥️ *Per visualizzare il Cruscotto Esecutivo grafico con telemetria e azioni rapide, digita semplicemente **`ui`**.*

---

### ⚡ Esecuzione Deterministica dei Comandi a 1 Parola (Zero-Hesitation)
Se l'utente digita uno di questi trigger rapidi, **NON fare domande, NON chiedere conferme preliminari e NON cercare file**: esegui immediatamente il relativo comando:
- **`"start <slug>"`** o **`"avvia <slug>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py start <slug>` ed incorpora nella risposta il tag `<agent-embed src="file:///...">` stampato dall'output del comando.
- **`"ui"`** o **`"dashboard"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py ui` ed incorpora nella risposta il tag `<agent-embed src="file:///...">` stampato dall'output del comando. *(⚠️ CRITICO: NON inserire MAI codice HTML all'interno del tag `<agent-embed>`. Deve contenere ESCLUSIVAMENTE l'attributo `src="file:///..."`, altrimenti l'interfaccia mostrerà l'errore "Invalid embed:").*
- **`"ingest <file>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py ingest <file> [--slug <slug>] [--apply]` e mostra l'audit di estrazione.
- **`"aggiorna"`** o **`"update"`** $\rightarrow$ Esegui subito: `python scripts/itinfra_sync.py` e mostra il report di sincronizzazione.
- **`"controlla"`** o **`"check"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py check-share` e mostra la tabella di salute.
- **`"pubblica <slug>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py publish <slug>` e mostra l'esito del Quality Gate.
- **`"scaffold <slug>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py scaffold <slug>` (con auto-inizializzazione trasparente se non presente) e mostra il report di auto-scaffolding.
- **`"stato <slug>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py status <slug>` e mostra l'avanzamento delle 7 fasi.
- **`"valida <file>"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py validate <file>` e mostra il report del linter.
- **`"test-suite"`** $\rightarrow$ Esegui subito: `python scripts/itinfra.py test-suite --no-html`.

### 🛡️ Quando le Ricerche Sono Consentite
Il divieto di ricerca è circoscritto rigorosamente a saluti, comandi e orientamento. Le ricerche e l'uso degli strumenti sono pienamente permesse per:
- Interrogazione dell'inventario hardware enterprise: usa `python scripts/itinfra.py inventory find "<query>"`.
- Lavoro documentale ordinario su progetti specifici: consultazione e redazione di file in `projects/<slug>/`.

---

## 📸 Protocollo Obbligatorio: Analisi Visiva Nativa SOTA (Pixel-to-Markdown) & OKF v0.2

Quando l'utente carica o allega un file (PDF, distinta tecnica, datasheet apparato di rete, schema topologico, offerta fornitore, scansione, capitolato tecnico, certificazione cablaggio):
1. **Analisi Visiva Nativa (Pixel-Level)**:
   - È **obbligatorio analizzare il documento a livello visivo nativo** (pixel-to-markdown) per preservare l'ordine di lettura corretto su colonne complesse, grafici, firme, quote rack e tabelle dense.
   - Attiva il massimo livello di **Deep Thinking** per decifrare codici prodotto, porte di rete, interfacce, memorie, dischi e specifiche elettriche/fisiche.
2. **Generazione Immediata dell'Artefatto OKF v0.2 (`.md`)**:
   - Genera un file Artefatto Markdown conforme allo standard **OKF v0.2** composto da:
     - **Frontmatter YAML**:
       ```yaml
       ---
       okf_version: "0.2"
       id: "spec-[slug]-[titolo]-01"
       title: "[Titolo effettivo del documento]"
       type: "specification" # o "concept", "architecture"
       description: "[Abstract sintetico del contenuto tecnico]"
       domain: "IT Infrastructure & Technical Ingestion"
       tags:
         - "document-intelligence"
         - "estrazione-sota"
         - "okf-v0.2"
       generated.at: "[ISO 8601 Timestamp]"
       sources:
         - "file://@[nome_documento.pdf]"
       ---
       ```
     - **Corpo del Documento Markdown**:
       - `# Punti Chiave`: specifiche salienti, vincoli di compatibilità e vincoli d'alimentazione/rack con indicazione `[Pagina X]`.
       - `# Contenuto Semantico`: architettura, topologia e ruoli logici con capitoli e note.
       - `# Tabelle Estratte`: tutte le tabelle BOM (Bill of Materials) e matrici hardware interamente ricostruite cella per cella in Markdown, senza omettere alcun componente, part number o quantità.
3. **Zero-Hallucination & Provenance Guardrail**:
   - È **SEVERAMENTE VIETATO** inventare indirizzi IP, apparati di rete, VLAN o porte non dichiarati nel documento.
   - I dettagli di configurazione non presenti nel documento devono essere esplicitamente contrassegnati come `DA-RICHIEDERE` o `NOT_FOUND`.
4. **Alimentazione Deterministica delle Pipeline**:
   - L'artefatto OKF v0.2 viene memorizzato in `projects/<slug>/docs/` (o cartella documentale di progetto) e ingerito deterministicamente tramite la CLI (`it ingest <file.okf.md> --slug <slug> --apply`) per popolare `project-manifest.yaml`, `06-As-Built.md` e `09-Handover-Inventory.md`.

---

## 🔒 Principi di Integrazione Hub-and-Spoke con itinfra-business-ops
1. **Separation of Concerns**: I dati contabili, i margini di ricarico e la fatturazione risiedono esclusivamente nel repository commerciale `itinfra-business-ops`.
2. **Read-Only Bridge**: L'applicativo business legge in sola lettura i manifest e gli As-Built tecnici in `projects/<slug>/` per effettuare il cross-check di coerenza commerciale.
3. **Shared Customer Slug**: Lo slug cliente (es. `teatek-spa`, `severino-srl`) deve essere rigorosamente identico tra i due repository.

---

## Contesto del progetto

Sei un agente AI chiamato a **compilare template documentali** per progetti di infrastrutture IT. I template si trovano in `/download/templates/` e seguono lo standard **OKF v0.2 (Open Knowledge Format)** nella sua forma nativa, compatibile col parser `src/lib/okfParser.ts` del Knowledge Vault.

Lo schema YAML combina **campi canonici OKF v0.2** (riconosciuti dal parser e visualizzati nel grafo D3) + **metadati estesi IT** (preservati in `rawFrontmatter` per uso futuro).

Il ciclo lavorativo è composto da **7 fasi operative** che producono **10 tipologie documentali (inclusa gestione incidenti e RCA)**, mappate in `00-INDEX.md`:

| Fase | Documenti |
|------|-----------|
| 1. Assessment | RSD/URS |
| 2. Design | HLD, LLD |
| 3. Procurement & Staging | MOP, Rollback |
| 4. Racking & Cabling | (confluisce in As-Built) |
| 5. Commissioning | (confluisce in As-Built) |
| 6. Testing | ATP |
| 7. Go-Live | As-Built, SOP/Runbook, Handover & Inventory, RCA/Troubleshooting |

---

## Regole operative per la compilazione documenti

### 1. Prima di iniziare la compilazione (SOLO per documenti di progetto specifici)

> ⚠️ **ATTENZIONE:** Questa sezione si applica **ESCLUSIVAMENTE** quando l'utente ti chiede di compilare o aggiornare un documento di un cliente (es. in `projects/<slug>/`). **NON si applica MAI** a saluti, richieste di comandi o assistenza generale sull'uso di ITInfra.

1. **Leggi `00-INDEX.md`** per capire il contesto del ciclo e la posizione del documento che devi compilare.
2. **Consulta `depends_on`** nel frontmatter del template: sono documenti che DEVONO essere già compilati e che devi leggere come contesto.
3. **Identifica il `type`** del documento (RSD-URS, HLD, LLD, MOP, Rollback, As-Built, ATP, SOP-Runbook, Handover-Inventory) e segui le AI-INSTRUCTIONS specifiche nel blocco commentato in testa al template.

### 2. Regole di compilazione del frontmatter YAML (OKF v0.2 nativo)

Il frontmatter DEVE contenere i **campi canonici OKF v0.2** (riconosciuti dal parser) + i **metadati estesi IT** (preservati in `rawFrontmatter`).

#### Campi canonici OKF v0.2 (OBBLIGATORI)

- **`okf_version`**: DEVE essere la stringa `"0.2"` (letterale)
- **`id`**: DEVE essere univoco nel vault. Pattern: `<type-canonical>-<project_slug>-<subtype>-<seq>` (es. `architecture-acme-milano-lld-01`). NON lasciare il placeholder.
- **`title`**: titolo chiaro e descrittivo (max 120 caratteri)
- **`type`**: DEVE essere uno dei 6 tipi canonici OKF: `concept`, `architecture`, `guide`, `specification`, `tool_description`, `prompt_skill`. Mappatura documenti IT:
  - RSD/URS → `specification`
  - HLD → `architecture`
  - LLD → `architecture`
  - MOP → `guide`
  - Rollback → `guide`
  - As-Built → `architecture`
  - ATP → `specification`
  - SOP/Runbook → `guide`
  - Handover & Inventory → `specification`
  - RCA & Troubleshooting → `guide`
- **`domain`**: ambito tematico (es. `"IT Infrastructure & Requirements Engineering"`)
- **`tags`**: array di almeno 2 tag in lowercase. PRIMO tag DEVE essere `okf-v0.2` per tracciabilità.
- **`entities`**: array di almeno 1 entità con struttura `{name, type, description}`. I `type` canonici entità sono: `concept`, `framework`, `technology`, `toolchain`, `pattern`, `organization`, `specification`.
- **`relations`**: array (può essere vuoto `[]`) di relazioni con struttura `{targetTitle, targetId, relationType, weight, description}`. `relationType` dal vocabolario: `references`, `implements`, `depends_on`, `extends`, `documents`, `governs`, `constrains`, `relates_to`. `weight` float tra 0.1 e 1.0.

#### Metadati estesi IT (preservati in rawFrontmatter)

- **`project_id`**, **`project_name`**, **`site`**, **`customer`**, **`phase`** (1-7)
- **`author`**, **`reviewer`**, **`approver`**, **`owner_team`**
- **`status`**: `draft` → `in-review` → `approved` → `superseded`
- **`version`**: incrementa a ogni modifica sostanziale (0.1 → 0.2 → 1.0 quando approvato)
- **`created_at`**, **`updated_at`**: data ISO 8601 (YYYY-MM-DD)
- **`related_docs`**: array di ID (non titoli) dei documenti correlati. NON usare path file.
- **`depends_on`**: array di ID dei documenti che sono input per questo. DEVE coincidere con quanto dichiarato nel template.
- **`classification`**, **`retention`**, **`lang`**

**CRITICO — Coerenza `relations` vs `related_docs`**: per ogni entry in `related_docs`, creare una corrispondente entry in `relations` con lo stesso `targetId` e un `relationType` semanticamente appropriato. Questo garantisce che il grafo D3 del Knowledge Vault visualizzi correttamente le relazioni.

**Rimuovi TUTTI i placeholder** `<...>` prima di salvare.

### 3. Regole di compilazione del body Markdown

- **NON inventare dati** se non sono forniti. Usa `<DA-RICHIEDERE>` e segnala la lacuna nella sezione "Open Issues" o equivalente.
- **Rispetta le tabelle esistenti** nel template: aggiungi righe ma NON cambiare colonne senza esplicita richiesta.
- **Placeholder `<...>`** = valore singolo da sostituire. **`[...]`** = array da espandere. **`[ ]`** / **`[x]`** = checkbox da compilare.
- **Snippet di codice**: mantieni i blocchi di codice esistenti come riferimento; sostituisci i placeholder (`<hostname>`, `<IP>`, ecc.) con valori reali. NON rimuovere i commenti `!` o `#`.
- **Lingua**: il documento DEVE essere in italiano (campo `lang: it`), inclusi label, sezioni e istruzioni. Eventuali termini tecnici inglesi (HLD, LLD, MOP, ecc.) restano in inglese.
- **Nessun emoji** a meno che non sia esplicitamente richiesto dall'utente.

### 4. Gestione delle credenziali e Direttiva Anti-Leak

🛑 **DIVIETO ASSOLUTO CHAT LEAKAGE & CLI HISTORY LEAK:**
- È SEVERAMENTE VIETATO chiedere o consentire all'utente di digitare o incollare password, chiavi API o secret in chiaro all'interno della chat agentica o nei prompt LLM.
- È SEVERAMENTE VIETATO utilizzare l'argomento CLI `--value "<secret>"` in comandi di terminale pubblici per non esporre le credenziali nella cronologia della shell (`.bash_history` o PowerShell History).
- Per memorizzare secret nel vault, utilizzare sempre il prompt interattivo mascherato (`it vault set <slug> <key>`), input da standard input (`Get-Content secret.txt | it vault set <slug> <key>`) o la variabile d'ambiente `ITINFRA_SECRET_VAL`.
- **VIETATO inserire password, chiavi API, token o qualsiasi secret in chiaro nei documenti Markdown.** Usa SEMPRE riferimenti URI `vault://it/projects/<slug>/...` oppure il token `<DA-RICHIEDERE>`.

Usa SEMPRE riferimenti al vault aziendale:

```yaml
# Sbagliato
admin_password: "Admin123!"

# Corretto
admin_password_ref: "vault://it/<project>/fw-01/admin"
```

```markdown
# Sbagliato
Connettersi via SSH con utente `admin` e password `Admin123!`

# Corretto
Connettersi via SSH con utente `admin`; credenziali in `vault://it/<project>/fw-01/admin`
```

### 5. Gestione delle relazioni tra documenti

Le relazioni tra documenti sono espresse in DUE modi complementari, entrambi OBBLIGATORI per la piena integrazione col Knowledge Vault:

#### a) `relations` canoniche OKF (per grafo D3)
Nel frontmatter, array di oggetti strutturati:
```yaml
relations:
  - targetTitle: "LLD — Low-Level Design"
    targetId: "architecture-acme-milano-lld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'LLD espande l'HLD con dettagli puntuali"
```
Queste vengono parse da `okfParser.ts` e visualizzate come archi nel grafo D3 del Knowledge Vault.

#### b) `related_docs` estese IT (per tracciabilità logica)
Nel frontmatter, array di stringhe ID:
```yaml
related_docs:
  - "architecture-acme-milano-lld-01"
  - "guide-acme-milano-mop-01"
```

#### c) Wiki-links `[[id]]` nel body (per citazioni testuali)
Nel corpo Markdown, sintassi Obsidian/Logsec:
```markdown
L'HLD fa riferimento ai requisiti definiti in [[specification-acme-milano-rsd-01]].
```

Il KnowledgeGraph del Vault ha 5 livelli di correlazione: il 1° livello usa `relations` canoniche, il 3° livello usa le citazioni testuali `[[id]]`.

**Regole**:
- Usa l'ID completo (es. `architecture-acme-milano-lld-01`), NON il titolo
- NON creare link a documenti che non esistono ancora: in quel caso, usa `[[<id>]] (da compilare)` come placeholder
- Per ogni `related_docs`, crea una `relations` corrispondente con `targetId` uguale

### 6. Strumenti di Automazione e CLI (scripts/itinfra.py)

Il repository include la suite di automazione `scripts/itinfra.py`:

```bash
# All-in-One: Inizializza progetto, auto-scaffold dei 10 documenti OKF v0.2 e apre la UI (Release v0.9.11):
python scripts/itinfra.py start <slug> [--client "<Nome>"] [--name "<Titolo>"]

# Auto-scaffold con propagazione automatica dal manifesto (auto-inizializza se non presente):
python scripts/itinfra.py scaffold <slug> [--dry-run] [--force]

# Inizializzare un nuovo progetto con manifesto condiviso:
python scripts/itinfra.py init <slug> --client "<Nome Cliente>" --name "<Titolo Progetto>"

# Controllare l'avanzamento delle 7 fasi:
python scripts/itinfra.py status <slug>

# Validare la conformità formale OKF v0.2 di un file o cartella:
python scripts/itinfra.py validate projects/<slug>/01-RSD-URS.md

# Audit di coerenza semantica incrociata & Zero-Hallucination (Strict Grounding):
python scripts/itinfra.py audit-consistency <slug>

# Gestione Local Encrypted Secret Vault (AES-256-GCM con File Lock atomico):
python scripts/itinfra.py vault [init|set|get|list|audit] <slug>

# Orchestrazione Multi-Agente su Git Worktree isolati:
python scripts/itinfra.py worktree [add|list|sync|cleanup]

# Esportazione Configuration Playbooks (RouterOS .rsc e PowerShell .ps1):
python scripts/itinfra.py export-configs <slug> --out projects/<slug>/configs

# Gestione Incidenti, Root Cause Analysis (RCA) e Live Telemetry:
python scripts/itinfra.py troubleshoot [init|list] <slug> <ticket_id>
python scripts/itinfra.py health-check <slug> [--timeout 1.0]

# Mappa Interattiva D3.js Knowledge Graph OKF v0.2:
python scripts/itinfra.py export-graph <slug|templates|all> [--out graph.html]

# Memoria Locale Ibrida (L1-L3), Global Scratchpad e Trust Signals (Release v0.6 & v0.8):
python scripts/itinfra.py memory [init|log|show|merge|consolidate|prune] <slug>
python scripts/itinfra.py memory [init|log|show|prune] --global

# Global Enterprise Asset & Entity Knowledge Graph (Release v0.7):
python scripts/itinfra.py inventory [find|list-hardware|summary]

# Enterprise System Test Suite & Verification Dashboard (Release v0.8):
python scripts/itinfra.py test-suite [--report-html] [--no-html] [--out projects/system-test-report.html]

# Reverse Reconciliation da As-Built a Manifesto (Release v0.9.12):
python scripts/itinfra.py reconcile <slug> [--from-doc <file>] [--dry-run]

# Intervista guidata modulare a checkpoint atomici (Release v0.9.12):
python scripts/itinfra.py interview <slug> [--status|--prompt <block>|--block <block> --set key=val]

# Architettura Local Workspace & Central Publish con Quality Gate e Remote Lock (Release v0.9 & v0.9.12):
python scripts/itinfra.py publish <slug> [--dest <path>] [--dry-run] [--force] [--include-vault]
python scripts/itinfra.py sync-engine [--source <path>] [--dry-run]
python scripts/itinfra.py check-share [--path <path>] [--user <user>] [--password <pass>]
python scripts/itinfra.py deploy-share [--dest <path>] [--dry-run]
```

### 7. Validazione finale & Gate di Qualità

Prima di restituire il documento compilato:
1. Esegui sempre `python scripts/itinfra.py validate <percorso_file>`
2. Esegui l'audit di coerenza semantica: `python scripts/itinfra.py audit-consistency <slug>`
3. **Completa la checklist di validazione** in fondo al template:
   - Tutti i flag `[ ]` devono diventare `[x]` (se la condizione è soddisfatta) o restare `[ ]` con una nota esplicativa.
   - Se la checklist o il linter segnalano errori, il documento NON può passare a `status: in-review`.

### 8. Cosa NON fare (Zero-Hallucination & Security Policy)

- ❌ **DIVIETO ASSOLUTO DI ALLUCINAZIONI:** Non inventare mai requisiti, indirizzi IP, subnet, seriali, MAC address, credenziali o versioni firmware non esplicitamente forniti dall'utente o dal manifesto di progetto.
- ❌ In assenza di un'informazione tecnica, l'UNICO valore ammesso è tassativamente `<DA-RICHIEDERE>`, da registrare nella sezione Open Issues.
- ❌ Non cambiare la struttura del template (sezioni, tabelle, ordine) senza esplicita richiesta dell'utente.
- ❌ Non inserire secret in chiaro: usare sempre `vault://it/projects/<slug>/...`.
- ❌ **DIVIETO ASSOLUTO DI CHAT LEAKAGE:** Non chiedere MAI e non farsi MAI incollare password, chiavi o secret in chiaro in chat. Per registrare credenziali, istruire l'utente a eseguire `it vault set <slug> <chiave>` nel terminale con input mascherato da getpass.
- ❌ Non mescolare lingue (mantieni l'italiano coerente; termini tecnici inglesi solo se standard).
- ❌ Non lasciare placeholder generici `<...>` nelle sezioni critiche (requisiti, IP, configurazioni).
- ❌ Non creare documenti "orfani": ogni documento DEVE avere almeno un `related_docs` e idealmente un `depends_on`.
- ❌ Non promuovere `status` a `approved` senza firma umana.
- ❌ Non rimuovere il blocco `<!-- AI-INSTRUCTIONS -->`: deve restare nel documento finale come traccia.

---

## Workflow di compilazione guidato (Step-by-Step)

```
1. Carica / Inizializza progetto (`python scripts/itinfra.py init <slug>`)
   ↓
2. Leggi il manifesto di progetto (`projects/<slug>/project-manifest.yaml`)
   ↓
3. Identifica il template (NN-TIPO.md) e verifica `depends_on`
   ↓
4. CONDUCI L'INTERVISTA GUIDATA A BLOCCHI TEMATICI (non chiedere tutto insieme):
   - Blocco 1: Scope, Stakeholder e SLA
   - Blocco 2: Topologia, Rete e Indirizzamento IP
   - Blocco 3: Compute, Storage e Virtualizzazione
   - Blocco 4: Sicurezza, Matrice Accessi e Compliance
   - Blocco 5: Piano di Rollback, ATP e Operations
   ↓
5. Compila il template inserendo diagrammi Mermaid per topologie e rack
   ↓
6. Esegui validazione formale (`python scripts/itinfra.py validate <file>`)
   ↓
7. Salva in `projects/<slug>/<NN-TIPO>.md` e aggiorna `status <slug>`
```

---

## Formato di output

Quando compili un documento, restituisci:

1. **Il documento completo** in un blocco di codice Markdown (```markdown ... ```), pronto da copiare-incollare
2. **Un riepilogo sintetico** (3-5 righe) di cosa è stato compilato e quali eventuali lacune rimangono
3. **Suggerimento di salvataggio**: path e `id` consigliati

Esempio:

```
Documento compilato: 01-RSD-URS (progetto acme-milano)
Salva in: /vault/projects/acme-milano/01-RSD-URS.md
ID: rsd-urs-acme-milano-01

Riepilogo:
- Compilati 12 requisiti funzionali (RF-001..RF-012)
- Compilati 8 requisiti non funzionali
- RTO/RPO definiti per 3 categorie di sistema
- Open Issues: 2 (OI-001 conferma modello fatturazione DR, OI-002 conferma penet-test)
- Stato: in-review (checklist completa)
```

---

## Riferimenti rapidi

- **Mappa dei documenti**: `00-INDEX.md`
- **Esempi di prompt**: `examples/00-prompt-master-template.md` e successivi
- **Convenzioni frontmatter**: `README.md` sezione "Convenzioni"
- **Domande FAQ**: `README.md` sezione "Domande frequenti"

Se ti trovi di fronte a un caso non coperto da queste istruzioni, **fermati e chiedi chiarimenti all'utente** invece di improvisare. La tracciabilità e la correttezza tecnica sono più importanti della velocità di compilazione.


---

## 🔗 Integrazione Hub-and-Spoke con `itinfra-business-ops` (SPEC-20..24)

1. **Shared Customer Slug**: La cartella `projects/<slug>/` corrisponde esattamente a `clients/<slug>/` nel repository operativo `itinfra-business-ops`.
2. **Ponte Incident-to-Report (SPEC-24)**: Ogni fascicolo `10-RCA.md` completato genera automaticamente un evento per la fatturazione/scarico SLA straordinario con maggiorazioni CCNL nel repository business.
3. **Workflow Tecnici FSM (SPEC-24)**: I comandi `it-ops workflow run [dr-drill|firmware-upgrade|hardware-decommissioning-raee] <slug>` eseguono procedure tecniche resilienti a stati finiti conforme a GDPR Art. 32 e D.Lgs. 49/2014.
4. **Presidio Fiscale Nazionale**: Tutte le anagrafiche sono verificate con controlli formali su Partita IVA (Luhn), Codice Fiscale (omocodie DM 23/12/1976) e canali SDI.
