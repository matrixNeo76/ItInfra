---
okf_version: "0.2"
id: "specification-roberto-viola-rsd-01"
title: "RSD/URS — Progetto Infrastruttura Roberto-viola"
type: "specification"
domain: "IT Infrastructure & Requirements Engineering"
tags: ["okf-v0.2", "rsd", "urs", "requirements", "assessment", "fase-1"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "roberto-viola"
project_name: "Progetto Infrastruttura Roberto-viola"
site: "DC-MIL-01"
customer: "Studio Legale Avv. Roberto Viola"
phase: 1
author: "System Architect"
reviewer: "<nome revisore>"
approver: "<nome approvatore>"
owner_team: "Network & Infrastructure Engineering"
status: "draft"
version: "0.1"
created_at: "2026-09-15"
updated_at: "2026-09-15"
related_docs:
  - "architecture-roberto-viola-hld-01"
  - "guide-roberto-viola-mop-01"
depends_on: []
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Stakeholder Requirements"
    type: "concept"
    description: "Insieme dei requisiti funzionali e non funzionali raccolti in fase di assessment"
  - name: "Service Level Agreement"
    type: "specification"
    description: "Contratto di servizio con target RTO/RPO e SLA definiti"
  - name: "Compliance Framework"
    type: "framework"
    description: "Quadro normativo applicabile (GDPR, ISO 27001, PCI-DSS, ...)"
  - name: "Disaster Recovery"
    type: "pattern"
    description: "Strategia di continuità operativa con sito DR e repliche async"

relations:
  - targetTitle: "HLD — High-Level Design"
    targetId: "architecture-roberto-viola-hld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'HLD traduce i requisiti del RSD/URS in proposta architetturale macroscopica"
  - targetTitle: "MOP — Method of Procedure"
    targetId: "guide-roberto-viola-mop-01"
    relationType: "references"
    weight: 0.85
    description: "Il MOP traduce i requisiti in sequenza operativa di deploy"
  - targetTitle: "ATP — Acceptance Test Plan"
    targetId: "specification-roberto-viola-atp-01"
    relationType: "references"
    weight: 0.9
    description: "I criteri di accettazione (§9) vengono verificati nell'ATP"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: compilare questo documento a partire dai dati raccolti in fase di Assessment.
  Input attesi: verbali di kick-off, output del site survey, interviste con stakeholder,
    eventuali documenti legacy (RSD precedenti, audit di compliance).
  Regole di compilazione:
    1. NON inventare requisiti: se un dato non è fornito, scrivere "<DA-RICHIEDERE>" e segnalarlo nella sezione "Open Issues".
    2. Ogni requisito deve avere un ID univoco (RF-001, RNF-002, ...) per poter essere tracciato nei documenti successivi (HLD, LLD, ATP).
    3. I requisiti devono essere SMART (Specifici, Misurabili, Azionabili, Rilevanti, Tracciabili).
    4. Per RTO/RPO fornire sempre valori numerici con unità di misura (es. "RTO ≤ 4h", non "basso").
    5. In `depends_on` indicare eventuali documenti pre-esistenti (es. audit ISO 27001, contratti di servizio).
    6. Al termine, popolare `related_docs` con gli id dell'HLD e del MOP che verranno generati.
    7. Validare la checklist in fondo prima di passare `status: in-review`.
-->

# RSD / URS — Requirements Specification Document

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

## 1. Contesto e Obiettivi Business

<!-- Descrivere il contesto aziendale che motiva l'intervento. Spiegare "il perché" prima del "cosa". -->

<Descrivere il contesto: situazione attuale, problemi/dolori, driver di business (costi, scalabilità, conformità, end-of-life hardware, espansione sedi, M&A, ...).>

**Obiettivi di business:**
- [ ] OB-001: <es. Ridurre TCO infrastruttura del 20% in 36 mesi>
- [ ] OB-002: <es. Garantire RTO ≤ 4h per sistemi mission-critical>
- [ ] OB-003: <es. Certificare conformità GDPR e ISO 27001>

## 2. Stakeholder e Ruoli

| Ruolo | Nome | Organizzazione | Contatto | Responsabilità |
|-------|------|----------------|----------|----------------|
| Sponsor | `<...>` | `<...>` | `<email>` | Approvazione budget |
| Project Manager | `<...>` | `<...>` | `<email>` | Coordinamento |
| Technical Lead | `<...>` | `<...>` | `<email>` | Approvazione tecnica |
| Security Officer | `<...>` | `<...>` | `<email>` | Review compliance |
| Operations Lead | `<...>` | `<...>` | `<email>` | Presa in carico post-rilascio |

## 3. Requisiti Funzionali

<!-- Ogni requisito deve avere ID, descrizione, priorità (Must/Should/Could), fonte. -->

| ID | Descrizione | Priorità | Fonte | Note |
|----|-------------|----------|-------|------|
| RF-001 | <es. Il sistema deve supportare l'autenticazione integrata via Active Directory esistente> | Must | Intervista con `<stakeholder>` in data `<data>` | |
| RF-002 | <es. Il sistema deve fornire quota storage per department con limiti configurabili> | Must | `<fonte>` | |
| RF-003 | <es. Il sistema deve esporre API REST per integrazione monitoring esterno> | Should | `<fonte>` | |

## 4. Requisiti Non Funzionali

### 4.1 Performance
- Carico stimato utenti concorrenti: `<numero>` (picco: `<numero>`)
- Throughput target I/O storage: `<MB/s o IOPS>`
- Latenza massima accettabile rete LAN: `<ms>`
- Throughput minimo WAN (siti remoti): `<Mbps>`

### 4.2 Disponibilità e Affidabilità
- SLA target disponibilità: `<99.9% / 99.99% / 99.999%>`
- Componenti ridondati richiesti: `<elenco: alimentazione, storage, link rete, controller>`
- Modalità di failover preferita: `<active/active | active/passive>`

### 4.3 Scalabilità
- Crescita stimata 12 mesi (storage): `<TB>`
- Crescita stimata 12 mesi (compute): `<n. VM / n. core>`
- Margini di espansione rack: `<U liberi>`
- Estendibilità max utenti/siti: `<...>`

### 4.4 Sicurezza
- Classificazione dati trattati: `<Public / Internal / Confidential / Restricted>`
- Requisiti di cifratura: `<at-rest | in-transit | entrambi>`
- MFA obbligatoria: `<sì/no, per quali ruoli>`
- Standard di compliance: `<GDPR, ISO 27001, PCI-DSS, HIPAA, ...>`

## 5. Requisiti di Continuità Operativa (Backup & DR)

| Sistema/Categoria | RTO | RPO | Frequenza Backup | Retention | Destinazione |
|-------------------|-----|-----|------------------|-----------|--------------|
| <Server mission-critical> | `<≤ 4h>` | `<≤ 1h>` | `<orario>` | `<30 giorni>` | `<sito DR>` |
| <File server> | `<≤ 24h>` | `<≤ 12h>` | `<giornaliero>` | `<90 giorni>` | `<NAS locale + cloud>` |
| <VM di test> | `<n/a>` | `<24h>` | `<settimanale>` | `<30 giorni>` | `<NAS locale>` |

**Sito di Disaster Recovery:**
- Indirizzo: `<indirizzo sito DR>`
- Distanza dal sito primario: `<km>`
- Capacità: `<n. rack, kW, link>`
- Modalità di replica: `<sync / async / snapshot>`

## 6. Vincoli di Compliance e Normativi

<!-- Elencare tutti gli obblighi legislativi, regolatori e contrattuali. -->

- [ ] **GDPR (Regolamento UE 2016/679)** — Tutela e riservatezza dei dati personali, registro trattamenti, data breach notification
- [ ] **NIS2 (Direttiva UE 2022/2555)** — Sicurezza delle reti e sistemi informativi per soggetti essenziali/importanti:
  - Misure di gestione dei rischi di cibersicurezza (analisi rischi, sicurezza supply chain)
  - Notifica tempestiva degli incidenti significativi (early warning entro 24h, notifica entro 72h)
  - Business continuity e gestione delle crisi (backup, disaster recovery, gestione emergenze)
- [ ] **ISO/IEC 27001:2022** — Information Security Management System (ISMS):
  - Controlli organizzativi (A.5), del personale (A.6), fisici (A.7) e tecnologici (A.8)
  - Gestione delle vulnerabilità e segregazione delle reti
- [ ] **DORA (Regolamento UE 2022/2554)** — Resilienza operativa digitale (settore finanziario & fornitori terzi ICT):
  - ICT Risk Management Framework e tolleranza all'interruzione dei servizi critici
  - Test periodici di resilienza operativa digitale (TLPT - Threat-Led Penetration Testing)
  - Gestione del rischio correlato ai fornitori terzi di servizi ICT
- [ ] **ISO/IEC 20000** — IT Service Management
- [ ] **PCI-DSS v4.0** (se trattamento dati carte di pagamento)
- [ ] **HIPAA** (se dati sanitari statunitensi o internazionali)
- [ ] **Normative nazionali di settore:** `<specificare, es. ACN/CSIRT Italia, Circolari Banca d'Italia>`
- [ ] **Vincoli contrattuali con clienti/partner:** `<elencare SLA specifici, penali, data residency>`

**Note di compliance:** `<eventuali clausole specifiche da rispettare, es. "data residency IT", "no trasferimento extra-UE", "segregazione logica multi-tenant">`

## 7. Capacità Stimate

### 7.1 Storage
- Capacità iniziale richiesta: `<TB>`
- Deduplicazione attesa: `<ratio>`
- Crescita annua stimata: `<%>`
- Split per tipologia dati: `<hot/warm/cold TB>`

### 7.2 Compute
- Numero VM previste (anno 1): `<n>`
- vCPU totali: `<n>`
- RAM totale: `<GB>`
- Hypervisor preferito: `<VMware ESXi / Hyper-V / Proxmox / KVM>`

### 7.3 Rete
- Banda interna richiesta: `<Gbps>`
- Banda verso WAN: `<Mbps>`
- Siti remoti da connettere (VPN/SD-WAN): `<n>`
- VLAN previste: `<n e schema di base>`

## 8. Requisiti di Sicurezza Specifici

- Segmentazione di rete obbligatoria: `<sì, specificare zone>`
- Firewall perimetrale: `<modello/classe o requisiti minimi>`
- IDS/IPS: `<richiesto/no>`
- SIEM/Log centralizzato: `<piattaforma target>`
- Antimalware: `<prodotto / managed service>`
- Penetration test post-deploy: `<richiesto entro X settimane>`

## 9. Criteri di Accettazione

Il progetto sarà considerato completato quando TUTTI i seguenti criteri saranno soddisfatti:

- [ ] CA-001: Tutti i requisiti funzionali `Must` implementati e verificati
- [ ] CA-002: SLA di disponibilità misurato per ≥ 30 giorni consecutivi
- [ ] CA-003: Test di DR eseguito con RTO/RPO entro target
- [ ] CA-004: Penetration test passato senza vulnerabilità critiche
- [ ] CA-005: Documentazione As-Built, SOP e Handover firmata
- [ ] CA-006: Training team operations completato

## 10. Assunzioni e Dipendenze

**Assunzioni:**
- `<es. La rete WAN esistente ha banda sufficiente per la replica DR>`
- `<es. Il team operations partecipa al training entro la settimana X>`
- `<es. I permessi di accesso fisico al sito sono ottenibili con preavviso di 5 gg>`

**Dipendenze:**
- DA-001: Approvazione budget aziendale (data target: `<...>`)
- DA-002: Contratto WAN con operatore (SLA ≥ `<...>`%)
- DA-003: Licenze software disponibili entro `<data>`

## 11. Open Issues

| ID | Descrizione | Owner | Scadenza | Stato |
|----|-------------|-------|----------|-------|
| OI-001 | `<es. Confermare modello di fatturazione cloud DR>` | `<...>` | `<data>` | open |

## 12. Riferimenti

- [Riferimento normativo 1] `<link/doc>`
- [Riferimento normativo 2] `<link/doc>`
- Documento correlato: [[02-HLD]]
- Documento correlato: [[04-MOP]]

## Appendice A — Glossario

| Acronimo | Espansione |
|----------|------------|
| RTO | Recovery Time Objective |
| RPO | Recovery Point Objective |
| SLA | Service Level Agreement |
| MFA | Multi-Factor Authentication |
| DR | Disaster Recovery |

---

## Checklist di Validazione (per l'agente AI)

Prima di passare `status: in-review`, verificare:

- [ ] Tutti gli ID requisiti (RF-xxx, RNF-xxx) sono univoci
- [ ] Tutti i requisiti `Must` hanno una fonte tracciabile
- [ ] RTO/RPO specificati per ogni categoria di sistema
- [ ] Capacità stimate popolate con numeri (non "<da definire>")
- [ ] Stakeholder identificati con contatto
- [ ] Criteri di accettazione verificabili e quantificati
- [ ] Frontmatter `id` popolato con valore univoco
- [ ] Frontmatter `related_docs` contiene almeno [[02-HLD]] e [[04-MOP]]
- [ ] `updated_at` aggiornato alla data di ultima modifica
- [ ] Nessun placeholder `<...>` rimasto in sezioni critiche (3, 4, 5, 9)
