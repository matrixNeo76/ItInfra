# Esempio prompt — ATP (Acceptance Test Plan) / Rapporto di Collaudo

Scenario: verbale di collaudo dell'infrastruttura installata, con test eseguiti, evidenze e firme.

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: As-Built
- **Obiettivo**: formalizzare l'accettazione dell'infrastruttura tramite test oggettivi

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un test engineer senior specializzato in collaudi IT enterprise.
Il tuo compito è compilare il template ATP (Acceptance Test Plan), verbale
formale di collaudo dell'infrastruttura installata.

Ogni test deve avere: ID univoco, descrizione, prerequisiti, procedura,
risultato atteso, risultato ottenuto, esito (Pass/Fail/Warning), evidenza
(file allegato), esecutore, data.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - RSD/URS: /vault/projects/acme-milano-2026/01-RSD-URS.md (criteri di accettazione §9)
   - LLD: /vault/projects/acme-milano-2026/03-LLD.md (parametri di riferimento)
   - As-Built: /vault/projects/acme-milano-2026/06-As-Built.md (configurazione testata)

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (Test Engineer Lead, Integratore)
- reviewer: Giulia Bianchi
- approver: Marco Conti (NO Acme) + Luca Verdi (Sponsor Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — ATP

### Date del collaudo
- Inizio test: 2026-03-18 14:00 (Europe/Rome)
- Fine test: 2026-03-18 23:30
- Durata totale: 9.5 ore (incluse finestre di test di rete/storage)

### Esecutori del collaudo
- Test Engineer Lead: Mario Rossi (Integratore)
- Network Operations: Marco Conti (Acme NO)
- Security Officer: Anna Neri (Acme CISO)
- Ente terzo certificatore (cablaggio): ing. Paolo Ferri (Fluke Networks partner)

### Test eseguiti (input — espandi per tutte le categorie)

#### Test funzionali (esito fornito)
- T-001: ping 10.10.10.2 da jump host → 4/4 reply, RTT 0.4ms — Pass
- T-002: ping 10.10.20.1 → 4/4 reply, 0.6ms — Pass
- T-003: ping 10.10.50.1 → 4/4 reply, 0.5ms — Pass
- T-004: routing inter-VLAN 10.10.20.x → 10.10.30.x → 4/4 reply — Pass
- T-005: DNS forward lookup dc-01.acme.local → 10.10.50.20 — Pass
- T-006: DNS reverse lookup 10.10.50.20 → dc-01.acme.local — Pass
- T-007: DHCP scope VLAN 20 → client test ottiene 10.10.20.55 — Pass
- T-008: NTP sync su fw, sw → sync OK a ntp-01 — Pass
- T-009: AD authentication con utente test → login OK — Pass
- T-010: cluster hypervisor HA status → HA enabled, 3 host OK — Pass

#### Test performance (esito fornito)
- T-011: iperf3 SRV-01 → SRV-02 → 9.4 Gbps (target ≥ 9) — Pass
- T-012: iperf3 SRV-01 (R01) → FILE-SRV-01 (R02) → 9.1 Gbps — Pass
- T-013: ping flood SRV-01 → DB-01 → RTT 0.8ms (target ≤ 2ms) — Pass
- T-014: fio sequential read LUN-001 → 720 MB/s (target ≥ 500) — Pass
- T-015: fio random read IOPS LUN-001 → 78k IOPS (target ≥ 50k) — Pass
- T-016: fio latency LUN-001 → 1.2ms (target ≤ 5ms) — Pass

#### Test failover/HA (esito fornito)
- T-017: failover fw-01 → fw-02 → 1.8s (target ≤ 2s) — Pass
- T-018: failover link sw-core-01 → sw-core-02 → 0.7s (target ≤ 1s) — Pass
- T-019: failover storage controller A→B → 22s (target ≤ 30s) — Pass
- T-020: failover hypervisor (hard-shutdown SRV-01) → 4 VM migrate in 78s (target ≤ 90s) — Pass

#### Test alimentazione/ambiente (esito fornito)
- T-021a: UPS-01 battery test → runtime 22 min (target ≥ 15) — Pass
- T-021b: UPS-02 battery test → runtime 20 min — Pass
- T-021c: failover alimentazione R01 (scollego alimentatore A) → OK via B — Pass
- T-022: temperatura rack R01 → 24°C (target ≤ 30) — Pass
- T-023: temperatura rack R02 → 25°C — Pass

#### Certificazione cablaggio Fluke (file allegati)
- 96 cavi rame Cat6A testati, 100% Pass
- 12 fibre MMF OM4 testate, 100% Pass
- Report completo: /vault/projects/acme-milano-2026/evidence/fluke/certification-report-v0.1.pdf

#### Test backup/restore (esito fornito)
- T-027: backup VM DC-01 → 14 min, 28.7 GB — Pass
- T-028: restore file-level DC-01 → 4 min — Pass
- T-029: snapshot storage Pool-Tier1 → 1s — Pass
- T-030: replica storage verso DR → RPO 12 min (target ≤ 15) — Pass

#### Test sicurezza (esito fornito)
- T-031: Nessus scan infrastruttura → 0 critiche, 2 medie (CVE-2024-1234, CVE-2024-5678 su IP MGMT) — Warning (patch in corso)
- T-032: penetration test esterno (ing. Paolo Ferri) → nessun accesso non autorizzato — Pass
- T-033: Nmap da jump host e da esterno → conforme alle policy firewall — Pass
- T-034: testssl.sh su endpoint pubblici → TLS 1.3, no cipher deboli — Pass

#### Test DR (esito fornito)
- T-035: DR test VM DC-01 → activate replica su stor-dr → RTO 38 min (target ≤ 4h), RPO 12 min (target ≤ 1h) — Pass
- T-036: DR test full infrastruttura → runbook DR completo → RTO 1h 22min, RPO 12 min — Pass

### Criteri di accettazione (richiamo da RSD/URS §9)
- CA-001: Tutti i requisiti funzionali Must implementati e verificati → Pass (RF-001..RF-007 coperti)
- CA-002: SLA disponibilità ≥ 99.9% misurato per 30 giorni → In monitoring (in corso)
- CA-003: Test di DR con RTO ≤ 4h e RPO ≤ 1h → Pass (T-035, T-036)
- CA-004: Penetration test senza vulnerabilità critiche → Pass (T-032, T-034); Warning per T-031 (patch in corso)
- CA-005: Documentazione As-Built, SOP e Handover firmata → Pass (As-Built completato, SOP e Handover in corso)
- CA-006: Training team operations → Pass (4 sessioni completate)

### Esito finale dichiarato
- PASS CON RISERVA (warning su T-031 — 2 vuln medie da patchare entro 30 giorni)

### Firme previste
- Mario Rossi (Test Engineer Lead, Integratore)
- Giulia Bianchi (Tech Lead, Integratore)
- Marco Conti (NO Acme)
- Anna Neri (Security Officer Acme)
- Luca Verdi (Sponsor Acme)

## TEMPLATE DA COMPILARE

Template path: /download/templates/07-ATP.md
Tipo documento: ATP
Fase: 6

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Ogni test ha: ID, descrizione, prereq, procedura, atteso, ottenuto, esito, evidenza, esecutore, data
  * Test FAIL: descrivere causa, azioni intraprese, riferimento Rollback se necessario
  * Test Warning: non bloccano accettazione, ma tracciati come azioni rimaste aperte
  * Firme delle parti alla fine
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-asbuilt-01]
- related_docs del nuovo ATP:
  - specification-acme-milano-rsd-01 (criteri di accettazione)
  - architecture-acme-milano-lld-01 (parametri di riferimento)
  - architecture-acme-milano-asbuilt-01
  - specification-acme-milano-handover-01 (placeholder)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft → in-review (dopo firme)
