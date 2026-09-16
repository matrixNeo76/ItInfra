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
    section Fase 2: CLI, Linter & Validazione
    Sviluppo scripts/itinfra.py        :done, p2, 2026-09-16, 1d
    Test di validazione su templates/  :done, p3, 2026-09-16, 1d
    section Fase 3: Visual & Pilota
    Mermaid Diagram & IPAM Export      :done, p4, 2026-09-16, 1d
    Progetto Pilota Severino (9 docs)  :done, p5, 2026-09-16, 1d
    Export Dashboard HTML Consolidata  :done, p6, 2026-09-16, 1d
    section Fase 4: v0.4 Enterprise
    Local Encrypted Vault AES-256-GCM  :active, p7, 2026-09-16, 1d
    Multi-Agent Git Worktree Engine    :active, p8, 2026-09-16, 1d
    Anti-Hallucination Consistency Linter:active, p9, 2026-09-16, 1d
    Multi-Framework Skills (.agents/)  :active, p10, 2026-09-16, 1d
```

---

## 2. Dettaglio Deliverable per Release

### Release v0.2 / v0.3 (Completati)
- Schema JSON e template per `project-manifest.yaml`.
- CLI Python `scripts/itinfra.py` (comandi `init`, `validate`, `status`, `list-templates`, `generate-diagram`, `export-ipam`, `export-html`).
- Integrazione framework di compliance (NIS2, ISO 27001, DORA).
- Completamento al 100% di tutte le 7 fasi del progetto reale Severino Srl (9 documenti OKF v0.2 convalidati).
- Generatore di reportistica HTML offline con diagrammi vettoriali Mermaid.js.

### Release v0.4 — Security, Multi-Agent & Zero-Hallucination (In Corso)
- **Local Encrypted Vault:** modulo `scripts/itinfra_vault.py` (AES-256-GCM, PBKDF2-HMAC-SHA256, lock atomico `.vault.lock`) e comandi CLI `vault`.
- **Git Worktree Orchestration:** comando CLI `itinfra.py worktree` per orchestrare agenti paralleli su branch isolati (`feat/architecture`, `feat/security-vault`, `feat/ops-mop`, `feat/testing-atp`).
- **Motore Anti-Allucinazione:** comando CLI `itinfra.py audit-consistency` e linter con regole di Strict Grounding (fallback obbligatorio a `<DA-RICHIEDERE>`).
- **Multi-Framework Skills:** cartella standard `.agents/skills/` con `itinfra-assistant` e `itinfra-vault`, allineate a `AGENTS.md` e `CLAUDE.md`.
- **Esportazione Script Operativi:** comando `export-configs` per estrarre script RouterOS `.rsc` e PowerShell `.ps1`.

