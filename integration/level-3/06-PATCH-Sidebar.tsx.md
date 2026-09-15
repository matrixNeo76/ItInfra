---
okf_version: "0.2"
id: "patch-level3-sidebar"
title: "Patch 06 — Estensione di src/components/Sidebar.tsx con voce Ciclo IT"
type: "specification"
domain: "UI Components & IT Infrastructure Integration"
tags: ["okf-v0.2", "patch", "sidebar", "it-infrastructure", "level-3"]
entities:
  - name: "ITInfrastructureSidebar trigger"
    type: "specification"
    description: "Voce nella sidebar principale che apre il drawer ITInfrastructureSidebar"
relations:
  - targetTitle: "Patch 05 — KnowledgeReader.tsx extension"
    targetId: "patch-level3-knowledge-reader"
    relationType: "extends"
    weight: 0.9
---

# Patch 06 — Estensione di `src/components/Sidebar.tsx`

## File target
`src/components/Sidebar.tsx`

## Strategia

Aggiungere una voce "Ciclo IT" nella sidebar che apre il drawer `ITInfrastructureSidebar`. La voce mostra anche un badge con il numero di documenti IT presenti nel vault.

---

## Modifica 1 — Aggiungere import in cima al file

### Posizione
Dopo gli import esistenti (in cima al file).

### Codice da aggiungere

```typescript
import { ITInfrastructureSidebar } from "./itInfrastructure/ITInfrastructureSidebar";
import { Network as NetworkIcon } from "lucide-react";
```

**Nota**: se `Network` è già importato, usa un alias come `Network as NetworkIcon` o un altro nome libero.

---

## Modifica 2 — Aggiungere stato per il drawer IT

### Posizione
Dopo le dichiarazioni di `useState` esistenti nel componente `Sidebar`.

### Codice da aggiungere

```typescript
  const [isITSidebarOpen, setIsITSidebarOpen] = useState(false);
```

---

## Modifica 3 — Calcolare il conteggio documenti IT

### Posizione
Dopo le dichiarazioni di stato, in un blocco `useMemo` o calcolo derivato.

### Codice da aggiungere

```typescript
  // Conteggio documenti IT nel vault (con metadati IT o alias IT riconosciuti)
  const itDocsCount = useMemo(() => {
    return allResources.filter(
      (r) => r.metadata?.isITAlias === true || r.metadata?.itMetadata
    ).length;
  }, [allResources]);
```

**Nota**: assicurati che `useMemo` sia importato da React. Se `allResources` non è disponibile come prop in `Sidebar`, passa ad `App.tsx` il compito di renderizzare il drawer e usa solo `itDocsCount` come prop.

---

## Modifica 4 — Aggiungere la voce "Ciclo IT" nella sidebar

### Posizione
Dopo le voci di navigazione esistenti (es. dopo "Tutti", "Preferiti", "Raw Files"), prima della chiusura della lista.

### Codice da aggiungere (pattern da adattare al codice esistente)

```tsx
{/* Voce Ciclo IT — solo se ci sono documenti IT nel vault */}
{itDocsCount > 0 && (
  <button
    onClick={() => setIsITSidebarOpen(true)}
    className="flex items-center justify-between w-full px-3 py-2 text-xs text-[#BBB] hover:text-white hover:bg-[#1A1A1A] rounded transition-colors group"
  >
    <span className="flex items-center gap-2">
      <NetworkIcon className="w-3.5 h-3.5 text-[#C5A059]" />
      <span>Ciclo IT</span>
    </span>
    <span className="text-[10px] text-[#777] bg-[#1A1A1A] px-1.5 py-0.5 rounded">
      {itDocsCount}
    </span>
  </button>
)}
```

---

## Modifica 5 — Renderizzare il drawer IT

### Posizione
In fondo al componente, prima della chiusura `return (</>)` o dell'ultimo `</div>`.

### Codice da aggiungere

```tsx
      {/* Drawer Ciclo IT */}
      <ITInfrastructureSidebar
        isOpen={isITSidebarOpen}
        onClose={() => setIsITSidebarOpen(false)}
        allResources={allResources}
        onNavigate={(resource) => {
          setIsITSidebarOpen(false);
          // Passa la navigazione al handler esistente
          if (typeof onNavigateToResource === "function") {
            onNavigateToResource(resource);
          }
        }}
      />
```

---

## Alternative: integrazione in `App.tsx` invece che in `Sidebar.tsx`

Se la tua `Sidebar` non ha accesso a `allResources` o `onNavigateToResource`, integra il drawer in `App.tsx` invece:

### In `App.tsx`

```typescript
// 1. Import
import { ITInfrastructureSidebar } from "./components/itInfrastructure/ITInfrastructureSidebar";

// 2. Stato
const [isITSidebarOpen, setIsITSidebarOpen] = useState(false);

// 3. Passa un callback alla Sidebar
<Sidebar
  // ... props esistenti ...
  onOpenITSidebar={() => setIsITSidebarOpen(true)}
  itDocsCount={itDocsCount}
/>

// 4. Renderizza il drawer
<ITInfrastructureSidebar
  isOpen={isITSidebarOpen}
  onClose={() => setIsITSidebarOpen(false)}
  allResources={allResources}
  onNavigate={handleNavigateToResource}
/>
```

E nella `Sidebar.tsx`, aggiungi le props `onOpenITSidebar?: () => void` e `itDocsCount?: number`, poi usa il pulsante della Modifica 4 con `onClick={onOpenITSidebar}`.

---

## Verifica post-modifica

1. ✅ `npm run lint` passa senza errori
2. ✅ Se il vault non ha documenti IT, la voce "Ciclo IT" non appare
3. ✅ Se il vault ha almeno 1 documento IT, la voce appare con badge contatore
4. ✅ Cliccando la voce, si apre il drawer laterale destro con timeline + lista progetti
5. ✅ Cliccando su un documento nella timeline, si naviga al reader

## Backward compatibility

- ✅ Tutte le voci esistenti della sidebar restano invariate
- ✅ La voce "Ciclo IT" appare SOLO se `itDocsCount > 0` (zero impatto per vault senza documenti IT)
- ✅ Il drawer è opzionale e non blocca altre interazioni
