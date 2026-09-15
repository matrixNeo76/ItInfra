# Livello 2 — Estensione del parser OKF per tipi documentali IT

Questa cartella contiene le **patch** e i **file aggiuntivi** per integrare i 9 tipi documentali IT del ciclo lavorativo nel parser OKF v0.2 nativo del Knowledge Vault (https://github.com/matrixNeo76/KnowledgeVault).

## Cosa cambia rispetto al Livello 1

| Aspetto | Livello 1 (già fatto) | Livello 2 (questa cartella) |
|---------|----------------------|------------------------------|
| Schema frontmatter | OKF v0.2 nativo ✅ | Invariato ✅ |
| Riconoscimento tipi | Parser sanitizza `RSD-URS` → `specification` (perdita semantica) | Parser riconosce i 9 tipi IT come **alias canonici** dei 6 OKF, preservando la semantica nel `rawType` |
| Metadati IT estesi | Preservati in `rawFrontmatter` | Esposti anche come `parsedDocument.itMetadata` tipizzato |
| Boilerplate template | Solo 6 OKF_TEMPLATES canonici | + 9 OKF_IT_TEMPLATES specifici |
| Tipizzazione TypeScript | Solo `OKFEntity`, `OKFRelation`, `ResourceMetadata` | + `ITProjectMetadata`, `ITDocType` |

## Strategia di integrazione

Per evitare di **rompere la backward compatibility** con documenti OKF v0.2 esistenti nel tuo vault, ho seguito queste regole:

1. **Non modificare i 6 tipi canonici OKF** (`concept`, `architecture`, `guide`, `specification`, `tool_description`, `prompt_skill`) — restano validi
2. **Aggiungere un layer di alias IT** che mappa i 9 tipi IT (`rsd_urs`, `hld`, `lld`, `mop`, `rollback`, `as_built`, `atp`, `sop_runbook`, `handover_inventory`) ai 6 canonici OKF
3. **Preservare il tipo IT originale** nel campo `originalDocType` del `ParsedOKFDocument` (NON viene sanitizzato via)
4. **Esporre metadati IT estesi** tramite un nuovo campo `itMetadata` tipizzato in `ParsedOKFDocument`
5. **Aggiungere 9 boilerplate template IT** in `OKF_IT_TEMPLATES` per authoring rapido

## File contenuti

```
integration-livello-2/
├── README.md                           ← questo file
├── 01-PATCH-okfParser.ts.md            ← patch con diff per src/lib/okfParser.ts
├── 02-PATCH-types.ts.md                ← patch con diff per src/types.ts
├── 03-NEW-okfItTemplates.ts            ← nuovo file src/lib/okfItTemplates.ts
├── 04-PR-DESCRIPTION.md                ← descrizione della PR pronta per GitHub
└── 05-MIGRATION-GUIDE.md               ← guida per applicare le modifiche
```

## Come applicare le modifiche

### Opzione A — Applicazione manuale (consigliata per review)

1. Apri `01-PATCH-okfParser.ts.md` e applica le modifiche descritte a `src/lib/okfParser.ts`
2. Apri `02-PATCH-types.ts.md` e applica le modifiche a `src/types.ts`
3. Crea il nuovo file `src/lib/okfItTemplates.ts` con il contenuto di `03-NEW-okfItTemplates.ts`
4. Esegui `npm run lint` per verificare la compilazione TypeScript
5. Esegui i test: `npm run test:cekikj` (se presenti) — i test esistenti devono continuare a passare

### Opzione B — Applicazione via git apply

Le patch sono in formato diff unificato. Dalla root del repo KnowledgeVault clonato:

```bash
# Copia i file .patch in /tmp
cp /path/to/integration-livello-2/*.patch /tmp/

# Applica le patch
cd /path/to/KnowledgeVault
git apply /tmp/01-okfParser.patch
git apply /tmp/02-types.patch

# Crea il nuovo file
cp /tmp/03-okfItTemplates.ts src/lib/okfItTemplates.ts

# Verifica
npm run lint
```

### Opzione C — PR via GitHub

La descrizione della PR è pronta in `04-PR-DESCRIPTION.md`. Puoi creare una branch `feature/it-infrastructure-types` nel tuo repo, applicare le modifiche, e aprire la PR.

## Test di regressione

Dopo aver applicato le modifiche, verifica:

1. **Backward compatibility**: i documenti OKF v0.2 esistenti nel tuo vault devono continuare a essere riconosciuti come validi
2. **Riconoscimento tipi IT**: crea un documento con `type: "rsd_urs"` e verifica che:
   - `parsedDocument.docType === "specification"` (sanitizzazione canonica)
   - `parsedDocument.originalDocType === "rsd_urs"` (preservazione semantica)
   - `parsedDocument.isValidOKF === true`
3. **Metadati IT**: un documento con `project_id`, `phase`, `related_docs` deve esporre questi campi in `parsedDocument.itMetadata`
4. **Boilerplate**: usa `OKF_IT_TEMPLATES["lld"]` per generare un documento e verifica che passi la validazione

## Vincoli rispettati

- ✅ **Zero breaking changes**: i documenti OKF v0.2 esistenti continuano a funzionare
- ✅ **Tipizzazione strict**: nessun `any` aggiunto, tutte le nuove interfacce sono tipizzate
- ✅ **Coerenza con il parser esistente**: la funzione `sanitizeDocType` viene estesa, non sostituita
- ✅ **Compatibile col grafo D3**: i 9 tipi IT vengono mappati ai 6 tipi canonici per la visualizzazione
- ✅ **Conforme alla specifica OKF v0.2**: il campo `type` nel frontmatter resta sempre uno dei 6 canonici (gli alias IT sono solo a livello di parsing, non di serializzazione)

## Limiti noti

1. **Serializzazione**: quando il Knowledge Vault genera un documento OKF (es. da sintesi Gemini), continua a usare solo i 6 tipi canonici. I 9 tipi IT sono riconosciuti solo in **ingesto** (parsing), non in **authoring** automatico. Per generare documenti IT tipizzati, l'utente deve usare i boilerplate `OKF_IT_TEMPLATES` manualmente.

2. **Grafo D3**: il grafo continua a visualizzare i 6 tipi canonici ( colore differente per ogni tipo). I 9 tipi IT NON avranno colore distinto — questo richiederebbe modifiche al `KnowledgeGraph.tsx` (fuori scope del Livello 2).

3. **KnowledgeReader**: la scheda "Grafo & Relazioni" non mostra ancora i metadati IT estesi (project_id, phase, related_docs). Per visualizzarli serve un nuovo componente `ITProjectMetadataCard.tsx` (fuori scope del Livello 2, candidato per il Livello 3).

## Prossimi passi

Dopo aver applicato il Livello 2, valuta se procedere col **Livello 3** (modulo `src/modules/itInfrastructure/` completo di UI e API dedicata) — ha senso solo se prevedi di usare il ciclo lavorativo IT su almeno 2-3 progetti ricorrenti.
