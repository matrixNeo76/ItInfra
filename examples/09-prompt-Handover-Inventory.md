# Esempio prompt — Handover & Asset Inventory Report

Scenario: verbale formale di presa in carico dell'infrastruttura da parte del team operations.

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: As-Built, ATP, SOP/Runbook
- **Obiettivo**: formalizzare l'handover e fornire il registro inventariale completo

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un project manager + asset manager specializzato in handover di infrastrutture IT.
Il tuo compito è compilare il template Handover & Asset Inventory Report, che
formalizza la presa in carico dell'infrastruttura da parte del team operations del
cliente e fornisce il registro inventariale completo degli asset.

L'inventario deve coincidere con quanto riportato nell'As-Built (§4) — in caso di
discrepanza, bloccare l'handover e risolvere.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - RSD/URS: /vault/projects/acme-milano-2026/01-RSD-URS.md (SLA)
   - As-Built: /vault/projects/acme-milano-2026/06-As-Built.md (inventario hardware)
   - ATP: /vault/projects/acme-milano-2026/07-ATP.md (verbale di collaudo)
   - SOP: /vault/projects/acme-milano-2026/08-SOP-Runbook.md (team operations)

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (PM + Tech Lead, Integratore)
- reviewer: Giulia Bianchi
- approver: Luca Verdi (Sponsor Acme) + Marco Conti (NO Acme)
- owner_team: Acme Operations
- Data handover: 2026-03-25
- Luogo: Sala riunioni Acme Milano, via Verdi 10, piano 1

## DATI SPECIFICI — Handover & Inventory

### Parti contraenti
- Sponsor (cliente): Luca Verdi (CFO Acme)
- NO Lead (cliente): Marco Conti
- Security Officer (cliente): Anna Neri
- PM (integratore): Mario Rossi
- Technical Lead (integratore): Giulia Bianchi

### Documentazione consegnata
- [x] RSD/URS (id: specification-acme-milano-rsd-01, version 1.0 approved)
- [x] As-Built (id: architecture-acme-milano-asbuilt-01, version 1.0 approved)
- [x] ATP (id: specification-acme-milano-atp-01, version 1.0 approved — esito PASS CON RISERVA)
- [x] SOP/Runbook (id: guide-acme-milano-sop-runbook-01, version 1.0 approved)
- [x] Configurazioni apparati (allegato ad As-Built, hash SHA256 verificati)
- [x] Certifiche Fluke cablaggio (allegato ad As-Built)
- [x] Licenze software (allegato al presente §4)
- [x] Contratti di manutenzione (allegato al presente §5)

### Training del team operations
- TR-01: 2026-03-20, 4h, Marco Conti + Paolo Ferri, "Overview infrastruttura + console principali" — Completato
- TR-02: 2026-03-21, 6h, Marco Conti + Paolo Ferri + Luca Bruni, "Procedure SOP L1/L2" — Completato
- TR-03: 2026-03-22, 4h, Marco Conti + Paolo Ferri, "Procedure DR + tabletop exercise" — Completato
- TR-04: 2026-03-23, 2h, Marco Conti, "Monitoring & escalation" — Completato
- Esito: tutti i partecipanti hanno superato la verifica finale (quiz pratico, soglia 80%)

### Inventario hardware (ereditato da As-Built)
- 3 server Dell PowerEdge R750 (SRV-01/02/03, service tag ABC1234/5/6)
- 4 switch Cisco N9K-C93180YC-FX (sw-core-01/02, sw-tor-01/02, serial FOC12345..8)
- 1 storage NetApp FAS8700 (stor-01, serial NETAPP-001) + 1 storage DR stor-dr (BG-01)
- 2 firewall Fortinet FortiGate 200F (fw-01/02, serial FG200F-001/2)
- 1 backup appliance Veeam Hardened (bkp-01, serial VHA-001, 72TB)
- 2 UPS APC SRT 10kVA (ups-01/02, serial AS230001/2)
- 4 PDU APC AP8941 (pdu-01..04, serial AP8941-001..4)
- Valore stimato totale: 178.500 €

