# Knowledge Vault — Template Documentali Ciclo Lavorativo IT

Questo repository contiene **10 template Markdown** (formato OKF v0.2) per la documentazione di infrastrutture IT complesse, dalla fase di Assessment fino al Go-Live. I template sono progettati per essere **compilati da agenti AI** tramite chat agentiche e salvati in un **knowledge vault** dove vengono relazionati tra loro tramite wiki-links.

---

## A chi è rivolto

- **Integratori / System Engineer IT** che producono documentazione tecnica per progetti di infrastruttura
- **Team Operations** che devono gestire la documentazione post-rilascio
- **Agenti AI** (Claude, GPT, Gemini, Cursor, Copilot, ecc.) chiamati a compilare i template a partire dai dati forniti in chat

---

## Struttura del repository

```
templates/
├── README.md                          ← questo file (lettura umana)
├── AGENTS.md                          ← istruzioni auto-caricate da Cursor/Aider/Continue/...
├── CLAUDE.md                          ← istruzioni auto-caricate da Claude Code
├── 00-INDEX.md                        ← mappa fasi ↔ documenti + link graph
│
├── 01-RSD-URS.md                      ← Fase 1 — Assessment
├── 02-HLD.md                          ← Fase 2 — High-Level Design
├── 03-LLD.md                          ← Fase 2 — Low-Level Design
├── 04-MOP.md                          ← Fase 3 — Method of Procedure
├── 05-Rollback.md                     ← Fase 3 — Rollback / Fallback Plan
├── 06-As-Built.md                     ← Fase 5-7 — As-Built Documentation
├── 07-ATP.md                          ← Fase 6 — Acceptance Test Plan
├── 08-SOP-Runbook.md                  ← Fase 7 — Standard Operating Procedures
├── 09-Handover-Inventory.md           ← Fase 7 — Handover & Asset Inventory
│
└── examples/                          ← esempi concreti di prompt per agenti AI
    ├── README.md
    ├── 00-prompt-master-template.md   ← struttura generica di prompt
    ├── 01-prompt-RSD-URS.md
    ├── 02-prompt-HLD.md
    ├── 03-prompt-LLD.md
    ├── 04-prompt-MOP.md
    ├── 05-prompt-Rollback.md
    ├── 06-prompt-As-Built.md
    ├── 07-prompt-ATP.md
    ├── 08-prompt-SOP-Runbook.md
    └── 09-prompt-Handover-Inventory.md
```

---

## Come funziona

### 1. Scegli il template da compilare

Consulta [`00-INDEX.md`](./00-INDEX.md) per capire quale template corrisponde alla fase corrente del progetto. La tabella delle fasi indica:
- A quale fase operativa (1–7) appartiene ciascun documento
- Quali documenti devono essere già compilati prima (`depends_on`)
- Quali documenti saranno generati dopo (`related_docs`)

### 2. Apri una chat agentic e invia il prompt

Copia il prompt di esempio corrispondente da `examples/` e personalizzalo con i dati reali del progetto. Il prompt contiene:
- L'ID del template da compilare
- I dati di input strutturati
- Ivincoli di output (formato, lingua, lingua, campi obbligatori)
- I riferimenti ai documenti correlati già compilati (per garantire coerenza)

Esempio semplificato:

```text
Compila il template /download/templates/01-RSD-URS.md per il progetto "DC Milano 2026".
Usa questi dati:
- Cliente: Acme S.p.A.
- Sito: Milano, via Verdi 10
- Obiettivo: sostituzione infrastruttura datacenter legacy
- ...
Rispetta le AI-INSTRUCTIONS nel frontmatter e popola tutti i campi obbligatori.
Salva l'output in /vault/projects/acme-dc-milano/01-RSD-URS.md con id "rsd-urs-acme-milano-01".
```

### 3. L'agente AI compila il documento

L'agente:
1. Legge `AGENTS.md` (o `CLAUDE.md` se è Claude Code) per capire le convenzioni
2. Legge il template specificato
3. Consulta i documenti `depends_on` per coerenza
4. Compila tutti i campi rispettando le `AI-INSTRUCTIONS`
5. Verifica la checklist di validazione finale
6. Salva il documento con un `id` univoco e i `related_docs` corretti

### 4. Salva nel knowledge vault

Il documento compilato viene salvato nel tuo vault (es. cartella Obsidian, Logsec, o qualsiasi file system). I wiki-links `[[id]]` permettono di:
- Navigare tra documenti correlati
- Visualizzare il grafo delle dipendenze
- Tracciare versioni e deviazioni

---

## Convenzioni

### Frontmatter YAML (OKF v0.2 nativo)

I template utilizzano lo schema YAML nativo dello standard **OKF v0.2 (Open Knowledge Format)**, compatibile col parser `src/lib/okfParser.ts` del Knowledge Vault. Lo schema combina **campi canonici OKF** (riconosciuti dal parser) + **metadati estesi IT** (preservati in `rawFrontmatter`).

