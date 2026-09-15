# Esempio prompt — As-Built Documentation

Scenario: fotografia dell'infrastruttura effettivamente installata (post-deploy).

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: RSD/URS, HLD, LLD, MOP, Rollback
- **Stato**: deploy completato con successo, alcune deviazioni dal LLD emerse durante l'installazione
- **Obiettivo**: documentare lo stato reale post-deploy per futuro supporto e operations

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un system engineer senior specializzato in documentazione tecnica post-deploy.
Il tuo compito è compilare il template As-Built Documentation, che rappresenta
la FOTOGRAFIA ESATTA dell'infrastruttura effettivamente installata e configurata.

Le informazioni DEVONO riflettere lo stato reale post-deploy, NON il progetto iniziale.
Ogni deviazione dal LLD deve essere documentata in sezione §3 con motivazione.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - RSD/URS: /vault/projects/acme-milano-2026/01-RSD-URS.md
   - LLD: /vault/projects/acme-milano-2026/03-LLD.md
   - MOP: /vault/projects/acme-milano-2026/04-MOP.md

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (Tech Lead, Integratore)
- reviewer: Giulia Bianchi
- approver: Marco Conti (NO Acme, presa in carico)
- owner_team: Acme Operations
- Data installazione: 2026-03-16 a 2026-03-18
- Data cutover: 2026-03-18 22:00

## DATI SPECIFICI — As-Built

### Stato finale dichiarato
- [x] Infrastruttura fisica installata e cablata (certificate)
- [x] Configurazioni caricate su tutti gli apparati
- [x] Cluster hypervisor operativo con VM base attive
- [x] Storage e repliche verso DR attivi
- [x] Cutover completato con esito positivo
- [x] Servizi pubblici accessibili dall'esterno

### Deviazioni dal LLD (da documentare in §3)
- DEV-001: Switch ToR sw-tor-01/02: modello Cisco N9K-C93180YC-FX invece di N9K-C93180YC-FX-XT (XT in EOL, sostituito con FX standard). Approvazione: Luca Verdi in data 2026-03-10.
- DEV-002: Storage LUN-002: dimensione 6 TB invece di 5 TB (crescita stima data applicativi). Approvazione: Mario Rossi in data 2026-03-15.
- DEV-003: VLAN 80 BACKUP: /23 invece di /24 (range IP esaurito per appliance backup). Approvazione: Giulia Bianchi in data 2026-03-16.
- DEV-004: Firewall policy EW-005: aggiunto logging enhanced (richiesto da compliance ISO 27001 audit interno). Approvazione: Anna Neri in data 2026-03-17.
- DEV-005: UPS-01: firmware 3.10.10.10 invece di 3.10.10.08 (aggiornamento automatico durante staging). Approvazione: Mario Rossi in data 2026-03-15.

### Inventario hardware installato (seriali e firmware reali)

#### Server / Hypervisor
- SRV-01: Dell PowerEdge R750, Service Tag ABC1234, Asset AST-001, Rack R01 U38-37, MAC iLO AA:BB:CC:DD:EE:01, IP iLO 10.10.50.101, 2x Xeon Gold 6338 (32c), 256GB RAM, 2x 480GB SSD RAID1, ESXi 8.0 U2 build 22380479, iLO firmware 3.10.10.10
- SRV-02: Dell PowerEdge R750, Service Tag ABC1235, Asset AST-002, Rack R01 U36-35, MAC iLO AA:BB:CC:DD:EE:02, IP iLO 10.10.50.102, same specs SRV-01
- SRV-03: Dell PowerEdge R750, Service Tag ABC1236, Asset AST-003, Rack R01 U34-33, MAC iLO AA:BB:CC:DD:EE:03, IP iLO 10.10.50.103, same specs SRV-01

#### Switch
- sw-core-01: Cisco N9K-C93180YC-FX, Serial FOC12345ABC, Asset AST-010, Rack R02 U30, MAC AA:11:22:33:44:01, IP 10.10.50.11, NX-OS 9.3(10), firmware 13.2(2n)
- sw-core-02: Cisco N9K-C93180YC-FX, Serial FOC12346ABD, Asset AST-011, Rack R02 U29, MAC AA:11:22:33:44:02, IP 10.10.50.12, NX-OS 9.3(10)
- sw-tor-01: Cisco N9K-C93180YC-FX, Serial FOC12347ABE, Asset AST-012, Rack R01 U41, MAC AA:11:22:33:44:03, IP 10.10.50.13, NX-OS 9.3(10)
- sw-tor-02: Cisco N9K-C93180YC-FX, Serial FOC12348ABF, Asset AST-013, Rack R01 U40, MAC AA:11:22:33:44:04, IP 10.10.50.14, NX-OS 9.3(10)

#### Storage
- stor-01: NetApp FAS8700, Serial NETAPP-001, Asset AST-020, Rack R02 U38-35, IP Mgmt 10.10.50.20, ONTAP 9.13.1, dual controller, 24x SSD NVMe 1.92TB + 12x NL-SAS 8TB, raw 142TB, usable 94TB

