---
okf_version: "0.2"
id: "specification-severino-srl-rsd-01"
title: "RSD/URS — Requisiti Infrastruttura LAN, Virtualizzazione Hyper-V e Collaboration Severino Srl"
type: "specification"
domain: "IT Infrastructure & Requirements Engineering"
tags: ["okf-v0.2", "rsd", "urs", "requirements", "assessment", "severino-srl", "hyper-v", "mikrotik"]

# Metadati estesi IT
project_id: "severino-srl"
project_name: "Infrastruttura LAN, Virtualizzazione Hyper-V e Collaboration Severino Srl"
site: "HQ-SEV"
customer: "Severino Srl"
phase: 1
author: "Marco Severino"
reviewer: "AI Systems Architect"
approver: "Marco Severino"
owner_team: "IT Operations Severino Srl"
status: "in-review"
version: "1.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-severino-srl-hld-01"
  - "guide-severino-srl-mop-01"
depends_on: []
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Infrastruttura Severino Srl"
    type: "concept"
    description: "Infrastruttura IT on-premise comprensiva di rete LAN/WLAN, server Hyper-V, file sharing e sala riunioni"
  - name: "Hyper-V Virtualization Platform"
    type: "technology"
    description: "Ambiente di virtualizzazione Windows Server 2022 Datacenter ospitato su workstation HP Z4"
  - name: "MikroTik CRS326 Core Switch & Firewall"
    type: "toolchain"
    description: "Apparato centrale per routing inter-VLAN, policy di firewalling perimetrale e commutazione LAN"
  - name: "ZeroTier Secure SD-WAN"
    type: "technology"
    description: "Rete virtuale crittografata per consentire l'accesso sicuro alle share SMB da postazioni remote"
  - name: "Backup Strategy & RustCopy"
    type: "pattern"
    description: "Strategia di replica dati verso NAS QNAP TS-233 tramite Cobian Reflector con migrazione a RustCopy"

relations:
  - targetTitle: "HLD — High-Level Design Severino Srl"
    targetId: "architecture-severino-srl-hld-01"
    relationType: "depends_on"
    weight: 1.0
    description: "L'HLD traduce i requisiti del RSD/URS in architettura di rete, virtualizzazione e storage"
  - targetTitle: "MOP — Method of Procedure Implementazione"
    targetId: "guide-severino-srl-mop-01"
    relationType: "references"
    weight: 0.85
    description: "Il MOP coordina la sequenza operativa di deploy fisico, configurazione switch e VM"
---

<!-- AI-INSTRUCTIONS:
  Questo documento definisce i requisiti di business, utente e sistema per l'infrastruttura di Severino Srl.
  Tutti i requisiti sono tracciati con ID univoci (RF-xxx, RNF-xxx, OB-xxx).
-->

# RSD/URS — Requisiti di Sistema e Utente: Severino Srl

## 1. Contesto e Obiettivi di Business

### 1.1 Contesto Generale
**Severino Srl** necessita di un'infrastruttura IT locale moderna, affidabile, sicura e scalabile per supportare le attività operative aziendali quotidiane, la gestione documentale interna e la condivisione protetta di dati per due aziende partner curate esternamente. 
Il sistema integra postazioni client desktop fisse, dispositivi portatili/mobile via Wi-Fi enterprise, un host di virtualizzazione centralizzato su base Windows Server 2022 Datacenter, accesso remoto sicuro e una sala conferenze multimediale avanzata per riunioni Microsoft Teams.

