# Guida alla Migrazione — Livello 3

Questa guida ti accompagna passo-passo nell'applicazione del modulo Livello 3 al tuo repo KnowledgeVault, dopo che il Livello 2 è già stato applicato.

## Prerequisiti

- [ ] Livello 2 applicato (vedi `integration-livello-2/05-MIGRATION-GUIDE.md`)
- [ ] `src/lib/okfParser.ts` riconosce `isITAlias` e `itMetadata`
- [ ] `src/types.ts` ha `ITProjectMetadata` e `ITDocType`
- [ ] `src/lib/okfItTemplates.ts` esiste con `OKF_IT_TEMPLATES` e `IT_DOC_TYPE_LIST`
- [ ] `GEMINI_API_KEY` (o `GOOGLE_API_KEY`) configurata nel file `.env`
- [ ] Working directory pulita: `git status` non deve mostrare modifiche non committate
- [ ] Branch attivo: `git checkout -b feature/it-infrastructure-ui`

## Step 1 — Creare la cartella `src/components/itInfrastructure/`

```bash
cd /path/to/KnowledgeVault
mkdir -p src/components/itInfrastructure
```

## Step 2 — Copiare i 4 nuovi componenti React

```bash
# Copia i 4 file .tsx dalla cartella integration-livello-3/
cp /path/to/integration-livello-3/01-NEW-ITProjectMetadataCard.tsx \
   src/components/itInfrastructure/ITProjectMetadataCard.tsx

cp /path/to/integration-livello-3/02-NEW-ITWorkflowTimeline.tsx \
   src/components/itInfrastructure/ITWorkflowTimeline.tsx

cp /path/to/integration-livello-3/03-NEW-ITInfrastructureSidebar.tsx \
   src/components/itInfrastructure/ITInfrastructureSidebar.tsx

cp /path/to/integration-livello-3/04-NEW-ITTemplateCompilerModal.tsx \
   src/components/itInfrastructure/ITTemplateCompilerModal.tsx

# Verifica
ls -lh src/components/itInfrastructure/
```

Output atteso:
```
ITInfrastructureSidebar.tsx
ITProjectMetadataCard.tsx
ITTemplateCompilerModal.tsx
ITWorkflowTimeline.tsx
```

## Step 3 — Copiare il servizio backend

```bash
cp /path/to/integration-livello-3/09-NEW-itInfrastructureService.ts \
   server/services/itInfrastructureService.ts

# Verifica
ls -lh server/services/itInfrastructureService.ts
```

## Step 4 — Aggiornare `.env.example` con nuove variabili

```bash
cat >> .env.example << 'EOF'

# IT Infrastructure Module (Livello 3)
# Modello Gemini da usare per la compilazione dei template IT
GEMINI_MODEL=gemini-2.5-flash
EOF
```

## Step 5 — Applicare patch a `src/components/KnowledgeReader.tsx`

Apri `05-PATCH-KnowledgeReader.tsx.md` e applica le 5 modifiche descritte:

1. Aggiungi import di `ITProjectMetadataCard`
2. Estendi il tipo `activeTab` con `"it_metadata"`
3. Aggiungi detection `hasITMetadata` (calcolato da `resource.metadata?.itMetadata || resource.metadata?.isITAlias`)
4. Aggiungi il pulsante tab "Ciclo IT" (condizionato a `hasITMetadata`)
5. Aggiungi il rendering del tab `it_metadata`

### Verifica
```bash
npm run lint
# Deve passare senza errori
```

## Step 6 — Applicare patch a `src/components/Sidebar.tsx`

Apri `06-PATCH-Sidebar.tsx.md` e applica le 5 modifiche:

1. Aggiungi import di `ITInfrastructureSidebar` e `Network` icon
2. Aggiungi stato `isITSidebarOpen`
3. Calcola `itDocsCount` con `useMemo`
4. Aggiungi la voce "Ciclo IT" nella lista (condizionata a `itDocsCount > 0`)
5. Renderizza il drawer `<ITInfrastructureSidebar />` in fondo al componente

**Alternativa**: se la tua `Sidebar.tsx` non ha accesso a `allResources`, integra il drawer in `App.tsx` invece (vedi sezione "Alternative" nella patch).

### Verifica
```bash
npm run lint
# Deve passare
```

## Step 7 — Applicare patch a `src/components/CaptureBar.tsx`

Apri `07-PATCH-CaptureBar.tsx.md` e applica le 5 modifiche:

1. Aggiungi import di `ITTemplateCompilerModal`
2. Estendi `CaptureBarProps` con `onOpenITCompiler?: () => void`
3. Aggiungi stato `isITCompilerOpen`
4. Aggiungi il pulsante "Template IT" con icona `Sparkles`
5. Renderizza il modale `<ITTemplateCompilerModal />`

### Verifica
```bash
npm run lint
# Deve passare
```

## Step 8 — Applicare patch a `server/routes/captureRoutes.ts`

Apri `08-PATCH-captureRoutes.ts.md` e applica le 2 modifiche:

1. Aggiungi import di `compileITTemplate`, `IT_DOC_TYPES`, `getITBoilerplate`, `ITDocType`
2. Aggiungi i 2 nuovi endpoint:
   - `POST /api/it-infrastructure/compile-template`
   - `GET /api/it-infrastructure/types`

### Verifica
```bash
npm run lint
# Deve passare
```

## Step 9 — Test funzionale end-to-end

### Avvia il server

```bash
npm run dev
```

Il server deve partire senza errori. Verifica che non ci siano warning TypeScript nella console.

### Test 1: endpoint lista tipi

```bash
curl http://localhost:3000/api/it-infrastructure/types | python3 -m json.tool
```

**Output atteso**: oggetto JSON con 9 tipi IT e relativi metadata (canonical, label, phase, description).

### Test 2: endpoint compilazione (richiede GEMINI_API_KEY)

```bash
curl -X POST http://localhost:3000/api/it-infrastructure/compile-template \
  -H "Content-Type: application/json" \
  -d '{
    "docType": "rsd_urs",
    "project_id": "test-proj-2026",
    "project_name": "Test Project Demo",
    "site": "MIL-01",
    "customer": "Acme S.p.A.",
    "author": "Mario Rossi",
    "owner_team": "Acme Operations",
    "custom_data": "Requisiti:\n- Sostituzione infrastruttura legacy\n- SLA 99.9%\n- RTO 4h, RPO 1h\n- Compliance GDPR + ISO 27001"
  }' | python3 -c "import sys, json; d = json.load(sys.stdin); print(d.get('markdown', '')[:500] if d.get('success') else d.get('error'))"
```

**Output atteso**: un documento Markdown che inizia con `---` (frontmatter YAML OKF v0.2) contenente `okf_version: "0.2"`, `type: "specification"`, `project_id: "test-proj-2026"`, ecc.

### Test 3: UI drawer Ciclo IT

1. Apri il browser su `http://localhost:5173` (o la porta del dev server Vite)
2. Carica almeno 1 documento IT nel vault (es. incolla il markdown del test precedente nella CaptureBar)
3. Verifica che la sidebar mostri la voce "Ciclo IT" con badge `1`
4. Clicca la voce — il drawer deve aprirsi
5. Verifica che la timeline mostri la fase 1 completata
6. Clicca sul documento nella timeline — deve aprire il KnowledgeReader con tab "Ciclo IT" attivo

### Test 4: modale compilazione AI

1. Clicca il pulsante "Template IT" nella CaptureBar
2. Seleziona un tipo (es. `hld`)
3. Compila i campi obbligatori (project_id, project_name)
4. (Opzionale) Aggiungi dati custom nella textarea
5. Clicca "Compila con AI"
6. Verifica che il documento generato sia OKF v0.2 valido e copiabile

## Step 10 — Commit e push

```bash
# Verifica modifiche
git status
git diff --stat

# Commit
git add src/components/itInfrastructure/ \
        server/services/itInfrastructureService.ts \
        src/components/KnowledgeReader.tsx \
        src/components/Sidebar.tsx \
        src/components/CaptureBar.tsx \
        server/routes/captureRoutes.ts \
        .env.example

git commit -m "feat(ui): modulo IT infrastructure completo — sidebar, timeline, reader tab, template compiler AI

- Aggiunto ITProjectMetadataCard nel KnowledgeReader (4° tab 'Ciclo IT')
- Aggiunto ITWorkflowTimeline con 7 fasi visualizzate verticalmente
- Aggiunto ITInfrastructureSidebar drawer laterale con stats + project selector + timeline
- Aggiunto ITTemplateCompilerModal per compilare template IT via Gemini
- Aggiunto servizio backend itInfrastructureService.ts (Gemini 3.7 Flash)
- Aggiunto endpoint POST /api/it-infrastructure/compile-template (stateless)
- Aggiunto endpoint GET /api/it-infrastructure/types
- Aggiunto pulsante 'Template IT' in CaptureBar
- Aggiunta voce 'Ciclo IT' in Sidebar con badge contatore
- Documentazione: PR description + migration guide incluse

Vedi integration-livello-3/README.md per dettagli."

# Push
git push origin feature/it-infrastructure-ui
```

