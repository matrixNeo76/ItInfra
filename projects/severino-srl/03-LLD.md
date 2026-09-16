---
okf_version: "0.2"
id: "architecture-severino-srl-lld-01"
title: "LLD — Low-Level Design Esecutivo Rete, Cablaggi, Virtualizzazione e Rack 10U Severino Srl"
type: "architecture"
domain: "IT Infrastructure & Systems Engineering"
tags: ["okf-v0.2", "lld", "architecture", "severino-srl", "mikrotik", "patch-panel", "rack-10u", "hyper-v", "ip-plan"]

# Metadati estesi IT
project_id: "severino-srl"
project_name: "Infrastruttura LAN, Virtualizzazione Hyper-V e Collaboration Severino Srl"
site: "HQ-SEV"
customer: "Severino Srl"
phase: 2
author: "Marco Severino"
reviewer: "AI Systems Architect"
approver: "Marco Severino"
owner_team: "IT Operations Severino Srl"
status: "in-review"
version: "1.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "specification-severino-srl-rsd-01"
  - "architecture-severino-srl-hld-01"
  - "guide-severino-srl-mop-01"
  - "specification-severino-srl-atp-01"
depends_on:
  - "architecture-severino-srl-hld-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Low-Level Design Severino Srl"
    type: "concept"
    description: "Specifiche esecutive di dettaglio per cablaggi, configurazione porte switch MikroTik e rack 10U"
  - name: "MikroTik CRS326 Port Mapping"
    type: "toolchain"
    description: "Configurazione RouterOS con ether1 WAN fuori bridge ed ether2-ether24 in hardware bridge"
  - name: "Patch Panel e Cablaggio Strutturato"
    type: "framework"
    description: "Matrice di interconnessione Cat6 tra porte switch, patch panel 24p e prese a muro LAN"
  - name: "Rack 10U Layout"
    type: "pattern"
    description: "Disposizione fisica ottimizzata dei componenti nell'armadio rack a 10 unità"
  - name: "Piano Indirizzamento IP e Reservation"
    type: "specification"
    description: "Allocazione subnet 192.168.120.0/24 con pool DHCP ed esclusioni statiche per server e apparati"

relations:
  - targetTitle: "RSD/URS — Requisiti di Sistema e Utente Severino Srl"
    targetId: "specification-severino-srl-rsd-01"
    relationType: "references"
    weight: 0.9
    description: "Riferimento ai requisiti funzionali e di continuità"
  - targetTitle: "HLD — High-Level Design Severino Srl"
    targetId: "architecture-severino-srl-hld-01"
    relationType: "implements"
    weight: 1.0
    description: "L'LLD implementa a livello esecutivo l'architettura logica approvata nell'HLD"
  - targetTitle: "MOP — Method of Procedure Implementazione"
    targetId: "guide-severino-srl-mop-01"
    relationType: "depends_on"
    weight: 0.9
    description: "Il MOP conterrà i comandi CLI e la sequenza esecutiva basati su questo LLD"
  - targetTitle: "ATP — Acceptance Test Plan Severino Srl"
    targetId: "specification-severino-srl-atp-01"
    relationType: "documents"
    weight: 0.85
    description: "L'ATP verificherà il corretto funzionamento delle porte e degli IP allocati nell'LLD"
verified: true
verified_by: "Mario Rossi (Tech Lead)"
last_vetted: "2026-09-16"
stale_after: "2026-12-15"
---

# LLD — Low-Level Design Esecutivo: Severino Srl

<!-- AI-INSTRUCTIONS:
  Questo documento definisce in dettaglio esecutivo vincolante la configurazione delle porte
  dello switch MikroTik CRS326, la matrice del patch panel, il piano IP e il rack 10U.
-->

## 1. Introduzione e Riferimenti

Il presente Low-Level Design costituisce il piano esecutivo di cablaggio, indirizzamento e configurazione degli apparati per la sede di **Severino Srl**.

**Documenti correlati:**
- Requisiti di business e compliance: [[specification-severino-srl-rsd-01]]
- Architettura macroscopica: [[architecture-severino-srl-hld-01]]

---

## 2. Piano di Indirizzamento IP e Subnetting

### 2.1 Schema di Subnetting

| Subnet | CIDR | VLAN ID | Zona | Gateway | DHCP | Utilizzo |
|--------|------|---------|------|---------|------|----------|
| 192.168.120.0 | /24 | 1 | LAN-CORP | 192.168.120.1 | sì (pool .2-.254 con reservation) | Rete Unificata Severino Srl (Server, Client, Wi-Fi, Storage) |

### 2.2 Mappatura VLAN → Zona → Trust

| VLAN ID | Nome | Zona | Trust level | Routing inter-VLAN / Uscita |
|---|---|---|---|---|
| 1 | default (bridge-local) | LAN-CORP | High / Trusted | Masquerade NAT via `ether1` (MikroTik WAN) |