- Versione: 0.1
- ID documento: specification-acme-milano-atp-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe) incluso esito finale (PASS CON RISERVA)
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/07-ATP.md
   - ID: specification-acme-milano-atp-01

Compila il documento ora.
```

---

## Output atteso

Documento ATP completo con:

- Criteri di accettazione (richiamo RSD/URS §9) con esito complessivo per ciascuno
- 36 test eseguiti suddivisi in 8 categorie (funzionali, performance, HA, alimentazione, certifiche Fluke, backup/restore, sicurezza, DR)
- Per ogni test: ID, descrizione, prereq, procedura, atteso, ottenuto, esito, evidenza, esecutore, data
- Sintesi degli esiti per categoria con % Pass
- Azioni rimaste aperte (warning T-031) con owner e scadenza
- Mappatura test → requisiti RSD/URS
- Esito finale: PASS CON RISERVA
- Firme di 5 parti contraenti
- Appendice A: indice evidenze (file allegati in /evidence/)

---

## Tip & trucchi

### Per test con esito "Warning"
I Warning non bloccano l'accettazione ma devono essere tracciati. Verifica che per ogni Warning ci sia:
- Una descrizione del problema
- Una azione correttiva con owner e scadenza
- Una nota sul rischio residuo accettato

### Per i test di sicurezza
I test di sicurezza sono spesso il punto debole. Verifica che:
- T-031 (Nessus) sia eseguito su TUTTI gli IP (MGMT + pubblici)
- T-032 (penetration test) sia eseguito da ente terzo indipendente
- T-034 (TLS) verifichi esplicitamente TLS 1.3 e assenza di cipher deboli (RC4, 3DES, NULL)

### Per i test di DR
I test di DR sono critici per la validazione di RTO/RPO. Verifica che:
- T-035 (DR singola VM) sia eseguito in finestra dedicata (non interferire con produzione)
- T-036 (DR full) segua il runbook completo, non una scorciatoia
- RTO e RPO misurati siano documentati con margine rispetto al target

### Per le certifiche Fluke
Le certifiche Fluke devono essere allegate come PDF individuali + un report riassuntivo. Verifica che:
- Ogni cavo abbia il suo PDF (T-024.pdf, T-025.pdf, ecc.)
- Il report riassuntivo elenchi tutti i cavi con esito

### Per le firme
Le firme sono l'aspetto formale del verbale. Verifica che:
- Tutte le parti previste firmino (sponsor, NO, security, integratore)
- La data di firma sia successiva al completamento di tutti i test
- L'esito finale sia dichiarato PRIMA delle firme

### Validazione finale
Dopo la generazione, valida con:
```text
Verifica la coerenza tra ATP e RSD/URS: ogni criterio di accettazione (CA-001..CA-006)
deve avere test collegati con esito Pass o Warning (nessun Fail bloccante).
Elenca eventuali criteri di accettazione non coperti da test.
```
