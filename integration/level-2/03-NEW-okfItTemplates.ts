/**
 * ============================================================================
 * IT INFRASTRUCTURE BOILERPLATE TEMPLATES — OKF v0.2 nativo
 * ============================================================================
 *
 * 9 boilerplate predefiniti per l'authoring rapido di documenti del ciclo
 * lavorativo IT. Ciascun boilerplate è conforme allo standard OKF v0.2
 * e usa il tipo canonico OKF corrispondente (mappato tramite IT_DOC_TYPE_ALIASES).
 *
 * Questi boilerplate NON sostituiscono i 9 template completi in
 * /download/templates/0[1-9]-*.md — forniscono solo lo scheletro YAML
 * iniziale per chi vuole generare un documento IT programmaticamente.
 *
 * Per il template completo (con sezioni body, tabelle, checklist di validazione)
 * usare i file in /download/templates/ anziché questi boilerplate.
 *
 * ============================================================================
 */

import { ITDocType } from "../types";

/**
 * Mappatura dei 9 tipi IT ai 6 tipi canonici OKF v0.2.
 * Deve coincidere con IT_DOC_TYPE_ALIASES in okfParser.ts.
 */
export const IT_DOC_TYPES: Record<ITDocType, {
  canonical: "specification" | "architecture" | "guide";
  label: string;
  phase: 1 | 2 | 3 | 4 | 5 | 6 | 7;
  description: string;
}> = {
  rsd_urs: {
    canonical: "specification",
    label: "RSD/URS — Requirements Specification",
    phase: 1,
    description: "Catalogo dei requisiti funzionali e non funzionali, RTO/RPO, compliance",
  },
  hld: {
    canonical: "architecture",
    label: "HLD — High-Level Design",
    phase: 2,
    description: "Architettura macroscopica: topologia, componenti, ADR",
  },
  lld: {
    canonical: "architecture",
    label: "LLD — Low-Level Design",
    phase: 2,
    description: "Blueprint esecutivo: IP plan, VLAN, rack, cable matrix, ACL",
  },
  mop: {
    canonical: "guide",
    label: "MOP — Method of Procedure",
    phase: 3,
    description: "Piano operativo passo-passo con RACI, gate di verifica, finestre manutenzione",
  },
  rollback: {
    canonical: "guide",
    label: "Rollback Plan",
    phase: 3,
    description: "Procedure di ripristino con trigger, NRP, verifiche post-rollback",
  },
  as_built: {
    canonical: "architecture",
    label: "As-Built Documentation",
    phase: 7,
    description: "Fotografia dell'infrastruttura installata con deviazioni dal LLD",
  },
  atp: {
    canonical: "specification",
    label: "ATP — Acceptance Test Plan",
    phase: 6,
    description: "Verbale di collaudo con test, evidenze, firme",
  },
  sop_runbook: {
    canonical: "guide",
    label: "SOP / Runbook",
    phase: 7,
    description: "Manuale operativo per sistemisti primo/secondo livello",
  },
  handover_inventory: {
    canonical: "specification",
    label: "Handover & Asset Inventory",
    phase: 7,
    description: "Verbale formale di presa in carico + registro inventariale",
  },
};

/**
 * Boilerplate YAML+Markdown minimi per ciascuno dei 9 tipi IT.
 * Da usare per generare rapidamente un documento iniziale (es. via script).
 *
 * NOTA: per il template completo con tutte le sezioni, usare i file
 * /download/templates/0[1-9]-*.md direttamente.
 */
