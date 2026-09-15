# Master Template — Struttura generica di un prompt

Questo file descrive la **struttura standard** che ogni prompt per compilare un template documentale dovrebbe seguire. Usa questa struttura come base per creare prompt personalizzati per qualsiasi tipo di documento.

---

## Anatomia di un prompt efficace

Un buon prompt per compilare un template contiene 6 sezioni:

```
1. RUOLO E CONTESTO          → chi è l'agente, cosa deve fare
2. INPUT DATI                 → i dati concreti del progetto
3. TEMPLATE DA COMPILARE      → path del template + AI-INSTRUCTIONS da rispettare
4. DOCUMENTI CORRELATI        → id e path dei documenti depends_on già esistenti
5. VINCOLI DI OUTPUT         → formato, lingua, campi obbligatori
6. SUGGERIMENTI DI SALVATAGGIO → path e id del documento finale
```

---

## Template di prompt (copia e personalizza)

```text
## 1. RUOLO E CONTESTO

Sei un system engineer senior specializzato in infrastrutture IT.
Il tuo compito è compilare il template documentale indicato di seguito,
partendo dai dati forniti in questo prompt.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md se sei Claude Code)
2. Leggi /download/templates/00-INDEX.md per il contesto del ciclo lavorativo
3. Conferma di averli letti con un riepilogo di 3 righe

## 2. INPUT DATI — Progetto

- project_id: <PROJECT_ID>
- project_name: <nome progetto>
- site: <SITE_CODE>
- customer: <cliente>
- author: <nome>
- reviewer: <nome>
- approver: <nome>
- owner_team: <team>

## 3. DATI SPECIFICI DEL DOCUMENTO

[INSERIRE QUI I DATI SPECIFICI DEL DOCUMENTO DA COMPILARE]
[Es. per RSD-URS: elenco requisiti funzionali e non funzionali]
[Es. per LLD: schema IP, VLAN, modelli apparati, configurazioni]
[Es. per As-Built: seriali, firmware, deviazioni dal LLD]

## 4. TEMPLATE DA COMPILARE

Template path: /download/templates/NN-TIPO.md
Tipo documento: <RSD-URS|HLD|LLD|MOP|Rollback|As-Built|ATP|SOP-Runbook|Handover-Inventory>
Fase: <1-7>

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter del template
- Rispetta TUTTE le regole elencate
- NON modificare la struttura del template (sezioni, tabelle, ordine)
- Sostituisci TUTTI i placeholder <...> con valori reali

## 5. SCHEMA OKF v0.2 NATIVO (OBBLIGATORIO per integrazione Knowledge Vault)

Il frontmatter DEVE contenere sia i campi canonici OKF v0.2 (per il grafo D3) sia i metadati estesi IT:

### Campi canonici OKF v0.2 (OBBLIGATORI)
- okf_version: "0.2"  (letterale)
- id: "<type-canonical>-<project_slug>-<subtype>-<seq>"  (es. "architecture-acme-milano-lld-01")
- title: <titolo chiaro>
- type: <uno dei 6 tipi canonici — vedi mappatura sotto>
- domain: <ambito tematico>
- tags: ["okf-v0.2", <altri tag>]
- entities: [{name, type, description}, ...]
- relations: [{targetTitle, targetId, relationType, weight, description}, ...]

### Mappatura tipo IT → tipo canonico OKF
- RSD/URS → specification
- HLD → architecture
- LLD → architecture
- MOP → guide
- Rollback → guide
- As-Built → architecture
- ATP → specification
- SOP/Runbook → guide
- Handover & Inventory → specification

### Metadati estesi IT (preservati in rawFrontmatter)
- project_id, project_name, site, customer, phase, author, reviewer, approver, owner_team
- status, version, created_at, updated_at
- related_docs: [<id1>, <id2>]  (array di stringhe ID)
- depends_on: [<id1>]
- classification, retention, lang

### COERENZA CRITICA
Per ogni ID presente in `related_docs`, creare una corrispondente entry in `relations`
con lo stesso `targetId` e un `relationType` semanticamente appropriato
(references, implements, depends_on, extends, documents, governs, constrains, relates_to).
Questo garantisce che il grafo D3 del Knowledge Vault visualizzi correttamente le relazioni.

## 6. DOCUMENTI CORRELATI GÀ COMPILATI (depends_on)

[INSERIRE QUI I RIFERIMENTI AI DOCUMENTI GIÀ ESISTENTI NEL VAULT]
[Es. per HLD: "RSD-URS già compilato: path /vault/projects/acme-milano/01-RSD-URS.md, id specification-acme-milano-rsd-01"]
[Es. per LLD: "RSD-URS e HLD già compilati: ..."]
[Se non esistono ancora documenti depends_on, scrivere "Nessun documento depends_on ancora disponibile"]

## 6. VINCOLI DI OUTPUT

- Lingua: italiano (campo lang: it)
- Status iniziale: draft
- Versione iniziale: 0.1
- NO password in chiaro (usa riferimenti al vault)
- NO dati inventati: se mancano, scrivi <DA-RICHIEDERE> e segnala in Open Issues
- Mantieni i blocchi di codice esistenti come riferimento (sostituisci solo i placeholder)
- Completa la checklist di validazione in fondo al template prima di restituire il documento

## 7. FORMATO DI OUTPUT ATTESO

Restituisci:
1. Il documento completo in un blocco Markdown (```markdown ... ```)
2. Un riepilogo sintetico (3-5 righe) di cosa è stato compilato e quali lacune rimangono
3. Il path e l'id suggeriti per il salvataggio:
   - Path: /vault/projects/<project_id>/NN-TIPO.md
   - ID: <tipo>-<project_slug>-01

## 8. AZIONE FINALE

Compila il documento ora. Non fare domande di chiarimento se i dati sono sufficienti;
in caso di dubbi su punti minori, procedi con la scelta più ragionevole e
segnalala nel riepilogo finale come "assunzione".
```

