---
okf_version: "0.2"
id: "specification-demo-aure-atp-01"
title: "ATP — Progetto Demo-aure"
type: "specification"
domain: "IT Infrastructure & Acceptance Testing"
tags: ["okf-v0.2", "atp", "testing", "collaudo", "fase-6", "acceptance"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "demo-aure"
project_name: "Progetto Demo-aure"
site: "DC-MIL-01"
customer: "Cliente Demo-aure"
phase: 6
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
  - "architecture-demo-aure-lld-01"
  - "architecture-demo-aure-asbuilt-01"
  - "specification-demo-aure-handover-01"
depends_on:
  - "architecture-demo-aure-asbuilt-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "10y"
lang: "it"

entities:
  - name: "Acceptance Criterion"
    type: "specification"
    description: "Criterio di accettazione oggettivo e misurabile derivato dal RSD/URS §9"
  - name: "Test Case"
    type: "specification"
    description: "Singolo test con ID, procedura, risultato atteso e ottenuto, esito Pass/Fail/Warning"
  - name: "Test Evidence"
    type: "pattern"
    description: "Evidenza allegata del test eseguito (log Fluke, screenshot, report iperf)"
  - name: "Failover Validation"
    type: "concept"
    description: "Verifica delle procedure di failover per componenti ridondati"
  - name: "Disaster Recovery Test"
    type: "pattern"
    description: "Test di attivazione DR con misurazione RTO/RPO"

relations:
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-demo-aure-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'ATP verifica la configurazione As-Built tramite test formali"
  - targetTitle: "RSD/URS — Requirements Specification Document"
    targetId: "specification-demo-aure-rsd-01"
    relationType: "references"
    weight: 0.95
    description: "I criteri di accettazione del RSD/URS (§9) vengono verificati nell'ATP"
  - targetTitle: "LLD — Low-Level Design"
    targetId: "architecture-demo-aure-lld-01"
    relationType: "references"
    weight: 0.85
    description: "I parametri di riferimento dei test sono definiti nell'LLD"
  - targetTitle: "Handover & Asset Inventory"
    targetId: "specification-demo-aure-handover-01"
    relationType: "references"
    weight: 0.95
    description: "L'handover formale è subordinato all'esito positivo dell'ATP"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: redigere il verbale formale di collaudo dell'infrastruttura installata.
  Input attesi: As-Built compilato, criteri di accettazione del RSD/URS (sezione §9),
    output dei test eseguiti (log Fluke, report iperf, screenshot console, etc.).
  Regole di compilazione:
    1. Ogni test deve avere: ID univoco, descrizione, prerequisiti, procedura, risultato atteso,
       risultato ottenuto, esito (Pass/Fail/Warning), evidenza (file allegato), esecutore, data.
    2. I test devono coprire TUTTI i criteri di accettazione del RSD/URS (CA-xxx).
    3. Se un test FAIL: descrivere la causa, le azioni intraprese, e se necessario richiamare il Rollback.
    4. I test "Warning" non bloccano l'accettazione ma devono essere tracciati come azioni rimaste aperte.
    5. Firme delle parti alla fine (cliente, integratore, eventuale ente terzo di certificazione).
    6. In `depends_on` deve figurare As-Built.
    7. Validare la checklist in fondo prima di `status: in-review`.
-->

# ATP — Acceptance Test Plan / Rapporto di Collaudo

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

**Date del collaudo:**
- Inizio test: `<YYYY-MM-DD HH:MM>`
- Fine test: `<YYYY-MM-DD HH:MM>`
- Durata totale: `<n>` ore

**Esecutori:**

| Ruolo | Nome | Organizzazione | Firma |
|-------|------|---------------|-------|
| Test Engineer lead | `<nome>` | `<integratore>` | `<...>` |
| Cliente — NO | `<nome>` | `Cliente Demo-aure` | `<...>` |
| Cliente — Security Officer | `<nome>` | `Cliente Demo-aure` | `<...>` |
| Ente terzo (se presente) | `<nome>` | `<ente>` | `<...>` |

## 1. Criteri di Accettazione (richiamo da RSD/URS)

Si riportano di seguito i criteri di accettazione definiti in [[01-RSD-URS]] sezione §9. Per ciascuno viene indicato l'esito complessivo in seguito ai test:

| Criterio | Descrizione | Test collegati | Esito |
|----------|-------------|-----------------|-------|
| CA-001 | Tutti i requisiti funzionali `Must` implementati e verificati | T-001...T-020 | `<Pass/Fail>` |
| CA-002 | SLA di disponibilità misurato per ≥ 30 giorni consecutivi | T-021 (in corso) | `<In monitoring>` |
| CA-003 | Test di DR eseguito con RTO/RPO entro target | T-022, T-023 | `<Pass/Fail>` |
| CA-004 | Penetration test passato senza vulnerabilità critiche | T-024 | `<Pass/Fail>` |
| CA-005 | Documentazione As-Built, SOP e Handover firmata | — | `<Pass/Fail>` |
| CA-006 | Training team operations completato | T-025 | `<Pass/Fail>` |

## 2. Lista dei Test Eseguiti

### 2.1 Test Funzionali

| ID Test | Descrizione | Prereq | Procedura | Risultato atteso | Risultato ottenuto | Esito | Evidenza | Esecutore | Data |
|---------|-------------|--------|-----------|------------------|-------------------|-------|----------|-----------|------|
| T-001 | Reachability VLAN 10 DMZ | §5 As-Built | ping da jump host a 10.10.10.2 | 4/4 reply, RTT < 1ms | 4/4 reply, RTT 0.4ms | Pass | `evidence/T-001-ping-vlan10.txt` | `<nome>` | `<data>` |
| T-002 | Reachability VLAN 20 PROD | §5 As-Built | ping a 10.10.20.1 | 4/4 reply | 4/4 reply, 0.6ms | Pass | `evidence/T-002-ping-vlan20.txt` | `<nome>` | `<data>` |
| T-003 | Reachability VLAN 50 MGMT | §5 As-Built | ping a 10.10.50.1 | 4/4 reply | 4/4 reply | Pass | `evidence/T-003.txt` | `<nome>` | `<data>` |
| T-004 | Routing inter-VLAN via core | §6 As-Built | ping 10.10.20.x → 10.10.30.x | 4/4 reply | 4/4 reply | Pass | `evidence/T-004.txt` | `<nome>` | `<data>` |
| T-005 | DNS forward lookup | §8.2 As-Built | nslookup dc-01.domain.local | 10.10.50.20 | 10.10.50.20 | Pass | `evidence/T-005.txt` | `<nome>` | `<data>` |
| T-006 | DNS reverse lookup | §8.2 As-Built | nslookup 10.10.50.20 | dc-01.domain.local | dc-01.domain.local | Pass | `evidence/T-006.txt` | `<nome>` | `<data>` |
| T-007 | DHCP scope VLAN 20 | §8.3 As-Built | Client test richiede IP | IP in range 10.10.20.50-200 | IP 10.10.20.55 | Pass | `evidence/T-007.txt` | `<nome>` | `<data>` |
| T-008 | NTP sync apparati | §8.4 As-Built | show ntp status su fw, sw | sync a ntp-01 | sync OK | Pass | `evidence/T-008.txt` | `<nome>` | `<data>` |
| T-009 | AD authentication | §8.1 As-Built | Login con utente test | Login OK | Login OK | Pass | `evidence/T-009.txt` | `<nome>` | `<data>` |
| T-010 | Cluster hypervisor HA status | §9 As-Built | check cluster health | HA enabled, 3 host OK | HA enabled, 3 host OK | Pass | `evidence/T-010.txt` | `<nome>` | `<data>` |

### 2.2 Test di Performance e Throughput

| ID Test | Descrizione | Strumento | Sorgente | Destinazione | Risultato atteso | Risultato ottenuto | Esito | Evidenza |
|---------|-------------|-----------|----------|--------------|------------------|-------------------|-------|----------|
| T-011 | Throughput intra-rack R01 | iperf3 | SRV-01 | SRV-02 | ≥ 9 Gbps | 9.4 Gbps | Pass | `evidence/T-011-iperf.txt` |
| T-012 | Throughput inter-rack | iperf3 | SRV-01 (R01) | FILE-SRV-01 (R02) | ≥ 9 Gbps | 9.1 Gbps | Pass | `evidence/T-012-iperf.txt` |
| T-013 | Latency inter-VLAN | ping flood | SRV-01 | DB-01 (VLAN 30) | RTT ≤ 2ms | 0.8ms | Pass | `evidence/T-013.txt` |
| T-014 | I/O storage - sequential read | fio | SRV-01 | LUN-001 | ≥ 500 MB/s | 720 MB/s | Pass | `evidence/T-014-fio.txt` |
| T-015 | I/O storage - random read IOPS | fio | SRV-01 | LUN-001 | ≥ 50k IOPS | 78k IOPS | Pass | `evidence/T-015-fio.txt` |
| T-016 | I/O storage - latency | fio | SRV-01 | LUN-001 | ≤ 5ms | 1.2ms | Pass | `evidence/T-016-fio.txt` |

### 2.3 Test di Failover / Ridondanza (HA)

| ID Test | Descrizione | Procedura | Risultato atteso | Risultato ottenuto | Tempo failover | Esito | Evidenza |
|---------|-------------|-----------|------------------|-------------------|----------------|-------|----------|
| T-017 | Failover firewall (active→standby) | kill fw-01 process | Traffico continua su fw-02 | OK, traffico su fw-02 | `<2s>` | Pass | `evidence/T-017-fw-failover.txt` |
| T-018 | Failover link switch core | Disconnettere link uplink primario sw-core-01 | Traffico su link secondario | OK, su link MLAG | `<1s>` | Pass | `evidence/T-018-link-failover.txt` |
| T-019 | Failover storage controller | Failover controller A→B | I/O continua, no drop | OK, I/O continuo | `<30s>` | Pass | `evidence/T-019-stor-failover.txt` |
| T-020 | Failover hypervisor host | Hard-shutdown SRV-01 | VM migrate su SRV-02/03 | OK, 4 VM migrate | `<90s>` | Pass | `evidence/T-020-vm-failover.txt` |

### 2.4 Test di Alimentazione e Ambiente

| ID Test | Descrizione | Procedura | Risultato atteso | Risultato ottenuto | Esito | Evidenza |
|---------|-------------|-----------|------------------|-------------------|-------|----------|
| T-021a | UPS-01 battery test | Comando `test battery` via management | Battery OK, runtime stimato ≥ 15 min | OK, runtime 22 min | Pass | `evidence/T-021a-ups1.txt` |
| T-021b | UPS-02 battery test | Idem | Battery OK | OK, runtime 20 min | Pass | `evidence/T-021b-ups2.txt` |
| T-021c | Failover alimentazione R01 | Scollegare alimentatore A | Alimentazione via B | OK, via B | Pass | `evidence/T-021c-pwr-failover.txt` |
| T-022 | Temperatura rack R01 | Lettura sensori PDU | ≤ 30°C | 24°C | Pass | `evidence/T-022-temp.txt` |
| T-023 | Temperatura rack R02 | Lettura sensori PDU | ≤ 30°C | 25°C | Pass | `evidence/T-023-temp.txt` |

### 2.5 Certificazione Cablaggio (Fluke)

| ID Test | Cavo | Da | A | Tipo | Lunghezza | NEXT | Return Loss | Esito | Certificato |
|---------|------|-----|---|------|-----------|------|-------------|-------|-------------|
| T-024 | PP01-01 → SRV-01 iLO | PP01 p.01 | SRV-01 iLO | Cat6A UTP | 12.4 m | 45.2 dB | 18.1 dB | Pass | `evidence/fluke/T-024.pdf` |
| T-025 | PP01-02 → SRV-01 eth0 | PP01 p.02 | SRV-01 NIC2 | Cat6A UTP | 11.8 m | 44.9 dB | 17.8 dB | Pass | `evidence/fluke/T-025.pdf` |
| T-026 | Fiber R01↔R02 | sw-core-01 Gi1/0/1 | sw-core-02 Gi1/0/1 | MMF OM4 | 35.2 m | n/a | n/a | Pass | `evidence/fluke/T-026.pdf` |

**Tabelle certifiche complete:** `evidence/fluke/certification-report-v<version>.pdf` (`<n>` cavi totali, tutti Pass).

### 2.6 Test di Backup / Restore

| ID Test | Descrizione | Procedura | Tempo | Risultato atteso | Risultato ottenuto | Esito | Evidenza |
|---------|-------------|-----------|-------|------------------|-------------------|-------|----------|
| T-027 | Backup VM DC-01 | Job-VM-PROD | 22:00→22:14 (14 min) | Backup completato, size ~30 GB | Backup OK, 28.7 GB | Pass | `evidence/T-027-backup.pdf` |
| T-028 | Restore VM DC-01 (test) | Restore file-level | 22:14→22:18 (4 min) | File restore OK | File restore OK | Pass | `evidence/T-028-restore.txt` |
| T-029 | Backup storage snapshot | Snapshot Pool-Tier1 | 22:00 (1s) | Snapshot creato | OK | Pass | `evidence/T-029-snap.txt` |
| T-030 | Replica storage verso DR | Replication async | ogni 15 min | RPO ≤ 15 min | RPO 12 min | Pass | `evidence/T-030-rep.txt` |

### 2.7 Test di Sicurezza

| ID Test | Descrizione | Strumento | Scope | Risultato atteso | Risultato ottenuto | Esito | Evidenza |
|---------|-------------|-----------|-------|------------------|-------------------|-------|----------|
| T-031 | Scan vulnerabilità infrastruttura | Nessus | IP MGMT + IP pubblici | Nessuna vulnerabilità critica | 0 critiche, 2 medie (patch in corso) | Warning | `evidence/T-031-nessus.pdf` |
| T-032 | Penetration test esterno | `<fornitore>` | IP pubblici | Nessun accesso non autorizzato | Nessun accesso | Pass | `evidence/T-032-pentest.pdf` |
| T-033 | Test policy firewall | Nmap da jump host e da esterno | Tutte le zone | Solo porte allow rispondono | Conforme | Pass | `evidence/T-033-nmap.txt` |
| T-034 | TLS cipher check | testssl.sh | Endpoint pubblici | TLS 1.3, no cipher deboli | OK, solo TLS 1.2/1.3 | Pass | `evidence/T-034-tls.txt` |

### 2.8 Test di DR (Disaster Recovery)

| ID Test | Descrizione | Procedura | RTO target | RPO target | RTO misurato | RPO misurato | Esito | Evidenza |
|---------|-------------|-----------|-----------|-----------|--------------|--------------|-------|----------|
| T-035 | DR test VM DC-01 | Activate replica su stor-dr, power on | ≤ 4h | ≤ 1h | 38 min | 12 min | Pass | `evidence/T-035-dr-test.pdf` |
| T-036 | DR test full infrastruttura | Runbook DR completo | ≤ 4h | ≤ 1h | 1h 22min | 12 min | Pass | `evidence/T-036-dr-full.pdf` |

## 3. Sintesi degli Esiti

### 3.1 Riepilogo per Categoria

| Categoria | Test eseguiti | Pass | Fail | Warning | % Pass |
|-----------|---------------|------|------|---------|--------|
| Funzionali | 10 | 10 | 0 | 0 | 100% |
| Performance | 6 | 6 | 0 | 0 | 100% |
| HA / Failover | 4 | 4 | 0 | 0 | 100% |
| Alimentazione / Ambiente | 5 | 5 | 0 | 0 | 100% |
| Certificazione cablaggio | `<n>` | `<n>` | 0 | 0 | 100% |
| Backup / Restore | 4 | 4 | 0 | 0 | 100% |
| Sicurezza | 4 | 3 | 0 | 1 | 75% |
| DR | 2 | 2 | 0 | 0 | 100% |
| **Totale** | `<n>` | `<n-1>` | 0 | 1 | `<%>` |

### 3.2 Azioni Rimaste Aperte (Warning)

| ID Test | Warning | Azione correttiva | Owner | Scadenza |
|---------|---------|-------------------|-------|----------|
| T-031 | 2 vulnerabilità medie su IP MGMT (CVE-xxxx-xxxx) | Applicare patch vendor | `<Sec Eng>` | `<data>` |

## 4. Mappatura Test → Requisiti RSD/URS

| Requisito RSD/URS | Test collegati | Esito complessivo |
|-------------------|----------------|---------------------|
| RF-001 (autenticazione AD) | T-009 | Pass |
| RF-002 (quota storage) | T-014, T-015 | Pass |
| RNF-001 (SLA 99.9%) | T-017, T-018, T-019, T-020 + monitoraggio 30gg (T-021 series) | Pass + monitoraggio in corso |
| RNF-002 (RTO ≤ 4h) | T-035, T-036 | Pass |
| CA-004 (penetration test) | T-032 | Pass |

## 5. Esito Finale del Collaudo

**Esito complessivo:** `<PASS / FAIL / PASS CON RISERVA>`

**Condizioni di accettazione:**

- [ ] Tutti i test Pass o Warning (nessun Fail bloccante)
- [ ] Tutti i requisiti `Must` del RSD/URS coperti da test Pass
- [ ] SLA monitoraggio 30 giorni attivo (anche se in corso)
- [ ] Azioni di warning tracciate con owner e scadenza

**Note finali:**

<Descrizione testuale dell'esito complessivo, eventuali raccomandazioni per il team operations, limitazioni note dell'infrastruttura installata.>

## 6. Firme e Accettazione Formale

Il presente verbale di collaudo viene accettato dalle parti sottoindicato, con effetti di presa in carico formale dell'infrastruttura da parte del cliente, fatti salvi gli eventuali punti aperti indicati in §3.2.

| Ruolo | Nome | Organizzazione | Data | Firma |
|-------|------|---------------|------|-------|
| Test Engineer Lead | `<nome>` | `<integratore>` | `<data>` | _______________________ |
| Project Manager (integratore) | `<nome>` | `<integratore>` | `<data>` | _______________________ |
| Network Operations (cliente) | `<nome>` | `Cliente Demo-aure` | `<data>` | _______________________ |
| Security Officer (cliente) | `<nome>` | `Cliente Demo-aure` | `<data>` | _______________________ |
| Sponsor / cliente finale | `<nome>` | `Cliente Demo-aure` | `<data>` | _______________________ |
| Ente terzo certificatore (se presente) | `<nome>` | `<ente>` | `<data>` | _______________________ |

## 7. Riferimenti e Documenti Correlati

- Requisiti: [[01-RSD-URS]] (criteri di accettazione §9)
- LLD: [[03-LLD]] (parametri di riferimento)
- As-Built: [[06-As-Built]] (configurazione testata)
- Handover: [[09-Handover-Inventory]] (presa in carico post-collaudo)

## Appendice A — Indice Evidenze

```
evidence/
├── T-001-ping-vlan10.txt
├── T-002-ping-vlan20.txt
├── ...
├── T-014-fio.txt
├── T-015-fio.txt
├── fluke/
│   ├── T-024.pdf
│   ├── T-025.pdf
│   ├── ...
│   └── certification-report-v<version>.pdf
├── T-027-backup.pdf
├── T-028-restore.txt
├── T-031-nessus.pdf
├── T-032-pentest.pdf
├── T-035-dr-test.pdf
└── T-036-dr-full.pdf
```

---

## Checklist di Validazione

- [ ] Tutti i criteri di accettazione del RSD/URS coperti da almeno un test
- [ ] Ogni test ha: ID, descrizione, procedura, atteso, ottenuto, esito, evidenza, esecutore, data
- [ ] Evidenze allegate in cartella `evidence/` con riferimenti nei singoli test
- [ ] Certifiche Fluke allegate per tutti i cavi (rame + fibra)
- [ ] Test di failover con tempo di failover misurato
- [ ] Test di DR con RTO/RPO misurati confrontati con target
- [ ] Penetration test eseguito e report allegato
- [ ] Sintesi degli esiti completa (§3) con % Pass
- [ ] Azioni di warning tracciate con owner e scadenza
- [ ] Esito finale dichiarato (PASS / FAIL / PASS CON RISERVA)
- [ ] Firme di tutte le parti raccoglitore
- [ ] `depends_on` contiene As-Built
