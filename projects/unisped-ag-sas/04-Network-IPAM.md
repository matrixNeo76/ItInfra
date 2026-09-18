---
okf_version: "0.2"
id: "architecture-unisped-ipam-01"
title: "Network IPAM — Schema Indirizzamento e Allocazione IP Unisped AG S.a.s."
type: "specification"
domain: "Networking & IPAM"
tags: ["okf-v0.2", "ipam", "networking", "subnets", "unisped"]
project_id: "unisped-ag-sas"
phase: 3
status: "approved"
version: "1.0"
created_at: "2025-08-20"
updated_at: "2026-09-18"
lang: "it"

entities:
  - name: "Subnet LAN Primaria Dogana"
    type: "specification"
    description: "Subnet 192.168.10.0/24 per gestione apparati core e server farm"
relations:
  - targetTitle: "As-Built Unisped AG S.a.s."
    targetId: "architecture-unisped-asbuilt-01"
    relationType: "references"
    weight: 1.0
---

# Network IPAM — Unisped AG S.a.s.

## 1. Subnet Censite
- **Subnet Primaria (CIDR)**: `192.168.10.0/24` (Gateway: `192.168.10.1`, Mask: `255.255.255.0`)

## 2. Tabella di Allocazione IP
| IP | Descrizione / Ruolo Apparato | VLAN | MAC / Note |
| :--- | :--- | :---: | :--- |
| `192.168.10.1` | Fortinet FortiGate-60F (Core Firewall & Gateway) | VLAN 10 | 00:09:0F:AA:BB:01 |
| `192.168.10.15` | Bastion Linux Debian (OpenSSH & AD Bridge) | VLAN 10 | 00:50:56:10:15:AA |
| `192.168.10.20` | Microsoft Exchange Server 2019 CU12 | VLAN 10 | 00:50:56:10:20:BB |
| `192.168.10.25` | Apache Tomcat 9.0 Web Portal Dogana | VLAN 10 | 00:50:56:10:25:CC |