### 1.2 Obiettivi di Business (OB)
- [x] **OB-001:** Centralizzare l'autenticazione, la sicurezza degli accessi e la gestione delle postazioni di lavoro tramite dominio Active Directory `severino.local`.
- [x] **OB-002:** Fornire storage ad alte prestazioni e ridondato per lo share documentale interno (2 TB) e per le 2 aziende partner (512 GB).
- [x] **OB-003:** Consentire l'accesso remoto sicuro alle condivisioni SMB per utenti smart-working tramite rete ZeroTier senza esporre porte SMB direttamente su Internet.
- [x] **OB-004:** Garantire la continuità operativa e il ripristino dei dati aziendali tramite backup giornalieri automatici su storage isolato (NAS QNAP TS-233).
- [x] **OB-005:** Dotare la sede di una sala videoconferenza immersiva e professionale per Microsoft Teams (TV 65" + Logitech Rally Bar + Tablet touch controller).

---

## 2. Stakeholder e Ruoli

| Ruolo | Nome | Organizzazione | Contatto | Responsabilità |
|-------|------|----------------|----------|----------------|
| Project Sponsor & Lead Architect | Marco Severino | Severino Srl | `vault://it/projects/severino-srl/contacts/marco` | Approvazione requisiti, budget e architettura |
| IT Operations & Systems | Team IT Severino | Severino Srl | `vault://it/projects/severino-srl/contacts/it-team` | Installazione, manutenzione ordinaria e backup |
| Security & Compliance Officer | Marco Severino | Severino Srl | `vault://it/projects/severino-srl/contacts/marco` | Controllo conformità GDPR e policy accessi |

---

## 3. Requisiti Funzionali

| ID | Descrizione | Priorità | Fonte / Riferimento | Note |
|----|-------------|----------|---------------------|------|
| **RF-001** | **Dominio Active Directory centralizzato:** Creazione del dominio AD `severino.local` su VM dedicata `dc01` con ruoli DNS, DHCP e gestione utenti/GPO. | Must | Requisiti Marco Severino | Gestione centralizzata policy Windows 11 |
| **RF-002** | **Client Desktop HP G6 a Dominio:** Ogni postazione client fissa (MiniPC HP G6, Core i5, 8GB RAM, 512GB NVMe, Windows 11 Pro) deve essere joinata al dominio con credenziali utente dedicate. | Must | Parco Macchine Client | Connessione cablata Gigabit LAN |
| **RF-003** | **Core Switching & Routing:** Lo switch MikroTik CRS326-24G-2S+RM deve gestire la commutazione Gigabit LAN, il routing inter-VLAN e fungere da primo firewall perimetrale a valle della Vodafone Station. | Must | Specifiche Rete | Connessione uplink verso Vodafone Station |
| **RF-004** | **Wi-Fi Enterprise UniFi:** Gli Access Point Ubiquiti UniFi devono diffondere SSID protetti (WPA2/WPA3 Enterprise o WPA3 Personal) per notebook e smartphone, con rete Guest segregata. | Must | Connettività Wireless | Segregazione su VLAN dedicata |
| **RF-005** | **File Server Principale (`fs01`):** Macchina virtuale Windows Server 2022 con disco dedicato da 2 TB allocato per le cartelle condivise SMB aziendali di Severino Srl. | Must | Storage Documentale | Permessi ACL basati su gruppi AD |
| **RF-006** | **File Server Aziende Esterne (`fs02`):** Macchina virtuale Windows Server 2022 che monta uno storage esterno SSK da 512 GB come base dati per cartelle SMB dedicate a 2 aziende curate. | Must | Multi-tenant Partner | Isolamento cartelle per azienda |
| **RF-007** | **Connettività Remota ZeroTier:** Sia `fs01` che `fs02` devono essere collegati alla rete virtuale ZeroTier per consentire agli utenti autorizzati in mobilità di mappare le share SMB in sicurezza. | Must | Accesso Remoto | Traffico crittografato end-to-end |
| **RF-008** | **Backup Giornaliero su QNAP TS-233:** Backup automatico programmato ogni notte di tutte le share e database da `fs01` e `fs02` verso il NAS QNAP TS-233 tramite Cobian Reflector. | Must | Strategia Continuità | Destinazione storage locale isolata |
| **RF-009** | **Roadmap Tool RustCopy:** Predisposizione dell'ambiente per migrare la pipeline di sincronizzazione/backup da Cobian Reflector a **RustCopy v7.4.1+** appena validato come stabile. | Should | Roadmap Software Proprietario | Maggiore efficienza, velocità e logging |
| **RF-010** | **Sala Riunioni Microsoft Teams:** Allestimento sala meeting con TV 65 pollici, apparato Logitech Rally Bar e tablet touch controller per gestione riunioni Teams Room. | Must | Collaboration Suite | Esperienza one-touch-join |

---

## 4. Requisiti Non Funzionali

### 4.1 Performance
- **Throughput LAN Cablata:** Velocità 1 Gbps non bloccante su tutte le porte client HP G6 e link 10G SFP+ di uplink se previsti.
- **Throughput Wi-Fi:** Copertura Wi-Fi 6 / 802.11ac dual-band con roaming trasparente per notebook e smartphone.
- **I/O Storage VM:** I/O ad alta velocità per il sistema operativo delle VM grazie agli NVMe dell'host HP Z4; accesso dati a banda piena Gigabit per lo storage 2 TB e il disco SSK 512 GB.

### 4.2 Disponibilità e Affidabilità
- **Host di Virtualizzazione:** Workstation HP Z4 con Windows Server 2022 Datacenter Edition e Hyper-V per garantire isolamento rigido tra `dc01`, `fs01` e `fs02`.
- **Continuità Operativa:** Gruppo di continuità UPS per proteggere l'host HP Z4, il MikroTik CRS326, la Vodafone Station e il NAS QNAP TS-233 da cali di tensione o blackout.

### 4.3 Scalabilità
- Possibilità di aggiungere nuovi MiniPC HP G6 o laptop senza dover riconfigurare la topologia di base.
- Espandibilità dello storage VHDX su `fs01` e possibilità di upgrade dello storage QNAP TS-233.

### 4.4 Sicurezza
- **Nessuna password in chiaro:** Tutte le credenziali amministrative (MikroTik RouterOS, Windows Server local admin, dominio AD, QNAP admin, ZeroTier network token) devono risiedere nel password manager aziendale con URI `vault://it/projects/severino-srl/...`.
- **Segregazione Reti:** Separazione logica tramite VLAN gestite dal MikroTik CRS326:
  - VLAN 10: Management (Host HP Z4, Switch MikroTik, AP UniFi, QNAP)
  - VLAN 20: Server & VM (`dc01`, `fs01`, `fs02`)
  - VLAN 30: Client Cablati (MiniPC HP G6)
  - VLAN 40: Wi-Fi Aziendale (Notebook, Smartphone aziendali)
  - VLAN 50: Collaboration & Meeting (TV 65", Logitech Rally Bar, Tablet Teams)
  - VLAN 90: Wi-Fi Ospiti (Internet-only isolata)

---

## 5. Requisiti di Continuità Operativa e Backup

| Sorgente Dati | Dimensione | Frequenza | Retention | Software Attuale | Software Target | Destinazione |
|---|---|---|---|---|---|---|
| **fs01 (Severino Srl)** | ~2 TB | Giornaliera (ore 22:00) | 30 giorni versionati | Cobian Reflector | RustCopy v7.4.1+ | QNAP TS-233 (Share Backup) |
| **fs02 (Aziende Partner)** | ~512 GB (SSK) | Giornaliera (ore 23:00) | 60 giorni versionati | Cobian Reflector | RustCopy v7.4.1+ | QNAP TS-233 (Share Partner) |
| **dc01 (System State AD)** | ~50 GB | Giornaliera (ore 01:00) | 14 giorni | Windows Backup | RustCopy v7.4.1+ | QNAP TS-233 |

**Obiettivi di Servizio (SLA):**
- **RTO (Recovery Time Objective):** ≤ 4 ore per ripristino share file server; ≤ 2 ore per ripristino controller di dominio.
- **RPO (Recovery Point Objective):** ≤ 24 ore (massima perdita tollerata: lavoro della giornata precedente).

---

## 6. Vincoli di Compliance e Normativi

- [x] **GDPR (Regolamento UE 2016/679):**
  - Trattamento dati aziendali e dati di terzi (aziende partner) segregati con permessi NTFS rigorosi.
  - Cifratura del traffico remoto tramite ZeroTier.
  - Registro accessi abilitato sul Domain Controller e sui File Server.
- [x] **NIS2 (Direttiva UE 2022/2555):**
  - Misure di sicurezza proporzionate per la resilienza informatica delle PMI e dei fornitori di servizi.
  - Protezione degli accessi privilegiati (PAM) per le postazioni server.
- [x] **Standard di Naming & Vault:**
  - Standardizzazione nomi host: `HP-Z4-HOST`, `VM-DC01`, `VM-FS01`, `VM-FS02`, `SW-CORE-01`, `NAS-QNAP-01`.
  - Credenziali gestite rigorosamente tramite riferimenti `vault://`.

---

## 7. Capacità Stimate e Dimensionamento Hardware

### 7.1 Compute (Host Fisico)
- **Workstation:** HP Z4 Workstation
- **Processore:** Intel Xeon / Core High-Performance
- **RAM:** Configurazione adeguata per host + 3 VM (minimo 32 GB / 64 GB raccomandati)
- **Storage Host:** SSD NVMe per SO host e dischi di avvio VM

### 7.2 Storage Dati
- **Volume Dati `fs01`:** 2 TB VHDX dedicato per archivio e documenti Severino Srl.
- **Storage Esterno `fs02`:** SSD Esterno SSK da 512 GB collegato in pass-through o montato su host per le cartelle delle 2 aziende partner.
- **Storage Backup QNAP TS-233:** 2-Bay NAS con dischi in mirroring RAID 1 (es. 2x 4TB o 2x 6TB) per accogliere retention Cobian Reflector / RustCopy.

### 7.3 Parco Client
- **MiniPC Fissi:** HP ProDesk/EliteDesk G6 con 8 GB RAM, 512 GB SSD NVMe, Windows 11 Pro a dominio.
- **Dispositivi Mobili:** Laptop e smartphone collegati tramite WPA3 su Access Point UniFi.

### 7.4 Collaboration & Meeting
- TV 65 pollici 4K HDR
- Logitech Rally Bar (videocamera motorizzata PTZ, altoparlanti e microfoni array)
- Tablet touch controller (Logitech Tap / IP) per gestione riunioni Microsoft Teams Room.

---

## 8. Dipendenze e Vincoli di Progetto

- **Fornitura Connettività:** Vodafone Station deve essere configurata con DMZ verso il MikroTik CRS326 oppure in modalità modem/bridge per evitare doppio NAT se necessario.
- **Licenziamento:** Windows Server 2022 Datacenter con CAL utente per dominio `severino.local`; licenze Windows 11 Pro OEM/Retail già presenti sui client HP G6; licenza Microsoft Teams Rooms per la sala riunioni.
- **ZeroTier Network ID:** Network ID privato gestito centralmente con autorizzazione esplicita dei nodi `fs01`, `fs02` e dei client remoti.

---

## 9. Checklist di Validazione Finale

- [x] Tutti i requisiti di business e tecnici sono stati definiti con Marco Severino.
- [x] RTO/RPO concordati (RTO ≤ 4h, RPO ≤ 24h).
- [x] Coerenza tra `related_docs` e `relations` OKF verificata.
- [x] Nessuna credenziale in chiaro presente nel documento (`vault://` utilizzato).
- [x] Parametri allineati con `project-manifest.yaml`.
- [x] Strategia di backup definita (QNAP TS-233, Cobian Reflector, roadmap RustCopy).
- [x] Specifiche sala videoconferenza Microsoft Teams incluse.
