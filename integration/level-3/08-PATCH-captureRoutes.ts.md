---
okf_version: "0.2"
id: "patch-level3-capture-routes"
title: "Patch 08 — Estensione di server/routes/captureRoutes.ts con endpoint compile-template"
type: "specification"
domain: "Backend API & IT Infrastructure Integration"
tags: ["okf-v0.2", "patch", "api", "capture-routes", "it-infrastructure", "level-3"]
entities:
  - name: "IT Template Compile Endpoint"
    type: "specification"
    description: "Endpoint POST /api/it-infrastructure/compile-template che usa Gemini per compilare template IT"
relations:
  - targetTitle: "Patch 07 — CaptureBar.tsx (UI compile modal)"
    targetId: "patch-level3-capture-bar"
    relationType: "depends_on"
    weight: 1.0
    description: "CaptureBar chiama questo endpoint per compilare i template IT"
  - targetTitle: "Patch 09 — itInfrastructureService.ts (new file)"
    targetId: "patch-level3-it-infrastructure-service"
    relationType: "depends_on"
    weight: 1.0
    description: "L'endpoint delega la logica di compilazione a itInfrastructureService"
---

# Patch 08 — Estensione di `server/routes/captureRoutes.ts`

## File target
`server/routes/captureRoutes.ts`

## Strategia

Aggiungere un nuovo endpoint `POST /api/it-infrastructure/compile-template` che:
1. Riceve `docType` (uno dei 9 tipi IT), dati di progetto (project_id, project_name, ecc.) e dati custom
2. Recupera il boilerplate YAML da `OKF_IT_TEMPLATES`
3. Costruisce un prompt strutturato per Gemini 3.7 Flash
4. Chiama il servizio `itInfrastructureService.compileITTemplate()` per ottenere il documento Markdown completo
5. Restituisce il documento generato al client

L'endpoint è **stateless** (non salva direttamente su Firestore — il client deve fare il salvataggio tramite CaptureBar esistente).

---

## Modifica 1 — Aggiungere import in cima al file

### Posizione
Dopo gli import esistenti.

### Codice da aggiungere

```typescript
import { compileITTemplate } from "../services/itInfrastructureService";
import { IT_DOC_TYPES, getITBoilerplate } from "../../src/lib/okfItTemplates";
import { ITDocType } from "../../src/types";
```

**Nota**: i path dipendono dalla struttura del tuo repo. Adatta `../../src/...` se necessario.

---

## Modifica 2 — Aggiungere il nuovo endpoint

### Posizione
In fondo al file, prima di `export const captureRouter = Router();` o dopo gli endpoint esistenti.

### Codice da aggiungere

