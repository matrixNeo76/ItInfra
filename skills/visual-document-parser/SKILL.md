---
name: visual-document-parser
description: Native visual document analysis (Pixel-to-Markdown) with OKF v0.2 Artifact generation and two-stage pipeline ingestion for ITInfra.
metadata:
  model: inherit
---

# 📸 Visual Document Parser & OKF v0.2 Intelligence Skill

Questo skill definisce il protocollo di **Analisi Visiva Nativa (Pixel-to-Markdown)** per documenti tecnici allegati e la loro trasformazione in artefatti conformi allo standard **OKF v0.2 (Open Knowledge Framework)** per l'applicativo `itinfra`.

---

## 🎯 Obiettivi Operativi

1. **Pixel-to-Markdown**: Analizzare i documenti tecnici a livello visivo per rispettare l'ordine topologico di lettura, preservare tabelle complesse, note a margine, layout a più colonne, schemi di rack e planimetrie.
2. **Cristallizzazione OKF v0.2**: Trasformare qualsiasi documento tecnico (datasheet switch/firewall, distinte base server, relazioni tecniche di fornitura, certificazioni cavi/fibra) in un "gemello digitale" peritale Markdown prima di aggiornare i manifest e i documenti di progetto.
3. **Zero-Hallucination Guardrail**: Nessun apparato, porta, subnet IP o componente può essere dedotto o inventato. Se non presente, deve essere marcato come `DA-RICHIEDERE` o `NOT_FOUND`.

---

## 📋 Struttura dell'Artefatto OKF v0.2

Ogni documento analizzato DEVE essere strutturato come segue:

```markdown
---
okf_version: "0.2"
id: "spec-[slug]-[titolo]-01"
title: "[Titolo effettivo e univoco del documento]"
type: "specification" # o concept / architecture
description: "[Abstract sintetico del contenuto tecnico, apparato o fornitura]"
domain: "IT Infrastructure & Technical Ingestion"
tags:
  - "document-intelligence"
  - "estrazione-sota"
  - "okf-v0.2"
generated.at: "[Data e ora ISO 8601, es. 2026-09-17T16:35:00Z]"
sources:
  - "file://@[nome_file_originale.ext]"
---

# Punti Chiave
- [Pagina 1] Elemento essenziale, modello apparato, requisiti di alimentazione o ingombro rack.
- [Pagina 1] Specifiche salienti di calcolo, memoria, storage o interfacce di rete.

# Contenuto Semantico
## [Sezione 1: Architettura & Ruolo nell'Infrastruttura]
Descrizione logico-funzionale del componente nel sistema informativo.

## [Sezione 2: Specifiche Tecniche Dettagliate]
Sintesi narrativa fedele delle caratteristiche hardware o dei servizi inclusi.

# Tabelle Estratte
### Tabella 1: [Titolo descrittivo tabella BOM / Hardware]
| Categoria | Prodotto / Descrizione | Quantità | Note / Specifiche |
|---|---|:---:|---|
| Cella 1 | Cella 2 | Cella 3 | Cella 4 |
```

---

## 🛠️ Regole per la Trascrizione delle Tabelle

1. **Completezza Cella per Cella**: È severamente vietato omettere righe o abbreviare con `...` tabelle di componenti o matrici porte.
2. **Preservazione Dati Tecnici**: Part number, capacità dischi (TB/GB), modelli CPU, clock memoria e tipologie di porte (10G SFP+, 25G, PoE+) devono essere trascritti fedelmente.
3. **Allineamento Colonne**:
   * Codici e Part Number: a sinistra o centrati.
   * Descrizioni: a sinistra.
   * Quantità: al centro.

---

## 💻 Ingestione nell'Applicativo CLI

Una volta generato il file `.okf.md`, eseguire l'ingestione deterministica nei file di progetto tramite:

```powershell
python scripts/itinfra.py ingest percorso/documento.okf.md --slug <slug-cliente> --apply
```