---

## Variabili da personalizzare per ogni progetto

| Variabile | Descrizione | Esempio |
|-----------|-------------|---------|
| `PROJECT_ID` | Identificatore univoco del progetto | `acme-milano-2026` |
| `project_name` | Nome completo del progetto | `Sostituzione Infrastruttura Datacenter Milano` |
| `SITE_CODE` | Codice del sito | `MIL-01` |
| `customer` | Nome del cliente | `Acme S.p.A.` |
| `NN-TIPO` | Numero e tipo del template | `03-LLD`, `06-As-Built`, ecc. |

---

## Errori comuni da evitare nel prompt

### ❌ Prompt troppo vago
```
Compila il template LLD con questi dati: cliente Acme, sito Milano.
```
→ L'agente non sa quali IP, VLAN, modelli usare; inventerà tutto.

### ✅ Prompt con dati strutturati
```
Compila il template LLD per il progetto Acme Milano.
Dati:
- Subnet: 10.10.10.0/24 DMZ, 10.10.20.0/24 PROD, ...
- VLAN: 10 DMZ, 20 PROD, 50 MGMT, 70 STORAGE
- Server: 3x Dell R750 (service tag: ...)
- Storage: NetApp FAS8700 (serial: ...)
```
→ L'agente ha dati concreti da inserire nelle tabelle.

### ❌ Nessun riferimento ai documenti depends_on
```
Compila LLD.
```
→ L'agente non sa quali requisiti deve soddisfare.

### ✅ Riferimento esplicito
```
Compila LLD. Il documento RSD-URS (id: specification-acme-milano-rsd-01) è già disponibile
in /vault/projects/acme-milano/01-RSD-URS.md — leggilo prima di iniziare.
Anche l'HLD (id: architecture-acme-milano-hld-01) è disponibile in /vault/projects/acme-milano/02-HLD.md.
```
→ L'agente ha il contesto necessario per coerenza.

---

## Cosa fare se l'agente non rispetta le AI-INSTRUCTIONS

Se l'agente ignora le istruzioni nel template, aggiungi al prompt:

```text
CRITICO: Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter del
template NN-TIPO.md. Per ogni regola elencata nelle AI-INSTRUCTIONS, dimostra nel
documento finale che l'hai rispettata (es. se la regola dice "NON inventare dati",
in caso di dato mancante scrivi <DA-RICHIEDERE> e aggiungilo in Open Issues).
Prima di restituire il documento, completa la checklist di validazione in fondo
al template: tutti i flag [ ] devono diventare [x] con una nota se la condizione
è soddisfatta, oppure restare [ ] con una nota che spiega perché non lo è.
```
