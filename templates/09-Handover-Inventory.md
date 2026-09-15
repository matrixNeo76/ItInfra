---
okf_version: "0.2"
id: "specification-<project_slug>-handover-01"
title: "Handover & Inventory — <titolo progetto, es. Infrastruttura DC Milano>"
type: "specification"
domain: "IT Infrastructure & Asset Management"
tags: ["okf-v0.2", "handover", "inventory", "assets", "fase-7", "sla"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "<PROJECT_ID>"
project_name: "<nome progetto>"
site: "<SITE_CODE>"
customer: "<cliente>"
phase: 7
author: "<nome>"
reviewer: "<nome>"
approver: "<nome>"
owner_team: "<team operations>"
status: "draft"
version: "0.1"
created_at: "<YYYY-MM-DD>"
updated_at: "<YYYY-MM-DD>"
related_docs:
  - "specification-<project_slug>-rsd-01"
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-atp-01"
  - "guide-<project_slug>-sop-runbook-01"
depends_on:
  - "architecture-<project_slug>-asbuilt-01"
  - "specification-<project_slug>-atp-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "10y"
lang: "it"

entities:
  - name: "Asset Inventory Register"
    type: "specification"
    description: "Registro inventariale completo con seriali, asset tag, MAC, IP, garanzie"
  - name: "Service Level Agreement"
    type: "specification"
    description: "SLA concordati con target, penalità, metodologia di misurazione"
  - name: "Warranty & Maintenance Contract"
    type: "specification"
    description: "Contratti di garanzia e manutenzione con vendor, date inizio/fine, copertura"
  - name: "Software License Register"
    type: "specification"
    description: "Registro licenze software con chiavi (riferimento vault), quantità, scadenze"
  - name: "Hypercare Period"
    type: "pattern"
    description: "Periodo di 30 giorni post-handover con supporto prioritario integratore"
  - name: "Vendor Support Contact"
    type: "organization"
    description: "Contatti vendor support con SLA risposta, contratto ID, portale ticket"

relations:
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'Handover eredita l'inventario dall'As-Built per la presa in carico formale"
  - targetTitle: "ATP — Acceptance Test Plan"
    targetId: "specification-<project_slug>-atp-01"
    relationType: "depends_on"
    weight: 0.95
    description: "L'handover formale è subordinato all'esito positivo dell'ATP"
  - targetTitle: "RSD/URS — Requirements Specification Document"
    targetId: "specification-<project_slug>-rsd-01"
    relationType: "references"
    weight: 0.85
    description: "Gli SLA concordati fanno riferimento ai requisiti del RSD/URS"
  - targetTitle: "SOP / Runbook"
    targetId: "guide-<project_slug>-sop-runbook-01"
    relationType: "references"
    weight: 0.95
    description: "L'handover include la consegna del SOP al team operations"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: formalizzare la presa in carico dell'infrastruttura da parte del team operations
    e fornire il registro inventariale completo degli asset.
  Input attesi: As-Built compilato (con tutti i seriali), ATP firmato, contratti di garanzia
    e licenze, elenco contatti del cliente e dei vendor.
  Regole di compilazione:
    1. L'inventario deve coincidere con quanto riportato nell'As-Built (§4) — in caso di
       discrepanza, bloccare l'handover e risolvere.
    2. Ogni asset deve avere: modello, seriale, asset tag, data installazione, garanzia fino al,
       contratto supporto, scadenza, MAC address.
    3. Le licenze software devono essere elencate con: prodotto, chiave (riferimento vault),
       quantità, scadenza, tipo (perpetua / subscription).
    4. I contatti del cliente e dei vendor devono essere verificati (data ultima verifica).
    5. Gli SLA concordati devono essere quelli del RSD/URS, confermati nel contratto.
    6. Firme del team operations e del cliente in fondo al documento.
    7. Validare la checklist in fondo prima di `status: in-review`.
-->

# Handover & Asset Inventory Report

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

**Data handover:** `<YYYY-MM-DD>`
**Luogo:** `<sala / ufficio>`

## 1. Verbale di Presa in Carico

### 1.1 Parti Contraenti

| Parte | Ruolo | Nome | Organizzazione |
|-------|-------|------|---------------|
| Committente | Sponsor | `<nome>` | `<cliente>` |
| Committente | Network Operations Lead | `<nome>` | `<cliente>` |
| Fornitore | Project Manager | `<nome>` | `<integratore>` |
| Fornitore | Technical Lead | `<nome>` | `<integratore>` |

### 1.2 Oggetto del Handover

Il presente verbale formalizza la presa in carico da parte del team operations del cliente dell'infrastruttura installata presso il sito `<site>` del progetto `<project_name>`, così come descritta nell'As-Built [[06-As-Built]] e validata dal rapporto di collaudo [[07-ATP]] in data `<data ATP>`.

### 1.3 Documentazione Consegnata

La presente presa in carico è subordinata alla consegna e alla presa visione dei seguenti documenti:

- [ ] [[01-RSD-URS]] — Requisiti e criteri di accettazione
- [ ] [[06-As-Built]] — Documentazione dell'infrastruttura installata (versione `<...>`)
- [ ] [[07-ATP]] — Rapporto di collaudo con esito `<Pass>`
- [ ] [[08-SOP-Runbook]] — Manuale operativo (versione `<...>`)
- [ ] Configurazioni degli apparati (allegato ad As-Built)
- [ ] Certifiche Fluke del cablaggio (allegato ad As-Built)
- [ ] Licenze software (allegato al presente documento §4)
- [ ] Contratti di manutenzione (allegato al presente documento §5)

### 1.4 Training del Team Operations

| Sessione | Data | Durata | Partecipanti | Argomenti | Esito |
|----------|------|--------|--------------|-----------|-------|
| TR-01 | `<data>` | 4h | `<nomi>` | Overview infrastruttura, console principali | Completato |
| TR-02 | `<data>` | 6h | `<nomi>` | Procedure SOP L1/L2 | Completato |
| TR-03 | `<data>` | 4h | `<nomi>` | Procedure DR + tabletop exercise | Completato |
| TR-04 | `<data>` | 2h | `<nomi>` | Monitoring & escalation | Completato |

**Esito training:** tutti i partecipanti hanno superato la verifica finale (quiz pratico, soglia 80%).

## 2. Asset Inventory

### 2.1 Server / Hypervisor

| Hostname | Modello | Service Tag | Asset Tag | Rack | U-pos | MAC (iLO/iDRAC) | IP Mgmt | Data install. | Garanzia fino al |
|----------|---------|------------|-----------|------|-------|------------------|---------|---------------|-------------------|
| SRV-01 | `<Dell PowerEdge R750>` | `<ABC1234>` | `<AST-001>` | R01 | U38-37 | `<AA:BB:CC:DD:EE:01>` | 10.10.50.101 | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` |
| SRV-02 | `<...>` | `<...>` | `<AST-002>` | R01 | U36-35 | `<...>` | 10.10.50.102 | `<...>` | `<...>` |
| SRV-03 | `<...>` | `<...>` | `<AST-003>` | R01 | U34-33 | `<...>` | 10.10.50.103 | `<...>` | `<...>` |

### 2.2 Switch

| Hostname | Modello | Service Tag | Asset Tag | Rack | U-pos | IP Mgmt | Data install. | Garanzia fino al | Contratto supporto |
|----------|---------|------------|-----------|------|-------|---------|---------------|-------------------|-------------------|
| sw-core-01 | `<Cisco N9K-C93180YC-FX>` | `<...>` | `<AST-010>` | R02 | U30 | 10.10.50.11 | `<...>` | `<...>` | Cisco SMARTnet 24x7x4 |
| sw-core-02 | `<...>` | `<...>` | `<AST-011>` | R02 | U29 | 10.10.50.12 | `<...>` | `<...>` | `<...>` |
| sw-tor-01 | `<...>` | `<...>` | `<AST-012>` | R01 | U41 | 10.10.50.13 | `<...>` | `<...>` | `<...>` |
| sw-tor-02 | `<...>` | `<...>` | `<AST-013>` | R01 | U40 | 10.10.50.14 | `<...>` | `<...>` | `<...>` |

### 2.3 Storage

| Hostname | Modello | Serial | Asset Tag | Rack | U-pos | IP Mgmt | Capacità raw | Capacità usable | Data install. | Garanzia fino al |
|----------|---------|--------|-----------|------|-------|---------|--------------|-----------------|---------------|-------------------|
| stor-01 | `<NetApp FAS8700>` | `<...>` | `<AST-020>` | R02 | U38-35 | 10.10.50.20 | `<142 TB>` | `<94 TB>` | `<...>` | `<...>` |
| stor-dr (sito DR) | `<...>` | `<...>` | `<AST-021>` | `<rack DR>` | `<...>` | 10.20.50.20 | `<...>` | `<...>` | `<...>` | `<...>` |

### 2.4 Firewall / Appliance Sicurezza

| Hostname | Modello | Serial | Asset Tag | Rack | IP Mgmt | Data install. | Garanzia fino al | Contratto supporto |
|----------|---------|--------|-----------|------|---------|---------------|-------------------|-------------------|
| fw-01 | `<Fortinet FG-200F>` | `<...>` | `<AST-030>` | R02 | 10.10.50.30 | `<...>` | `<...>` | FortiCare 24x7 UTM bundle 36m |
| fw-02 | `<...>` | `<...>` | `<AST-031>` | R02 | 10.10.50.31 | `<...>` | `<...>` | `<...>` |

### 2.5 Backup Appliance

| Hostname | Modello | Serial | Asset Tag | Rack | IP Mgmt | Capacità | Data install. | Garanzia fino al |
|----------|---------|--------|-----------|------|---------|----------|---------------|-------------------|
| bkp-01 | `<Veeam Hardened Appliance>` | `<...>` | `<AST-040>` | R02 | 10.10.50.40 | `<72 TB>` | `<...>` | `<...>` |

### 2.6 UPS / PDU

| Hostname | Modello | Serial | Asset Tag | Rack | Capacità | IP Mgmt | Data install. | Garanzia fino al | Batteria replace entro |
|----------|---------|--------|-----------|------|----------|---------|---------------|-------------------|-----------------------|
| ups-01 | `<APC SRT 10kVA>` | `<...>` | `<AST-050>` | R01 | 10 kVA | 10.10.50.50 | `<...>` | `<...>` | `<...>` |
| ups-02 | `<...>` | `<...>` | `<AST-051>` | R02 | 10 kVA | 10.10.50.51 | `<...>` | `<...>` | `<...>` |
| pdu-01 | `<APC AP8941>` | `<...>` | `<AST-060>` | R01 | 16A | 10.10.50.60 | `<...>` | n/a | n/a |
| pdu-02 | `<...>` | `<...>` | `<AST-061>` | R02 | 16A | 10.10.50.61 | `<...>` | n/a | n/a |
| pdu-03 | `<...>` | `<...>` | `<AST-062>` | R01 | 16A | 10.10.50.62 | `<...>` | n/a | n/a |
| pdu-04 | `<...>` | `<...>` | `<AST-063>` | R02 | 16A | 10.10.50.63 | `<...>` | n/a | n/a |

### 2.7 Riepilogo Asset Totali

| Categoria | Quantità | Valore stimato (€) | Garanzia media |
|-----------|----------|--------------------|----|
| Server / Hypervisor | `<n>` | `<€>` | `<n>` anni |
| Switch | `<n>` | `<€>` | `<n>` anni |
| Storage | `<n>` | `<€>` | `<n>` anni |
| Firewall | `<n>` | `<€>` | `<n>` anni |
| Backup appliance | `<n>` | `<€>` | `<n>` anni |
| UPS | `<n>` | `<€>` | `<n>` anni |
| PDU | `<n>` | `<€>` | n/a |
| **TOTALE** | `<n>` | `<€>` | — |

## 3. Contratti di Garanzia e Manutenzione

| Contratto | Vendor | Asset coperti | Tipo | Data inizio | Data fine | Note |
|-----------|--------|---------------|------|--------------|-----------|------|
| CTR-001 | Dell ProSupport Plus | SRV-01/02/03 | 5y NBD + 24x7 phone | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Incluso firmware update on-site |
| CTR-002 | Cisco SMARTnet | sw-core, sw-tor | 5y 24x7x4 | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Spare parts on-site 4h |
| CTR-003 | NetApp Support | stor-01, stor-dr | 5y Premium 24x7 | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Incl. software subscription |
| CTR-004 | FortiCare + UTM | fw-01, fw-02 | 3y 24x7 | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Rinnovo richiesto entro `<data>` |
| CTR-005 | Veeam Premium Care | bkp-01 | 3y | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Incl. upgrade major releases |
| CTR-006 | APC Standard | UPS-01/02 | 3y | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Battery replace coperto |

## 4. Licenze Software

### 4.1 Hypervisor / Virtualization

| Prodotto | Vendor | Chiave / Contratto | Quantità | Tipo | Data inizio | Data scadenza | Note |
|----------|--------|-------------------|----------|------|--------------|---------------|------|
| vSphere Enterprise Plus | VMware | `<riferimento vault>` | 3 CPU | subscription | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Rinnovo annuale |
| vCenter Standard | VMware | `<riferimento vault>` | 1 istanza | subscription | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | Rinnovo annuale |
| vSAN Advanced | VMware | `<riferimento vault>` | 3 CPU | subscription | `<YYYY-MM-DD>` | `<YYYY-MM-DD>` | In cluster |

### 4.2 Storage Software

| Prodotto | Vendor | Chiave | Quantità | Tipo | Scadenza |
|----------|--------|--------|----------|------|----------|
| ONTAP Standard | NetApp | `<riferimento vault>` | 1 cluster | subscription | `<YYYY-MM-DD>` |
| SnapMirror | NetApp | `<riferimento vault>` | 1 cluster | subscription | `<YYYY-MM-DD>` |

### 4.3 Sicurezza

| Prodotto | Vendor | Chiave | Quantità | Tipo | Scadenza |
|----------|--------|--------|----------|------|----------|
| FortiGate UTM bundle | Fortinet | `<riferimento vault>` | 2 appliance | subscription | `<YYYY-MM-DD>` |
| Nessus Professional | Tenable | `<riferimento vault>` | 1 console | subscription | `<YYYY-MM-DD>` |

### 4.4 Backup

| Prodotto | Vendor | Chiave | Quantità | Tipo | Scadenza |
|----------|--------|--------|----------|------|----------|
| Veeam Backup & Replication Enterprise Plus | Veeam | `<riferimento vault>` | 1 instance + 1 socket | subscription | `<YYYY-MM-DD>` |
| Veeam Cloud Connect | `<provider>` | `<account ID>` | 1 subscription | subscription | `<YYYY-MM-DD>` |

### 4.5 Sistema Operativo e Servizi

| Prodotto | Vendor | Chiave | Quantità | Tipo | Scadenza |
|----------|--------|--------|----------|------|----------|
| Windows Server 2022 STD | Microsoft | `<riferimento vault>` | `<n>` licenze | perpetua + SA | `<YYYY-MM-DD>` |
| Windows Server CAL | Microsoft | `<riferimento vault>` | `<n>` CAL | perpetua + SA | `<YYYY-MM-DD>` |
| RHEL Subscription | Red Hat | `<riferimento vault>` | `<n>` socket | subscription | `<YYYY-MM-DD>` |

### 4.6 Riepilogo Scadenze (prossimi 12 mesi)

| Data | Prodotto | Asset | Importo stimato | Azione richiesta |
|------|----------|-------|----------------|-------------------|
| `<YYYY-MM-DD>` | FortiGate UTM bundle | fw-01/02 | `<€>` | Rinnovo entro 60gg |
| `<YYYY-MM-DD>` | vSphere Enterprise Plus | SRV-01/02/03 | `<€>` | Rinnovo entro 90gg |
| `<YYYY-MM-DD>` | `<...>` | `<...>` | `<€>` | `<...>` |

## 5. SLA Concordati

| Servizio | Metrica | Target | Penalità in caso di mancato rispetto |
|----------|---------|--------|---------------------------------------|
| Disponibilità infrastruttura | Uptime mensile | ≥ 99.9% | `<%>/%` sotto target |
| Risposta NO H24 (sev-1) | Tempo risposta | ≤ 15 min | `<...>` |
| Risoluzione sev-1 | Tempo risoluzione | ≤ 4h | `<...>` |
| Backup restore | Tempo restore singolo file | ≤ 4h | `<...>` |
| DR activation | Tempo da trigger a servizi up | ≤ 4h | `<...>` |

**Metodologia di misurazione:** `<descrizione di come viene calcolato l'SLA, fonte dati (monitoring system, report automatici, ...)>`

## 6. Contatti di Riferimento

### 6.1 Cliente

| Ruolo | Nome | Cellulare | Email | Disponibilità |
|-------|------|-----------|-------|---------------|
| Sponsor | `<nome>` | `<phone>` | `<email>` | Office hours |
| Network Operations Lead | `<nome>` | `<phone>` | `<email>` | H24 (rotazione) |
| Security Officer | `<nome>` | `<phone>` | `<email>` | Office + on-call |
| System Engineer on-call | `<rotazione>` | `<phone>` | `<email>` | H24 rotazione settimanale |
| Facility Management (accesso fisico) | `<nome>` | `<phone>` | `<email>` | Office + emergenze |

### 6.2 Fornitore (integratore) — Post-Handover

| Ruolo | Nome | Cellulare | Email | Disponibilità |
|-------|------|-----------|-------|---------------|
| Account Manager | `<nome>` | `<phone>` | `<email>` | Office hours |
| Technical Lead | `<nome>` | `<phone>` | `<email>` | Office + emergenze |
| Support contrattuale (TAC) | `<vendor>` | `<phone>` | `<email>` / ticket | H24 con SLA contratto |

### 6.3 Vendor Support

| Vendor | Prodotto | Numero supporto | Portale ticket | Contratto ID | SLA risposta |
|--------|----------|-----------------|----------------|--------------|--------------|
| Dell | PowerEdge | `<phone>` | `<URL>` | `<CTR-001>` | 24x7 NBD |
| Cisco | N9K / Meraki | `<phone>` | `<URL>` | `<CTR-002>` | 24x7x4 |
| NetApp | FAS / ONTAP | `<phone>` | `<URL>` | `<CTR-003>` | 24x7 Premium |
| Fortinet | FortiGate | `<phone>` | `<URL>` | `<CTR-004>` | 24x7 |
| Veeam | VBR | `<phone>` | `<URL>` | `<CTR-005>` | 24x7 Premium |
| APC | Smart-UPS | `<phone>` | `<URL>` | `<CTR-006>` | 24x7 Standard |

## 7. Piano di Monitoraggio Post-Handover

### 7.1 Periodo di Hypercare

Le prime **30 giornate** dalla data di handover sono considerate periodo di hypercare:
- Team integratore fornisce supporto prioritario (risposta ≤ 2h per sev-2/3)
- NO cliente e Technical Lead integratore si incontrano quotidianamente (15 min stand-up)
- Report settimanale di SLA e incidenti al `<Sponsor>`

### 7.2 Maturità Operativa

| Milestone | Quando | Criterio di superamento |
|-----------|--------|-------------------------|
| M1 — Chiusura punch list | T+7gg | Tutte le azioni OA-xxx completate |
| M2 — SLA stabile | T+30gg | SLA ≥ target per 30gg consecutivi |
| M3 — DR test funzionante | T+60gg | DR test eseguito con successo dal team cliente |
| M4 — Hypercare concluso | T+30gg | Passaggio a regime operativo standard |

## 8. Stato Finanziario (Asset + Contratti)

| Voce | Importo (€) |
|------|-------------|
| Hardware (capex) | `<€>` |
| Software licenze iniziali (capex) | `<€>` |
| Servizi installazione (capex) | `<€>` |
| Contratti di manutenzione annuali (opex) | `<€>` |
| Licenze subscription annuali (opex) | `<€>` |
| **TOTALE investito (capex)** | `<€>` |
| **TOTALE ricorrente annuo (opex)** | `<€>` |

## 9. Limitazioni Note e Azioni Future

| ID | Limitazione / Azione futura | Impatto | Piano | Owner |
|----|-----------------------------|---------|-------|-------|
| LIM-001 | `<es. Sito DR non ancora dotato di storage secondario di emergenza>` | DR parzialmente coperto | Installare Q3 `<YYYY>` | `<Sponsor>` |
| LIM-002 | `<es. 2 VM legacy non ancora migrate>` | Funzionalità ridotta | Migrare entro `<data>` | `<PM>` |
| LIM-003 | `<es. Pen-test annuale non ancora schedulato>` | Compliance | Schedulare entro `<data>` | `<Sec Officer>` |

## 10. Firme e Accettazione Formale

Con la firma del presente verbale, le parti:
1. Confermano la consegna e presa in visione della documentazione elencata in §1.3
2. Attestano l'avvenuto collaudo con esito positivo (riferimento ATP [[07-ATP]])
3. Formalizzano la presa in carico dell'infrastruttura da parte del team operations del cliente
4. Si impegnano a rispettare i SLA concordati (§5) e le procedure operative (SOP [[08-SOP-Runbook]])

| Ruolo | Nome | Organizzazione | Data | Firma |
|-------|------|---------------|------|-------|
| Sponsor (cliente) | `<nome>` | `<cliente>` | `<data>` | _______________________ |
| NO Lead (cliente) | `<nome>` | `<cliente>` | `<data>` | _______________________ |
| Security Officer (cliente) | `<nome>` | `<cliente>` | `<data>` | _______________________ |
| PM (integratore) | `<nome>` | `<integratore>` | `<data>` | _______________________ |
| Technical Lead (integratore) | `<nome>` | `<integratore>` | `<data>` | _______________________ |

## 11. Riferimenti e Documenti Correlati

- Requisiti e SLA: [[01-RSD-URS]]
- As-Built: [[06-As-Built]]
- Rapporto di collaudo: [[07-ATP]]
- SOP / Runbook: [[08-SOP-Runbook]]

## Appendice A — Asset Inventory Esportabile

**File allegato:** `assets/handover-asset-inventory-v<version>.xlsx`

Contiene per ogni asset: hostname, modello, seriale, asset tag, MAC, IP, posizione rack, firmware, data installazione, garanzia fino al, contratto di supporto, valore stimato.

## Appendice B — Calendario Rinnovi (12 mesi)

**File allegato:** `assets/handover-renewals-calendar-v<version>.ics`

Calendario importabile con reminder 90gg / 60gg / 30gg prima di ogni scadenza rilevante (licenze, contratti manutenzione, garanzie).

## Appendice C — Acronimi

| Acronimo | Espansione |
|----------|------------|
| TAC | Technical Assistance Center |
| SLA | Service Level Agreement |
| NBD | Next Business Day |
| SA | Software Assurance |
| UTM | Unified Threat Management |
| CAL | Client Access License |
| HCL | Hardware Compatibility List |

---

## Checklist di Validazione

- [ ] Verbale di presa in carico completo (§1)
- [ ] Tutta la documentazione elencata in §1.3 consegnata
- [ ] Training completato e registrato
- [ ] Inventario hardware completo per ogni categoria (§2)
- [ ] Riepilogo asset totali con valore (§2.7)
- [ ] Contratti di manutenzione tutti registrati con date (§3)
- [ ] Licenze software tutte elencate con scadenza (§4)
- [ ] Riepilogo scadenze prossimi 12 mesi popolato (§4.6)
- [ ] SLA concordati con target e penalità (§5)
- [ ] Contatti cliente e vendor verificati (§6)
- [ ] Piano di hypercare definito (§7.1)
- [ ] Milestone di maturità operative (§7.2)
- [ ] Stato finanziario completo (§8)
- [ ] Limitazioni note e azioni future tracciate (§9)
- [ ] Firme di tutte le parti (§10)
- [ ] Asset inventory esportato in Excel (Appendice A)
- [ ] Calendario rinnovi generato (Appendice B)
- [ ] `depends_on` contiene As-Built e ATP
