---
okf_version: "0.2"
id: "specification-itinfra-visual-ingestion-v01"
title: "Specifica Tecnica — Analisi Visiva Nativa (Pixel-to-Markdown) & OKF v0.2 Ingestion"
type: "specification"
domain: "IT Infrastructure & Technical Ingestion"
tags: ["okf-v0.2", "specification", "document-intelligence", "pixel-to-markdown", "deep-thinking", "zero-hallucination", "pipeline"]
project_id: "itinfra-core"
project_name: "ITInfra Automation Suite"
phase: 0
author: "matrixNeo76"
reviewer: "Lead Architect"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture & Knowledge Engineering"
status: "approved"
version: "1.0.0"
created_at: "2026-09-17"
updated_at: "2026-09-17"
related_docs:
  - "guide-pipeline-creazione-guidata-antigravity-01"
  - "specification-itinfra-assistant-v02"
depends_on:
  - "architecture-itinfra-docs-index-01"
classification: "public"
retention: "permanent"
lang: "it"
---

# Specifica Tecnica — Analisi Visiva Nativa (Pixel-to-Markdown) & OKF v0.2 Ingestion

## 1. Visione d'Insieme
Questo documento formalizza lo standard architetturale per la lettura, decodifica e integrazione di documenti tecnici complessi (datasheet apparati di rete, distinte base hardware/server BOM, topologie, planimetrie rack, certificazioni cablaggio) all'interno dell'ecosistema ingegneristico **ITInfra**.

---

## 2. Architettura a Due Stadi (Two-Stage Architecture)

```
+---------------------------+       +-------------------------------+
|  Documento Tecnico Allegato|       |  Stage 1: Analisi Visiva SOTA  |
|  (PDF, Immagine, Scanner) | ----> |  (Pixel-to-Markdown + Thinking)|
+---------------------------+       +-------------------------------+
                                                    |
                                                    v
                                    +-------------------------------+
                                    |  Artefatto Certificato OKF v0.2|
                                    |  (docs/<slug>-<nome>.okf.md)  |
                                    +-------------------------------+
                                                    |
                                                    v
+---------------------------+       +-------------------------------+
|  Aggiornamento Deterministico      |  Stage 2: CLI Ingestion        |
|  - project-manifest.yaml   | <---- |  `it ingest <file> --apply`   |
|  - 06-As-Built.md          |       +-------------------------------+
|  - 09-Handover-Inventory.md|
+---------------------------+
```

### Stadio 1: Analisi Visiva Nativa & Generazione Artefatto OKF v0.2
* **Input**: File binario (PDF, JPG, PNG) caricato in chat Antigravity.
* **Motore**: Visione Multimodale Nativa + Deep Thinking.
* **Output**: Artefatto Markdown conforme a **OKF v0.2 (`.okf.md`)**.
* **Principio Guida**: Preservazione dell'ordine topologico reale di lettura, celle unite, riquadri a colonna e trascrizione integrale delle matrici porte e distinte hardware senza sintesi né omissioni.

### Stadio 2: Ingestione Deterministica nei File di Progetto
* **Input**: File `.okf.md` generato nello Stadio 1.
* **Motore**: CLI ITInfra (`scripts/itinfra_ingest.py` via `it ingest`).
* **Output**: Aggiornamento convalidato da schema di:
  * `projects/<slug>/project-manifest.yaml` (blocco hardware censito).
  * `projects/<slug>/06-As-Built.md` (§2 Architettura Fisica e §4 Inventario Hardware Installato).
  * `projects/<slug>/09-Handover-Inventory.md` (§2 Inventario Apparati Hardware).

---

## 3. Schema Frontmatter OKF v0.2

```yaml
---
okf_version: "0.2"
id: "spec-[slug]-[titolo]-01"
title: "[Nome/Titolo Univoco Documento]"
type: "specification" # o concept / architecture
description: "[Abstract sintetico del contenuto]"
domain: "IT Infrastructure & Technical Ingestion"
tags:
  - "document-intelligence"
  - "estrazione-sota"
  - "okf-v0.2"
generated.at: "[ISO 8601 Timestamp]"
sources:
  - "file://@[nome_file.pdf]"
---
```

---

## 4. Sezioni Strutturali dell'Artefatto Tecnico

1. `# Punti Chiave`
   - Sintesi dei vincoli dimensionali, alimentazione, raffreddamento e caratteristiche salienti con tag `[Pagina X]`.
2. `# Contenuto Semantico`
   - Architettura logico-funzionale, topologia e ruoli organizzati per sezioni pulite.
3. `# Tabelle Estratte`
   - Matrice componenti BOM (Server, Switch, Firewall, CPU, RAM, Dischi SSD/NVMe, Moduli transceiver) trascritta integralmente cella per cella.

---

## 5. Regole Anti-Allucinazione e Integrazione Hub-and-Spoke
* **Nessun Dato Tecnico Inventato**: Indirizzi IP, subnet, password, tag VLAN o porte switch non presenti nel documento devono essere marcati `DA-RICHIEDERE` o `NOT_FOUND`.
* **Integrazione con itinfra-business-ops**: L'artefatto OKF v0.2 è condiviso tramite lo **Shared Customer Slug** (`<slug>`). La componente commerciale elabora prezzi e commesse nel repository business, mentre ITInfra gestisce l'architettura tecnica e l'As-Built.
