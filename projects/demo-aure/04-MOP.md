---
okf_version: "0.2"
id: "guide-demo-aure-mop-01"
title: "MOP — Progetto Demo-aure"
type: "guide"
domain: "IT Infrastructure & Operations Management"
tags: ["okf-v0.2", "mop", "procedure", "operations", "fase-3", "deploy", "raci"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "demo-aure"
project_name: "Progetto Demo-aure"
site: "DC-MIL-01"
customer: "Cliente Demo-aure"
phase: 3
author: "Mario Rossi"
reviewer: "<nome>"
approver: "<nome>"
owner_team: "Network & Infrastructure Engineering"
status: "draft"
version: "0.1"
created_at: "2026-09-15"
updated_at: "2026-09-15"
related_docs:
  - "specification-demo-aure-rsd-01"
  - "architecture-demo-aure-hld-01"
  - "architecture-demo-aure-lld-01"
  - "guide-demo-aure-rollback-01"
  - "architecture-demo-aure-asbuilt-01"
depends_on:
  - "architecture-demo-aure-lld-01"
  - "guide-demo-aure-rollback-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Maintenance Window"
    type: "pattern"
    description: "Finestra temporale programmata per l'intervento con impatto utente definito"
  - name: "RACI Matrix"
    type: "pattern"
    description: "Matrice Responsabile/Accountable/Consultato/Informato per ogni attività"
  - name: "Verification Gate"
    type: "concept"
    description: "Punto di verifica intermedia che blocca il prosieguo in caso di esito negativo"
  - name: "Implementation Sequence"
    type: "specification"
    description: "Sequenza temporale degli interventi organizzati in fasi (A-I)"

relations:
  - targetTitle: "LLD — Low-Level Design"
    targetId: "architecture-demo-aure-lld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "Il MOP usa l'LLD come blueprint operativo passo-passo"
  - targetTitle: "HLD — High-Level Design"
    targetId: "architecture-demo-aure-hld-01"
    relationType: "references"
    weight: 0.85
    description: "Il MOP fa riferimento all'architettura macro definita nell'HLD"
  - targetTitle: "Rollback Plan"
    targetId: "guide-demo-aure-rollback-01"
    relationType: "references"
    weight: 1.0
    description: "Procedura di ripristino in caso di criticità bloccanti durante il deploy"
  - targetTitle: "RSD/URS — Requirements Specification Document"
    targetId: "specification-demo-aure-rsd-01"
    relationType: "references"
    weight: 0.85
    description: "I criteri di accettazione del RSD vengono verificati negli output del MOP"
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-demo-aure-asbuilt-01"
    relationType: "references"
    weight: 0.9
    description: "L'As-Built viene redatto a partire dall'esecuzione del MOP"
  - targetTitle: "ATP — Acceptance Test Plan"
    targetId: "specification-demo-aure-atp-01"
    relationType: "references"
    weight: 0.85
    description: "L'ATP verifica gli output del MOP tramite test formali"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: definire la sequenza operativa passo-passo dell'intervento di deploy.
  Input attesi: LLD approvato, calendario del cliente, elenco dei tecnici disponibili,
    eventuali runbook vendor.
  Regole di compilazione:
    1. Ogni step deve avere: ID univoco, descrizione, durata stimata, owner, prerequisiti.
    2. Indicare la finestra di manutenzione (inclusi fusi orari se multi-site).
    3. Definire i punti di verifica intermedia (gate): nessuno può procedere allo step successivo
       senza esito positivo del gate.
    4. In caso di bloccante, riferimento al [[05-Rollback]] per il ripristino.
    5. Popolare una matrice RACI per ogni fase significativa.
    6. Tutte le comunicazioni devono avere canale (email, telefono, chat) e responsabile.
    7. Specificare le modalità di accesso fisico/logico (badge, credenziali vault, jump host).
    8. In `depends_on` devono figurare sia LLD che Rollback Plan.
    9. Validare la checklist in fondo prima di `status: in-review`.
-->

# MOP — Method of Procedure

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

## 1. Obiettivo dell'Intervento

<!-- Sintesi: cosa verrà fatto, su quale infrastruttura, con quale risultato atteso. -->

<Descrizione sintetica dell'intervento: "Il presente MOP descrive la sequenza operativa per l'installazione, la configurazione e il collaudo di <componenti> presso il sito <site>, secondo l'architettura definita in [[03-LLD]]. Al termine dell'intervento l'infrastruttura sarà pronta per il cutover definitivo e il passaggio in produzione.>

**Riferimenti progettuali:**
- Requisiti: [[01-RSD-URS]]
- HLD: [[02-HLD]]
- LLD: [[03-LLD]]
- Rollback Plan: [[05-Rollback]]

## 2. Scope dell'Intervento

### 2.1 In Scope
- Installazione hardware nei rack R01 e R02 (server, switch, storage, UPS)
- Cablaggio strutturato in rame e fibra con certificazione Fluke
- Configurazione switch core/ToR, firewall perimetrale, storage array
- Setup cluster hypervisor, provisioning VM base (DC, DNS, NTP)
- Test di integrazione pre-cutover

### 2.2 Out of Scope
- Migrazione dei dati applicativi (sarà oggetto di MOP separato)
- Configurazione di reti e servizi dei siti remoti
- Formazione del team operations (oggetto di SOP [[08-SOP-Runbook]])

## 3. Prerequisiti

### 3.1 Prerequisiti Hardware
- [ ] PR-HW-001: Hardware ricevuto e verificato (vedi verbale di consegna `<ID>`)
- [ ] PR-HW-002: Staging completato: firmware aggiornato, baseline config caricata
- [ ] PR-HW-003: Etichettatura apparati conforme al LLD (hostname, asset tag)
- [ ] PR-HW-004: Soddisfatte le condizioni ambientali sala server (T 22±2°C, UR 45-55%)

### 3.2 Prerequisiti Logici
- [ ] PR-LOG-001: Credenziali admin per apparati disponibili in vault `<percorso>`
- [ ] PR-LOG-002: Licenze software caricate (vedi allegato licenze)
- [ ] PR-LOG-003: Accesso jump host / VPN abilitato per i tecnici
- [ ] PR-LOG-004: Pianificazione finestra di manutenzione approvata dal cliente

### 3.3 Prerequisiti Operativi
- [ ] PR-OP-001: Squadra tecnica assegnata e disponibilità confermata
- [ ] PR-OP-002: Contatti cliente (NO, operations) notificati 7gg prima
- [ ] PR-OP-003: Backup configurazioni pre-esistenti completato (se applicabile)
- [ ] PR-OP-004: Piani di emergenza (sala server,UPS,portieri) attivati

## 4. Finestra di Manutenzione

| Aspetto | Dettaglio |
|---------|-----------|
| Data e ora inizio | `<YYYY-MM-DD HH:MM TZ>` |
| Data e ora fine prevista | `<YYYY-MM-DD HH:MM TZ>` |
| Durata totale stimata | `<n> ore` |
| Tolleranza max (no escal.) | `<+n> ore` |
| Impatto utente | `<Nessuno / Ridotto / Completo>` — spiegare |
| Comunicazione utenti | `<Data e canale>` |
| Fuso orario | `<Europe/Rome>` (o specificare) |
| Comitato di gara | `<sì/no>` — start war room chat `<chat_id>` |

## 5. Risorse Umane e Responsabilità (RACI)

| Attività | Responsabile | Accountable | Consultato | Informato |
|----------|--------------|-------------|------------|-----------|
| Approvazione MOP | `<PM>` | `<Sponsor>` | `<Tech Lead>` | `<NO>` |
| Esecuzione installazione fisica | `<Tech R01>` | `<Team Lead>` | `<...>` | `<NO>` |
| Esecuzione configurazione | `<Net Engineer>` | `<Team Lead>` | `<...>` | `<NO>` |
| Verifiche di collaudo | `<QA>` | `<Tech Lead>` | `<...>` | `<NO>` |
| Decisione rollback | `<Tech Lead>` | `<PM>` | `<Sponsor>` | `<NO>` |
| Cutover finale | `<Net Engineer>` | `<PM>` | `<Sponsor>` | `<Utenti>` |
| Firma presa in carico | `<NO>` | `<PM>` | `<Team Lead>` | `<...>` |

## 6. Sequenza Temporale degli Interventi

### Fase A — Preparazione (T-7gg → T-1gg)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| A.01 | Verifica PR-HW e PR-LOG | 2h | `<Tech Lead>` | — | Checklist firmata |
| A.02 | Briefing squadra | 1h | `<PM>` | A.01 | Verbale briefing |
| A.03 | Backup configurazioni esistenti | 2h | `<Net Engineer>` | A.01 | Backup file in vault |
| A.04 | Notifica utenti finale | 0.5h | `<PM>` | A.02 | Email/avviso inviato |

### Fase B — Installazione Fisica (T-0, giorno 1)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| B.01 | Accesso sala server (badge) | 0.25h | `<Tech R01>` | A.04 | Ingresso consentito |
| B.02 | Mount rack R01: switch ToR, server | 2h | `<Tech R01>` | B.01 | Componenti montati |
| B.03 | Mount rack R02: storage, backup app | 2h | `<Tech R02>` | B.01 | Componenti montati |
| B.04 | Posizionamento UPS e connessione alimentazione | 1h | `<Tech R01>` | B.02, B.03 | UPS connessi |
| B.05 | **GATE-1**: verifica montaggio fisico | 0.5h | `<QA>` | B.02-04 | Verbale ispezione |

### Fase C — Cablaggio (T-0, giorno 1-2)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| C.01 | Posarame intra-rack R01 | 1.5h | `<Cabling Tech>` | B.05 | Cavi posati |
| C.02 | Posarame intra-rack R02 | 1.5h | `<Cabling Tech>` | B.05 | Cavi posati |
| C.03 | Fibra inter-rack e core | 2h | `<Cabling Tech>` | C.01, C.02 | Fibre posate |
| C.04 | Certificazione Fluke (rame + fibra) | 3h | `<Cabling Tech>` | C.01-03 | Report certifiche |
| C.05 | **GATE-2**: tutte le certifiche PASS | 0.25h | `<QA>` | C.04 | Report firmato |

### Fase D — Configurazione Rete (T-0, giorno 2)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| D.01 | Configurazione switch core sw-core-01/02 | 2h | `<Net Engineer>` | C.05 | Config caricata |
| D.02 | Configurazione switch ToR sw-tor-01/02 | 1.5h | `<Net Engineer>` | D.01 | Config caricata |
| D.03 | Configurazione firewall fw-01/02 | 2h | `<Sec Engineer>` | D.02 | Policy attive |
| D.04 | Verifica routing e reachability inter-VLAN | 1h | `<Net Engineer>` | D.03 | Test PASS |
| D.05 | **GATE-3**: rete operativa | 0.5h | `<QA>` | D.04 | Verbale |

### Fase E — Configurazione Storage (T-0, giorno 2)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| E.01 | Inizializzazione storage stor-01 | 1h | `<Storage Engineer>` | D.05 | Storage ready |
| E.02 | Creazione pool e LUN | 1h | `<Storage Engineer>` | E.01 | Pool/LUN creati |
| E.03 | Configurazione replica async verso DR | 0.5h | `<Storage Engineer>` | E.02 | Replica attiva |
| E.04 | **GATE-4**: storage operativo | 0.5h | `<QA>` | E.03 | Verbale |

### Fase F — Virtualizzazione (T-0, giorno 3)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| F.01 | Installazione hypervisor su SRV-01/02/03 | 2h | `<Hypervisor Eng>` | E.04 | Hypervisor installati |
| F.02 | Join al cluster CL-PROD-01 | 1h | `<Hypervisor Eng>` | F.01 | Cluster ready |
| F.03 | Configurazione vSwitch e port group | 1h | `<Hypervisor Eng>` | F.02 | Networking VM pronto |
| F.04 | Provisioning VM base (DC, DNS, NTP) | 2h | `<Sysadmin>` | F.03 | VM attive |
| F.05 | **GATE-5**: cluster hypervisor operativo | 0.5h | `<QA>` | F.04 | Verbale |

### Fase G — Verifiche Pre-Cutover (T-0, giorno 3)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| G.01 | Test failover storage | 1h | `<Storage Eng>` | F.05 | Test PASS |
| G.02 | Test failover firewall | 0.5h | `<Sec Eng>` | F.05 | Test PASS |
| G.03 | Test di throughput rete | 0.5h | `<Net Eng>` | F.05 | Test PASS |
| G.04 | Penetration test rapido (scan base) | 1h | `<Sec Eng>` | G.02 | Nessuna vulnerabilità critica |
| G.05 | **GATE-6**: go/no-go per cutover | 0.5h | `<Tech Lead>` | G.01-04 | Decisione formale |

### Fase H — Cutover (T-0, sera giorno 3)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| H.01 | Notifica START cutover | 0.1h | `<PM>` | G.05 | Broadcast a utenti |
| H.02 | Switch DNS pubblico → nuovo ambiente | 0.5h | `<Sysadmin>` | G.05 | DNS aggiornato |
| H.03 | Verifica servizi pubblici accessibili | 1h | `<QA>` | H.02 | Servizi UP |
| H.04 | **GATE-7**: cutover completato | 0.5h | `<PM>` | H.03 | Approvazione formale |
| H.05 | Notifica END cutover | 0.1h | `<PM>` | H.04 | Broadcast a utenti |

### Fase I — Post-Cutover (T+1 → T+7gg)
| Step ID | Attività | Durata | Owner | Prereq | Output atteso |
|---------|----------|--------|-------|--------|---------------|
| I.01 | Monitoraggio intensivo 24h | 24h | `<NOC>` | H.04 | Nessun allarme critico |
| I.02 | Verifica SLA 7 giorni | 168h | `<NOC>` | I.01 | SLA ≥ target |
| I.03 | Compilazione As-Built | 4h | `<Tech Lead>` | H.04 | [[06-As-Built]] approvato |
| I.04 | Handover formale al team ops | 2h | `<PM>` + `<NO>` | I.03 | Verbale firmato |

## 7. Punti di Verifica Intermedia (Gate)

| Gate ID | Quando | Criterio di passaggio | Decision Maker | Se FAIL |
|---------|--------|----------------------|---------------|---------|
| GATE-1 | Dopo installazione fisica | Ispezione visiva, montaggio conforme | `<QA>` | Sospendere e ri-allineare |
| GATE-2 | Dopo certifiche cavi | 100% certifiche PASS (Fluke) | `<QA>` | Ricablaggio e ri-certifica |
| GATE-3 | Dopo configurazione rete | Reachability inter-VLAN OK | `<Tech Lead>` | Rollback rete (sezione ROLL-C) |
| GATE-4 | Dopo configurazione storage | Pool/LUN/replica attivi | `<Tech Lead>` | Rollback storage |
| GATE-5 | Dopo setup hypervisor | Cluster HA attivo | `<Tech Lead>` | Rollback hypervisor |
| GATE-6 | Pre-cutover | Tutti i test PASS | `<PM>` + `<Sponsor>` | NO-GO: posticipare cutover |
| GATE-7 | Post-cutover | Servizi pubblici UP, SLA rispettato | `<PM>` | Rollback DNS + indagine |

## 8. Comunicazioni

| Quando | Canale | Mittente | Destinatari | Contenuto |
|--------|--------|----------|-------------|-----------|
| T-7gg | email | `<PM>` | Sponsor, NO, utenti impattati | Avviso manutenzione programmata |
| T-1gg | email | `<PM>` | Idem + Team Lead | Conferma finestra, contatti |
| T-0 start | chat `<chat_id>` | `<PM>` | Tutti gli stakeholder | START intervento |
| Ogni gate | chat + email | `<QA>` | PM, Sponsor | Esito gate (PASS/FAIL) |
| T+0 end | chat + email | `<PM>` | Tutti | Fine intervento + riepilogo |
| T+1gg post | email | `<NOC>` | Sponsor, NO | Report monitoraggio 24h |

## 9. Gestione degli Imprevisti

### 9.1 Criteri di Blocco Intervento
- Hardware non conforme (danneggiato, errato)
- Configurazione non applicabile per discrepanze vs LLD non risolvibili on-site
- Sicurezza: emergenza ambientale, alimentazione, incendio
- Mancanza di accesso fisico/logico oltre 2 ore dalla finestra prevista

### 9.2 Criteri di Rollback (richiamo)
- Cutover non completato entro finestra massima (T+`<n>h`)
- Servizi pubblici non raggiungibili per > 30 min
- Vulnerabilità critica emersa durante penetration test
- Per dettagli: [[05-Rollback]]

### 9.3 Escalation Path

| Livello | Trigger | Owner | Contatto | SLA risposta |
|---------|---------|-------|----------|--------------|
| L1 | Anomalia minore | `<Tech Lead>` | `<phone>` | 15 min |
| L2 | Blocco intervento | `<PM>` | `<phone>` | 30 min |
| L3 | Decidere rollback | `<Sponsor>` | `<phone>` | 60 min |
| L4 | Disastro / DR | `<Crisis Mgmt>` | `<phone>` | immediato |

## 10. Modalità di Accesso

| Tipo | Mezzo | Credenziali | Note |
|------|-------|-------------|------|
| Fisico | Badge nominale | Rilasciato da `<ente cliente>` | Restituire a fine intervento |
| Logico jump host | VPN aziendale + MFA | Vault `<path>` | Session recording attivo |
| Apparati | Account admin dedicati | Vault `<path>` | Audit log attivo |
| Storage management | Console web HTTPS | Vault `<path>` | Solo da MGMT VLAN |
| Hypervisor | vCenter/PowerShell | Vault `<path>` | Solo da jump host |

## 11. Output Attesi dell'Intervento

- [ ] OUT-001: Infrastruttura installata fisicamente e cablata (certificata)
- [ ] OUT-002: Configurazioni caricate su tutti gli apparati
- [ ] OUT-003: Cluster hypervisor operativo, VM base pronte
- [ ] OUT-004: Repliche storage verso DR attive
- [ ] OUT-005: Cutover eseguito con esito positivo
- [ ] OUT-006: Documento [[06-As-Built]] compilato e approvato
- [ ] OUT-007: Verbale di collaudo (ATP) firmato → vedi [[07-ATP]]
- [ ] OUT-008: Handover al team operations firmato → vedi [[09-Handover-Inventory]]

## 12. Riferimenti e Documenti Correlati

- Requisiti: [[01-RSD-URS]]
- HLD: [[02-HLD]]
- LLD: [[03-LLD]]
- Rollback Plan: [[05-Rollback]]
- As-Built (output): [[06-As-Built]]
- ATP (output): [[07-ATP]]

## Appendice A — Snippet Operativi per l'Esecutore

### A.1 Pre-flight checklist tecnico (1h prima dell'inizio)
```
[ ] Tutti i PR-HW-xxx completati
[ ] Tutti i PR-LOG-xxx completati (accessi, credenziali)
[ ] Backup configurazioni esistenti in vault
[ ] Comunicazione utenti inviata (T-1gg)
[ ] Sala server accessibile e condizioni ambientali OK
[ ] Tool kit: cacciaviti, fascette, etichettatrice, Fluke, laptop console
[ ] Contatti di emergenza del cliente verificati
[ ] Rollback Plan stampato/disponibile offline
```

### A.2 Logbook (template)
| Timestamp (UTC) | Operatore | Evento | Note |
|-----------------|-----------|--------|------|
| `<T0>` | `<Tech Lead>` | Inizio intervento | Tutti presenti |
| `<...>` | `<...>` | `<...>` | `<...>` |

---

## Checklist di Validazione

- [ ] Obiettivo e scope chiari
- [ ] Prerequisiti HW/LOG/OP tutti elencati
- [ ] Finestra di manutenzione completa (date, fuso, impatto)
- [ ] Matrice RACI popolata per ogni attività chiave
- [ ] Ogni step ha: ID, durata, owner, prereq, output
- [ ] Gate di verifica definiti con criteri di passaggio
- [ ] Piano comunicazioni completo
- [ ] Criteri di blocco e rollback richiamati
- [ ] Escalation path con SLA
- [ ] Modalità di accesso (fisico/logico) specificate
- [ ] Output attesi quantificati (8 elementi)
- [ ] `depends_on` contiene LLD e Rollback
