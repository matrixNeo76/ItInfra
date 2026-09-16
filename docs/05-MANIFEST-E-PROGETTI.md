---
okf_version: "0.2"
id: "specification-itinfra-manifest-projects-01"
title: "Specifica del Registro Progetti e del Manifesto Condiviso (projects/)"
type: "specification"
domain: "IT Infrastructure & Project State Management"
tags: ["okf-v0.2", "specification", "manifest", "projects", "state-management", "yaml-schema"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra State & Registry Suite"
phase: 0
author: "matrixNeo76"
reviewer: "System Architects"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture"
status: "approved"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "specification-itinfra-assistant-v02"
  - "guide-itinfra-cli-manual-01"
  - "guide-itinfra-agentic-assistant-01"
depends_on:
  - "specification-itinfra-assistant-v02"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "Project Manifest Architecture"
    type: "pattern"
    description: "Pattern per la condivisione dello stato globale dell'infrastruttura tra le 7 fasi del ciclo IT"
  - name: "Manifest Schema Definition"
    type: "specification"
    description: "Schema JSON formale per la validazione di project-manifest.yaml"
  - name: "Project Storage Structure"
    type: "framework"
    description: "Organizzazione gerarchica della cartella projects/ per progetti multi-sito e multi-cliente"

relations:
  - targetTitle: "Indice e Navigazione della Documentazione"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Indice master della documentazione tecnica"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 1.0
    description: "Specifica del componente Project Context Registry"
  - targetTitle: "Manuale Operativo CLI ITInfra"
    targetId: "guide-itinfra-cli-manual-01"
    relationType: "references"
    weight: 0.95
    description: "Comandi init e status che operano sui file di manifesto"
  - targetTitle: "Guida all'Uso dell'Assistente Agentico"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "governs"
    weight: 0.95
    description: "Regola l'ereditarietà delle variabili di contesto da parte degli agenti"
---

# Specifica del Registro Progetti e del Manifesto Condiviso (`projects/`)

<!-- AI-INSTRUCTIONS:
  Questo documento specifica la struttura della cartella projects/, i campi obbligatori
  e facoltativi del file project-manifest.yaml e il meccanismo di ereditarietà tra le 7 fasi.
-->

## 1. Obiettivo e Problema Risolto

Nel ciclo di vita di un'infrastruttura IT complessa (dalla fase 1 di Assessment alla fase 7 di Go-Live e Handover), un set consistente di informazioni rimane immutato attraverso tutti i documenti:
- CIDR della Supernet IPv4 e IPv6
- Numeri di Autonomous System (BGP ASN)
- Nomi e indirizzi dei Data Center primari e di Disaster Recovery
- Server DNS, NTP e Syslog aziendali
- SLA target, finestre di manutenzione e prefissi del password vault

Senza un archivio centrale, ogni compilazione di template richiederebbe di ridigitare (o far ricordare all'AI) tutti questi parametri. Il **Project Manifest** (`project-manifest.yaml`) funge da **Single Source of Truth** condivisa.

---

## 2. Struttura della Cartella `projects/`

```
projects/
├── _schema/
│   └── project-manifest.schema.json       ← Schema formale JSON Schema Draft-07
├── _template/
│   └── project-manifest.yaml              ← Modello base commentato copiato da `init`
└── <project-slug>/                        ← Cartella isolata per ciascun progetto
    ├── project-manifest.yaml              ← Configurazione globale del progetto
    ├── 01-RSD-URS.md                      ← Requisiti (Fase 1)
    ├── 02-HLD.md                          ← High-Level Design (Fase 2)
    ├── 03-LLD.md                          ← Low-Level Design (Fase 2)
    ├── 04-MOP.md                          ← Method of Procedure (Fase 3)
    ├── 05-Rollback.md                     ← Rollback Plan (Fase 3)
    ├── 06-As-Built.md                     ← As-Built Documentation (Fase 5)
    ├── 07-ATP.md                          ← Acceptance Test Plan (Fase 6)
    ├── 08-SOP-Runbook.md                  ← Runbook & Procedure (Fase 7)
    ├── 09-Handover-Inventory.md           ← Handover & Asset (Fase 7)
    └── exports/                           ← Esportazioni generate (CSV/JSON per NetBox)
```

---

## 3. Struttura Dettagliata di `project-manifest.yaml`

Il file YAML è composto da quattro sezioni semantiche:

### 3.1 Identificativi Generali
```yaml
project_id: "acme-milano-dc"               # Slug univoco lowercase con trattini
project_name: "Modernizzazione DC Milano" # Titolo completo descrittivo
customer: "Acme S.p.A."                   # Ragione sociale del cliente
lead_architect: "Mario Rossi"             # Nominativo dell'architetto responsabile
owner_team: "Network Engineering"          # Team proprietario post-rilascio
status: "in-planning"                     # draft | in-planning | in-execution | completed | archived
version: "0.1.0"                          # Versione semantica del progetto
```

### 3.2 Elenco Siti e Data Center (`sites`)
Definisce le location geografiche su cui insiste il perimetro dell'infrastruttura:
```yaml
sites:
  - code: "DC-MIL-01"
    name: "Primary Data Center Milano Caldera"
    role: "Primary DC"                    # Primary DC | Secondary DC | DR Site | Branch | Cloud Region
    location: "Via Caldera 21, Milano"
  - code: "DC-ROM-02"
    name: "Disaster Recovery DC Roma"
    role: "DR Site"
    location: "Via Tiburtina 1020, Roma"
```

### 3.3 Baseline di Rete Condivisa (`network_baseline`)
Variabili che vengono ereditate in `02-HLD`, `03-LLD`, `04-MOP`, `06-As-Built`:
```yaml
network_baseline:
  supernet_ipv4: "10.100.0.0/16"
  supernet_ipv6: "2001:db8:100::/48"
  bgp_asn_internal: 65100
  bgp_asn_external_primary: 65200
  dns_servers:
    - "10.100.10.11"
    - "10.100.10.12"
  ntp_servers:
    - "10.100.10.21"
    - "10.100.10.22"
  syslog_server: "10.100.20.50"
  vault_secret_prefix: "vault://it/projects/acme-milano-dc"
```

### 3.4 Baseline SLA e Operativa (`sla_baseline`)
Variabili ereditate in `01-RSD-URS`, `04-MOP`, `07-ATP`, `08-SOP-Runbook`:
```yaml
sla_baseline:
  tier1_rto: "15 minuti"
  tier1_rpo: "0 minuti (RPO zero sincrono)"
  tier2_rto: "4 ore"
  tier2_rpo: "1 ora"
  change_window: "Sabato 22:00 - Domenica 06:00 CET"
```

### 3.5 Matrice Avanzamento Documentale (`documents`)
Stato di avanzamento monitorato dal comando `python scripts/itinfra.py status <slug>`:
```yaml
documents:
  01-RSD-URS: "approved"
  02-HLD: "in-review"
  03-LLD: "draft"
  04-MOP: "missing"
  05-Rollback: "missing"
  06-As-Built: "missing"
  07-ATP: "missing"
  08-SOP-Runbook: "missing"
  09-Handover-Inventory: "missing"
```

---

## 4. Validazione con Schema JSON

Il manifest viene convalidato contro lo schema formale [`project-manifest.schema.json`](../../projects/_schema/project-manifest.schema.json).
In ambiente CI/CD o prima di avviare compilazioni avanzate, è possibile verificare la validità del manifest tramite la CLI `scripts/itinfra.py`.
