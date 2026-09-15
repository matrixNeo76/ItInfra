# PR — Modulo UI Ciclo Lavorativo IT (Livello 3)

## Titolo

`feat(ui): modulo IT infrastructure completo — sidebar, timeline, reader tab, template compiler AI`

## Descrizione

Questa PR aggiunge il modulo UI completo per il ciclo lavorativo IT nel Knowledge Vault, costruendo sopra le estensioni del parser (Livello 2 già mergiato). Gli utenti potranno visualizzare i documenti IT con metadati arricchiti, navigare la timeline delle 7 fasi, e compilare nuovi documenti tramite AI Gemini.

## Cosa cambia

### Nuovi componenti UI (`src/components/itInfrastructure/`)

1. **`ITProjectMetadataCard.tsx`** — Scheda dedicata per visualizzare metadati IT estesi nel KnowledgeReader (project_id, phase, owner_team, related_docs, depends_on, status, version, ecc.)

2. **`ITWorkflowTimeline.tsx`** — Timeline visuale verticale delle 7 fasi del ciclo IT con stato di avanzamento (completato/in_progress/pending) basato sui documenti presenti nel vault

3. **`ITInfrastructureSidebar.tsx`** — Drawer laterale che mostra:
   - Statistiche globali (numero progetti, documenti, doc/progetto)
   - Selettore progetto attivo
   - Timeline fasi per progetto selezionato
   - Distribuzione documenti per tipo IT (9 tipi)

4. **`ITTemplateCompilerModal.tsx`** — Modale full-screen per compilare template IT via AI:
   - Selezione tipo documento (9 tipi raggruppati per fase)
   - Form dati progetto (project_id, project_name, site, customer, author, owner_team)
   - Textarea per dati specifici del documento
   - Anteprima boilerplate YAML
   - Output Markdown completo con azioni Copia/Download

### Patch ai componenti esistenti

5. **`KnowledgeReader.tsx`** — Aggiunto 4° tab "Ciclo IT" (visibile solo se il documento ha metadati IT)

6. **`Sidebar.tsx`** — Aggiunta voce "Ciclo IT" con badge contatore (visibile solo se ci sono documenti IT nel vault)

7. **`CaptureBar.tsx`** — Aggiunto pulsante "Template IT" con icona Sparkles che apre il modale compilatore

### Nuovo servizio backend

8. **`server/services/itInfrastructureService.ts`** — Servizio che usa Gemini 3.7 Flash per compilare template IT a partire da dati strutturati

### Endpoint API

9. **`POST /api/it-infrastructure/compile-template`** — Endpoint stateless che riceve docType + dati progetto + custom_data, restituisce markdown OKF v0.2 completo

10. **`GET /api/it-infrastructure/types`** — Endpoint che restituisce la lista dei 9 tipi IT con metadata (per UI dropdown)

## Schema del flusso utente

```
[CaptureBar]
    ↓ click "Template IT"
[ITTemplateCompilerModal]
    ↓ seleziona tipo + inserisci dati + custom_data
    ↓ POST /api/it-infrastructure/compile-template
[itInfrastructureService.compileITTemplate()]
    ↓ Gemini 3.7 Flash generate
[Markdown OKF v0.2 completo]
    ↓ copia o download
[CaptureBar incolla markdown]
    ↓ onCapture("knowledge")
[Documento salvato nel vault con itMetadata riconosciuto]
    ↓
[Sidebar mostra voce "Ciclo IT" con badge]
    ↓ click
[ITInfrastructureSidebar drawer]
    ↓ seleziona progetto + visualizza timeline
[KnowledgeReader mostra tab "Ciclo IT"]
    ↓ click tab
[ITProjectMetadataCard mostra metadati IT estesi]
```

## Screenshot descrittivi (placeholder per PR reale)

