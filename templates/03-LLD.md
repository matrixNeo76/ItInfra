---
okf_version: "0.2"
id: "architecture-<project_slug>-lld-01"
title: "LLD — <titolo progetto, es. Sostituzione Infrastruttura Datacenter Milano>"
type: "architecture"
domain: "IT Infrastructure & Detailed Engineering"
tags: ["okf-v0.2", "lld", "design", "esecutivo", "fase-2", "ip-plan", "vlan", "cable-matrix"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "<PROJECT_ID>"
project_name: "<nome progetto>"
site: "<SITE_CODE>"
customer: "<cliente>"
phase: 2
author: "<nome>"
reviewer: "<nome>"
approver: "<nome>"
owner_team: "<team>"
status: "draft"
version: "0.1"
created_at: "<YYYY-MM-DD>"
updated_at: "<YYYY-MM-DD>"
related_docs:
  - "specification-<project_slug>-rsd-01"
  - "architecture-<project_slug>-hld-01"
  - "guide-<project_slug>-mop-01"
  - "architecture-<project_slug>-asbuilt-01"
depends_on:
  - "architecture-<project_slug>-hld-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "IP Subnetting Plan"
    type: "specification"
    description: "Schema di subnetting e VLAN per tutte le zone di rete (DMZ, PROD, MGMT, STORAGE, BACKUP)"
  - name: "Rack Elevation"
    type: "pattern"
    description: "Layout fisico unità rack per server, switch, storage, UPS"
  - name: "Cable Matrix"
    type: "specification"
    description: "Mappatura fisica delle porte switch, patch panel e interfacce"
  - name: "Storage LUN Mapping"
    type: "specification"
    description: "Configurazione LUN, RAID pool, protocolli iSCSI/NFS/SMB, repliche"
  - name: "Firewall ACL Matrix"
    type: "specification"
    description: "Policy east-west e north-south con sorgente, destinazione, porta, azione"
  - name: "VLAN Topology"
    type: "pattern"
    description: "Topologia di VLAN tagging e trunk 802.1Q tra switch e hypervisor"

relations:
  - targetTitle: "HLD — High-Level Design"
    targetId: "architecture-<project_slug>-hld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'LLD espande l'HLD con dettagli puntuali (IP, porte, parametri config)"
  - targetTitle: "RSD/URS — Requirements Specification Document"
    targetId: "specification-<project_slug>-rsd-01"
    relationType: "references"
    weight: 0.9
    description: "I requisiti del RSD/URS sono soddisfatti puntualmente nell'LLD"
  - targetTitle: "MOP — Method of Procedure"
    targetId: "guide-<project_slug>-mop-01"
    relationType: "references"
    weight: 0.9
    description: "Il MOP usa l'LLD come blueprint operativo passo-passo"
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "references"
    weight: 0.95
    description: "L'As-Built documenta lo stato reale post-deploy confrontandolo con l'LLD"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: produrre il blueprint tecnico esecutivo per installatori e configuratori.
  Input attesi: HLD approvato, sito survey, eventuali vendor best-practice.
  Regole di compilazione:
    1. QUI servono i dettagli puntuali: IP, porte, VLAN ID, LUN, ACL, parametri config.
    2. Ogni tabella deve essere completa e coerente con le sezioni precedenti.
    3. Gli ID VLAN/SUBNET devono essere univoci e tracciati anche nel As-Built post-rilascio.
    4. Indicare sempre il riferimento alla porta fisica dell'apparato (es. SW01-Gi1/0/24).
    5. Per ogni policy firewall indicare: sorgente, destinazione, porta, azione, log.
    6. NON inserire password in chiaro: usare riferimento al password vault (es. "riferimento in vault://...").
    7. In `depends_on` inserire l'id dell'HLD da cui deriva.
    8. Validare la checklist in fondo prima di `status: in-review`.
-->

# LLD — Low-Level Design

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

## 1. Introduzione e Riferimenti

**Scopo del documento:** definire il blueprint esecutivo di installazione e configurazione. Ogni tabella e parametro qui riportato deve essere considerato **vincolante** per la fase di implementazione (salvo variazioni formalmente approvate e tracciate nel As-Built).

**Documenti di riferimento:**
- Requisiti: [[01-RSD-URS]]
- Architettura macro: [[02-HLD]]
- Piano operativo: [[04-MOP]]

## 2. Piani di Indirizzamento IP e Subnetting

### 2.1 Schema di Subnetting

| Subnet | CIDR | VLAN ID | Zona | Gateway | DHCP | Utilizzo |
|--------|------|---------|------|---------|------|----------|
| 10.10.10.0 | /24 | 10 | DMZ | 10.10.10.1 | no | Servizi esposti |
| 10.10.20.0 | /24 | 20 | PROD | 10.10.20.1 | no | VM applicative |
| 10.10.30.0 | /24 | 30 | PROD | 10.10.30.1 | no | Database tier |
| 10.10.50.0 | /24 | 50 | MGMT | 10.10.50.1 | no | Management apparati |
| 10.10.70.0 | /24 | 70 | STORAGE | 10.10.70.1 | no | Traffico iSCSI |
| 10.10.80.0 | /24 | 80 | BACKUP | 10.10.80.1 | no | Traffico backup |

### 2.2 Mappatura VLAN → Zona → Trust

| VLAN ID | Nome | Zona | Trust level | Routing inter-VLAN |
|---------|------|------|-------------|---------------------|
| 10 | VLAN-DMZ | DMZ | Low | via firewall |
| 20 | VLAN-PROD-APP | PROD | Medium | via core L3 |
| 30 | VLAN-PROD-DB | PROD | Medium (isolata) | via firewall |
| 50 | VLAN-MGMT | MGMT | Restricted | via firewall + jump host |
| 70 | VLAN-STORAGE | STORAGE | Restricted | no routing (L2 only) |
| 80 | VLAN-BACKUP | BACKUP | Restricted | via firewall |

### 2.3 Allocazione IP degli Host Fissi

| Hostname | IP | MAC | VLAN | Ruolo | Note |
|----------|-----|-----|------|-------|------|
| fw-01 | 10.10.10.2 | `<AA:BB:CC:DD:EE:01>` | 10 | Firewall primary | Active node |
| fw-02 | 10.10.10.3 | `<AA:BB:CC:DD:EE:02>` | 10 | Firewall secondary | Standby |
| sw-core-01 | 10.10.50.11 | `<...>` | 50 | Core switch 1 | Management IP |
| sw-core-02 | 10.10.50.12 | `<...>` | 50 | Core switch 2 | Management IP |
| stor-01-a | 10.10.70.10 | `<...>` | 70 | Controller A | iSCSI target |
| stor-01-b | 10.10.70.11 | `<...>` | 70 | Controller B | iSCSI target |

## 3. Rack Elevation

### 3.1 Layout Rack R01 (Compute)

```
Rack: R01 — Server Rack 42U
Locale: Sala Server 1 — Datacenter <site>

U  | Componente                 | Note
---|----------------------------|------------------------------
42 | [PDU 01]                   | PDU gestito, 2x 16A
41 | [Switch ToR R01]           | sw-tor-01, 48p 10GbE
40 | [Switch ToR R01]           | sw-tor-01 (secondaria)
39 | ------------------------- | cablaggio spare
38 | [Server SRV-01]            | hypervisor node 1
37 | [Server SRV-01]            | ...
36 | [Server SRV-02]            | hypervisor node 2
35 | [Server SRV-02]            | ...
34 | [Server SRV-03]            | hypervisor node 3
33 | [Server SRV-03]            | ...
...
 4 | [KVM / Console]            | IP KVM
 3 | [UPS 01]                   | UPS 10kVA
 2 | [UPS 01]                   | ...
 1 | [PDU 02]                   | PDU gestito, 2x 16A
```

### 3.2 Layout Rack R02 (Storage + Network)

<!-- Analogamente a R01, includere rack elevation testuale con unità 1-42. -->

```
Rack: R02 — Storage & Network Rack 42U
Locale: Sala Server 1 — Datacenter <site>

U  | Componente                 | Note
---|----------------------------|------------------------------
42 | [PDU 03]                   | PDU gestito, 2x 16A
41 | [Switch ToR R02]           | sw-tor-02
40 | [Switch ToR R02]           | sw-tor-02 (secondaria)
39 | ------------------------- | cablaggio spare
38 | [Storage Controller A]     | stor-01-a
37 | [Storage Controller A]      | ...
36 | [Storage Controller B]     | stor-01-b
35 | [Storage Controller B]      | ...
...
 4 | [Backup Appliance]         | bkp-01
 3 | [UPS 02]                   | UPS 10kVA
 2 | [UPS 02]                   | ...
 1 | [PDU 04]                   | PDU gestito, 2x 16A
```

## 4. Mappatura Porte Fisiche (Cable Matrix)

### 4.1 Switch Core sw-core-01

| Porta | Tipo | Dispositivo collegato | Porta remota | VLAN | Tagging | Note |
|-------|------|----------------------|--------------|------|---------|------|
| Gi1/0/1 | 10GbE SR | sw-core-02 | Gi1/0/1 | trunk | 802.1Q | Inter-switch link (MLAG peer) |
| Gi1/0/2 | 10GbE SR | sw-tor-01 | Gi1/0/47 | trunk | 802.1Q | Uplink ToR R01 |
| Gi1/0/3 | 10GbE SR | sw-tor-02 | Gi1/0/47 | trunk | 802.1Q | Uplink ToR R02 |
| Gi1/0/10 | 10GbE SR | fw-01 | port1 | access VLAN 10 | — | DMZ |
| Gi1/0/11 | 10GbE SR | fw-02 | port1 | access VLAN 10 | — | DMZ (standby) |
| Gi1/0/20 | 1GbE Cu | stor-01-a | mgmt0 | access VLAN 50 | — | Management storage |
| Gi1/0/24 | 1GbE Cu | KVM-IP | eth0 | access VLAN 50 | — | KVM console |

### 4.2 Switch ToR sw-tor-01 (Rack R01)

| Porta | Dispositivo | Porta remota | VLAN | Note |
|-------|-------------|--------------|------|------|
| Gi1/0/1 | sw-core-01 | Gi1/0/2 | trunk | uplink primario |
| Gi1/0/2 | sw-core-02 | Gi1/0/2 | trunk | uplink secondario (MLAG) |
| Gi1/0/10 | SRV-01 NIC1 | iLO | access 50 | Management |
| Gi1/0/11 | SRV-01 NIC2 | eth0 | trunk | Data (multi-VLAN) |
| Gi1/0/12 | SRV-01 NIC3 | eth1 | trunk | Data (multi-VLAN) |
| Gi1/0/20 | SRV-02 NIC1 | iLO | access 50 | Management |
| Gi1/0/21 | SRV-02 NIC2 | eth0 | trunk | Data |

### 4.3 Patch Panel Matrix

| Patch Panel | Porta | Switch Porta | destinazione finale | Tipo cavo | Certificazione |
|-------------|-------|--------------|----------------------|-----------|----------------|
| PP01 (R01) | 01 | sw-tor-01 Gi1/0/10 | SRV-01 iLO | Cat6A UTP | ≤ 50m, Fluke cert. |
| PP01 (R01) | 02 | sw-tor-01 Gi1/0/11 | SRV-01 eth0 | Cat6A UTP | ≤ 50m, Fluke cert. |
| PP02 (R02) | 01 | sw-tor-02 Gi1/0/20 | stor-01-a mgmt | Cat6A UTP | ≤ 30m, Fluke cert. |

## 5. Configurazione Storage

### 5.1 Layout Fisico Storage

| Storage Array | Modello | N. dischi | Tipo disco | Capacità raw | Capacità usable |
|---------------|---------|-----------|------------|--------------|----------------|
| stor-01 | `<vendor/model>` | 24 | SSD NVMe 1.92TB | 46 TB | ~30 TB (RAID6) |
| stor-01 | `<vendor/model>` | 12 | NL-SAS 8TB | 96 TB | ~64 TB (RAID6) |

### 5.2 Pool e RAID

| Pool | Dischi | RAID | Capacità usable | Dedupe/Compressione | Destinazione |
|------|--------|------|-----------------|--------------------|--------------|
| Pool-Tier1 (SSD) | 24 SSD | RAID6 (8+2)x2 | 30 TB | On (inline) | VM mission-critical |
| Pool-Tier2 (NL-SAS) | 12 NL-SAS | RAID6 (10+2) | 64 TB | On (post-process) | File server, backup locale |

### 5.3 LUN e Volume Mapping

| LUN/Vol ID | Nome | Pool | Protocollo | Dimensione | Initiator/i | LUN ID | QoS |
|-----------|------|------|-----------|------------|-------------|--------|-----|
| LUN-001 | esxi-datastore-01 | Pool-Tier1 | iSCSI | 5 TB | SRV-01,02,03 IQN | 0 | high |
| LUN-002 | esxi-datastore-02 | Pool-Tier1 | iSCSI | 5 TB | SRV-01,02,03 IQN | 1 | high |
| VOL-010 | nfs-share-app | Pool-Tier2 | NFS | 10 TB | SRV-01,02,03 | n/a | medium |
| VOL-020 | smb-share-file | Pool-Tier2 | SMB3 | 20 TB | server file | n/a | medium |

### 5.4 Repliche e Snapshot

| Source | Target | Tipo | Frequenza | Retention | RPO target |
|--------|--------|------|-----------|-----------|------------|
| stor-01 Pool-Tier1 | stor-dr Pool-Tier1 | Async replication | ogni 15 min | 24 snapshot | ≤ 15 min |
| stor-01 Pool-Tier2 | stor-dr Pool-Tier2 | Async replication | ogni 1h | 7 giorni | ≤ 1h |
| Pool-Tier1 | snapshot locale | Snapshot | ogni 1h | 24 ore | ≤ 1h |

## 6. Configurazione Routing

### 6.1 Protocolli di Routing Dinamico

| Protocollo | ASN / Area | Router partecipanti | Scopo |
|-----------|-----------|----------------------|-------|
| OSPF | Area 0.0.0.0 | fw-01, fw-02, sw-core-01, sw-core-02 | Routing interno DC |
| BGP | ASN `<65500>` | fw-01 ↔ ISP-A, fw-02 ↔ ISP-B | Multihoming Internet |

### 6.2 Route Statiche

| Destinazione | Next-hop | Metrica | Note |
|--------------|----------|---------|------|
| 0.0.0.0/0 | fw-01 (10.10.10.2) | 10 | Default gateway (via OSPF) |
| 192.168.0.0/16 | VPN tunnel a sito remoto | 5 | Sedi remote via SD-WAN |
| 172.16.0.0/12 | tunnel IPsec a sito DR | 5 | DR via WAN dedicata |

### 6.3 NAT

| Regola | Origine | Traduzione | Direzione | Note |
|--------|---------|------------|-----------|------|
| NAT-001 | 10.10.20.0/24 | `<public IP>` | outbound | NAT overload per uscita Internet PROD |
| NAT-002 | `<public IP>:443` | 10.10.10.5:443 | inbound | Port-forward verso reverse proxy DMZ |

## 7. Matrice delle Policy Firewall (ACL)

### 7.1 Policy East-West (Inter-Zone)

| ID | Sorgente | Destinazione | Servizio/Porta | Azione | Log | Note |
|----|----------|---------------|----------------|--------|-----|------|
| EW-001 | VLAN-PROD-APP (10.10.20.0/24) | VLAN-PROD-DB (10.10.30.0/24) | TCP/5432, TCP/3306 | allow | yes | App → DB |
| EW-002 | VLAN-PROD-DB | qualsiasi | qualsiasi | deny | yes | DB isolato, no outbound |
| EW-003 | VLAN-MGMT (10.10.50.0/24) | qualsiasi | TCP/22, TCP/443, ICMP | allow | yes | Management access |
| EW-004 | VLAN-PROD-APP | VLAN-MGMT | qualsiasi | deny | yes | No management da PROD |
| EW-005 | qualsiasi | VLAN-STORAGE | qualsiasi | deny | yes | Storage L2-only |

### 7.2 Policy North-South (Internet ↔ DC)

| ID | Sorgente | Destinazione | Servizio | Azione | Log | Note |
|----|----------|--------------|---------|--------|-----|------|
| NS-001 | qualsiasi (Internet) | `<public VIP>:443` | TCP/443 | allow | yes | HTTPS inbound |
| NS-002 | qualsiasi (Internet) | qualsiasi | qualsiasi | deny | yes | Deny-all default |
| NS-003 | VLAN-PROD-APP | 0.0.0.0/0 | TCP/443, TCP/53, UDP/53 | allow | yes | Outbound HTTPS+DNS |
| NS-004 | VLAN-PROD-APP | 0.0.0.0/0 | qualsiasi | deny | yes | No altro outbound da PROD |

### 7.3 VPN e Tunnel

| Tunnel ID | Tipo | Endpoint locale | Endpoint remoto | Auth | Crypto | Subnet interessate |
|-----------|------|----------------|------------------|------|--------|---------------------|
| VPN-001 | IPsec site-to-site | fw-01 public IP | `<sito DR public IP>` | PSK (in vault) | AES256-GCM, DH14 | 10.10.0.0/16 ↔ 10.20.0.0/16 |
| VPN-002 | SSL VPN (remote access) | fw-01 | client admin | Cert + MFA | TLS 1.3 | Solo subnet MGMT accessibile |

## 8. Configurazione Servizi Base

### 8.1 Active Directory / LDAP

| Componente | Hostname | IP | Ruolo | Forest/Domain | Note |
|-----------|----------|-----|-------|---------------|------|
| dc-01 | dc-01.<domain> | 10.10.50.20 | Primary DC | `<domain.local>` | FSMO roles |
| dc-02 | dc-02.<domain> | 10.10.50.21 | Secondary DC | `<domain.local>` | replica |

**Struttura OU proposta:**
- `<domain.local>`
  - `OU=Infrastruttura` (server, hypervisor, storage)
  - `OU=Servizi` (account di servizio)
  - `OU=Utenti` (utenti aziendali)
  - `OU=Gruppi` (gruppi RBAC)

### 8.2 DNS

| Zona | Tipo | Server | Record chiave |
|------|------|--------|--------------|
| `<domain.local>` | Forward | dc-01, dc-02 | A, SRV (AD), CNAME |
| `10.10.in-addr.arpa` | Reverse | dc-01, dc-02 | PTR per host fissi |
| Forwarder esterno | Forward | 8.8.8.8, 1.1.1.1 | Risoluzione Internet |

### 8.3 DHCP

| Scope | Range | Mask | Gateway | DNS | Lease | Esclusioni |
|-------|-------|------|---------|-----|-------|-----------|
| VLAN 20 PROD | 10.10.20.50-200 | /24 | 10.10.20.1 | 10.10.50.20,21 | 8h | 10.10.20.1-49 (fissi) |
| VLAN 50 MGMT | 10.10.50.100-200 | /24 | 10.10.50.1 | 10.10.50.20,21 | 8h | 10.10.50.1-99 (fissi) |

### 8.4 NTP

| Server | IP | Stratrum | Note |
|--------|-----|----------|------|
| ntp-01 | 10.10.50.30 | 2 | Sync verso pool.ntp.org |
| ntp-02 | 10.10.50.31 | 2 | Sync verso pool.ntp.org |
| Tutti gli apparati | ntp-01, ntp-02 | — | Sync obbligatorio verso i server NTP interni |

## 9. Configurazione Virtualizzazione (Hypervisor)

### 9.1 Cluster Hypervisor

| Cluster | Nodi | Hypervisor | vSwitch | DRS | HA |
|---------|------|------------|---------|-----|-----|
| CL-PROD-01 | SRV-01, SRV-02, SRV-03 | `<VMware ESXi 8.0 U2>` | vDS `<nome>` | enabled (fully automated) | enabled (host failure monitoring) |

### 9.2 Port Group vSwitch

| Port Group | VLAN | Tipo | Uso |
|-----------|------|------|-----|
| PG-MGMT | 50 | access | Management hypervisor |
| PG-PROD-APP | 20 | access | VM traffic PROD app |
| PG-PROD-DB | 30 | access | VM traffic PROD DB |
| PG-STORAGE-iSCSI | 70 | access | iSCSI traffic |
| PG-BACKUP | 80 | access | Backup traffic |

### 9.3 Provisioning VM — Template

| Template | vCPU | RAM | Disk | OS | Note |
|----------|------|-----|------|----|------|
| TPL-WIN-2022-STD | 2 | 8 GB | 60 GB thin | Windows Server 2022 | Joined to domain, patchato |
| TPL-DEB-12 | 2 | 4 GB | 30 GB thin | Debian 12 minimal | cloud-init ready |

## 10. Configurazione Backup

| Host/VM | Job | Software | Schedule | Target locale | Target remoto | Retention |
|---------|-----|----------|----------|---------------|---------------|-----------|
| Tutte VM PROD | Job-VM-PROD | `<Veeam>` | 22:00 daily | bkp-01 (Dedup) | cloud + DR | 30 gg locali, 365 cloud |
| File server | Job-FILE | `<Veeam>` | 02:00 daily | bkp-01 | cloud | 90 gg |
| Storage snapshot | Auto (storage) | stor-01 fw | ogni 1h | stor-01 | stor-dr | 24 snapshot |

## 11. Configurazione Monitoring e Logging

| Componente | Tool | Endpoint raccolta | Frequenza | Allarmi |
|-----------|------|---------------------|-----------|---------|
| Network | `<Zabbix/PRTG/Nagios>` | `<server>` | 60s polling | CPU, link, errori |
| Hypervisor | `<vROps/...>` | `<server>` | 60s | HA events, capacity |
| Storage | `<vendor tool>` | `<server>` | 60s | IOPS, latency, capacity |
| Syslog | `<rsyslog/Splunk/...>` | `<server>` | real-time | Auth, security, config change |

## 12. Riferimenti e Documenti Correlati

- Requisiti: [[01-RSD-URS]]
- Architettura macro: [[02-HLD]]
- Piano operativo: [[04-MOP]]
- As-Built (post-realizzazione): [[06-As-Built]]

## Appendice A — Snippet di Configurazione

<!-- Inserire snippet di config puntuali per apparati critici. NON includere secret. -->

### Switch core — baseline config (estratto)

```
! sw-core-01 baseline
hostname sw-core-01
!
vlan 10
 name VLAN-DMZ
vlan 20
 name VLAN-PROD-APP
vlan 30
 name VLAN-PROD-DB
vlan 50
 name VLAN-MGMT
vlan 70
 name VLAN-STORAGE
vlan 80
 name VLAN-BACKUP
!
interface Gi1/0/1
 description [MLAG-peer] sw-core-02 Gi1/0/1
 switchport mode trunk
 switchport trunk allowed vlan 10,20,30,50,70,80
 channel-group 1 mode active
!
! ... (continua)
```

### Firewall — baseline policy (estratto)

```
! fw-01 baseline (vendor-agnostic pseudocode)
policy {
  rule EW-001 {
    from VLAN-PROD-APP to VLAN-PROD-DB
    service [tcp-5432 tcp-3306]
    action allow
    log enable
  }
  rule NS-002 {
    from any to any
    action deny
    log enable
  }
}
```

## Appendice B — Acronimi

| Acronimo | Espansione |
|----------|------------|
| MLAG | Multi-Chassis Link Aggregation |
| LUN | Logical Unit Number |
| ACl | Access Control List |
| ToR | Top of Rack |
| OU | Organizational Unit |
| vDS | vSphere Distributed Switch |

---

## Checklist di Validazione

- [ ] Tabelle IP/VLAN complete e coerenti
- [ ] Rack elevation per ogni rack popolato
- [ ] Cable matrix con ogni porta fisica mappata
- [ ] Storage: pool, LUN, replica documentati
- [ ] Firewall: policy east-west e north-south con ID univoci
- [ ] Servizi base (AD, DNS, DHCP, NTP) con IP e ruoli specificati
- [ ] Hypervisor: cluster, vSwitch, port group, template VM
- [ ] Backup: job, schedule, retention, target
- [ ] Nessun secret in chiaro (riferimenti a vault)
- [ ] `depends_on` contiene HLD
- [ ] `related_docs` include RSD, HLD, MOP e As-Built (placeholder)