## Step 11 — Aprire la PR su GitHub

1. Vai su https://github.com/matrixNeo76/KnowledgeVault
2. Clicca "Compare & pull request" per il branch `feature/it-infrastructure-ui`
3. Usa il titolo e la descrizione da `10-PR-DESCRIPTION.md`
4. Aggiungi label: `enhancement`, `ui`, `it-infrastructure`, `ai-integration`
5. Collega la PR alla issue del Livello 3 (se esiste)
6. Verifica che CI passi (lint, test)

## Troubleshooting

### Errore: "Cannot find module './itInfrastructure/ITProjectMetadataCard'"

**Causa**: la cartella `src/components/itInfrastructure/` non esiste o il file non è stato copiato.

**Fix**:
```bash
mkdir -p src/components/itInfrastructure
ls src/components/itInfrastructure/
# Se vuoto, copia i file come descritto nello Step 2
```

### Errore: "IT_DOC_TYPES is not exported from ../../lib/okfItTemplates"

**Causa**: il Livello 2 non è stato applicato correttamente.

**Fix**: verifica che `src/lib/okfItTemplates.ts` esista ed esporti `IT_DOC_TYPES`:
```bash
grep "export const IT_DOC_TYPES" src/lib/okfItTemplates.ts
# Se non trova nulla, applica il Livello 2 prima di procedere
```

### Errore: "GEMINI_API_KEY is not configured"

**Causa**: la variabile d'ambiente non è impostata.

**Fix**:
```bash
# Verifica
echo $GEMINI_API_KEY

# Se vuota, aggiungila a .env (NON committare il file .env)
echo 'GEMINI_API_KEY=your_actual_key_here' >> .env

# Verifica che .env sia in .gitignore
grep "^\.env$" .gitignore
```

### Errore 429 da Gemini (rate limit)

**Causa**: troppe richieste in poco tempo.

**Fix**: attendi 60 secondi e riprova. Se persiste, configura `GEMINI_MODEL=gemini-2.5-flash` (più generoso) invece di `gemini-3.7-flash`.

### La voce "Ciclo IT" non appare nella sidebar

**Causa probabile**: non ci sono documenti IT nel vault (la voce è condizionata a `itDocsCount > 0`).

**Fix**: crea un documento IT di test. Puoi usare uno dei 9 template in `/download/templates/0[1-9]-*.md` e incollarlo nella CaptureBar.

### Il modale "Template IT" non si apre

**Causa**: la prop `onOpenITCompiler` non è passata alla CaptureBar, e lo stato interno non è configurato correttamente.

**Fix**: verifica la Modifica 3 e 4 della patch `07-PATCH-CaptureBar.tsx.md`. Lo stato `isITCompilerOpen` deve essere dichiarato e il pulsante deve chiamare `setIsITCompilerOpen(true)`.

### Il documento generato da Gemini non è OKF v0.2 valido

**Causa**: Gemini a volte ignora le istruzioni o genera output non conforme.

**Fix**:
1. Verifica che il `systemPrompt` in `itInfrastructureService.ts` sia completo
2. Prova a fornire più dati specifici nella textarea del modale
3. Come fallback, copia il boilerplate YAML da `OKF_IT_TEMPLATES` e popola manualmente i campi

## Rollback in caso di problemi

```bash
# Ripristina il branch di backup
git checkout backup/pre-it-ui  # se creato prima

# Oppure resetta
git checkout main
git branch -D feature/it-infrastructure-ui

# Rimuovi i file creati (se necessario)
rm -rf src/components/itInfrastructure/
rm server/services/itInfrastructureService.ts
```

## Conclusione

Dopo aver completato gli Step 1-11, il tuo Knowledge Vault ha:

1. ✅ Parser esteso (Livello 2) che riconosce 9 tipi IT
2. ✅ Modulo UI completo (Livello 3) per visualizzare e compilare documenti IT
3. ✅ Endpoint API stateless per compilazione AI via Gemini
4. ✅ Timeline visuale delle 7 fasi con stato avanzamento
5. ✅ Drawer laterale con statistiche e filtro per progetto
6. ✅ Modale "Compila template IT" accessibile dalla CaptureBar

Il sistema è pronto per l'uso operativo. Per futuri miglioramenti (Livello 4) considera:
- Colori D3 dedicati per i 9 tipi IT
- Export Excel/CSV degli asset inventariati
- Modifica inline dei metadati IT
- Integrazione con calendar per scadenze contratti
- Tool MCP per agenti AI esterni
