---
okf_version: "0.2"
id: "guide-itinfra-global-memory-01"
title: "Global Enterprise Staging Memory & Architectural Best Practices — ITInfra"
type: "guide"
domain: "IT Infrastructure Knowledge Engineering"
tags: ["okf-v0.2", "memory", "global-scratchpad", "best-practices", "known-issues"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Enterprise Memory Pool"
phase: 0
author: "Enterprise Solutions Architect"
reviewer: "System Architecture Board"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture"
status: "in-review"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "guide-memoria-ibrida-trust-signals-v02"
depends_on: []
classification: "internal"
retention: "permanent"
lang: "it"

entities:
  - name: "Global Enterprise Staging Memory"
    type: "framework"
    description: "Pool di memoria di secondo livello condivisa per best practice, pattern e lezioni apprese"
  - name: "ZeroTier Overlay Best Practice"
    type: "technology"
    description: "Impostazione di MTU 1400 e TCP MSS Clamping per evitare frammentazione su tunnel VPN"
  - name: "MikroTik CRS326 Port Isolation"
    type: "technology"
    description: "Policy di isolamento porte e HW offloading per switch di accesso e distribuzione"
  - name: "Dell PowerEdge R630 Firmware Baseline"
    type: "technology"
    description: "Requisiti minimi di BIOS 2.9.0 e iDRAC 2.80+ per stabilità schede 10GbE"

relations:
  - targetTitle: "Indice Generale della Documentazione"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Hub documentale master ITInfra"
  - targetTitle: "Guida Operativa Memoria Ibrida a 3 Livelli"
    targetId: "guide-memoria-ibrida-trust-signals-v02"
    relationType: "extends"
    weight: 0.95
    description: "Estende la memoria ibrida a livello globale enterprise"
---

# ITInfra Global Enterprise Memory Scratchpad
<!-- Staging Memory Globale (Livello 2 Enterprise). 100% File-Based & Git-Native. -->
<!-- Raccoglie best practice architetturali, bug noti di vendor e linee guida trasversali a tutti i clienti. -->
<!-- Policy Zero-Leakage: VIETATO inserire secret, credenziali o IP di produzione specifici di un singolo tenant. -->

## 1. Best Practices & Design Patterns
- [2026-09-16 10:00] [architect] [ZeroTier/VPN] Su tutti i collegamenti overlay Layer 2/Layer 3 ZeroTier verso file server Windows (SMB/DFS), configurare sempre MTU 1400 e abilitare TCP MSS Clamping (change-tcp-mss=yes) sui router di confine per evitare frammentazione e timeout di sessione. <!-- id:mem-bp01zt --> <!-- promoted:LES-NET-001 -->
- [2026-09-16 10:15] [network-eng] [MikroTik/Switching] Negli switch della famiglia MikroTik CRS3xx (es. CRS326), mantenere sempre attivo il flag hardware offloading (hw=yes) sui bridge VLAN e configurare le regole di isolation tramite switch-rule per garantire throughput a wire-speed senza saturare la CPU. <!-- id:mem-bp02mt -->
- [2026-09-16 10:30] [sysadmin] [Hyper-V/Virtualization] I virtual switch dedicati al traffico di produzione e cluster heartbeat devono essere configurati in Switch Embedded Teaming (SET) con algoritmo Dynamic e failover subordinato a LACP lato switch top-of-rack. <!-- id:mem-bp03hv -->

## 2. Known Issues & Hardware Limitations
- [2026-09-16 10:45] [security] [ZeroTier/MSS] I pacchetti SMB con flag DF (Don't Fragment) e payload > 1360 byte vengono silenziati (Black Hole drop) se il router intermedio non invia ICMP Type 3 Code 4 (Fragmentation Needed). Workaround validato in RCA Severino: clamp MSS a 1360 byte. <!-- id:mem-ki01smb -->
- [2026-09-16 11:00] [hardware] [Dell R630/Broadcom] Le schede di rete Broadcom BCM5720/5719 installate su Dell PowerEdge R630 manifestano link flapping casuale sotto Linux/ESXi se il firmware dell'interfaccia non è aggiornato alla release >= 21.60.x. <!-- id:mem-ki02bcm -->

## 3. Hardware & Vendor Guidelines
- [2026-09-16 11:15] [infra-lead] [Dell Server] Tutti i nodi Dell PowerEdge serie R630/R730 ricondizionati o in produzione richiedono BIOS >= 2.9.0 e firmware iDRAC8 Enterprise >= 2.83.83.83 per conformità crittografica TLS 1.2/1.3 e gestione remota via HTML5. <!-- id:mem-hw01dell -->
- [2026-09-16 11:30] [cabling] [Transceiver SFP+] Utilizzare esclusivamente transceiver ottici multimodale 10GBASE-SR codificati compatibili (es. FS.com codifica MikroTik o Dell) ed evitare cavi DAC passivi di lunghezza > 3m tra switch di vendor differenti. <!-- id:mem-hw02sfp -->

## 4. Open Architectural Questions
- [2026-09-16 11:45] [board] Valutare l'adozione di WireGuard kernel-native come alternativa a ZeroTier per tunnel site-to-site punto-punto ad altissimo throughput (>1 Gbps). <!-- id:mem-oa01wg -->
