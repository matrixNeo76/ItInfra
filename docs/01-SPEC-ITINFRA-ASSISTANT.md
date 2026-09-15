---
okf_version: "0.2"
id: "specification-itinfra-assistant-v02"
title: "Specifica Tecnica — Assistente Agentico Interattivo ITInfra & Framework di Compilazione"
type: "specification"
domain: "IT Infrastructure & Agentic Workflow Engineering"
tags: ["okf-v0.2", "specification", "agentic-framework", "itinfra", "antigravity", "python-cli", "guided-wizard"]

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
  - "guide-itinfra-development-plan-v02"
  - "guide-repo-integration-complete"
  - "index-ciclo-lavorativo-it"
depends_on:
  - "index-ciclo-lavorativo-it"
classification: "internal"
retention: "5-years"
lang: "it"

entities:
  - name: "ITInfra Assistant"
    type: "framework"
    description: "Suite agentica per la compilazione guidata passo-passo della documentazione di infrastruttura IT su standard OKF v0.2"
  - name: "Antigravity Skill Engine"
    type: "toolchain"
    description: "Modulo di skill specializzate e intervista interattiva a turni per Google Antigravity"
  - name: "ITInfra Python CLI & Linter"
    type: "toolchain"
    description: "Tool da riga di comando per inizializzazione progetti, validazione OKF v0.2 e monitoraggio avanzamento"
  - name: "Project Context Registry"
    type: "pattern"
    description: "Architettura per la memorizzazione centralizzata delle variabili d'infrastruttura condivise tra le 7 fasi"

relations:
  - targetTitle: "Piano di Sviluppo e Roadmap ITInfra Assistant"
    targetId: "guide-itinfra-development-plan-v02"
    relationType: "implements"
    weight: 1.0
    description: "Specifica tecnica di riferimento attuata dal piano di sviluppo"
  - targetTitle: "Guida Integrazione Repo — Knowledge Vault"
    targetId: "guide-repo-integration-complete"
    relationType: "references"
    weight: 0.85
    description: "Riferimento per la compatibilità con il Knowledge Vault"
  - targetTitle: "Indice Navigazionale — Template Ciclo Lavorativo IT"
    targetId: "index-ciclo-lavorativo-it"
    relationType: "depends_on"
    weight: 1.0
    description: "Mappatura delle 7 fasi e dei 9 template documentali gestiti dal sistema"
---

# Specifica Tecnica: ITInfra Agentic Assistant & Python CLI Suite

## 1. Obiettivo e Visione

Il progetto **ITInfra Assistant** estende il set di template statici OKF v0.2 per trasformare il repository in un **sistema agentico attivo e interattivo**, focalizzato sull'integrazione nativa con **Google Antigravity**, **Claude Code**, **Cursor** e altri ambienti agentici dotati di shell terminale.

L'approccio sostituisce la generazione statica monolitica ("one-shot") con un **workflow guidato a intervista modulare**, supportato da:
1. Una **CLI Python** snella, senza dipendenze esterne pesanti, per inizializzare progetti, validare la conformità OKF v0.2 e verificare lo stato dei documenti.
2. Una **Skill Antigravity** strutturata per orchestrare l'intervista per blocchi tematici (Requisiti, Rete, Compute, Storage, Security, Collaudo).
3. Un **Registro di Progetto** (`project-manifest.yaml`) che eredita automaticamente i parametri comuni a tutte le 7 fasi.

*(Nota architetturale: l'implementazione di un server demone FastMCP è posposta a favore di questa architettura diretta basata su CLI e Skill native, eliminando l'overhead di background daemon).*

---

## 2. Architettura dei Componenti

```mermaid
graph TD
    User[Operatore / System Engineer] -->|Intervista Guidata| Agent[Agente AI: Antigravity / Cursor / Claude Code]
    
    subgraph "Agentic Layer"
        Agent --> Skill[Antigravity Skill: itinfra-assistant]
        Agent --> Rules[Istruzioni AGENTS.md / CLAUDE.md]
    end
    
    subgraph "CLI & Automation Layer"
        Agent -->|Esegue comandi CLI| CLI[scripts/itinfra.py]
        CLI --> CmdInit[cmd: init]
        CLI --> CmdValidate[cmd: validate]
        CLI --> CmdStatus[cmd: status]
        CLI --> CmdList[cmd: list-templates]
    end
    
    subgraph "Data & Document Layer"
        CmdInit --> ProjManifest[(projects/<slug>/project-manifest.yaml)]
        CmdValidate --> ValidRules[(OKF v0.2 Rules)]
        CmdStatus --> DocVault[(projects/<slug>/*.md)]
        Agent --> Templates[(templates/ 00..09)]
    end
```

### 2.1 Project Context Registry & Manifest (`projects/`)
Evita la duplicazione di informazioni tra le fasi:
- Posizione: `projects/<project-slug>/project-manifest.yaml`
- Parametri condivisi:
  - `project_id`, `client_name`, `site_list`, `lead_architect`
  - Parametri di rete (CIDR Supernet, ASN BGP, pool VLAN, server DNS, NTP)
  - Parametri di business (SLA, RTO, RPO, Change Windows)
  - Stato di avanzamento (matrice dei 9 documenti con stato `draft`, `in-review`, `approved`)

### 2.2 ITInfra CLI & Linter (`scripts/itinfra.py`)
Script Python standalone che fornisce:
- `python scripts/itinfra.py init <slug> [--client <name>]`: inizializza la directory del progetto con il manifesto precompilato.
- `python scripts/itinfra.py validate <file_o_dir>`: analizza i documenti Markdown:
  - Convalida del frontmatter YAML conforme a OKF v0.2.
  - Verifica della coerenza biunivoca tra `related_docs` e `relations` (`targetId`).
  - Rilevamento di segreti in chiaro (esige `vault://`).
  - Conteggio e segnalazione di placeholder orfani (`<DA-RICHIEDERE>`, `<...>`).
- `python scripts/itinfra.py status <slug>`: visualizza la matrice di avanzamento del ciclo a 7 fasi.
- `python scripts/itinfra.py list-templates`: catalogo dei template con fasi e dipendenze.

### 2.3 Antigravity Native Skill (`skills/itinfra-assistant/SKILL.md`)
Istruisce Antigravity a:
- Condurre interviste a blocchi prima di compilare un template.
- Estrarre e inserire automaticamente le variabili dal `project-manifest.yaml`.
- Eseguire il linter `itinfra.py validate` prima di restituire il documento all'utente.
