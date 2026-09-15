---
okf_version: "0.2"
id: "guide-itinfra-development-plan-v02"
title: "Piano di Sviluppo e Roadmap — Suite ITInfra Assistant (Skill & Python CLI)"
type: "guide"
domain: "IT Infrastructure & Software Development Lifecycle"
tags: ["okf-v0.2", "guide", "roadmap", "development-plan", "itinfra", "phases"]

# Metadati estesi IT
project_id: "itinfra-assistant-core"
project_name: "ITInfra Agentic Assistant & Python CLI Suite"
phase: 2
author: "AI Solutions Architect"
reviewer: "Tech Lead"
approver: "Project Sponsor"
owner_team: "DevOps & Infrastructure Architecture"
status: "approved"
version: "1.1.0"
created_at: "2026-09-15"
updated_at: "2026-09-15"
related_docs:
  - "specification-itinfra-assistant-v02"
  - "index-ciclo-lavorativo-it"
  - "guide-repo-integration-complete"
depends_on:
  - "specification-itinfra-assistant-v02"
classification: "internal"
retention: "5-years"
lang: "it"

entities:
  - name: "Piano di Sviluppo ITInfra"
    type: "pattern"
    description: "Roadmap focalizzata su Python CLI, gestione progetti e Skill Antigravity per la compilazione guidata"
  - name: "ITInfra CLI & Linter"
    type: "toolchain"
    description: "Script Python per automazione, validazione OKF v0.2 e monitoraggio avanzamento"
  - name: "Antigravity Custom Skill"
    type: "framework"
    description: "Skill per intervista interattiva a turni e generazione guidata"

relations:
  - targetTitle: "Specifica Tecnica — Assistente Agentico Interattivo ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 1.0
    description: "Attua i requisiti e l'architettura definiti nella specifica tecnica v1.1.0"
  - targetTitle: "Indice Navigazionale — Template Ciclo Lavorativo IT"
    targetId: "index-ciclo-lavorativo-it"
    relationType: "references"
    weight: 0.9
    description: "Usa la mappatura delle 7 fasi e dei 9 template come catalogo operativo"
  - targetTitle: "Guida Integrazione Repo — Knowledge Vault"
    targetId: "guide-repo-integration-complete"
    relationType: "relates_to"
    weight: 0.8
    description: "Allinea i deliverable con le specifiche del Knowledge Vault"
---

# Piano di Sviluppo e Roadmap: Suite ITInfra Assistant

## 1. Fasi di Sviluppo

```mermaid
gantt
    title Roadmap Sviluppo ITInfra Assistant (Snella)
    dateFormat  YYYY-MM-DD
    section Fase 1: Project Registry
    Schema & Template Manifest         :done, p1, 2026-09-16, 1d
    section Fase 2: CLI & Linter
    Sviluppo scripts/itinfra.py        :active, p2, 2026-09-16, 1d
    Test di validazione su templates/  :p3, 2026-09-16, 1d
    section Fase 3: Antigravity Skill
    Creazione Skill e Schede Wizard    :p4, 2026-09-17, 1d
    Aggiornamento AGENTS.md & CLAUDE.md:p5, 2026-09-17, 1d
    section Fase 4: Collaudo E2E
    Test Progetto Demo Acme            :p6, 2026-09-17, 1d
```

---

## 2. Dettaglio Deliverable

### Step 1: Base Progetti & Manifest (`projects/`)
- `projects/_schema/project-manifest.schema.json`
- `projects/_template/project-manifest.yaml`
- `.gitignore` aggiornato

### Step 2: CLI Python & Validatore OKF v0.2 (`scripts/itinfra.py`)
- Sviluppo della CLI Python standalone (senza dipendenze pesanti obbligatorie)
- Comandi: `init`, `validate`, `status`, `list-templates`
- Verifica su tutti i file in `templates/`

### Step 3: Antigravity Skill & Istruzioni Agenti
- `skills/itinfra-assistant/SKILL.md` (e registrazione in `.gemini/antigravity/skills/itinfra-assistant/SKILL.md`)
- Schede guida per intervista a blocchi logici (Networking, Compute, Storage, Security, ATP, Runbook)
- Aggiornamento di `AGENTS.md` e `CLAUDE.md` con riferimenti alla CLI `scripts/itinfra.py`

### Step 4: Collaudo E2E
- Creazione progetto di test demo tramite CLI
- Compilazione assistita e validazione automatica
- Verifica di conformità e assenza errori