### 2.3 Allocazione IP degli Host Fissi e Reservation DHCP

Il pool dinamico copre `192.168.120.2` - `192.168.120.254`. I dispositivi infrastrutturali chiave utilizzano IP statici dedicati (o reservation DHCP su base MAC address):

| Hostname / Dispositivo | IP | MAC Address | VLAN | Ruolo Architetturale | Note Operative |
|---|---|---|---|---|---|
| `router-core` (MikroTik CRS326) | `192.168.120.1` | `vault://it/projects/severino-srl/mac/crs326` | 1 | Default Gateway & DNS Relay | Switch Core & Firewall |
| `host-hp-z4` (HP Z4 Physical) | `192.168.120.10` | `vault://it/projects/severino-srl/mac/hp-z4` | 1 | Host Fisico Hyper-V | Scheda Intel Gigabit LAN |
| `dc01` (Windows Server 2022) | `192.168.120.239` | `vault://it/projects/severino-srl/mac/dc01` | 1 | Domain Controller AD, DNS primario, DHCP | Dominio `severino` |
| `fs01` (Windows Server 2022) | `192.168.120.240` | `vault://it/projects/severino-srl/mac/fs01` | 1 | File Server Severino Srl (2 TB) | Share SMB + ZeroTier |
| `fs02` (Windows Server 2022) | `192.168.120.241` | `vault://it/projects/severino-srl/mac/fs02` | 1 | File Server Partner (512 GB SSK) | Share SMB + ZeroTier |
| `nas-qnap` (QNAP TS-233) | `192.168.120.250` | `vault://it/projects/severino-srl/mac/qnap` | 1 | Backup Repository NAS | Target Cobian / RustCopy |
| `ap-unifi-01` (UniFi AP) | `192.168.120.251` | `vault://it/projects/severino-srl/mac/unifi` | 1 | Access Point Wi-Fi Aziendale | Gestione via UniFi App/Network |
| `mfp-printer` (Multifunzione) | `192.168.120.245` | `vault://it/projects/severino-srl/mac/printer` | 1 | Stampante di Rete & Scanner | Scan-to-folder con utente `scanner` |
| `teams-room` (Logitech Rally Bar) | `192.168.120.246` | `vault://it/projects/severino-srl/mac/teams` | 1 | Sala Videoconferenza Teams | Connessa via cavo LAN |
| *Client HP G6 (dir01, ops01, ecc.)* | `192.168.120.50` - `.199` | Dinamici / DHCP Lease | 1 | Postazioni desktop fisse cablate | Ricevono DNS `192.168.120.239` |

---

## 3. Layout Fisico Armadio Rack 10U

L'armadio rack a parete/pavimento da **10 Unità (10U)** è allestito con la seguente sequenza verticale (dall'alto in basso):

```
Armadio: Rack 10U Severino Srl
Posizione: Locale Tecnico / Ufficio CED

U  | Componente                          | Note
---|-------------------------------------|---------------------------------------------------------
10 | [PDU Superiore]                     | Multipresa rack 19" 8 posti con interruttore magneto-termico
09 | [Patch Panel 24 Porte Cat6 RJ45]    | Terminazione cavi rigidi prese a muro e AP UniFi
08 | [Pannello Passacavi a Spazzola 1U]  | Gestione e instradamento patch cord ordinati
07 | [Switch Core MikroTik CRS326]       | CRS326-24G-2S+RM (24p GbE + 2x SFP+) montato a rack 1U
06 | [Mensola Fissa Ripiano 1]           | NAS QNAP TS-233 (2-Bay) + Vodafone Station
05 | [Spazio di Areazione Ripiano 1]     | Circolazione termica e alimentatori QNAP / Vodafone
04 | [Mensola Heavy-Duty Ripiano 2]      | Workstation HP Z4 (posizionata orizzontalmente)
03 | [Workstation HP Z4]                 | Chassis host fisico Hyper-V (occupa 3U-4U complessive)
02 | [Gruppo di Continuità UPS 1]        | UPS a protezione apparati attivi (MikroTik, HP Z4, QNAP)
01 | [PDU Inferiore / Base Rack]         | Alimentazione ausiliaria e collegamento di terra
```

---

## 4. Mappatura Porte Fisiche Switch MikroTik CRS326 (Cable Matrix)

Configurazione logica RouterOS:
- **`ether1`**: **FUORI BRIDGE** (Uplink WAN collegato a porta LAN Vodafone Station). Riceve configurazione IP dalla Vodafone Station (o IP statico dedicato) con masquerade NAT attivo.
- **`ether2` - `ether24`**: **APPARTENGONO AL `bridge-local`** (Switching hardware offloaded a 1 Gbps).