### 1. KnowledgeReader con tab "Ciclo IT"
```
┌────────────────────────────────────────────────────────┐
│ [Lettore Markdown] [Connessioni (5)] [Spec OKF] [Ciclo IT]│
├────────────────────────────────────────────────────────┤
│ [LLD — DC Milano]  [Fase 2 — Design]  [draft]          │
│                                                        │
│ IDENTITÀ                  PROGETTO                     │
│ ID: architecture-acme...  Project ID: acme-milano-2026│
│ Versione: 0.1             Nome: Sostituzione DC Milano │
│ Creato: 2026-03-15        Sito: MIL-01                 │
│                           Cliente: Acme S.p.A.         │
│                                                        │
│ PERSONE                   GOVERNANCE                   │
│ Autore: Mario Rossi       Classificazione: confidential│
│ Revisore: Giulia Bianchi  Retention: 7y                │
│ Approvatore: Luca Verdi   Lingua: it                   │
│ Team: Acme Operations                                 │
│                                                        │
│ DOCUMENTI CORRELATI (3)                                │
│ 01 → HLD — DC Milano                                   │
│ 02 → MOP — Deploy DC Milano                           │
│ 03 → As-Built — DC Milano                              │
└────────────────────────────────────────────────────────┘
```

### 2. ITInfrastructureSidebar drawer
```
                                          ┌────────────────────┐
                                          │ Ciclo Lavorativo IT│
                                          ├────────────────────┤
                                          │ [3 progetti]       │
                                          │ [12 documenti]     │
                                          │ [4.0 doc/progetto] │
                                          ├────────────────────┤
                                          │ PROGETTO ATTIVO    │
                                          │ ▼ Tutti i progetti │
                                          │   • acme-milano-26 │
                                          │   • beta-roma-25   │
                                          │   • gamma-napoli   │
                                          ├────────────────────┤
                                          │ TIMELINE FASI      │
                                          │ ● Fase 1 - Assess. │
                                          │   └ RSD/URS (1)    │
                                          │ ● Fase 2 - Design  │
                                          │   └ HLD (1)         │
                                          │   └ LLD (1)         │
                                          │ ● Fase 3 - Procure.│
                                          │   └ MOP (1)         │
                                          │ ○ Fase 4 - Racking │
                                          │ ○ Fase 5 - Commis. │
                                          │ ○ Fase 6 - Testing │
                                          │ ○ Fase 7 - Go-Live │
                                          └────────────────────┘
```

## Test di regressione

### Pre-condizioni (Livello 2 già mergiato)
- [ ] `src/lib/okfParser.ts` riconosce `isITAlias` e `itMetadata`
- [ ] `src/types.ts` ha `ITProjectMetadata` e `ITDocType`
- [ ] `src/lib/okfItTemplates.ts` esiste con `OKF_IT_TEMPLATES`

### Nuovi test da aggiungere

```typescript
// test/itInfrastructure.test.tsx

import { render, screen, fireEvent } from "@testing-library/react";
import { ITProjectMetadataCard } from "../src/components/itInfrastructure/ITProjectMetadataCard";
import { ITWorkflowTimeline } from "../src/components/itInfrastructure/ITWorkflowTimeline";

describe("ITProjectMetadataCard", () => {
  it("mostra empty state per documento non IT", () => {
    const resource = {
      id: "test-1",
      title: "Generic doc",
      type: "knowledge",
      summary: "test",
      tags: [],
      metadata: {},
    };
    render(<ITProjectMetadataCard resource={resource as any} allResources={[]} onNavigate={() => {}} />);
    expect(screen.getByText(/non fa parte del ciclo lavorativo IT/i)).toBeInTheDocument();
  });

  it("mostra metadati IT per documento con itMetadata", () => {
    const resource = {
      id: "test-2",
      title: "LLD Test",
      type: "knowledge",
      summary: "test",
      tags: [],
      metadata: {
        isITAlias: true,
        originalDocType: "lld",
        itMetadata: {
          project_id: "acme-milano",
          phase: 2,
          status: "draft",
          author: "Mario Rossi",
          related_docs: ["architecture-acme-hld-01"],
        },
      },
    };
    render(<ITProjectMetadataCard resource={resource as any} allResources={[]} onNavigate={() => {}} />);
    expect(screen.getByText("acme-milano")).toBeInTheDocument();
    expect(screen.getByText(/Fase 2/i)).toBeInTheDocument();
    expect(screen.getByText("Mario Rossi")).toBeInTheDocument();
  });
});

describe("ITWorkflowTimeline", () => {
  it("mostra empty state se nessun documento IT", () => {
    render(<ITWorkflowTimeline allResources={[]} onNavigate={() => {}} />);
    expect(screen.getByText(/Nessun documento IT nel vault/i)).toBeInTheDocument();
  });

  it("mostra timeline con 7 fasi", () => {
    render(<ITWorkflowTimeline allResources={[]} onNavigate={() => {}} />);
    expect(screen.getByText(/Fase 1.*Assessment/i)).toBeInTheDocument();
    expect(screen.getByText(/Fase 7.*Go-Live/i)).toBeInTheDocument();
  });
});
```