#### Firewall
- fw-01: Fortinet FortiGate 200F, Serial FG200F-001, Asset AST-030, Rack R02, IP Mgmt 10.10.50.30, FortiOS 7.4.3
- fw-02: Fortinet FortiGate 200F, Serial FG200F-002, Asset AST-031, Rack R02, IP Mgmt 10.10.50.31, FortiOS 7.4.3

#### Backup Appliance
- bkp-01: Veeam Hardened Appliance, Serial VHA-001, Asset AST-040, Rack R02, IP Mgmt 10.10.50.40, Veeam 12.1, 72TB usable

#### UPS / PDU
- ups-01: APC SRT 10kVA, Serial AS230001, Asset AST-050, Rack R01, IP 10.10.50.50, firmware 3.10.10.10
- ups-02: APC SRT 10kVA, Serial AS230002, Asset AST-051, Rack R02, IP 10.10.50.51, firmware 3.10.10.10
- pdu-01: APC AP8941, Serial AP8941-001, Asset AST-060, Rack R01 U42, IP 10.10.50.60
- pdu-02: APC AP8941, Serial AP8941-002, Asset AST-061, Rack R02 U42, IP 10.10.50.61
- pdu-03: APC AP8941, Serial AP8941-003, Asset AST-062, Rack R01 U1, IP 10.10.50.62
- pdu-04: APC AP8941, Serial AP8941-004, Asset AST-063, Rack R02 U1, IP 10.10.50.63

### Indirizzi IP assegnati (estratto principali)
- 10.10.10.2: fw-01 (VLAN 10 DMZ) — MAC AA:BB:CC:01
- 10.10.10.3: fw-02 (VLAN 10 DMZ) — MAC AA:BB:CC:02
- 10.10.50.11..14: switch (VLAN 50 MGMT)
- 10.10.50.20: stor-01 (VLAN 50)
- 10.10.50.30-31: firewall mgmt (VLAN 50)
- 10.10.50.101-103: SRV-01/02/03 iLO (VLAN 50)
- 10.10.70.10: stor-01-a (iSCSI A) — MAC AA:CC:01
- 10.10.70.11: stor-01-b (iSCSI B) — MAC AA:CC:02
- Subnet totali: VLAN 10 /24, VLAN 20 /24, VLAN 30 /24, VLAN 50 /24, VLAN 70 /24, VLAN 80 /23

### Configurazioni finali (file allegati)
- /vault/projects/acme-milano-2026/configs/fw-01.cfg — SHA256 <calcola durante compilazione>
- /vault/projects/acme-milano-2026/configs/fw-02.cfg
- /vault/projects/acme-milano-2026/configs/sw-core-01.cfg
- /vault/projects/acme-milano-2026/configs/sw-core-02.cfg
- /vault/projects/acme-milano-2026/configs/sw-tor-01.cfg
- /vault/projects/acme-milano-2026/configs/sw-tor-02.cfg
- /vault/projects/acme-milano-2026/configs/stor-01.cfg
- /vault/projects/acme-milano-2026/configs/hv-cluster.json

### Credenziali (riferimenti al vault, NO password)
- fw-01 admin: vault://it/acme-milano-2026/fw-01/admin
- fw-02 admin: vault://it/acme-milano-2026/fw-02/admin
- sw-core-01 admin: vault://it/acme-milano-2026/sw-core-01/admin
- ... (per ogni apparato)
- vCenter admin: vault://it/acme-milano-2026/vcenter/admin
- bkp-01 admin: vault://it/acme-milano-2026/bkp-01/admin
- UPS/PDU admin: vault://it/acme-milano-2026/ups/admin

### Servizi base configurati
- DC-01: 10.10.50.20, primary, FSMO roles
- DC-02: 10.10.50.21, secondary, replica
- DNS zones: acme.local (forward), 10.10.in-addr.arpa (reverse), forwarders 8.8.8.8 1.1.1.1
- DHCP scopes: VLAN 20 (10.10.20.50-200), VLAN 50 (10.10.50.100-200)
- NTP: ntp-01 (10.10.50.30), ntp-02 (10.10.50.31)

### Backup configurati
- Job-VM-PROD: SRV-01/02/03 + DC-01/02, 22:00 daily, Veeam → bkp-01 (30gg locali) + cloud S3 (365gg)
- Job-FILE: FILE-SRV-01, 02:00 daily, Veeam → bkp-01 (90gg)
- Job-CONFIG: fw-01/02, sw-core-01/02, 04:00 daily, script → bkp-01 + vault (180gg)
- Job-STORAGE-SNAP: stor-01 pool, ogni 1h, ONTAP → stor-01 + stor-dr (24 snapshot)
- Repliche: stor-01 → stor-dr (BG-01) ogni 15 min (Tier1) e ogni 1h (Tier2)
- bkp-01 → cloud S3 (cifrato lato client), sync copy continua