#### Campi canonici OKF v0.2 (OBBLIGATORI per il parser)

| Campo | Descrizione |
|-------|-------------|
| `okf_version` | DEVE essere la stringa `"0.2"` |
| `id` | ID univoco nel vault, pattern `<type-canonical>-<project_slug>-<subtype>-<seq>` |
| `title` | Titolo chiaro e descrittivo (max 120 caratteri) |
| `type` | Uno dei 6 tipi canonici OKF (vedi mappatura sotto) |
| `domain` | Ambito tematico (es. `"IT Infrastructure & Requirements Engineering"`) |
| `tags` | Array di almeno 2 tag in lowercase. PRIMO tag DEVE essere `okf-v0.2` |
| `entities` | Array di entità `{name, type, description}` (min 1). `type`: concept/framework/technology/toolchain/pattern/organization/specification |
| `relations` | Array di relazioni `{targetTitle, targetId, relationType, weight, description}` (può essere vuoto) |

#### Mappatura 9 tipi documentali IT → 6 tipi canonici OKF

| Tipo IT | Tipo canonico OKF | Razionale |
|---------|-------------------|-----------|
| RSD/URS | `specification` | Definisce requisiti e contratti formali |
| HLD | `architecture` | Blueprint architetturale macro |
| LLD | `architecture` | Blueprint architetturale esecutivo |
| MOP | `guide` | Procedura operativa passo-passo |
| Rollback | `guide` | Procedura operativa di contingency |
| As-Built | `architecture` | Stato reale dell'infrastruttura installata |
| ATP | `specification` | Contratto di collaudo con criteri formali |
| SOP/Runbook | `guide` | Manuale operativo |
| Handover & Inventory | `specification` | Verbale formale di presa in carico |

#### Metadati estesi IT (preservati in `rawFrontmatter`)

Questi campi non sono canonici OKF ma vengono conservati dal parser come rawFrontmatter e possono essere letti dal KnowledgeReader per visualizzazione custom:

| Sezione | Contenuto |
|---------|-----------|
| **Identità estesa** | `status`, `version`, `created_at`, `updated_at` |
| **Progetto** | `project_id`, `project_name`, `site`, `customer`, `phase` |
| **Persone** | `author`, `reviewer`, `approver`, `owner_team` |
| **Relazioni estese** | `related_docs`, `depends_on`, `supersedes`, `superseded_by` |
| **Governance** | `classification`, `retention`, `lang` |

### Relazioni tra documenti

Le relazioni sono espresse in **3 modi complementari**:

1. **`relations` canoniche OKF** (frontmatter) — array di oggetti strutturati, parse da `okfParser.ts`, visualizzate come archi nel grafo D3 del Knowledge Vault
2. **`related_docs` estese IT** (frontmatter) — array di stringhe ID, per tracciabilità logica
3. **Wiki-links `[[id]]`** (body Markdown) — sintassi Obsidian/Logsec, catturate dal 3° livello di correlazione del KnowledgeGraph

**Regola di coerenza**: per ogni entry in `related_docs`, creare una corrispondente entry in `relations` con lo stesso `targetId` e un `relationType` semanticamente appropriato.

### Pattern degli ID

L'`id` deve essere univoco nel vault. Pattern:

```
<type-canonical>-<project_slug>-<subtype>-<seq>
```

Esempi:
- `specification-acme-milano-rsd-01`
- `architecture-acme-milano-hld-01`
- `architecture-acme-milano-lld-01`
- `guide-acme-milano-mop-01`
- `architecture-acme-milano-asbuilt-01`

### Stati del documento

| `status` | Significato |
|----------|-------------|
| `draft` | Compilazione in corso |
| `in-review` | Pronto per revisione |
| `approved` | Approvato formalmente |
| `superseded` | Sostituito da versione più recente |

### Naming dei file

```
NN-CODICE.md
```

| Codice | Documento |
|--------|-----------|
| 01 | RSD/URS |
| 02 | HLD |
| 03 | LLD |
| 04 | MOP |
| 05 | Rollback |
| 06 | As-Built |
| 07 | ATP |
| 08 | SOP/Runbook |
| 09 | Handover & Inventory |

I documenti compilati nel vault possono mantenere lo stesso naming (`01-RSD-URS.md`) oppure usare l'`id` come nome file (`rsd-urs-acme-milano-01.md`) — scegli una convenzione e mantienila coerente in tutto il vault.

### Placeholder

Nei template:
- `<...>` = valore singolo da sostituire
- `[...]` = array da espandere
- `[ ]` / `[x]` = checkbox da completare durante la compilazione

### Credenziali

**NESSUNA password o secret in chiaro nei documenti.** Usa sempre riferimenti al vault segreto aziendale:

