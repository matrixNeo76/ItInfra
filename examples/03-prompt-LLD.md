# Esempio prompt — LLD (Low-Level Design)

Scenario: blueprint esecutivo con tutti i dettagli puntuali (IP, VLAN, porte, LUN, ACL).

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: RSD/URS + HLD
- **Obiettivo**: produrre il blueprint tecnico esecutivo per installatori e configuratori

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un network/storage architect senior specializzato in dettagli di implementazione.
Il tuo compito è compilare il template LLD (Low-Level Design) partendo dall'HLD già approvato.
QUI servono i dettagli puntuali: IP, porte, VLAN ID, LUN, ACL, parametri config.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - RSD/URS: /vault/projects/acme-milano-2026/01-RSD-URS.md (id: specification-acme-milano-rsd-01)
   - HLD: /vault/projects/acme-milano-2026/02-HLD.md (id: architecture-acme-milano-hld-01)
4. Conferma con un riepilogo di 5 righe delle decisioni architetturali principali

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (Network/Storage Architect)
- reviewer: Giulia Bianchi (Tech Lead)
- approver: Luca Verdi (Sponsor Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — LLD

### Subnet e VLAN (da specifica utente)
- 10.10.10.0/24 → VLAN 10 → DMZ
- 10.10.20.0/24 → VLAN 20 → PROD-APP
- 10.10.30.0/24 → VLAN 30 → PROD-DB (isolata)
- 10.10.50.0/24 → VLAN 50 → MGMT
- 10.10.70.0/24 → VLAN 70 → STORAGE (iSCSI)
- 10.10.80.0/23 → VLAN 80 → BACKUP
- Subnet DR: 10.20.0.0/16 (sito BG-01)

### Hardware installato
- 3x Dell PowerEdge R750 (service tag: ABC1234, ABC1235, ABC1236)
  - 2x Xeon Gold 6338 (32c), 256GB RAM, 2x 480GB SSD RAID1 (boot)
- 2x Cisco Nexus N9K-C93180YC-FX (core, MLAG)
- 2x Cisco Nexus N9K-C93180YC-FX (ToR)
- 1x NetApp FAS8700 (serial: NETAPP-001):
  - 24x SSD NVMe 1.92TB (Pool-Tier1, RAID6 8+2)
  - 12x NL-SAS 8TB (Pool-Tier2, RAID6 10+2)
- 2x Fortinet FortiGate 200F (HA active/passive)
- 1x Veeam Hardened Appliance (72 TB usable)
- 2x APC SmartUPS SRT 10kVA

### Porte fisiche (cable matrix parziale — espandi per tutte le porte)
- sw-core-01 Gi1/0/1 ↔ sw-core-02 Gi1/0/1 (MLAG peer link, trunk)
- sw-core-01 Gi1/0/2 ↔ sw-tor-01 Gi1/0/47 (uplink R01, trunk)
- sw-core-01 Gi1/0/3 ↔ sw-tor-02 Gi1/0/47 (uplink R02, trunk)
- sw-core-01 Gi1/0/10 ↔ fw-01 port1 (VLAN 10 access)
- sw-core-01 Gi1/0/11 ↔ fw-02 port1 (VLAN 10 access)
- sw-tor-01 Gi1/0/10 ↔ SRV-01 iLO (VLAN 50)
- sw-tor-01 Gi1/0/11 ↔ SRV-01 NIC2 (trunk)
- sw-tor-01 Gi1/0/20 ↔ SRV-02 iLO (VLAN 50)
- sw-tor-01 Gi1/0/21 ↔ SRV-02 NIC2 (trunk)
- sw-tor-01 Gi1/0/30 ↔ SRV-03 iLO (VLAN 50)
- sw-tor-01 Gi1/0/31 ↔ SRV-03 NIC2 (trunk)
- sw-tor-02 Gi1/0/10 ↔ stor-01 controller A mgmt (VLAN 50)
- sw-tor-02 Gi1/0/20 ↔ stor-01 controller A iSCSI-A (VLAN 70)
- sw-tor-02 Gi1/0/21 ↔ stor-01 controller B iSCSI-B (VLAN 70)
- sw-tor-02 Gi1/0/30 ↔ bkp-01 mgmt (VLAN 50)
- sw-tor-02 Gi1/0/31 ↔ bkp-01 data (VLAN 80)

### Storage configuration
- Pool-Tier1 (SSD): 30 TB usable, iSCSI, LUN-001 (5TB esxi-datastore-01), LUN-002 (5TB esxi-datastore-02)
- Pool-Tier2 (NL-SAS): 64 TB usable, NFS share nfs-share-app (10TB), SMB share smb-share-file (20TB)
- Replica async verso stor-dr (BG-01) ogni 15 min per Tier1, ogni 1h per Tier2
- Snapshot locali ogni 1h, retention 24h

### Firewall policy principali
- EW-001: PROD-APP → PROD-DB su TCP/5432 (PostgreSQL) e TCP/3306 (MySQL) — allow
- EW-002: PROD-DB → any — deny (DB isolato)
- EW-003: MGMT → any su TCP/22, TCP/443, ICMP — allow
- EW-004: PROD-APP → MGMT — deny
- EW-005: any → STORAGE — deny (L2 only)
- NS-001: Internet → public VIP:443 — allow
- NS-002: any → any — deny (default)
- NS-003: PROD-APP → 0.0.0.0/0 su TCP/443, TCP/53, UDP/53 — allow (HTTPS+DNS)
- VPN-001: IPsec site-to-site verso BG-01 (stor-dr), AES256-GCM, DH14
- VPN-002: SSL VPN per remote access admin, MFA + cert

### Servizi base
- DC-01: 10.10.50.20 (primary, FSMO)
- DC-02: 10.10.50.21 (secondary, replica)
- DNS: forward zone acme.local su DC-01/02, forwarder 8.8.8.8 e 1.1.1.1
- DHCP scope VLAN 20: 10.10.20.50-200, gateway 10.10.20.1, lease 8h
- NTP: ntp-01 (10.10.50.30), ntp-02 (10.10.50.31), stratrum 2

### Hypervisor
- Cluster CL-PROD-01 (3 nodi SRV-01/02/03)
- vDS (vSphere Distributed Switch) "DS-PROD"
- Port group: PG-MGMT (VLAN 50), PG-PROD-APP (VLAN 20), PG-PROD-DB (VLAN 30), PG-STORAGE-iSCSI (VLAN 70), PG-BACKUP (VLAN 80)
- DRS: fully automated, HA: enabled

## TEMPLATE DA COMPILARE

Template path: /download/templates/03-LLD.md
Tipo documento: LLD
Fase: 2

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * QUI servono i dettagli puntuali (IP, porte, VLAN ID, LUN, ACL)
  * Ogni tabella deve essere completa e coerente
  * Indicare SEMPRE il riferimento alla porta fisica (es. SW01-Gi1/0/24)
  * Per ogni policy firewall: sorgente, destinazione, porta, azione, log
  * NO password in chiaro (riferimento al vault)
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-hld-01]
- related_docs del nuovo LLD:
  - specification-acme-milano-rsd-01
  - architecture-acme-milano-hld-01
  - guide-acme-milano-mop-01 (placeholder, da compilare)
  - architecture-acme-milano-asbuilt-01 (placeholder, da compilare post-deploy)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft
