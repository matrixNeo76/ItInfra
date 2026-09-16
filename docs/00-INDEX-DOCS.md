---
okf_version: "0.2"
id: "architecture-itinfra-docs-index-01"
title: "Indice e Navigazione della Documentazione Tecnica e Operativa — ITInfra"
type: "architecture"
domain: "IT Infrastructure & Documentation Lifecycle"
tags: ["okf-v0.2", "index", "documentation", "itinfra", "manuals"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Documentation Suite"
phase: 0
author: "matrixNeo76"
reviewer: "System Architects & DevOps"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture"
status: "approved"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "specification-itinfra-assistant-v02"
  - "guide-itinfra-development-plan-v02"
  - "guide-itinfra-cli-manual-01"
  - "guide-itinfra-agentic-assistant-01"
  - "specification-itinfra-manifest-projects-01"
  - "specification-itinfra-compliance-security-01"
  - "guide-risoluzione-problematiche-ai-v02"
  - "guide-memoria-ibrida-trust-signals-v02"
  - "guide-global-enterprise-graph-v02"
  - "guide-global-memory-system-test-01"
  - "guide-itinfra-repository-roadmap-v02"
depends_on: []
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "ITInfra Documentation Hub"
    type: "framework"
    description: "Hub documentale centrale per guide operative, specifiche tecniche e manuali d'uso"
  - name: "OKF v0.2 Standard"
    type: "specification"
    description: "Standard di formattazione della documentazione compatibile con Knowledge Vault"
  - name: "ITInfra CLI Suite"
    type: "toolchain"
    description: "Strumenti di automazione e validazione per il ciclo lavorativo IT"

relations:
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "documents"
    weight: 1.0
    description: "Architettura dei componenti e specifiche tecniche di base"
  - targetTitle: "Piano di Sviluppo e Roadmap Esecutiva"
    targetId: "guide-itinfra-development-plan-v02"
    relationType: "documents"
    weight: 0.95
    description: "Pianificazione esecutiva e criteri di collaudo"
  - targetTitle: "Manuale Operativo CLI ITInfra"
    targetId: "guide-itinfra-cli-manual-01"
    relationType: "documents"
    weight: 1.0
    description: "Guida completa all'uso dei comandi della CLI scripts/itinfra.py"
  - targetTitle: "Guida all'Uso con Agenti AI e Framework Agentici"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "documents"
    weight: 1.0
    description: "Metodologia di intervista guidata a turni per Antigravity, Claude Code e Cursor"
  - targetTitle: "Specifica Registro Progetti e Manifest Condiviso"
    targetId: "specification-itinfra-manifest-projects-01"
    relationType: "documents"
    weight: 0.95
    description: "Struttura cartella projects e schema di configurazione globale"
  - targetTitle: "Framework di Compliance e Resilienza Operativa"
    targetId: "specification-itinfra-compliance-security-01"
    relationType: "documents"
    weight: 0.95
    description: "Requisiti normativi NIS2, ISO 27001:2022 e DORA"
  - targetTitle: "Guida alla Risoluzione Disservizi e Troubleshooting IT con AI"
    targetId: "guide-risoluzione-problematiche-ai-v02"
    relationType: "documents"
    weight: 0.95
    description: "Metodologia operativa per troubleshooting L1-L7 deterministico e schede post-mortem 10-RCA"
  - targetTitle: "Guida Operativa — Sistema di Memoria Locale Ibrida a 3 Livelli & Trust Signals"
    targetId: "guide-memoria-ibrida-trust-signals-v02"
    relationType: "documents"
    weight: 0.95
    description: "Architettura di staging memory anti-inquinamento Git e metadati di confidenza OKF v0.2"
  - targetTitle: "Guida al Knowledge Graph Globale Enterprise & Entity Bridges"
    targetId: "guide-global-enterprise-graph-v02"
    relationType: "documents"
    weight: 0.95
    description: "Interpolazione ontologica cross-progetto, inventario globale hardware e correlazione RCA"
  - targetTitle: "Guida alla Memoria Globale Enterprise & Verification Dashboard"
    targetId: "guide-global-memory-system-test-01"
    relationType: "documents"
    weight: 0.95
    description: "Gestione dello staging scratchpad globale, atomic locking, sanitizer multi-tenant e test suite unificata"
  - targetTitle: "Visione Strategica e Roadmap Esecutiva ITInfra"
    targetId: "guide-itinfra-repository-roadmap-v02"
    relationType: "documents"
    weight: 0.9
    description: "Allineamento strategico e cronoprogramma evolutivo del repository"
---

# Indice Generale della Documentazione ITInfra

<!-- AI-INSTRUCTIONS:
  Questo file è l'indice master di navigazione per tutti i documenti della cartella docs/.
  Tutti i file sono formattati in standard OKF v0.2.
-->

Benvenuto nell'hub di documentazione tecnica e operativa del repository **ItInfra**.

Questa directory raccoglie i manuali operativi per gli utenti e per gli agenti AI, le specifiche architetturali e i dettagli normativi necessari per governare l'intero ciclo documentale di infrastrutture IT complesse.

---

## 🗺️ Mappa della Documentazione

```mermaid
graph TD
    DOCS[docs/00-INDEX-DOCS.md] --> SPEC[01-SPEC-ITINFRA-ASSISTANT.md<br/>Specifica Tecnica Architettura]
    DOCS --> ROAD[02-ROADMAP-PIANO-SVILUPPO.md<br/>Piano di Sviluppo Esecutivo]
    DOCS --> CLI[03-GUIDA-CLI-ITINFRA.md<br/>Manuale Operativo CLI itinfra.py]
    DOCS --> AGENT[04-GUIDA-ASSISTENTE-AGENTICO.md<br/>Guida Agenti AI & Antigravity]
    DOCS --> MANIF[05-MANIFEST-E-PROGETTI.md<br/>Registro Progetti & Manifest]
    DOCS --> COMPL[06-COMPLIANCE-E-SICUREZZA.md<br/>NIS2, ISO 27001, DORA]
    DOCS --> TROUBLE[07-GUIDA-RISOLUZIONE-PROBLEMATICHE-AI.md<br/>Troubleshooting & RCA]
    DOCS --> MEM[08-GUIDA-MEMORIA-IBRIDA-TRUST-SIGNALS.md<br/>Memoria Locale Ibrida & Trust]
    DOCS --> GLOBAL[09-GUIDA-GLOBAL-ENTERPRISE-GRAPH.md<br/>Global Enterprise Graph & Inventory]
    DOCS --> TEST[10-GUIDA-GLOBAL-MEMORY-SYSTEM-TEST.md<br/>Global Memory & Test Suite]
    
    CLI -.-> CLI_PY[scripts/itinfra.py]
    GLOBAL -.-> INV_CLI[scripts/itinfra_inventory.py]
    TEST -.-> TEST_PY[scripts/itinfra_test_suite.py]
    TROUBLE -.-> SKILL_TB[.agents/skills/itinfra-troubleshooter/]
    AGENT -.-> SKILL[.agents/skills/itinfra-assistant/]
    MANIF -.-> PROJ_DIR[projects/<slug>/]
    COMPL -.-> TPL_DIR[templates/]
```

---

## 📚 Elenco dei Documenti

| Documento | Tipo OKF | Scopo e Contenuto |
|-----------|----------|-------------------|
| [`01-SPEC-ITINFRA-ASSISTANT.md`](./01-SPEC-ITINFRA-ASSISTANT.md) | `specification` | Architettura dei componenti della suite: Project Registry, Linter CLI, Wizard a turni e Skill. |
| [`02-ROADMAP-PIANO-SVILUPPO.md`](./02-ROADMAP-PIANO-SVILUPPO.md) | `guide` | Tabella di marcia esecutiva a 5 fasi, criteri di accettazione e tracciabilità. |
| [`03-GUIDA-CLI-ITINFRA.md`](./03-GUIDA-CLI-ITINFRA.md) | `guide` | Guida passo-passo a tutti i comandi di `scripts/itinfra.py` (`init`, `status`, `validate`, `inventory`, `test-suite`). |
| [`04-GUIDA-ASSISTENTE-AGENTICO.md`](./04-GUIDA-ASSISTENTE-AGENTICO.md) | `guide` | Come utilizzare Google Antigravity, Claude Code e Cursor per condurre l'intervista guidata per blocchi. |
| [`05-MANIFEST-E-PROGETTI.md`](./05-MANIFEST-E-PROGETTI.md) | `specification` | Gestione della cartella `projects/`, ereditarietà parametri di rete e schema `project-manifest.yaml`. |
| [`06-COMPLIANCE-E-SICUREZZA.md`](./06-COMPLIANCE-E-SICUREZZA.md) | `specification` | Approfondimento normativo: integrazione e checklist per NIS2, ISO/IEC 27001:2022 e regolamento DORA. |
| [`07-GUIDA-RISOLUZIONE-PROBLEMATICHE-AI.md`](./07-GUIDA-RISOLUZIONE-PROBLEMATICHE-AI.md) | `guide` | Metodologia operativa per richiedere a Antigravity, Claude Code o Cursor la risoluzione di disservizi IT (OSI L1-L7, 5 Perché, CAPA e template 10-RCA). |
| [`08-GUIDA-MEMORIA-IBRIDA-TRUST-SIGNALS.md`](./08-GUIDA-MEMORIA-IBRIDA-TRUST-SIGNALS.md) | `guide` | Architettura di memoria locale a 3 livelli (Short, Staging Scratchpad, Truth OKF v0.2), anti-inquinamento Git e Trust Signals di confidenza. |
| [`09-GUIDA-GLOBAL-ENTERPRISE-GRAPH.md`](./09-GUIDA-GLOBAL-ENTERPRISE-GRAPH.md) | `guide` | Knowledge Graph globale enterprise con nodi ponte (Shared Entity Bridges), inventario cross-progetto e incident intelligence. |
| [`10-GUIDA-GLOBAL-MEMORY-SYSTEM-TEST.md`](./10-GUIDA-GLOBAL-MEMORY-SYSTEM-TEST.md) | `guide` | Staging scratchpad globale (`_global_scratchpad.md`), AtomicFileLock, sanitizer multi-tenant e test suite unificata. |

---

## 🔗 Collegamenti Rapidi Esterni

- **Visione Strategica:** [`ROADMAP.md`](../ROADMAP.md)
- **Regole per Agenti AI:** [`AGENTS.md`](../AGENTS.md)
- **Istruzioni per Claude Code:** [`CLAUDE.md`](../CLAUDE.md)
- **Catalogo dei 10 Template:** [`templates/00-INDEX.md`](../templates/00-INDEX.md)
- **Integrazione con Knowledge Vault:** [`INTEGRAZIONE-REPO.md`](../INTEGRAZIONE-REPO.md)
