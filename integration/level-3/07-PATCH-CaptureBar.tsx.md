---
okf_version: "0.2"
id: "patch-level3-capture-bar"
title: "Patch 07 — Estensione di src/components/CaptureBar.tsx con pulsante Compila Template IT"
type: "specification"
domain: "UI Components & IT Infrastructure Integration"
tags: ["okf-v0.2", "patch", "capture-bar", "it-infrastructure", "level-3"]
entities:
  - name: "ITTemplateCompilerModal trigger"
    type: "specification"
    description: "Pulsante nella CaptureBar che apre il modale ITTemplateCompilerModal"
relations:
  - targetTitle: "Patch 08 — captureRoutes.ts (API compile-template)"
    targetId: "patch-level3-capture-routes"
    relationType: "depends_on"
    weight: 1.0
---

# Patch 07 — Estensione di `src/components/CaptureBar.tsx`

## File target
`src/components/CaptureBar.tsx`

## Strategia

Aggiungere un pulsante "Compila template IT" nella CaptureBar che apre il modale `ITTemplateCompilerModal`. Il pulsante è distinguibile dalle altre azioni grazie all'icona `Sparkles` e al colore gold.

---

## Modifica 1 — Aggiungere import in cima al file

### Posizione
Dopo gli import esistenti.

### Codice da aggiungere

```typescript
import { ITTemplateCompilerModal } from "./itInfrastructure/ITTemplateCompilerModal";
```

**Nota**: `Sparkles` è già importato da `lucide-react` nella CaptureBar (verifica, altrimenti aggiungilo).

---

## Modifica 2 — Estendere le props del componente

### Posizione
Nell'interfaccia `CaptureBarProps` (riga ~22 circa).

### Codice da aggiungere alle props

```typescript
interface CaptureBarProps {
  // ... props esistenti ...
  onOpenITCompiler?: () => void; // nuovo callback opzionale
}
```

**Nota**: rendere `onOpenITCompiler` opzionale (`?`) per non rompere i chiamanti esistenti.

---

## Modifica 3 — Aggiungere stato per il modale

### Posizione
Dopo le dichiarazioni `useState` esistenti.

### Codice da aggiungere

```typescript
  const [isITCompilerOpen, setIsITCompilerOpen] = useState(false);
```

---

## Modifica 4 — Aggiungere il pulsante nella UI

### Posizione
Nel blocco di rendering della CaptureBar, vicino agli altri pulsanti di azione (es. dopo "Upload raw file" o "Diagnostic").

### Codice da aggiungere (pattern da adattare al layout esistente)

```tsx
{/* Pulsante Compila Template IT */}
<button
  onClick={() => {
    if (onOpenITCompiler) {
      onOpenITCompiler();
    } else {
      setIsITCompilerOpen(true);
    }
  }}
  className="flex items-center gap-1.5 text-xs font-medium bg-[#C5A059]/10 hover:bg-[#C5A059]/20 text-[#C5A059] border border-[#C5A059]/30 px-3 py-1.5 rounded transition-colors"
  title="Compila un template documentale IT con AI"
>
  <Sparkles className="w-3.5 h-3.5" />
  <span>Template IT</span>
</button>
```

---

## Modifica 5 — Renderizzare il modale

### Posizione
In fondo al rendering del componente, prima della chiusura del fragment principale.

### Codice da aggiungere

```tsx
      {/* Modale Compilatore Template IT */}
      <ITTemplateCompilerModal
        isOpen={isITCompilerOpen}
        onClose={() => setIsITCompilerOpen(false)}
        onResourceCompiled={(resource) => {
          // Opzionale: callback quando un documento viene compilato
          // Esempio: triggerare un refresh della lista risorse
          if (onCapture) {
            // Si può riutilizzare onCapture per salvare il documento compilato
            // nel vault (passa il markdown come input)
          }
        }}
      />
```

---

## Modifica 6 (opzionale) — Auto-salvataggio del documento compilato

Se vuoi che il documento compilato venga automaticamente salvato nel vault dopo la generazione AI, modifica il callback `onResourceCompiled`:

```tsx
        onResourceCompiled={async (compiledMarkdown: string) => {
          // Salva nel vault usando onCapture esistente
          if (onCapture) {
            await onCapture(compiledMarkdown, "knowledge");
          }
          setIsITCompilerOpen(false);
        }}
```

In questo caso, modifica anche l'interfaccia di `ITTemplateCompilerModal` per passare il markdown compilato invece di un `ResourceItem`.

---

## Verifica post-modifica

1. ✅ `npm run lint` passa
2. ✅ La CaptureBar mostra il pulsante "Template IT" con icona Sparkles
3. ✅ Cliccando il pulsante si apre il modale `ITTemplateCompilerModal`
4. ✅ Nel modale si può selezionare il tipo documento, inserire dati progetto, e compilare via AI
5. ✅ Il documento generato è copiabile e scaricabile

## Backward compatibility

- ✅ Tutti i pulsanti e le azioni esistenti restano invariati
- ✅ La prop `onOpenITCompiler` è opzionale — se non passata, il modale si gestisce internamente
- ✅ Il modale è opzionale e indipendente dalla CaptureBar esistente