export const OKF_IT_TEMPLATES: Record<ITDocType, string> = {
  rsd_urs: `---
okf_version: "0.2"
id: "specification-<project_slug>-rsd-01"
title: "RSD/URS — <titolo progetto>"
type: "specification"
domain: "IT Infrastructure & Requirements Engineering"
tags: ["okf-v0.2", "rsd", "urs", "requirements", "assessment", "fase-1"]
project_id: "<PROJECT_ID>"
phase: 1
status: "draft"
version: "0.1"
related_docs:
  - "architecture-<project_slug>-hld-01"
entities:
  - name: "Stakeholder Requirements"
    type: "concept"
    description: "Requisiti funzionali e non funzionali raccolti in assessment"
  - name: "Service Level Agreement"
    type: "specification"
    description: "Contratto con target RTO/RPO e SLA"
relations:
  - targetTitle: "HLD"
    targetId: "architecture-<project_slug>-hld-01"
    relationType: "depends_on"
    weight: 1.0
---

# RSD/URS — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/01-RSD-URS.md
`,

  hld: `---
okf_version: "0.2"
id: "architecture-<project_slug>-hld-01"
title: "HLD — <titolo progetto>"
type: "architecture"
domain: "IT Infrastructure & Architectural Design"
tags: ["okf-v0.2", "hld", "design", "architettura", "fase-2"]
project_id: "<PROJECT_ID>"
phase: 2
status: "draft"
version: "0.1"
related_docs:
  - "specification-<project_slug>-rsd-01"
  - "architecture-<project_slug>-lld-01"
depends_on:
  - "specification-<project_slug>-rsd-01"
entities:
  - name: "Hypervisor Cluster"
    type: "technology"
    description: "Cluster di virtualizzazione con HA e DRS"
  - name: "Storage Array"
    type: "technology"
    description: "Array storage dual controller"
relations:
  - targetTitle: "RSD/URS"
    targetId: "specification-<project_slug>-rsd-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "LLD"
    targetId: "architecture-<project_slug>-lld-01"
    relationType: "extends"
    weight: 0.95
---

# HLD — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/02-HLD.md
`,

  lld: `---
okf_version: "0.2"
id: "architecture-<project_slug>-lld-01"
title: "LLD — <titolo progetto>"
type: "architecture"
domain: "IT Infrastructure & Detailed Engineering"
tags: ["okf-v0.2", "lld", "design", "esecutivo", "fase-2", "ip-plan", "vlan", "cable-matrix"]
project_id: "<PROJECT_ID>"
phase: 2
status: "draft"
version: "0.1"
related_docs:
  - "architecture-<project_slug>-hld-01"
  - "guide-<project_slug>-mop-01"
  - "architecture-<project_slug>-asbuilt-01"
depends_on:
  - "architecture-<project_slug>-hld-01"
entities:
  - name: "IP Subnetting Plan"
    type: "specification"
    description: "Schema subnet e VLAN per tutte le zone di rete"
  - name: "Cable Matrix"
    type: "specification"
    description: "Mappatura porte switch, patch panel, interfacce"
  - name: "Firewall ACL Matrix"
    type: "specification"
    description: "Policy east-west e north-south con sorgente, destinazione, porta, azione"
relations:
  - targetTitle: "HLD"
    targetId: "architecture-<project_slug>-hld-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "MOP"
    targetId: "guide-<project_slug>-mop-01"
    relationType: "references"
    weight: 0.9
  - targetTitle: "As-Built"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "references"
    weight: 0.95
---

# LLD — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/03-LLD.md
`,

  mop: `---
okf_version: "0.2"
id: "guide-<project_slug>-mop-01"
title: "MOP — <titolo progetto>"
type: "guide"
domain: "IT Infrastructure & Operations Management"
tags: ["okf-v0.2", "mop", "procedure", "operations", "fase-3", "deploy", "raci"]
project_id: "<PROJECT_ID>"
phase: 3
status: "draft"
version: "0.1"
related_docs:
  - "architecture-<project_slug>-lld-01"
  - "guide-<project_slug>-rollback-01"
  - "architecture-<project_slug>-asbuilt-01"
depends_on:
  - "architecture-<project_slug>-lld-01"
  - "guide-<project_slug>-rollback-01"
entities:
  - name: "Maintenance Window"
    type: "pattern"
    description: "Finestra temporale programmata con impatto utente"
  - name: "RACI Matrix"
    type: "pattern"
    description: "Responsabile/Accountable/Consultato/Informato per attività"
  - name: "Verification Gate"
    type: "concept"
    description: "Punto di verifica intermedia che blocca il prosieguo in caso di esito negativo"
relations:
  - targetTitle: "LLD"
    targetId: "architecture-<project_slug>-lld-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "Rollback Plan"
    targetId: "guide-<project_slug>-rollback-01"
    relationType: "references"
    weight: 1.0
  - targetTitle: "As-Built"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "references"
    weight: 0.9
---

# MOP — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/04-MOP.md
`,

  rollback: `---
okf_version: "0.2"
id: "guide-<project_slug>-rollback-01"
title: "Rollback Plan — <titolo progetto>"
type: "guide"
domain: "IT Infrastructure & Contingency Planning"
tags: ["okf-v0.2", "rollback", "contingency", "fallback", "fase-3", "disaster-recovery"]
project_id: "<PROJECT_ID>"
phase: 3
status: "draft"
version: "0.1"
related_docs:
  - "guide-<project_slug>-mop-01"
  - "architecture-<project_slug>-lld-01"
depends_on:
  - "guide-<project_slug>-mop-01"
entities:
  - name: "Rollback Trigger"
    type: "concept"
    description: "Condizione oggettiva e misurabile che attiva il ripristino"
  - name: "No-Return Point"
    type: "concept"
    description: "Punto oltre il quale il rollback non è più sicuro"
  - name: "Baseline Snapshot"
    type: "pattern"
    description: "Snapshot stato pre-intervento con hash SHA256"
relations:
  - targetTitle: "MOP"
    targetId: "guide-<project_slug>-mop-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "LLD"
    targetId: "architecture-<project_slug>-lld-01"
    relationType: "references"
    weight: 0.85
---

# Rollback Plan — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/05-Rollback.md
`,

  as_built: `---
okf_version: "0.2"
id: "architecture-<project_slug>-asbuilt-01"
title: "As-Built — <titolo progetto>"
type: "architecture"
domain: "IT Infrastructure & Documentation Delivery"
tags: ["okf-v0.2", "as-built", "delivery", "post-work", "fase-7", "inventory"]
project_id: "<PROJECT_ID>"
phase: 7
status: "draft"
version: "0.1"
related_docs:
  - "architecture-<project_slug>-lld-01"
  - "guide-<project_slug>-mop-01"
  - "specification-<project_slug>-atp-01"
depends_on:
  - "architecture-<project_slug>-lld-01"
  - "guide-<project_slug>-mop-01"
entities:
  - name: "Asset Inventory"
    type: "specification"
    description: "Inventario completo con seriali, MAC, firmware, IP"
  - name: "Configuration Snapshot"
    type: "pattern"
    description: "Snapshot configurazioni finali con hash SHA256"
  - name: "Deviation Record"
    type: "concept"
    description: "Deviazione dal LLD originale con motivazione"
relations:
  - targetTitle: "LLD"
    targetId: "architecture-<project_slug>-lld-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "MOP"
    targetId: "guide-<project_slug>-mop-01"
    relationType: "depends_on"
    weight: 0.95
  - targetTitle: "ATP"
    targetId: "specification-<project_slug>-atp-01"
    relationType: "references"
    weight: 0.95
---

# As-Built — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/06-As-Built.md
`,

  atp: `---
okf_version: "0.2"
id: "specification-<project_slug>-atp-01"
title: "ATP — <titolo progetto>"
type: "specification"
domain: "IT Infrastructure & Acceptance Testing"
tags: ["okf-v0.2", "atp", "testing", "collaudo", "fase-6", "acceptance"]
project_id: "<PROJECT_ID>"
phase: 6
status: "draft"
version: "0.1"
related_docs:
  - "specification-<project_slug>-rsd-01"
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-handover-01"
depends_on:
  - "architecture-<project_slug>-asbuilt-01"
entities:
  - name: "Acceptance Criterion"
    type: "specification"
    description: "Criterio di accettazione oggettivo e misurabile dal RSD/URS §9"
  - name: "Test Case"
    type: "specification"
    description: "Singolo test con ID, procedura, risultato atteso e ottenuto"
  - name: "Test Evidence"
    type: "pattern"
    description: "Evidenza allegata del test eseguito"
relations:
  - targetTitle: "As-Built"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "RSD/URS"
    targetId: "specification-<project_slug>-rsd-01"
    relationType: "references"
    weight: 0.95
  - targetTitle: "Handover"
    targetId: "specification-<project_slug>-handover-01"
    relationType: "references"
    weight: 0.95
---

# ATP — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/07-ATP.md
`,

  sop_runbook: `---
okf_version: "0.2"
id: "guide-<project_slug>-sop-runbook-01"
title: "SOP/Runbook — <titolo progetto>"
type: "guide"
domain: "IT Infrastructure & Operations Runbook"
tags: ["okf-v0.2", "sop", "runbook", "operations", "fase-7", "procedures"]
project_id: "<PROJECT_ID>"
phase: 7
status: "draft"
version: "0.1"
related_docs:
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-atp-01"
  - "specification-<project_slug>-handover-01"
depends_on:
  - "architecture-<project_slug>-asbuilt-01"
entities:
  - name: "Standard Operating Procedure"
    type: "concept"
    description: "Procedura operativa standard con ID, prereq, step, verifica, escalation"
  - name: "Disaster Recovery Runbook"
    type: "specification"
    description: "Procedura completa di attivazione DR con fasi, RTO/RPO, trigger"
  - name: "Escalation Path"
    type: "pattern"
    description: "Catena di escalation con SLA per livelli L1-L4"
relations:
  - targetTitle: "As-Built"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "ATP"
    targetId: "specification-<project_slug>-atp-01"
    relationType: "references"
    weight: 0.85
  - targetTitle: "Handover"
    targetId: "specification-<project_slug>-handover-01"
    relationType: "references"
    weight: 0.95
---

# SOP/Runbook — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/08-SOP-Runbook.md
`,

  handover_inventory: `---
okf_version: "0.2"
id: "specification-<project_slug>-handover-01"
title: "Handover & Inventory — <titolo progetto>"
type: "specification"
domain: "IT Infrastructure & Asset Management"
tags: ["okf-v0.2", "handover", "inventory", "assets", "fase-7", "sla"]
project_id: "<PROJECT_ID>"
phase: 7
status: "draft"
version: "0.1"
related_docs:
  - "specification-<project_slug>-rsd-01"
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-atp-01"
  - "guide-<project_slug>-sop-runbook-01"
depends_on:
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-atp-01"
entities:
  - name: "Asset Inventory Register"
    type: "specification"
    description: "Registro completo con seriali, asset tag, MAC, IP, garanzie"
  - name: "Service Level Agreement"
    type: "specification"
    description: "SLA concordati con target, penalità, misurazione"
  - name: "Warranty & Maintenance Contract"
    type: "specification"
    description: "Contratti di garanzia e manutenzione con vendor"
  - name: "Software License Register"
    type: "specification"
    description: "Registro licenze software con chiavi (riferimento vault)"
  - name: "Hypercare Period"
    type: "pattern"
    description: "Periodo 30 giorni post-handover con supporto prioritario"
relations:
  - targetTitle: "As-Built"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
  - targetTitle: "ATP"
    targetId: "specification-<project_slug>-atp-01"
    relationType: "depends_on"
    weight: 0.95
  - targetTitle: "SOP/Runbook"
    targetId: "guide-<project_slug>-sop-runbook-01"
    relationType: "references"
    weight: 0.95
---

# Handover & Inventory — <titolo progetto>

> Template boilerplate. Per il template completo con sezioni, tabelle e checklist, usare /download/templates/09-Handover-Inventory.md
`,
};

/**
 * Lista ordinata dei 9 tipi IT per uso in UI (dropdown, sidebar, ecc.).
 */
export const IT_DOC_TYPE_LIST: Array<{
  type: ITDocType;
  canonical: "specification" | "architecture" | "guide";
  label: string;
  phase: 1 | 2 | 3 | 4 | 5 | 6 | 7;
  description: string;
}> = Object.entries(IT_DOC_TYPES).map(([type, info]) => ({
  type: type as ITDocType,
  ...info,
}));

/**
 * Helper per ottenere il boilerplate di un tipo IT specifico.
 */
export function getITBoilerplate(docType: ITDocType): string {
  return OKF_IT_TEMPLATES[docType];
}

/**
 * Helper per ottenere le info di un tipo IT (canonical, label, phase).
 */
export function getITDocTypeInfo(docType: ITDocType) {
  return IT_DOC_TYPES[docType];
}
