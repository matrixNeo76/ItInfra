---
okf_version: "0.2"
id: "specification-demo-acme-rsd-01"
title: "RSD/URS — Modernizzazione Rete Datacenter Acme Milano"
type: "specification"
domain: "IT Infrastructure & Requirements Engineering"
tags: ["okf-v0.2", "rsd", "urs", "requirements", "assessment", "fase-1"]

# Metadati estesi IT
project_id: "demo-acme"
project_name: "Modernizzazione Rete Datacenter"
site: "DC-MIL-01"
customer: "Acme Corporation"
phase: 1
author: "Mario Rossi"
reviewer: "Team Lead Infrastructure"
approver: "CTO Acme Corporation"
owner_team: "Network & Infrastructure Engineering"
status: "in-review"
version: "1.0"
created_at: "2026-09-15"
updated_at: "2026-09-15"
related_docs:
  - "architecture-demo-acme-hld-01"
  - "guide-demo-acme-mop-01"
depends_on: []
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Requisiti Architetturali Acme"
    type: "concept"
    description: "Requisiti funzionali e di affidabilita' per il nuovo Datacenter Milano"
  - name: "Disaster Recovery SLA"
    type: "specification"
    description: "Obiettivi RTO di 15 min e RPO zero sincrono su sito secondario"
  - name: "Spine-Leaf DC Fabric"
    type: "pattern"
    description: "Topologia di rete fabric leaf-spine a 100G/25G"

relations:
  - targetTitle: "HLD — High-Level Design Datacenter Acme"
    targetId: "architecture-demo-acme-hld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'HLD traduce i requisiti del RSD/URS in architettura Spine-Leaf"
  - targetTitle: "MOP — Method of Procedure Migrazione"
    targetId: "guide-demo-acme-mop-01"
    relationType: "references"
    weight: 0.85
    description: "Il MOP coordina la migrazione dei carichi in finestra di manutenzione"
---

<!-- AI-INSTRUCTIONS:
  Documento compilato tramite procedura guidata ITInfra Assistant.
-->

# RSD/URS — Requisiti di Sistema e Utente: Acme Datacenter

## 1. Obiettivi di Business
Il progetto persegue la sostituzione dell'infrastruttura di switching e routing del Data Center primario di Milano (`DC-MIL-01`), garantendo scalabilita' a 100G, segmentazione EVPN-VXLAN e continuita' operativa con il sito di Disaster Recovery di Roma (`DC-ROM-02`).

## 2. Requisiti di Rete & Indirizzamento
- **Supernet Principale:** `10.100.0.0/16`
- **BGP Autonomous System:** ASN `65100` (interno)
- **Ridondanza Gateway:** Anycast Gateway su Leaf switches
- **Credenziali e Secret:** Gestiti centralmente via `vault://it/projects/demo-acme/dc-mil-01/admin`

## 3. Matrice SLA e Continuità
| Servizio | Tier | RTO Target | RPO Target |
|---|---|---|---|
| Core Banking & Transazioni | Tier 1 | 15 minuti | 0 minuti (Sincrono) |
| Web Portal & API Gateway | Tier 1 | 15 minuti | 5 minuti |
| Portale Interno & Analytics | Tier 2 | 4 ore | 1 ora |

## 4. Checklist di Validazione
- [x] Tutti i requisiti di business e tecnici sono stati definiti.
- [x] RTO/RPO concordati con il business owner.
- [x] Coerenza tra `related_docs` e `relations` OKF verificata.
- [x] Nessuna credenziale in chiaro presente nel documento.
- [x] Parametri allineati con `project-manifest.yaml`.
