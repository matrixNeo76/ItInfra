# CLAUDE.md — Istruzioni per Claude Code

> Questo file è letto automaticamente da **Claude Code** (CLI di Anthropic) quando opera in questa directory. Il contenuto è equivalente a `AGENTS.md`; viene mantenuto separato perché Claude Code cerca specificamente `CLAUDE.md`.

---

## Contesto del progetto

Stai lavorando in un **knowledge vault di template documentali IT** basati sullo standard **OKF v0.2 (Open Knowledge Format)** nella sua forma nativa, compatibile col parser `src/lib/okfParser.ts` del Knowledge Vault di matrixNeo76. I template sono in `/download/templates/` e devono essere compilati a partire dai dati forniti in chat.

Lo schema YAML combina **campi canonici OKF v0.2** (riconosciuti dal parser e visualizzati come archi nel grafo D3) + **metadati estesi IT** (preservati in `rawFrontmatter` per uso futuro). Il ciclo lavorativo è composto da 7 fasi che producono 10 tipologie documentali (inclusa gestione incidenti e RCA), mappate in `00-INDEX.md`.

Consulta `AGENTS.md` per le istruzioni operative complete (regole di compilazione del frontmatter OKF v0.2 nativo, gestione credenziali, validazione, workflow, mappatura 9 tipi IT → 6 tipi canonici OKF). Di seguito le note specifiche per Claude Code.

---

## Note specifiche per Claude Code

### Uso dei TodoWrite

Per compilazioni non banali (es. LLD con più di 10 sezioni, MOP completo, As-Built), usa il tool `TodoWrite` per pianificare:

1. Lettura del template
2. Lettura dei documenti `depends_on`
3. Compilazione del frontmatter
4. Compilazione delle sezioni del body
5. Verifica della checklist di validazione
6. Restituzione del documento all'utente

Per compilazioni semplici (singolo template con dati già forniti), puoi procedere senza TodoWrite.

### Uso di Read e Write

- **Read**: usa per leggere il template da compilare e i documenti `depends_on` dal vault
- **Write**: usa per salvare il documento compilato nel path suggerito dall'utente; se l'utente non specifica un path, **chiedilo** prima di salvare (non inventare path arbitrari)
- **Edit**: usa se l'utente richiede modifiche a un documento già compilato

### Formato di output

Restituisci sempre:
1. Il documento completo in un blocco Markdown (```markdown ... ```)
2. Un riepilogo sintetico (3-5 righe)
3. Il path e l'id suggeriti per il salvataggio

NON restituire solo un riepilogo: l'utente deve poter copiare il documento compilato.

### Quando fermarti e chiedere

FERMATI e chiedi chiarimenti all'utente se:
- I dati forniti sono insufficienti per popolare sezioni critiche (requisiti, IP, configurazioni)
- Esistono conflitti tra i dati forniti e i documenti `depends_on`
- L'utente richiede modifiche alla struttura del template (cambio di sezioni/colonne)
- Il documento dovrebbe avere `status: approved` ma non c'è traccia di revisione umana

### Gestione delle versioni

Se l'utente chiede di "aggiornare" un documento esistente:
1. Leggi la versione corrente dal vault
2. Incrementa `version` (0.1 → 0.2 per modifiche minori, 1.0 → 2.0 per revisioni sostanziali)
3. Aggiorna `updated_at`
4. Se la nuova versione sostituisce completamente la precedente: popola `supersedes` con l'id della vecchia versione, e segnala all'utente di aggiornare la vecchia con `status: superseded` e `superseded_by`

### Uso della CLI (scripts/itinfra.py)

Claude Code dispone dell'esecuzione di comandi da terminale (`Bash`). Usala attivamente per:
- Inizializzare un progetto: `python scripts/itinfra.py init <slug> --client "<Cliente>"`
- Verificare lo stato di avanzamento delle 7 fasi: `python scripts/itinfra.py status <slug>`
- Validare il documento Markdown compilato prima di restituirlo: `python scripts/itinfra.py validate projects/<slug>/<NN-TIPO>.md`
- Audit di coerenza semantica (Zero-Hallucination): `python scripts/itinfra.py audit-consistency <slug>`
- Gestione credenziali e secret vault AES-256-GCM: `python scripts/itinfra.py vault [init|set|get|list|audit] <slug>`
- Gestione worktree per subagenti paralleli: `python scripts/itinfra.py worktree [add|list|sync|cleanup]`
- Esportazione script RouterOS e PowerShell: `python scripts/itinfra.py export-configs <slug>`
- Gestione incidenti e live health-check: `python scripts/itinfra.py troubleshoot init <slug> <ticket_id>` / `python scripts/itinfra.py health-check <slug>`
- Mappa interattiva D3.js Knowledge Graph OKF v0.2: `python scripts/itinfra.py export-graph <slug|templates|all>`
- Memoria locale ibrida, Global Scratchpad e Trust Signals (Release v0.6 & v0.8): `python scripts/itinfra.py memory [init|log|show|merge|consolidate|prune] <slug>` e `python scripts/itinfra.py memory [init|log|show|prune] --global`
- Global Enterprise Asset & Entity Knowledge Graph (Release v0.7): `python scripts/itinfra.py inventory [find|list-hardware|summary]`
- Enterprise System Test Suite & Verification Dashboard (Release v0.8): `python scripts/itinfra.py test-suite [--report-html]`
- Architettura Local Workspace & Central Publish con Quality Gate (Release v0.9): `python scripts/itinfra.py publish <slug>` e `python scripts/itinfra.py sync-engine`

### Anti-pattern da evitare (Zero-Hallucination Policy)

- ❌ **Non inventare parametri:** divieto assoluto di generare IP, subnet, password o seriali non forniti; usa sempre `<DA-RICHIEDERE>`
- ❌ Non usare `Complete` tool: non stai sviluppando un'app web, stai compilando documentazione
- ❌ Non creare file README o documentazione aggiuntiva non richiesta
- ❌ Non eseguire comandi bash per modificare il vault senza esplicita autorizzazione
- ❌ Non mescolare conversazioni diverse: ogni compilazione è un task autonomo
- ❌ Non rimuovere il blocco `<!-- AI-INSTRUCTIONS -->` dal documento finale (deve restare come traccia)

---

## Riferimenti rapidi (Claude Code)

- **Istruzioni operative complete**: `AGENTS.md`
- **Mappa dei documenti**: `00-INDEX.md`
- **Esempi di prompt**: `examples/00-prompt-master-template.md` e successivi
- **README umano**: `README.md`

Quando ricevi un prompt tipo: *"Compila il template X con questi dati: ..."*, segui esattamente il workflow in `AGENTS.md` sezione "Workflow di compilazione consigliato".