- Versione: 0.1
- ID documento: architecture-acme-milano-lld-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe) con coerenza rispetto a HLD
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/03-LLD.md
   - ID: architecture-acme-milano-lld-01

Compila il documento ora. Il documento sarà lungo (400+ righe), non sintetizzare.
```

---

## Output atteso

Documento LLD completo con:

- 12 sezioni principali compilate
- Tabelle IP/VLAN complete e coerenti (subnets, mapping VLAN→zona, allocazione host fissi con MAC)
- Rack elevation per R01 (compute) e R02 (storage+network) — 42U ciascuno
- Cable matrix completa per sw-core-01, sw-core-02, sw-tor-01, sw-tor-02 (ogni porta mappata)
- Patch panel matrix con certificazione Fluke
- Storage: pool, RAID, LUN, replica, snapshot
- Routing: OSPF area 0, BGP ASN, route statiche, NAT
- Firewall: policy east-west (5 regole), north-south (4 regole), VPN (2 tunnel)
- Servizi base: AD con OU structure, DNS zones, DHCP scopes, NTP
- Hypervisor: cluster config, vSwitch, port group, template VM
- Backup: job, schedule, retention
- Monitoring: tool, endpoint, frequenza
- Appendice A: snippet di configurazione per switch core e firewall
- Checklist di validazione completa

---

## Tip & trucchi

### Per coerenza con HLD
Dopo aver letto l'HLD, l'agente dovrebbe verificare che:
- Tutti i componenti HLD siano presenti nel LLD
- Le modalità HA siano rispettate (active/active, MLAG, dual controller)
- I protocolli siano coerenti (iSCSI per storage, se HLD dice così)

### Per la cable matrix
La cable matrix è la sezione più critica. Verifica che:
- Ogni porta abbia un dispositivo remoto e una porta remota
- Le VLAN siano corrette (access vs trunk)
- Non ci siano porte orfane (senza destinazione)

### Per le policy firewall
Verifica che l'agente rispetti il principio di **default deny** (regola NS-002: any→any deny) e che le regole allow siano specifiche (no `any` come sorgente o destinazione, se possibile).

### Per snippet di configurazione
Gli snippet in Appendice A dovrebbero essere **pseudo-codice vendor-agnostic** o chiaramente etichettati per vendor. Richiedi esplicitamente se vuoi snippet reali:

```text
Per gli snippet in Appendice A, usa sintassi reale vendor-specific:
- Cisco Nexus: NX-OS syntax
- Fortinet: FortiOS CLI syntax
- VMware: PowerCLI
```

### Validazione incrociata
Dopo la generazione, chiedi all'agente di validare:
- Subnet totali utilizzate vs allocation
- Capacità storage: raw vs usable vs allocato
- Numero di porte switch: fisiche vs utilizzate
- MAC address univoci