```typescript
// ============================================================================
// IT INFRASTRUCTURE — Template compiler endpoint (Livello 3)
// ============================================================================

interface ITCompileRequest {
  docType: string;            // uno dei 9 ITDocType
  project_id: string;
  project_name: string;
  site?: string;
  customer?: string;
  author?: string;
  reviewer?: string;
  approver?: string;
  owner_team?: string;
  custom_data?: string;        // textarea libera con dati specifici del documento
}

interface ITCompileResponse {
  success: boolean;
  markdown?: string;          // documento OKF v0.2 completo generato
  id?: string;                 // ID suggerito per il salvataggio
  error?: string;
  modelUsed?: string;
  durationMs?: number;
}

// POST /api/it-infrastructure/compile-template
// Compila un template documentale IT usando Gemini 3.7 Flash
captureRouter.post("/it-infrastructure/compile-template", async (req, res) => {
  const startTime = Date.now();

  try {
    const body = req.body as ITCompileRequest;

    // 1. Validazione input
    if (!body.docType || !body.project_id || !body.project_name) {
      return res.status(400).json({
        success: false,
        error: "Campi obbligatori mancanti: docType, project_id, project_name sono richiesti",
      } as ITCompileResponse);
    }

    // 2. Verifica che docType sia uno dei 9 tipi IT canonici
    const docType = body.docType.toLowerCase().replace(/[\s-]+/g, "_");
    if (!(docType in IT_DOC_TYPES)) {
      return res.status(400).json({
        success: false,
        error: `docType '${body.docType}' non valido. Tipi IT ammessi: ${Object.keys(IT_DOC_TYPES).join(", ")}`,
      } as ITCompileResponse);
    }

    // 3. Recupera il boilerplate YAML per il tipo richiesto
    const boilerplate = getITBoilerplate(docType as ITDocType);
    if (!boilerplate) {
      return res.status(500).json({
        success: false,
        error: `Boilerplate non trovato per docType '${docType}'`,
      } as ITCompileResponse);
    }

    // 4. Sostituisci i placeholder del project_slug nel boilerplate
    const projectSlug = body.project_id.toLowerCase().replace(/[^a-z0-9-]/g, "-");
    const boilerplateWithProject = boilerplate.replace(/<project_slug>/g, projectSlug);

    // 5. Costruisci il prompt per Gemini
    const promptContext = {
      docType,
      docTypeInfo: IT_DOC_TYPES[docType as ITDocType],
      boilerplate: boilerplateWithProject,
      project: {
        id: body.project_id,
        name: body.project_name,
        site: body.site,
        customer: body.customer,
        author: body.author,
        reviewer: body.reviewer,
        approver: body.approver,
        owner_team: body.owner_team,
      },
      customData: body.custom_data,
    };

    // 6. Chiama il servizio di compilazione
    const result = await compileITTemplate(promptContext);

    if (!result.success) {
      return res.status(500).json({
        success: false,
        error: result.error || "Errore sconosciuto durante la compilazione",
      } as ITCompileResponse);
    }

    // 7. Risposta di successo
    return res.json({
      success: true,
      markdown: result.markdown,
      id: `${IT_DOC_TYPES[docType as ITDocType].canonical}-${projectSlug}-${docType}-01`,
      modelUsed: result.modelUsed,
      durationMs: Date.now() - startTime,
    } as ITCompileResponse);

  } catch (err: any) {
    console.error("[IT Infrastructure] Errore compile-template:", err);
    return res.status(500).json({
      success: false,
      error: err?.message || "Errore interno del server durante la compilazione del template IT",
    } as ITCompileResponse);
  }
});

// GET /api/it-infrastructure/types — lista tipi IT disponibili (per UI dropdown)
captureRouter.get("/it-infrastructure/types", (req, res) => {
  try {
    const types = Object.entries(IT_DOC_TYPES).map(([type, info]) => ({
      type,
      ...info,
    }));
    return res.json({
      success: true,
      types,
    });
  } catch (err: any) {
    return res.status(500).json({
      success: false,
      error: err?.message || "Errore recupero tipi IT",
    });
  }
});
```

---

## Verifica post-modifica

1. ✅ `npm run lint` passa
2. ✅ Avvia il server: `npm run dev`
3. ✅ Test endpoint lista tipi:
   ```bash
   curl http://localhost:3000/api/it-infrastructure/types
   ```
   Deve restituire i 9 tipi IT con metadata.

4. ✅ Test endpoint compilazione (richiede `GEMINI_API_KEY` configurata):
   ```bash
   curl -X POST http://localhost:3000/api/it-infrastructure/compile-template \
     -H "Content-Type: application/json" \
     -d '{
       "docType": "lld",
       "project_id": "test-proj",
       "project_name": "Test Project",
       "site": "MIL-01",
       "customer": "Acme",
       "author": "Mario Rossi",
       "custom_data": "Subnet: 10.10.10.0/24 DMZ\\nVLAN: 10 DMZ, 20 PROD"
     }'
   ```
   Deve restituire un documento Markdown completo con frontmatter OKF v0.2 valido.

## Backward compatibility

- ✅ Tutti gli endpoint esistenti restano invariati
- ✅ Il nuovo endpoint non interferisce con `/api/analyze-resource` o altri
- ✅ Il nuovo endpoint è stateless — non scrive su Firestore, non altera il vault