### Contratti di manutenzione
- CTR-001: Dell ProSupport Plus — copre SRV-01/02/03 — 5y NBD + 24x7 phone — dal 2026-03-16 al 2031-03-16 — €18.000/anno
- CTR-002: Cisco SMARTnet — copre sw-core/tor — 5y 24x7x4 — dal 2026-03-16 al 2031-03-16 — €6.500/anno
- CTR-003: NetApp Premium — copre stor-01, stor-dr — 5y 24x7 — dal 2026-03-16 al 2031-03-16 — €22.000/anno
- CTR-004: Fortinet FortiCare + UTM — copre fw-01/02 — 3y 24x7 — dal 2026-03-16 al 2029-03-16 — €4.800/anno — RINNOVO ENTRO 2029-01-16
- CTR-005: Veeam Premium Care — copre bkp-01 — 3y — dal 2026-03-16 al 2029-03-16 — €3.200/anno — RINNOVO ENTRO 2029-01-16
- CTR-006: APC Standard — copre UPS-01/02 — 3y — dal 2026-03-16 al 2029-03-16 — €1.000/anno

### Licenze software
- VMware vSphere Enterprise Plus: 3 CPU (SRV-01/02/03), subscription, rinnovo annuale, scadenza 2027-03-16, €6.000/anno
- VMware vCenter Standard: 1 istanza, subscription, scadenza 2027-03-16, €2.500/anno
- VMware vSAN Advanced: 3 CPU, subscription, scadenza 2027-03-16, €4.500/anno
- NetApp ONTAP Standard: 1 cluster, subscription, scadenza 2031-03-16 (incluso in CTR-003)
- NetApp SnapMirror: 1 cluster, subscription, scadenza 2031-03-16 (incluso in CTR-003)
- Fortinet FortiGate UTM bundle: 2 appliance, subscription, scadenza 2029-03-16 (incluso in CTR-004)
- Tenable Nessus Professional: 1 console, subscription, scadenza 2027-03-16, €2.000/anno
- Veeam Backup Enterprise Plus: 1 istanza + 1 socket, subscription, scadenza 2029-03-16 (incluso in CTR-005)
- Veeam Cloud Connect: 1 subscription, scadenza 2027-03-16, €1.500/anno
- Microsoft Windows Server 2022 STD: 16 licenze (8x2cpu), perpetua + SA, scadenza SA 2028-03-16, €0/anno (già pagato)
- Microsoft Windows Server CAL: 100 CAL, perpetua + SA, scadenza SA 2028-03-16
- Red Hat Enterprise Linux: 4 socket subscription, scadenza 2027-03-16, €2.800/anno

### SLA concordati
- Disponibilità infrastruttura: ≥ 99.9% mensile
- Risposta NO H24 sev-1: ≤ 15 min
- Risoluzione sev-1: ≤ 4h
- Backup restore singolo file: ≤ 4h
- DR activation: ≤ 4h
- Penalità SLA: 5% fattura mensile per ogni 0.1% sotto target, max 30%

### Contatti cliente
- Luca Verdi (Sponsor CFO): +39 335 100200, luca.verdi@acme.it, office hours
- Marco Conti (NO Lead): +39 333 1234567, marco.conti@acme.it, H24 rotazione
- Anna Neri (CISO): +39 333 4567890, anna.neri@acme.it, office + on-call
- System Engineer on-call: rotazione settimanale (Marco/ Paolo/ Luca), contatti in rotation calendar
- Acme Facility (accesso fisico): +39 02 1234567, facility@acme.it, office + emergenze

### Contatti fornitore (integratore)
- Account Manager: Stefano Gallo, +39 348 999000, s.gallo@integ.it, office hours
- Technical Lead: Mario Rossi, +39 333 111222, m.rossi@integ.it, office + emergenze
- Support contrattuale (TAC): support@integ.it, ticket portal https://support.integ.it, H24 con SLA contratto

