---
okf_version: "0.2"
id: "patch-level3-knowledge-reader"
title: "Patch 05 — Estensione di src/components/KnowledgeReader.tsx con tab Ciclo IT"
type: "specification"
domain: "UI Components & IT Infrastructure Integration"
tags: ["okf-v0.2", "patch", "knowledge-reader", "it-infrastructure", "level-3"]
entities:
  - name: "ITProjectMetadataCard integration"
    type: "specification"
    description: "Nuovo tab 'Ciclo IT' nel KnowledgeReader che mostra metadati IT estesi"
relations:
  - targetTitle: "Patch 06 — Sidebar.tsx extension"
    targetId: "patch-level3-sidebar"
    relationType: "extends"
    weight: 0.9
    description: "Sidebar integra la voce Ciclo IT che apre il drawer laterale"
---

# Patch 05 — Estensione di `src/components/KnowledgeReader.tsx`

## File target
`src/components/KnowledgeReader.tsx`

## Strategia

Aggiungere un 4° tab "Ciclo IT" al KnowledgeReader esistente, che mostra il componente `ITProjectMetadataCard` quando il documento selezionato è un documento IT riconosciuto (presenza di `itMetadata` o `isITAlias: true`).

Il tab viene visualizzato **solo** se il documento ha metadati IT — per documenti OKF generici resta invisibile (zero impatto su UX esistente).

---

## Modifica 1 — Aggiungere import in cima al file

### Posizione
Dopo gli import esistenti (riga ~32 circa, dopo `import { identifyRelatedResources }`).

### Codice da aggiungere

```typescript
import { ITProjectMetadataCard } from "./itInfrastructure/ITProjectMetadataCard";
```

---

## Modifica 2 — Estendere il tipo `activeTab`

### Posizione
Riga ~55 (riga con `useState<"document" | "okf_spec" | "graph_links">`).

### Vecchio codice

```typescript
  const [activeTab, setActiveTab] = useState<"document" | "okf_spec" | "graph_links">("document");
```

### Nuovo codice

```typescript
  const [activeTab, setActiveTab] = useState<"document" | "okf_spec" | "graph_links" | "it_metadata">("document");
```

---

## Modifica 3 — Aggiungere detection documento IT

### Posizione
Dopo le dichiarazioni di stato (riga ~60, prima di `const handleDownloadPdf`).

### Codice da aggiungere

```typescript
  // === IT Infrastructure detection (Livello 3) ===
  // Verifica se il documento corrente ha metadati IT (ciclo lavorativo IT)
  const currentResource = currentResource_ || resource; // alias per coerenza
  const hasITMetadata = Boolean(
    (currentResource_ || resource)?.metadata?.itMetadata ||
    (currentResource_ || resource)?.metadata?.isITAlias
  );
```

**Nota**: usa `currentResource_` se già esiste nel tuo file (alcune versioni del reader usano `currentResource` invece di `resource`). Adatta il nome della variabile.

---

## Modifica 4 — Aggiungere il pulsante tab "Ciclo IT"

### Posizione
Dopo il pulsante tab "okf_spec" (riga ~404, prima della chiusura del `<div>` dei tab).

### Vecchio codice (fine, riga ~404-405 circa)

```typescript
            <span>Specifica OKF</span>
          </button>
        </div>
```

### Nuovo codice (aggiungi PRIMA della chiusura `</div>`)

```typescript
            <span>Specifica OKF</span>
          </button>
          {hasITMetadata && (
            <button
              onClick={() => setActiveTab("it_metadata")}
              className={`py-2.5 sm:py-3 text-xs font-medium border-b-2 transition-colors flex items-center gap-1.5 shrink-0 ${
                activeTab === "it_metadata"
                  ? "border-[#C5A059] text-white"
                  : "border-transparent text-[#777] hover:text-[#BBB]"
              }`}
            >
              <FolderKanban className="w-3.5 h-3.5 text-[#C5A059]" />
              <span>Ciclo IT</span>
            </button>
          )}
        </div>
```

**Nota**: aggiungi `FolderKanban` agli import di `lucide-react` in cima al file se non è già presente.

---

## Modifica 5 — Aggiungere rendering del tab "it_metadata"

### Posizione
Dopo il rendering del tab "okf_spec" (riga ~760 circa, prima della chiusura del componente principale).

### Vecchio codice (fine, riga ~765-768 circa)

```typescript
          {activeTab === "okf_spec" && (
            // ... contenuto esistente ...
          )}
        </div>
      </div>
    </>
  );
};
```

### Nuovo codice (aggiungi PRIMA della chiusura `</div></div>`)

```typescript
          {activeTab === "okf_spec" && (
            // ... contenuto esistente ...
          )}

          {activeTab === "it_metadata" && hasITMetadata && (
            <div className="flex-1 overflow-y-auto">
              <ITProjectMetadataCard
                resource={currentResource_ || resource}
                allResources={allResources}
                onNavigate={onNavigateToResource}
              />
            </div>
          )}
        </div>
      </div>
    </>
  );
};
```

---

## Verifica post-modifica

Dopo aver applicato le modifiche:

1. ✅ `npm run lint` deve passare senza errori TypeScript
2. ✅ Apri un documento OKF generico — il tab "Ciclo IT" NON deve essere visibile
3. ✅ Apri un documento con `type: "lld"` o con metadati IT — il tab "Ciclo IT" deve apparire
4. ✅ Cliccando sul tab "Ciclo IT", il componente `ITProjectMetadataCard` mostra project_id, phase, related_docs, depends_on, ecc.

## Backward compatibility

- ✅ I 3 tab esistenti (`document`, `graph_links`, `okf_spec`) restano invariati
- ✅ Il tab "it_metadata" appare SOLO se il documento ha metadati IT (`hasITMetadata`)
- ✅ Per documenti OKF generici non c'è nessun impatto visivo
- ✅ Nessun cambiamento nelle props del componente `KnowledgeReader`