### 4.1 Tabella Cablaggi Switch MikroTik CRS326-24G-2S+RM

| Porta Switch | Ruolo / Configurazione | Destinazione Cablata (Patch Panel / Apparato) | Presa a Muro / Apparato Finale | Tipo Cavo | Note |
|---|---|---|---|---|---|
| **ether1** | **WAN (Fuori Bridge)** | Vodafone Station (Porta LAN 1) | Router Vodafone | Cat6 UTP | Uplink Internet con NAT |
| **ether2** | Bridge LAN | Patch Panel Porta 01 | Postazione Direzione (`dir01` - HP G6) | Cat6 UTP | Presa Muro A1 |
| **ether3** | Bridge LAN | Patch Panel Porta 02 | Postazione Operativa (`ops01` - HP G6) | Cat6 UTP | Presa Muro A2 |
| **ether4** | Bridge LAN | Patch Panel Porta 03 | Postazione Amm. 1 (`adm01` - HP G6) | Cat6 UTP | Presa Muro B1 |
| **ether5** | Bridge LAN | Patch Panel Porta 04 | Postazione Amm. 2 (`adm02` - HP G6) | Cat6 UTP | Presa Muro B2 |
| **ether6** | Bridge LAN | Patch Panel Porta 05 | Postazione HR 1 (`hr01` - HP G6) | Cat6 UTP | Presa Muro C1 |
| **ether7** | Bridge LAN | Patch Panel Porta 06 | Postazione HR 2 (`hr02` - HP G6) | Cat6 UTP | Presa Muro C2 |
| **ether8** | Bridge LAN | Patch Panel Porta 07 | Postazione Area Manager (`amg01` - HP G6) | Cat6 UTP | Presa Muro D1 |
| **ether9** | Bridge LAN | Patch Panel Porta 08 | Stampante Multifunzione MFP (`printerusr`) | Cat6 UTP | Presa Muro Stampante |
| **ether10** | Bridge LAN | Patch Panel Porta 09 | Sala Riunioni (Logitech Rally Bar / TV 65") | Cat6 UTP | Presa Muro Sala Meeting |
| **ether11** | Bridge LAN | Patch Panel Porta 10 | Sala Riunioni (Tablet Touch Controller) | Cat6 UTP | Presa Muro Sala Meeting |
| **ether12** | Bridge LAN | Patch Panel Porta 11 | Ubiquiti UniFi AP (via PoE Injector) | Cat6 UTP | Access Point Soffitto |
| **ether13** | Bridge LAN | Patch Panel Porta 12 | Ubiquiti UniFi AP 2 (Predisposizione) | Cat6 UTP | Spare WiFi |
| **ether14** | Bridge LAN | Patch Panel Porta 13 | Presa Muro Tavolo Riunioni 1 | Cat6 UTP | Connessione ospite cablata |
| **ether15** | Bridge LAN | Patch Panel Porta 14 | Presa Muro Tavolo Riunioni 2 | Cat6 UTP | Connessione ospite cablata |
| **ether16** | Bridge LAN | Patch Panel Porta 15 | Presa Muro Ufficio Tecnico 1 | Cat6 UTP | Postazione spare |
| **ether17** | Bridge LAN | Patch Panel Porta 16 | Presa Muro Ufficio Tecnico 2 | Cat6 UTP | Postazione spare |
| **ether18** | Bridge LAN | Connessione Diretta Rack | Host Fisico HP Z4 (NIC Primaria Hyper-V) | Cat6 UTP | VSwitch LAN per VM dc01, fs01, fs02 |
| **ether19** | Bridge LAN | Connessione Diretta Rack | Host Fisico HP Z4 (NIC Secondaria / iLO se presente) | Cat6 UTP | Management host |
| **ether20** | Bridge LAN | Connessione Diretta Rack | NAS QNAP TS-233 (Porta Gigabit LAN) | Cat6 UTP | Backup storage |
| **ether21** | Bridge LAN | Connessione Diretta Rack | Presa di Servizio Locale CED (Notebook manutenzione) | Cat6 UTP | Porta frontale test |
| **ether22** | Bridge LAN | Patch Panel Porta 21 | Presa Muro Reception / Ingresso | Cat6 UTP | Spare |
| **ether23** | Bridge LAN | Patch Panel Porta 22 | Predisposizione Telecamera IP / Sicurezza | Cat6 UTP | Spare |
| **ether24** | Bridge LAN | Patch Panel Porta 23 | Predisposizione Telecamera IP / Sicurezza | Cat6 UTP | Spare |
| **sfp-sfpplus1** | Disabilitata / Spare | Rack Slot SFP+ | Predisposizione uplink 10G host o NAS | Fibra/DAC | Spare 10 Gbps |
| **sfp-sfpplus2** | Disabilitata / Spare | Rack Slot SFP+ | Predisposizione uplink 10G futuro | Fibra/DAC | Spare 10 Gbps |

---

## 5. Configurazione Esecutiva Storage & USB Passthrough

### 5.1 Storage Host HP Z4 e File Server `fs01`
- **Volume VHDX:** File `D:\Hyper-V\Virtual Hard Disks\fs01_data.vhdx` di tipo dinamico espandibile con dimensione massima 2 TB.
- **Partizione Guest:** Disco formattato NTFS a blocchi 4K con label `DATI_SEVERINO`.
- **Condivisione SMB:** Share di rete `\\fs01\DatiAziendali` con permessi NTFS profilati per reparto (Direzione, Operazioni, Amministrazione, Risorse Umane, Commerciale).

### 5.2 Storage Esterno SSK 512GB e File Server `fs02`
- **Storage Fisico:** SSD Esterno USB 3.2 Gen2 SSK da 512 GB collegato su porta posteriore USB 3.0 dell'host HP Z4.
- **Assegnazione Hyper-V:** Disco offline su host e montato in modalità **Pass-Through fisico** direttamente nella VM `fs02` (oppure VHDX mappato sul volume SSK).
- **Condivisione SMB:** Share di rete separate per le 2 aziende curate:
  - `\\fs02\AziendaPartner1`
  - `\\fs02\AziendaPartner2`
- **Isolamento Accessi:** Nessun utente di Severino Srl ha permessi su tali cartelle, garantendo riservatezza rigorosa.

---

## 6. Configurazione ZeroTier SD-WAN

1. **Rete Central:**
   - Network ID: **`65228D8D6D71CA23`**
   - Gestore: `salviozt01@gmail.com`
   - Range IP Virtuale ZeroTier: `10.147.17.0/24` (o assegnato da controller)
2. **Configurazione Client Server:**
   - Servizio ZeroTier One installato su `fs01` e `fs02`.
   - Assegnazione IP ZeroTier fisso (es. `10.147.17.10` per `fs01` e `10.147.17.11` per `fs02`).
3. **Configurazione Utenti Remoti:**
   - Installazione client ZeroTier su notebook degli utenti `remote01`..`remote04`.
   - Mappatura cartella remota: `net use Z: \\10.147.17.10\DatiAziendali /persistent:yes`.

---

## 7. Strategia Backup su QNAP TS-233

### 7.1 Configurazione QNAP
- Hostname: `NAS-QNAP-01`
- IP Statico: `192.168.120.250`
- Share protetta creata: `\\192.168.120.250\Backup_Severino`
- Utente autorizzato: `severino\backup` con password memorizzata in `vault://it/projects/severino-srl/nas/backup-user`

### 7.2 Job Cobian Reflector (Stato Attuale)
- **Job 1 (fs01):** Esecuzione ogni notte ore 22:00. Backup differenziale giornaliero, full settimanale (Sabato).
- **Job 2 (fs02):** Esecuzione ogni notte ore 23:00. Backup differenziale dello storage SSK.

### 7.3 Piano di Migrazione a RustCopy v7.4.1+ (Stato Target)
- Script PowerShell schedulato su Task Scheduler delle VM:
  ```powershell
  # Esempio esecuzione RustCopy v7.4.1+:
  rustcopy.exe sync "D:\DatiAziendali" "\\192.168.120.250\Backup_Severino\fs01" --threads 8 --log "C:\Logs\rustcopy_fs01.log"
  ```

---

## 8. Checklist di Validazione Finale

- [x] Configurazione `ether1` (WAN fuori bridge) ed `ether2-ether24` (LAN bridge) documentata.
- [x] Matrice delle 24 porte switch e collegamenti al patch panel completata.
- [x] Piano IP con DC a `192.168.120.239` e pool DHCP `192.168.120.2-254` formalizzato.
- [x] Layout armadio rack 10U dettagliato da 10U a 1U.
- [x] Montaggio storage esterno SSK 512GB su `fs02` definito.
- [x] Network ID ZeroTier e mapping utenti remoti configurato.
- [x] Coerenza tra `related_docs` e `relations` OKF verificata.
- [x] Nessuna password in chiaro (esclusivo uso di riferimenti `vault://`).

## Decisioni Tecniche Consolidate da Staging Memory
> Consolidato dallo Scratchpad il `2026-09-16` con attestazione di confidenza da parte di `Mario Rossi (Tech Lead)`.
> Certificazione valida fino al: `2026-12-15`.

- [2026-09-16 11:04] [agent] (Lead Architect) Standardizzato schema subnet management su 192.168.120.0/24 <!-- id:mem-0dc0cb7b -->
- [2026-09-16 11:04] [infra-architect] (Mario Rossi) Confermato passaggio a Jumbo Frame MTU 9000 su VLAN 40 iSCSI <!-- id:mem-faa58890 -->
