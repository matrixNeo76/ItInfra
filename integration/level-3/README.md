# Livello 3 — Modulo UI completo per IT Infrastructure

Questa cartella contiene il **modulo completo** per integrare il ciclo lavorativo IT nella UI del Knowledge Vault (https://github.com/matrixNeo76/KnowledgeVault), andando oltre le patch additive del Livello 2.

## Cosa cambia rispetto al Livello 2

| Aspetto | Livello 2 (gia fatto) | Livello 3 (questa cartella) |
|---------|----------------------|------------------------------|
| Parser OKF | Esteso per riconoscere 9 alias IT | Invariato ✅ |
| Tipi TypeScript | `ITProjectMetadata`, `ITDocType` | Invariato ✅ |
| Boilerplate | `OKF_IT_TEMPLATES` (9 YAML minimi) | Invariato ✅ |
| **UI Reader** | Metadati IT NON visualizzati | Nuovo tab "Ciclo IT" con `ITProjectMetadataCard` |
| **Timeline fasi** | Non presente | Nuovo componente `ITWorkflowTimeline` |
| **Sidebar voce** | Non presente | Nuova voce "Ciclo IT" in `Sidebar` |
| **CaptureBar** | Solo capture generico | Nuovo pulsante "Compila template IT" |
| **API backend** | Solo `/api/analyze-resource` | Nuovo endpoint `/api/it-infrastructure/compile-template` |
| **Filtri vault** | Solo per tipo canonico | Filtro per `phase` e `project_id` |

## File contenuti

```
integration-livello-3/
├── README.md                                    ← questo file
├── 01-NEW-ITProjectMetadataCard.tsx             ← scheda metadata IT nel reader
├── 02-NEW-ITWorkflowTimeline.tsx               ← timeline visuale 7 fasi
├── 03-NEW-ITInfrastructureSidebar.tsx          ← voce sidebar "Ciclo IT"
├── 04-NEW-ITTemplateCompilerModal.tsx          ← modale "Compila template IT"
├── 05-PATCH-KnowledgeReader.tsx.md              ← patch: aggiungi tab "Ciclo IT"
├── 06-PATCH-Sidebar.tsx.md                      ← patch: aggiungi voce "Ciclo IT"
├── 07-PATCH-CaptureBar.tsx.md                   ← patch: aggiungi pulsante "Compila template IT"
├── 08-PATCH-captureRoutes.ts.md                 ← patch: nuovo endpoint /api/it-infrastructure/compile-template
├── 09-NEW-itInfrastructureService.ts            ← servizio backend (Gemini compile)
├── 10-PR-DESCRIPTION.md                         ← descrizione PR per GitHub
└── 11-MIGRATION-GUIDE.md                        ← guida applicazione step-by-step
```

## Strategia di integrazione

Tutti i componenti nuovi sono **autonomi** e **opzionali**: possono essere integrati singolarmente senza rompere nulla. La strategia è:

1. **Componenti nuovi** (file `01-NEW-*` a `04-NEW-*`) — file `.tsx` pronti per essere droppati in `src/components/itInfrastructure/`
2. **Patch ai componenti esistenti** (file `05-PATCH-*` a `08-PATCH-*`) — istruzioni precise su cosa aggiungere e dove
3. **Servizio backend nuovo** (file `09-NEW-itInfrastructureService.ts`) — file `.ts` da droppare in `server/services/`
4. **PR description + migration guide** — per GitHub workflow

## Dipendenze

Il Livello 3 **dipende dal Livello 2**: presuppone che `okfParser.ts`, `types.ts` e `okfItTemplates.ts` siano già stati estesi con i tipi IT e i boilerplate.

Verifica prerequisiti prima di iniziare:
- [ ] `src/types.ts` contiene `ITProjectMetadata` e `ITDocType`
- [ ] `src/lib/okfParser.ts` riconosce `isITAlias` ed estrae `itMetadata`
- [ ] `src/lib/okfItTemplates.ts` esiste con `OKF_IT_TEMPLATES` e `IT_DOC_TYPE_LIST`

Se il Livello 2 non è ancora applicato, fermati e applicalo prima (vedi `integration-livello-2/README.md`).

## Stile UI

Per coerenza col Knowledge Vault esistente:
- **Tema scuro**: background `#0A0A0A`, text `white`, accent `#C5A059` (gold champagne)
- **Font**: Tailwind CSS classes esistenti
- **Icone**: `lucide-react` (già dipendenza)
- **Lingua**: italiano per label UI (coerente col resto dell'app)

## Limiti noti

1. **Performance**: il caricamento del modulo IT aggiunge ~50KB al bundle JS (soprattutto `ITWorkflowTimeline` con 9 fasi). Trascurabile per la maggior parte dei deployment.

2. **Persistenza**: i metadati IT (`itMetadata`) sono già salvati nel Firestore dal Livello 1 (rawFrontmatter preservato). Il Livello 3 li **legge** ma non li modifica — la modifica richiederebbe estendere `useVaultMutations.ts` (fuori scope).

3. **KnowledgeGraph.tsx**: il grafo D3 continua a usare i 6 colori canonici. Per visualizzare i 9 tipi IT con colori distinti servirebbe patchare `KnowledgeGraph.tsx` (candidato per Livello 4 futuro, se richiesto).

4. **MCP / agenti**: il modulo IT non espone strumenti MCP. Se vuoi che un agente AI esterno possa compilare template IT via MCP, serve una nuova implementazione in `server/routes/mcpRoutes.ts` (fuori scope).

## Come applicare le modifiche

Vedi `11-MIGRATION-GUIDE.md` per la guida passo-passo.

In sintesi:

1. Crea la cartella `src/components/itInfrastructure/` nel tuo repo KnowledgeVault
2. Copia i 4 file `0[1-4]-NEW-*.tsx` dentro quella cartella (rimuovendo il prefisso numerico)
3. Applica le 4 patch ai componenti esistenti (KnowledgeReader, Sidebar, CaptureBar, captureRoutes)
4. Copia il servizio `09-NEW-itInfrastructureService.ts` in `server/services/`
5. Verifica con `npm run lint` e test funzionali
6. Commit + PR come descritto in `10-PR-DESCRIPTION.md`

## Prossimi passi

Dopo aver applicato il Livello 3, il tuo Knowledge Vault è pronto per gestire il ciclo lavorativo IT in modo nativo e visuale. Per evoluzioni future (Livello 4) considera:

- Colori D3 dedicati per i 9 tipi IT (richiede patch a `KnowledgeGraph.tsx`)
- Export Excel/CSV degli asset inventariati (richiede nuovo componente `ITAssetInventoryExporter.tsx`)
- Integrazione con calendar per scadenze contratti (richiede nuovo endpoint `/api/it-infrastructure/renewals-calendar`)
- Tool MCP per agenti AI esterni (richiede patch a `mcpRoutes.ts`)