### Piano di hypercare
- Prime 30 giornate (2026-03-25 → 2026-04-24): supporto prioritario integratore, risposta ≤ 2h per sev-2/3
- Stand-up quotidiani (15 min) tra NO Acme e Tech Lead integratore
- Report settimanale SLA e incidenti a Luca Verdi (Sponsor)

### Milestones di maturità
- M1: Chiusura punch list (T+7gg, 2026-04-01) — tutte le azioni OA-001..OA-004 completate
- M2: SLA stabile (T+30gg, 2026-04-24) — SLA ≥ target per 30gg consecutivi
- M3: DR test funzionante (T+60gg, 2026-05-24) — DR test eseguito con successo dal team Acme
- M4: Hypercare concluso (T+30gg, 2026-04-24) — passaggio a regime operativo standard

### Stato finanziario
- Hardware (capex): 142.500 €
- Software licenze iniziali (capex): 28.000 €
- Servizi installazione (capex): 8.000 €
- Contratti di manutenzione annuali (opex): 55.500 €/anno
- Licenze subscription annuali (opex): 19.300 €/anno
- TOTALE capex investito: 178.500 €
- TOTALE opex ricorrente annuo: 74.800 €/anno

### Limitazioni note e azioni future
- LIM-001: Sito DR non ancora dotato di storage secondario di emergenza (oltre stor-dr) — Impatto: DR parzialmente coperto in caso di perdita both siti — Piano: installare Q3 2026
- LIM-002: 3 VM legacy (LO-APP-01/02/03) non ancora migrate — Impatto: funzionalità residua su vecchia infrastruttura fino a 2026-04-30 — Piano: migrazione entro 2026-04-30 (Owner: PM)
- LIM-003: Pen-test annuale non ancora schedulato — Impatto: compliance ISO 27001 — Piano: schedulare entro 2026-04-30 (Owner: Anna Neri)
- LIM-004: 2 vuln medie su IP MGMT (CVE-2024-1234, CVE-2024-5678) — Impatto: security posture — Piano: patch entro 2026-04-25 (Owner: Anna Neri)

## TEMPLATE DA COMPILARE

Template path: /download/templates/09-Handover-Inventory.md
Tipo documento: Handover-Inventory
Fase: 7

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Inventario deve coincidere con As-Built §4 — verifica coerenza
  * Ogni asset: modello, seriale, asset tag, MAC, IP, data install, garanzia fino al, contratto supporto
  * Licenze: prodotto, chiave (riferimento vault), quantità, scadenza, tipo
  * SLA concordati = RSD/URS §9 + contratto
  * Firme in fondo al documento
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-asbuilt-01, specification-acme-milano-atp-01]
- related_docs del nuovo Handover:
  - specification-acme-milano-rsd-01
  - architecture-acme-milano-asbuilt-01
  - specification-acme-milano-atp-01
  - guide-acme-milano-sop-runbook-01

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft → approved (dopo firme)
- Versione: 0.1
- ID documento: specification-acme-milano-handover-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe) incluso il valore capex e opex
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/09-Handover-Inventory.md
   - ID: specification-acme-milano-handover-01

Compila il documento ora. Sarà lungo (380+ righe).

INOLTRE, genera due file allegati:
1. Asset inventory in CSV: /vault/projects/acme-milano-2026/09-handover-asset-inventory.csv
   Colonne: hostname, modello, seriale, asset_tag, MAC, IP, rack, U-pos, firmware, data_install, garanzia_fino_al, contratto_supporto, valore_eur
2. Calendario rinnovi in ICS: /vault/projects/acme-milano-2026/09-handover-renewals-calendar.ics
   Eventi: ogni rinnovo licenza/contratto con reminder 90gg, 60gg, 30gg prima