### Note di installazione
- Switch ToR R01 ha surriscaldamento in U41 durante i primi 2 giorni (ventola rack insufficiente). Risolto con attivazione ventola ausiliaria rack.
- Cablaggio intra-rack R02 ha richiesto 2 ore extra per conflitto canalina (preesistente).
- UPS-01 ha segnalato allarme batteria durante test iniziale (risolto con reset controller).
- WAN verso BG-01 ha latenza variabile 10:00-12:00 (fenomeno già noto con ISP).

### Azioni rimaste aperte (punch list)
- OA-001: Configurare MFA su vCenter — Owner: Anna Neri — Scadenza: 2026-03-25
- OA-002: Aggiornare firmware UPS-02 alla stessa versione di UPS-01 — Owner: Mario Rossi — Scadenza: 2026-04-15
- OA-003: Completare migrazione ultimi 3 server legacy (LO-APP-01/02/03) — Owner: PM — Scadenza: 2026-04-30
- OA-004: Penetration test completo (post-cutover) — Owner: Anna Neri — Scadenza: 2026-04-30

## TEMPLATE DA COMPILARE

Template path: /download/templates/06-As-Built.md
Tipo documento: As-Built
Fase: 7

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Informazioni DEVONO riflettere lo stato reale post-deploy
  * Ogni deviazione dal LLD in §3 con motivazione e approvazione
  * Includere seriali, versioni firmware, MAC address
  * Configurazioni complete allegate come file separati (NON inline)
  * NO credenziali in chiaro (riferimento al vault)
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-lld-01, guide-acme-milano-mop-01]
- related_docs del nuovo As-Built:
  - architecture-acme-milano-lld-01
  - guide-acme-milano-mop-01
  - specification-acme-milano-atp-01 (placeholder, da compilare)
  - guide-acme-milano-sop-runbook-01 (placeholder, da compilare)
  - specification-acme-milano-handover-01 (placeholder, da compilare)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft (passa a in-review dopo compilazione ATP)
- Versione: 0.1
- ID documento: architecture-acme-milano-asbuilt-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe) incluse le 5 deviazioni dal LLD
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/06-As-Built.md
   - ID: architecture-acme-milano-asbuilt-01

Compila il documento ora. Sarà lungo (350+ righe).
```

---

## Output atteso

Documento As-Built completo con:

- Sintesi infrastruttura installata
- Diagrammi as-built (logico + fisico)
- 5 deviazioni dal LLD documentate con motivazione e approvazione
- Inventario hardware completo per ogni categoria (server, switch, storage, firewall, backup, UPS/PDU) con seriali, MAC, firmware
- IP plan assegnato completo + subnet totali utilizzate
- Riferimenti ai file di configurazione (con hash SHA256 da calcolare)
- Riferimenti alle credenziali nel vault (no password in chiaro)
- Servizi base (AD, DNS, DHCP, NTP) con stato reale
- Backup e repliche as-built con stato attuale
- Note di installazione qualitative
- Punch list (4 azioni rimaste aperte)
- Checklist di validazione completa

---

## Tip & trucchi

### Per le deviazioni dal LLD
Le deviazioni sono NORMALI in qualsiasi progetto reale. Verifica che ogni DEV-xxx abbia:
- ID univoco
- Differenza chiara tra "LLD prevedeva" e "As-Built realizzato"
- Motivazione tecnica o operativa
- Approvazione (nome, data)

### Per gli hash SHA256
Dopo aver salvato i file di configurazione, calcola l'hash con:
```bash
sha256sum /vault/projects/acme-milano-2026/configs/fw-01.cfg
```
oppure su PowerShell:
```powershell
Get-FileHash -Algorithm SHA256 "C:\vault\...\fw-01.cfg"
```
Inserisci l'hash nel documento per permettere verifica di integrità futura.

### Per le configurazioni complete
NON incollare le configurazioni complete nel body del documento (sarebbe troppo lungo). Salva i file `.cfg` come allegati e referenziali nella tabella §6.

### Per l'inventario esportabile
Genera anche un file Excel con l'inventario (un record per asset) come allegato Appendice A. L'agente può generare la struttura CSV/Excel:

```text
Genera anche un file CSV con l'inventario completo degli asset,
con colonne: hostname, modello, seriale, asset_tag, MAC, IP, rack, U-pos, firmware, data_install, garanzia_fino_al
Salva in /vault/projects/acme-milano-2026/06-As-Built-inventory.csv
```

### Per coerenza con ATP e SOP
L'As-Built è il documento CARDINE post-lavoro. Verifica che:
- Tutti i componenti citati nell'ATP siano presenti nell'As-Built
- Tutte le procedure nel SOP/Runbook facciano riferimento a hostnames/IP dell'As-Built
- L'Handover & Inventory erediti l'inventario dall'As-Built
