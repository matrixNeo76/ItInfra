# AGENTS.md — Istruzioni per agenti AI

> Questo file è letto automaticamente da Cursor, Aider, Continue, Cline, Roo Code e altri agenti che seguono la convenzione `AGENTS.md`. Per Claude Code vedere `CLAUDE.md` (contenuto equivalente).

---

## Contesto del progetto

Sei un agente AI chiamato a **compilare template documentali** per progetti di infrastrutture IT. I template si trovano in `/download/templates/` e seguono lo standard **OKF v0.2 (Open Knowledge Format)** nella sua forma nativa, compatibile col parser `src/lib/okfParser.ts` del Knowledge Vault.

Lo schema YAML combina **campi canonici OKF v0.2** (riconosciuti dal parser e visualizzati nel grafo D3) + **metadati estesi IT** (preservati in `rawFrontmatter` per uso futuro).

Il ciclo lavorativo è composto da **7 fasi operative** che producono **9 tipologie documentali**, mappate in `00-INDEX.md`:

| Fase | Documenti |
|------|-----------|
| 1. Assessment | RSD/URS |
| 2. Design | HLD, LLD |
| 3. Procurement & Staging | MOP, Rollback |
| 4. Racking & Cabling | (confluisce in As-Built) |
| 5. Commissioning | (confluisce in As-Built) |
| 6. Testing | ATP |
| 7. Go-Live | As-Built, SOP/Runbook, Handover & Inventory |

---

## Regole operative imprescindibili

### 1. Prima di iniziare

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

### 4. Gestione delle credenziali

**VIETATO inserire password, chiavi API, token o qualsiasi secret in chiaro nel documento.**

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

### 6. Validazione finale

Prima di restituire il documento compilato, **completa la checklist di validazione** in fondo a ogni template:

- Tutti i flag `[ ]` devono diventare `[x]` (se la condizione è soddisfatta) o restare `[ ]` con una nota che spiega perché non lo sono.
- Se la checklist non è completamente soddisfatta, il documento NON può passare a `status: in-review`.

### 7. Cosa NON fare

- ❌ Non inventare requisiti, IP, seriali, MAC, versioni firmware non forniti.
- ❌ Non cambiare la struttura del template (sezioni, tabelle, ordine) senza esplicita richiesta dell'utente.
- ❌ Non inserire secret in chiaro.
- ❌ Non mescolare lingue (mantieni l'italiano coerente; termini tecnici inglesi solo se standard).
- ❌ Non lasciare placeholder `<...>` nelle sezioni critiche (requisiti, IP, configurazioni).
- ❌ Non creare documenti "orfani": ogni documento DEVE avere almeno un `related_docs` e idealmente un `depends_on`.
- ❌ Non promuovere `status` a `approved` senza firma umana.
- ❌ Non rimuovere il blocco `<!-- AI-INSTRUCTIONS -->`: deve restare nel documento finale come traccia.

---

## Workflow di compilazione consigliato

```
1. Ricevi il prompt dell'utente (esempi in examples/)
   ↓
2. Identifica il template da compilare (NN-TIPO.md)
   ↓
3. Leggi il blocco AI-INSTRUCTIONS nel template
   ↓
4. Identifica depends_on nel frontmatter
   ↓
5. Leggi i documenti depends_on dal vault (se esistono già)
   ↓
6. Compila il frontmatter YAML (id, project_id, status, related_docs, ...)
   ↓
7. Compila tutte le sezioni del body
   ↓
8. Sostituisci TUTTI i placeholder <...>
   ↓
9. Verifica la checklist di validazione
   ↓
10. Restituisci il documento completo all'utente
    ↓
11. Suggerisci all'utente dove salvarlo e quale id usare
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