### Test E2E manuali

1. **Apertura drawer Ciclo IT**: nel vault con almeno 1 documento IT, cliccare la voce "Ciclo IT" nella sidebar — il drawer deve aprirsi
2. **Selezione progetto**: nel drawer, selezionare un progetto — la timeline deve filtrare per quel progetto
3. **Navigazione documento**: cliccare su un documento nella timeline — deve navigare al reader con tab "Ciclo IT" attivo
4. **Compilazione AI**: cliccare "Template IT" nella CaptureBar, compilare il form, e verificare che il documento generato sia conforme OKF v0.2

## Checklist

- [ ] Codice compilato senza errori TypeScript (`npm run lint`)
- [ ] Test esistenti passano (`npm run test:cekikj` se presenti)
- [ ] Nuovi test aggiunti e passano
- [ ] Cartella `src/components/itInfrastructure/` creata con 4 file .tsx
- [ ] `server/services/itInfrastructureService.ts` creato
- [ ] Endpoint `POST /api/it-infrastructure/compile-template` testato via curl
- [ ] Endpoint `GET /api/it-infrastructure/types` restituisce 9 tipi
- [ ] KnowledgeReader mostra tab "Ciclo IT" solo per documenti IT
- [ ] Sidebar mostra voce "Ciclo IT" solo se `itDocsCount > 0`
- [ ] CaptureBar pulsante "Template IT" apre il modale
- [ ] Modale funziona end-to-end: form → Gemini → markdown → copia/download
- [ ] `GEMINI_API_KEY` (o `GOOGLE_API_KEY`) documentata in `.env.example`

## File aggiunti

```
src/components/itInfrastructure/
├── ITProjectMetadataCard.tsx       (NUOVO, ~280 righe)
├── ITWorkflowTimeline.tsx          (NUOVO, ~290 righe)
├── ITInfrastructureSidebar.tsx      (NUOVO, ~250 righe)
└── ITTemplateCompilerModal.tsx     (NUOVO, ~320 righe)

server/services/
└── itInfrastructureService.ts      (NUOVO, ~200 righe)
```

## File modificati

```
src/components/KnowledgeReader.tsx     (+20 righe: import, stato, tab pulsante, rendering)
src/components/Sidebar.tsx              (+25 righe: import, stato, voce sidebar, drawer)
src/components/CaptureBar.tsx           (+30 righe: import, prop, pulsante, modale)
server/routes/captureRoutes.ts         (+90 righe: endpoint POST + GET)
```

## Variabili d'ambiente

Aggiungere a `.env.example`:

```bash
# IT Infrastructure Module (Livello 3)
# Modello Gemini da usare per la compilazione dei template IT
GEMINI_MODEL=gemini-2.5-flash

# NOTA: GEMINI_API_KEY o GOOGLE_API_KEY devono già essere configurate (Livello 1+)
```

## Limiti noti

1. **KnowledgeGraph.tsx non modificato**: il grafo D3 continua a usare 6 colori canonici. I 9 tipi IT non hanno colore distinto. (Candidato per Livello 4.)

2. **Modifica metadati IT non supportata**: il modulo IT è read-only per i metadati. Per modificarli, l'utente deve editare il frontmatter manualmente e ri-caricare il documento. Estendere `useVaultMutations.ts` per edit metadati IT richiede lavoro aggiuntivo (fuori scope).

3. **Compilazione AI non salva nel vault**: l'endpoint `/api/it-infrastructure/compile-template` è stateless. Il client deve copiare il markdown e salvarlo tramite CaptureBar esistente. Auto-salvataggio diretto richiede estensione del servizio (candidato per follow-up).

4. **Quota Gemini**: la compilazione AI consuma quota Gemini. In caso di rate limit (429), il servizio restituisce errore e l'utente deve riprovare. Considerare caching delle compilazioni se il traffico cresce.