```yaml
# Sbagliato
password: "Admin123!"

# Corretto
password_ref: "vault://it/acme-milano/fw-01/admin"
```

---

## File auto-caricati dagli agenti AI

### `AGENTS.md`

Letto automaticamente da:
- Cursor
- Aider
- Continue
- Cline / Roo Code
- Molti altri agenti che seguono la convenzione

Contiene le istruzioni operative universali: come leggere i template, come compilare il frontmatter, come gestire le relazioni, cosa NON fare.

### `CLAUDE.md`

Letto automaticamente da **Claude Code** (CLI di Anthropic). Contiene le stesse istruzioni di `AGENTS.md`, con note specifiche per Claude (es. gestione dei todo, formato di output).

> **Nota:** se usi un agente che non legge automaticamente questi file, puoi referenziarli nel prompt: *"Prima di iniziare, leggi /download/templates/AGENTS.md per le convenzioni operative."*

---

## Workflow tipico di un progetto

```
[Assessment]
   │
   │ Dati: requisiti, site survey, stakeholder
   ▼
[RSD/URS] ────────────────► (input per HLD, MOP)
   │
   │ Approvazione requisiti
   ▼
[Design]
   │
   │ Dati: architettura, scelte tecnologiche
   ▼
[HLD] ─────────────────────► (input per LLD)
   │
   ▼
[LLD] ─────────────────────► (input per MOP, As-Built)
   │
   │ Approvazione progetto
   ▼
[Procurement & Staging]
   │
   │ Dati: piano operativo, finestre manutenzione
   ▼
[MOP] ◄──────► [Rollback] (bidirezionale)
   │
   │ Esecuzione deploy
   ▼
[Commissioning + Testing]
   │
   │ Dati: risultati test, deviazioni
   ▼
[As-Built] ───► [ATP] ─────► (verbale di collaudo)
   │
   ▼
[Go-Live / Handover]
   │
   │ Dati: inventario, contratti, SLA
   ▼
[SOP/Runbook] + [Handover & Inventory]
```

---

## Estendere il sistema

### Aggiungere un nuovo tipo di documento

1. Crea il file `NN-NEWTYPE.md` seguendo la struttura di un template esistente
2. Aggiorna `00-INDEX.md` con la nuova riga nella tabella fasi
3. Crea il prompt di esempio in `examples/NN-prompt-NEWTYPE.md`
4. Aggiorna `examples/README.md`
5. Aggiorna `AGENTS.md` e `CLAUDE.md` se introduce convenzioni nuove

### Personalizzare i template

I template sono pensati come punto di partenza. Sentiti libero di:
- Aggiungere campi specifici del tuo settore (es. compliance HIPAA per sanità)
- Rimuovere sezioni non rilevanti per la tua realtà
- Estendere le tabelle con colonne aggiuntive
- Adattare i livelli di rischio (L1/L2/L3/L4) alla tua organizzazione

**Mantieni però invariati:**
- Lo schema YAML del frontmatter (5 blocchi)
- La sintassi dei wiki-links `[[id]]`
- Il blocco `<!-- AI-INSTRUCTIONS -->`
- La checklist di validazione finale

---

## Licenza e attribuzione

Questi template sono rilasciati come strumento di lavoro interno. Adattali liberamente al tuo contesto. Nessuna attribuzione richiesta, ma feedback e miglioramenti sono benvenuti.

---

## Domande frequenti

**D: Posso usare questi template con agenti AI diversi da Claude?**
R: Sì. I template sono agnostic — funzionano con qualsiasi LLM. `AGENTS.md` è la convenzione cross-tool; `CLAUDE.md` è specifica per Claude Code ma il contenuto è identico.

**D: Devo usare Obsidian o Logsec per il vault?**
R: No. I wiki-links `[[id]]` sono riconosciuti da entrambi, ma funzionano anche come semplice testo in qualsiasi editor Markdown. Il vantaggio di Obsidian/Logsec è la visualizzazione del grafo.

**D: Come gestisco le versioni di un documento?**
R: Quando un documento cambia sostanzialmente, crea una nuova copia con:
- `version` incrementata
- `supersedes` che punta all'id della versione precedente
- Il vecchio documento viene marcato `status: superseded` e `superseded_by` punta al nuovo

**D: Cosa fare se un agente AI non rispetta le AI-INSTRUCTIONS?**
R: Riprova con un prompt più esplicito che include: *"Leggi attentamente il blocco AI-INSTRUCTIONS nel frontmatter del template e attieniti a TUTTE le regole elencate. Prima di salvare l'output, verifica che ogni voce della checklist finale sia soddisfatta."*

**D: Posso usare questi template per progetti non IT?**
R: La struttura è generica (requisiti → design → implementazione → collaudo → handover) ed è adattabile a progetti OT, IoT, building automation. Modifica le sezioni tecniche specifiche.