```

---

## Output atteso

Documento Handover & Inventory completo con:

- Verbale di presa in carico con 5 firme (Sponsor, NO Lead, Security, PM, Tech Lead)
- Documentazione consegnata spuntata (5 documenti + allegati)
- Training del team operations documentato (4 sessioni con esito)
- Asset inventory completo per categoria (server, switch, storage, firewall, backup, UPS/PDU) — coerente con As-Built §4
- Riepilogo asset totali con valore stimato
- 6 contratti di manutenzione registrati con date e importi
- 11 licenze software elencate con scadenza
- Riepilogo scadenze prossimi 12 mesi popolato
- SLA concordati con target e penalità
- Contatti cliente e vendor verificati (con data ultima verifica)
- Piano di hypercare 30 giorni definito
- 4 milestones di maturità operative
- Stato finanziario completo (capex + opex)
- 4 limitazioni note con piano di risoluzione
- Firme di 5 parti contraenti
- Asset inventory esportato in CSV (Appendice A)
- Calendario rinnovi in ICS (Appendice B)

---

## Tip & truccoli

### Per coerenza con As-Built
L'inventario nell'Handover DEVE coincidere con l'As-Built §4. Verifica che:
- Stessi seriali per ogni asset
- Stessi MAC address
- Stessi IP management
- Stesse date di installazione
- Se ci sono discrepanze, l'handover è bloccato

### Per le scadenze
Le scadenze sono critiche per evitare sorprese (licenze scadute, contratti non rinnovati). Verifica che:
- Ogni licenza e contratto abbia una data di scadenza
- Le scadenze prossime 12 mesi siano elencate in ordine cronologico
- Il calendario ICS includa reminder 90/60/30 giorni prima

### Per generare il CSV asset inventory
L'agente dovrebbe generare un file CSV separato con tutte le colonne specificate. Esempio di struttura:

```csv
hostname,modello,seriale,asset_tag,MAC,IP,rack,U-pos,firmware,data_install,garanzia_fino_al,contratto_supporto,valore_eur
SRV-01,Dell PowerEdge R750,ABC1234,AST-001,AA:BB:CC:DD:EE:01,10.10.50.101,R01,U38-37,3.10.10.10,2026-03-16,2031-03-16,CTR-001,42000
...
```

### Per generare il calendario ICS
Il calendario ICS deve essere importabile in Outlook/Google Calendar. Struttura tipica:

```
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Acme//Handover Renewals//IT
BEGIN:VEVENT
UID:renewal-001@acme.it
DTSTAMP:20260325T080000Z
DTSTART:20290116T080000Z
DTEND:20290116T090000Z
SUMMARY:RINNOVO Fortinet UTM bundle (CTR-004)
DESCRIPTION:Contratto in scadenza il 2029-03-16\nAsset: fw-01/02\nImporto: 4800 EUR/anno
BEGIN:VALARM
TRIGGER:-90D
ACTION:DISPLAY
DESCRIPTION:Reminder 90gg - rinnovo CTR-004
END:VALARM
END:VEVENT
...
END:VCALENDAR
```

### Per il piano di hypercare
Il piano di hypercare 30 giorni è importante per la transizione. Verifica che:
- Sia chiaramente delimitato nel tempo (data inizio/fine)
- Indichi i livelli di supporto e SLA durante l'hypercare
- Indichi le milestone di chiusura hypercare

### Per le firme
Le firme formalizzano la presa in carico. Verifica che:
- Siano presenti tutti i ruoli previsti (Sponsor, NO, Security, PM, Tech Lead)
- La data di firma sia coerente con la data di handover dichiarata
- Lo status del documento passi da draft a approved dopo le firme

### Validazione finale
Dopo la generazione, valida con:
```text
Verifica la coerenza tra Handover e As-Built: ogni asset nell'inventario
dell'Handover deve avere corrispondenza nell'As-Built §4 (stesso seriale, stesso MAC).
Elenca eventuali discrepanze.
```
