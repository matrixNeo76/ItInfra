---
okf_version: "0.2"
id: "architecture-unisped-asbuilt-01"
title: "As-Built — Documentazione Tecnica Finale Apparati Unisped AG S.a.s."
type: "architecture"
domain: "IT Infrastructure & Documentation Delivery"
tags: ["okf-v0.2", "as-built", "inventory", "hardware", "unisped"]
project_id: "unisped-ag-sas"
phase: 5
status: "approved"
version: "1.0"
created_at: "2025-08-20"
updated_at: "2026-09-18"
lang: "it"

entities:
  - name: "Hardware Inventory Unisped"
    type: "specification"
    description: "Inventario apparati di rete e server farm installati presso la sede doganale"
relations:
  - targetTitle: "Network IPAM Unisped"
    targetId: "architecture-unisped-ipam-01"
    relationType: "references"
    weight: 1.0
---

# As-Built — Unisped AG S.a.s.

## 1. Inventario Apparati Hardware e Virtual Appliance

| Apparato | Modello | Seriale / IP | Note di Configurazione |
| :--- | :--- | :--- | :--- |
| Core Firewall | Fortinet FortiGate-60F | FGT60FTK21004521 / 192.168.10.1 | FortiOS 7.2 con ispezione NGFW e SSL VPN |
| Server Host | Dell PowerEdge R450 | CN-0R450-70123 / 192.168.10.10 | Xeon Silver 4314, 64 GB RAM, RAID-10 SSD |
| Bastion Host | Linux Debian 12 (VM) | VIRT-SRV-DEB01 / 192.168.10.15 | OpenSSH 9.2p1, autenticazione a chiavi |
| Mail Server | MS Exchange Server 2019 (VM) | VIRT-SRV-EXCH01 / 192.168.10.20 | CU12, Kerberos authentication |
| Web Portal Dogana | Apache Tomcat 9.0 (VM) | VIRT-SRV-TC01 / 192.168.10.25 | Portale dichiarazioni doganali e tracking |
