# Esempi di prompt per agenti AI

Questa cartella contiene **prompt di esempio** che l'utente può inviare a un agente AI per fargli compilare i template documentali del knowledge vault.

---

## Come usare questi esempi

### Workflow tipico

1. **Scegli l'esempio** corrispondente al documento che devi compilare (es. `03-prompt-LLD.md` per il Low-Level Design)
2. **Copia il prompt** nell'esempio e incollalo nella tua chat agentic (Claude, Cursor, ChatGPT, ecc.)
3. **Personalizza i dati** sostituendo i valori fittizi (Acme S.p.A., IP, hostname) con quelli del tuo progetto reale
4. **Invia il prompt** all'agente
5. **Verifica l'output**: l'agente dovrebbe restituire il documento completo in un blocco Markdown + un riepilogo + suggerimento di salvataggio
6. **Salva il documento** nel tuo vault (path suggerito dall'agente o da te scelto)

### Struttura di ogni esempio

Ogni file `NN-prompt-TIPO.md` contiene:

1. **Scenario**: descrizione del progetto fittizio usato come esempio
2. **Prompt completo**: il testo da copiare nella chat agentic
3. **Output atteso**: struttura del documento che l'agente dovrebbe produrre
4. **Tip & trucchi**: suggerimenti specifici per quel tipo di documento

---

## Indice degli esempi

| File | Documento | Fase | Complessità |
|------|-----------|------|-------------|
| [00-prompt-master-template.md](./00-prompt-master-template.md) | Struttura generica | — | — |
| [01-prompt-RSD-URS.md](./01-prompt-RSD-URS.md) | Requisiti | 1 | Bassa |
| [02-prompt-HLD.md](./02-prompt-HLD.md) | High-Level Design | 2 | Media |
| [03-prompt-LLD.md](./03-prompt-LLD.md) | Low-Level Design | 2 | Alta |
| [04-prompt-MOP.md](./04-prompt-MOP.md) | Method of Procedure | 3 | Alta |
| [05-prompt-Rollback.md](./05-prompt-Rollback.md) | Rollback Plan | 3 | Media |
| [06-prompt-As-Built.md](./06-prompt-As-Built.md) | As-Built | 5-7 | Alta |
| [07-prompt-ATP.md](./07-prompt-ATP.md) | Acceptance Test Plan | 6 | Media |
| [08-prompt-SOP-Runbook.md](./08-prompt-SOP-Runbook.md) | SOP / Runbook | 7 | Alta |
| [09-prompt-Handover-Inventory.md](./09-prompt-Handover-Inventory.md) | Handover & Inventory | 7 | Media |

---

## Prima di iniziare: leggi questi file

Se è la prima volta che usi questi template, invia all'agente questo prompt iniziale:

```text
Prima di iniziare a compilare i documenti, leggi questi file per capire le convenzioni:
1. /download/templates/AGENTS.md (o CLAUDE.md se sei Claude Code)
2. /download/templates/00-INDEX.md
3. /download/templates/README.md

Conferma di averli letti e fammi un riepilogo di 5 righe delle regole principali.
```

Solo dopo la conferma dell'agente, procedi con il prompt specifico del documento da compilare.

---

## Convenzioni dei prompt di esempio

- I dati di esempio sono **fittizi** (cliente "Acme S.p.A.", sito "Milano") — vanno sostituiti con dati reali
- I percorsi dei file sono relativi a `/home/z/my-project/download/templates/` — adattali alla struttura del tuo vault
- Gli `id` dei documenti di esempio seguono il pattern `<type-canonical>-<project_slug>-<subtype>-<seq>` (es. `architecture-acme-milano-lld-01`)
- I prompt sono scritti in italiano per coerenza con la lingua dei template

---

## Personalizzazione avanzata

Se il tuo progetto ha esigenze specifiche (compliance aggiuntive, vendor particolari, struttura team custom), aggiungi al prompt una sezione "Contesto aggiuntivo" con queste informazioni. L'agente le integrerà nelle sezioni appropriate del documento.

Esempio:

```text
[...prompt standard...]

CONTESTO AGGIUNTIVO:
- Compliance: oltre a GDPR, dobbiamo rispettare la normativa ACN per crittografia
- Vendor storage: NetApp (NON HPE/Dell)
- Team operations: 3 persone (1 NO H24, 1 system engineer, 1 storage engineer)
- Lingua documentazione: italiano per body, inglese per label tecniche
```
