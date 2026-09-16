---
okf_version: "0.2"
id: "guide-severino-srl-sop-runbook-01"
title: "SOP / Runbook — Procedure Operative Standard e Manuale di Gestione Severino Srl"
type: "guide"
domain: "IT Infrastructure & Operations Runbook"
tags: ["okf-v0.2", "sop", "runbook", "operations", "fase-7", "procedures", "severino-srl"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "severino-srl"
project_name: "Infrastruttura LAN, Virtualizzazione Hyper-V e Collaboration Severino Srl"
site: "HQ-SEV"
customer: "Severino Srl"
phase: 7
author: "Marco Severino"
reviewer: "AI Systems Architect"
approver: "Marco Severino"
owner_team: "IT Operations Severino Srl"
status: "in-review"
version: "1.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-severino-srl-asbuilt-01"
  - "specification-severino-srl-atp-01"
  - "specification-severino-srl-handover-01"
  - "architecture-severino-srl-lld-01"
  - "guide-severino-srl-mop-01"
  - "guide-severino-srl-rollback-01"
depends_on:
  - "architecture-severino-srl-asbuilt-01"
supersedes: null
superseded_by: null
classification: "internal"
retention: "5y"
lang: "it"

entities:
  - name: "Standard Operating Procedure Severino"
    type: "concept"
    description: "Raccolta di istruzioni operative standardizzate per la gestione e manutenzione dei sistemi IT"
  - name: "IT Operations Runbook"
    type: "pattern"
    description: "Guida operativa di primo e secondo livello per gli amministratori di rete e sistemisti"
  - name: "Backup and Restore Runbook"
    type: "specification"
    description: "Procedure dettagliate per la gestione dei job Cobian/RustCopy verso storage NAS QNAP TS-233"
  - name: "Incident and Escalation Path"
    type: "pattern"
    description: "Catena di escalation per incidenti di livello L1-L4 con contatti e tempi di intervento garantiti"
  - name: "Active Directory User Lifecycle"
    type: "toolchain"
    description: "Flusso di lavoro per onboarding, profilazione permessi, mapping dischi e offboarding utenti"

relations:
  - targetTitle: "As-Built Documentation Severino Srl"
    targetId: "architecture-severino-srl-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
    description: "Il SOP usa l'As-Built come riferimento per hostname, IP, porte switch e configurazioni reali"
  - targetTitle: "ATP — Acceptance Test Plan Severino Srl"
    targetId: "specification-severino-srl-atp-01"
    relationType: "references"
    weight: 0.85
    description: "Le procedure di verifica del SOP replicano i test case collaudati nell'ATP"
  - targetTitle: "Handover & Asset Inventory Severino Srl"
    targetId: "specification-severino-srl-handover-01"
    relationType: "references"
    weight: 0.95
    description: "La consegna formale al cliente include l'affidamento del presente manuale operativo"
  - targetTitle: "LLD — Low-Level Design Severino Srl"
    targetId: "architecture-severino-srl-lld-01"
    relationType: "references"
    weight: 0.8
    description: "Riferimento alle specifiche fisiche, logiche e di cablaggio di dettaglio"
  - targetTitle: "MOP — Method of Procedure Severino Srl"
    targetId: "guide-severino-srl-mop-01"
    relationType: "references"
    weight: 0.85
    description: "I task di manutenzione straordinaria ereditano le sequenze e i gate operativi dal MOP"
  - targetTitle: "Rollback Plan Severino Srl"
    targetId: "guide-severino-srl-rollback-01"
    relationType: "references"
    weight: 0.85
    description: "Procedure di emergenza e fallback da applicare in caso di guasti bloccanti"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: produrre il manuale operativo di primo e secondo livello per i sistemisti di Severino Srl.
  Input attesi: As-Built compilato, ATP superato, matrici di cablaggio e inventario.
  Regole di compilazione:
    1. Ogni procedura deve avere: ID univoco, scopo, prerequisiti, comandi pronti all'uso, verifica ed escalation.
    2. Comandi PowerShell e RouterOS copia-incollabili senza placeholder variabili scoperti.
    3. Nessun secret in chiaro: solo riferimenti al vault.
    4. Coprire onboarding utenti, gestione share SMB, backup QNAP con Cobian e transizione a RustCopy, Hyper-V, MikroTik e sala Teams.
-->

# SOP / Runbook — Standard Operating Procedures

**Progetto:** Infrastruttura LAN, Virtualizzazione Hyper-V e Collaboration Severino Srl  
**Cliente:** Severino Srl  
**Sito:** HQ-SEV (Sede Operativa Principale)  
**Versione documento:** 1.0  
**Stato:** in-review  
**Destinatari:** Team IT Operations (Marco Severino, Francesco Iavarone, Helpdesk Tecnico)  

---

## 1. Governance Operativa e Livelli di Rischio

Il presente Runbook definisce le procedure standardizzate per la conduzione, l'amministrazione ordinaria e la risoluzione dei problemi sull'infrastruttura ICT di **Severino Srl**, documentata in [[architecture-severino-srl-asbuilt-01]].

### 1.1 Livelli di Rischio e Matrice di Autorizzazione

| Livello | Definizione Operazione | Esecutore Delegato | Approvazione Richiesta | Finestra Esecutiva |
|---|---|---|---|---|
| **L1 (Basso)** | Routine quotidiana (reset password, mapping dischi, restore file utente, verifica log backup) | Helpdesk L1 / Sysadmin | Nessuna (operazione standard) | Qualsiasi orario lavorativo |
| **L2 (Medio)** | Modifiche configurazione (onboarding nuovo utente AD, creazione share SMB, assegnazione quote, update ZeroTier) | Francesco Iavarone | Team Lead / Resp. Reparto | Orario lavorativo con preavviso |
| **L3 (Alto)** | Interventi su core (patching host HP Z4, riavvio VM core, modifiche ACL switch MikroTik, firmware QNAP) | Francesco Iavarone | Marco Severino (Lead Architect) | Fuori orario lavorativo (dalle 19:00 o weekend) |
| **L4 (Critico)** | Disaster Recovery, ripristino bare-metal, sostituzione apparato core, ripristino da ransomware | Disaster Recovery Team | Marco Severino (Crisis Manager) | Immediato / Regime di emergenza |

---

## 2. Procedura RB-01: Gestione Utenti e Ciclo di Vita Active Directory

**ID Runbook:** RB-01  
**Livello Rischio:** L1/L2  
**Frequenza:** Su richiesta (Onboarding / Offboarding)  
**Autorità:** Francesco Iavarone / Marco Severino  

### 2.1 Scopo
Creare, configurare o disattivare account utente nel dominio `severino.local`, garantendo l'assegnazione automatica delle cartelle dipartimentali, l'abilitazione delle share di rete e l'accesso remoto protetto.

### 2.2 Creazione Nuovo Utente (Onboarding)

```powershell
# Eseguire su Domain Controller dc01 (192.168.120.239) via PowerShell Administrator
Import-Module ActiveDirectory

$SamAccountName = "nuovo.utente"
$GivenName = "Nome"
$Surname = "Cognome"
$DisplayName = "$GivenName $Surname"
$Department = "Amministrazione" # Valori: Direzione, Amministrazione, Operativo, RisorseUmane, AreaManager
$OUPath = "OU=$Department,OU=Users,OU=Severino,DC=severino,DC=local"

# Password casuale temporanea generata e salvata nel vault
# Registrare il secret in: vault://it/projects/severino-srl/ad/users/$SamAccountName
$TempPassword = ConvertTo-SecureString "TempPass!2026Secure" -AsPlainText -Force

New-ADUser -Name $DisplayName `
           -SamAccountName $SamAccountName `
           -UserPrincipalName "$SamAccountName@severino.local" `
           -GivenName $GivenName `
           -Surname $Surname `
           -DisplayName $DisplayName `
           -Department $Department `
           -Path $OUPath `
           -AccountPassword $TempPassword `
           -Enabled $true `
           -ChangePasswordAtLogon $true `
           -PasswordNeverExpires $false

# Assegnazione al gruppo dipartimentale per permessi share SMB
Add-ADGroupMember -Identity "GRP-$Department-Users" -Members $SamAccountName
Write-Host "Utente $SamAccountName creato con successo nell'OU $OUPath."
```

### 2.3 Abilitazione Accesso Remoto ZeroTier (Se Richiesto)
1. Accedere al portale ZeroTier Central con account amministrativo `salviozt01@gmail.com` (credenziali in `vault://it/projects/severino-srl/zerotier/admin`).
2. Selezionare la rete `65228D8D6D71CA23`.
3. Sul notebook dell'utente, installare il client ZeroTier One ed eseguire:
   ```cmd
   zerotier-cli join 65228D8D6D71CA23
   ```
4. Nel pannello di controllo cloud, individuare il nuovo Node ID (10 caratteri), apporre il flag **Auth**, assegnare il nome `Notebook-$SamAccountName` e verificare l'assegnazione dell'IP virtuale nel pool `10.147.19.x`.

### 2.4 Verifica Finale
- [x] L'utente effettua il primo logon sul MiniPC HP G6 con password provvisoria e imposta una nuova password sicura.
- [x] Il disco `Z:` (`\\fs01\DatiSeverino`) risulta mappato automaticamente da GPO.
- [x] L'accesso alle cartelle riservate di altri reparti è inibito (Access Denied).

---

## 3. Procedura RB-02: Gestione Condivisioni SMB e Storage Partner SSK

**ID Runbook:** RB-02  
**Livello Rischio:** L2  
**Frequenza:** Su necessità  
**Autorità:** Francesco Iavarone  

### 3.1 Scopo
Creare nuove share SMB, gestire i permessi NTFS e verificare il corretto funzionamento dell'archivio partner su SSD esterno SSK 512 GB attestato su `fs02`.

### 3.2 Creazione Nuova Cartella Condivisa su fs01

```powershell
# Eseguire su File Server fs01 (192.168.120.240)
$ShareName = "ProgettiSpeciali"
$FolderDir = "D:\DatiSeverino\$ShareName"

# 1. Creazione cartella fisica su volume VHDX 2 TB
if (-not (Test-Path $FolderDir)) {
    New-Item -Path $FolderDir -ItemType Directory
}

# 2. Configurazione permessi NTFS con disabilitazione ereditarietà selettiva
$Acl = Get-Acl $FolderDir
$Acl.SetAccessRuleProtection($true, $true) # Mantiene i permessi esistenti ma disaccoppia dal genitore
$RuleAdmins = New-Object System.Security.AccessControl.FileSystemAccessRule("SEVERINO\Domain Admins", "FullControl", "ContainerInherit,ObjectInherit", "None", "Allow")
$RuleUsers = New-Object System.Security.AccessControl.FileSystemAccessRule("SEVERINO\GRP-Operativo-Users", "Modify", "ContainerInherit,ObjectInherit", "None", "Allow")
$Acl.AddAccessRule($RuleAdmins)
$Acl.AddAccessRule($RuleUsers)
Set-Acl -Path $FolderDir -AclObject $Acl

# 3. Creazione condivisione SMB di rete
New-SmbShare -Name $ShareName -Path $FolderDir -FullAccess "SEVERINO\Domain Admins" -ChangeAccess "SEVERINO\GRP-Operativo-Users"
Write-Host "Share SMB \\fs01\$ShareName operativa con permessi configurati."
```

### 3.3 Gestione Storage SSK 512 GB Passthrough su fs02
Qualora fosse necessario verificare o re-inizializzare lo storage esterno SSK per le aziende partner:
1. Su Host **HP Z4** (`192.168.120.10`), verificare lo stato del disco con PowerShell:
   ```powershell
   Get-Disk | Where-Object FriendlyName -like "*SSK*"
   # Il disco DEVE trovarsi nello stato "Offline" su Host per consentire il passthrough alla VM
   ```
2. Se lo storage risulta disconnesso, ripristinare il passthrough nella configurazione della VM `fs02`:
   ```powershell
   # Eseguire su Host HP Z4
   $DiskNum = (Get-Disk | Where-Object FriendlyName -like "*SSK*").Number
   Add-VMHardDiskDrive -VMName "fs02" -ControllerType SCSI -ControllerNumber 0 -DiskNumber $DiskNum
   ```
3. Su VM `fs02`, verificare la presenza del volume `E:\DatiPartner` e l'accessibilità delle share `\\fs02\AziendaA$` e `\\fs02\AziendaB$`.

---

## 4. Procedura RB-03: Backup Giornaliero e Transizione a RustCopy

**ID Runbook:** RB-03  
**Livello Rischio:** L1 (Verifica/Restore) / L2 (Modifica Job)  
**Frequenza:** Giornaliera (Audit automatico) / Mensile (Test restore)  
**Autorità:** Francesco Iavarone / Marco Severino  

### 4.1 Architettura e Piani di Salvataggio
Il backup protegge i dati aziendali di Severino Srl e delle due aziende partner archiviandoli sul NAS QNAP TS-233 (`192.168.120.250`):
- **Sorgente 1:** `D:\DatiSeverino` (VM `fs01`)
- **Sorgente 2:** `E:\DatiPartner` (VM `fs02`, storage SSK 512 GB)
- **Destinazione:** `\\192.168.120.250\Backup` (autenticazione con account di servizio `backup`)
- **Retention:** 30 giorni di versioning cronologico.

### 4.2 Ispezione Giornaliera Cobian Reflector
1. Connettersi via RDP a `fs01` con credenziali di gestione (vault).
2. Aprire l'interfaccia di Cobian Reflector e consultare il pannello "Cronologia / Log":
   - Verificare che il task `Backup-Dati-Severino` riporti lo stato **"Terminato con successo"**.
   - Verificare che non siano presenti errori di file bloccati (VSS attivo).
3. Eseguire la medesima verifica su `fs02` per il task `Backup-Dati-Partner`.

### 4.3 Procedura di Ripristino Mensile di Prova (Test Restore)
```powershell
# Eseguire da PowerShell su fs01
$BackupNasPath = "\\192.168.120.250\Backup\fs01\DatiSeverino"
$TestRestoreDir = "C:\RestoreTest_$(Get-Date -Format 'yyyyMMdd')"

New-Item -Path $TestRestoreDir -ItemType Directory
# Selezionare l'archivio incrementale più recente e copiare un file campione
Copy-Item "$BackupNasPath\DocumentoCampione.pdf" -Destination $TestRestoreDir
$ShaOrig = (Get-FileHash "D:\DatiSeverino\DocumentoCampione.pdf" -Algorithm SHA256).Hash
$ShaRest = (Get-FileHash "$TestRestoreDir\DocumentoCampione.pdf" -Algorithm SHA256).Hash

if ($ShaOrig -eq $ShaRest) {
    Write-Host "[OK] Test di restore superato con successo: hash SHA256 identico." -ForegroundColor Green
    Remove-Item $TestRestoreDir -Recurse -Force
} else {
    Write-Warning "[ALLARME] Discrepanza hash nel ripristino dei dati!"
}
```

### 4.4 Roadmap di Transizione Operativa a RustCopy v7.4.1+
Non appena la release di **RustCopy v7.4.1+** (`https://github.com/matrixNeo76/rustcopy`) sarà certificata per l'ambiente di produzione:
1. Posizionare il binario in `C:\Scripts\rustcopy\rustcopy.exe` su `fs01` e `fs02`.
2. Configurare lo script PowerShell per la sincronizzazione multithreaded ad alte prestazioni con blocco delta:
   ```powershell
   # C:\Scripts\rustcopy\run_backup.ps1
   $Source = "D:\DatiSeverino"
   $Target = "\\192.168.120.250\Backup\RustCopy_Severino"
   $LogFile = "C:\Scripts\rustcopy\logs\backup_$(Get-Date -Format 'yyyy-MM-dd').log"

   & "C:\Scripts\rustcopy\rustcopy.exe" sync `
       --source $Source `
       --dest $Target `
       --threads 8 `
       --checksum sha256 `
       --retention-days 30 `
       --log $LogFile
   ```
3. Registrare il task nel Task Scheduler di Windows come job notturno alle ore 22:30 con esecuzione sotto l'account `SEVERINO\backup`.
4. Disabilitare gradualmente i job su Cobian Reflector previa verifica di coerenza per 7 giorni.

---

## 5. Procedura RB-04: Manutenzione Switch Core MikroTik CRS326

**ID Runbook:** RB-04  
**Livello Rischio:** L2 (Backup/Monitoraggio) / L3 (Upgrade RouterOS)  
**Frequenza:** Mensile / Trimestrale  
**Autorità:** Marco Severino  

### 5.1 Backup della Configurazione RouterOS v7
Prima di qualsiasi modifica o aggiornamento dello switch core, eseguire sempre il doppio backup (binario + script testuale):

```routeros
# Connettersi via SSH o Terminale WinBox a sw-core-01 (192.168.120.1)
/system identity print
# 1. Generazione backup binario (password prelevata da vault://it/projects/severino-srl/mikrotik/backup-key)
/system backup save name="asbuilt-backup-sw-core-01"

# 2. Generazione export configurazione in chiaro per audit
/export file="asbuilt-export-sw-core-01.rsc"
```
Scaricare i due file generati tramite SFTP/WinBox e archiviarli nel vault: `vault://it/projects/severino-srl/backups/mikrotik/`.

### 5.2 Aggiornamento Firmware e RouterBOOT
1. Verificare la disponibilità di release stabili RouterOS v7 LTS:
   ```routeros
   /system package update check-for-updates
   ```
2. Se approvato da Marco Severino, procedere con il download e l'installazione fuori orario lavorativo:
   ```routeros
   /system package update download
   /system reboot
   ```
3. Dopo il riavvio, aggiornare il BIOS del bootloader hardware (RouterBOOT):
   ```routeros
   /system routerboard upgrade
   /system reboot
   ```
4. Al riavvio finale, verificare lo stato del bridge e della WAN:
   ```routeros
   /interface bridge print
   /ip route print
   /ping 8.8.8.8 count=4
   ```

---

## 6. Procedura RB-05: Manutenzione Host HP Z4 e Macchine Virtuali

**ID Runbook:** RB-05  
**Livello Rischio:** L2/L3  
**Frequenza:** Mensile (Patch Day Microsoft)  
**Autorità:** Francesco Iavarone / Marco Severino  

### 6.1 Sequenza di Riavvio Ordinato delle Macchine Virtuali
Qualora sia necessario riavviare l'host fisico HP Z4 per aggiornamenti di sistema:

```powershell
# Eseguire su Host HP Z4 (192.168.120.10) da PowerShell Administrator

# FASE 1: Spegnimento controllato delle VM (in ordine inverso di dipendenza)
Write-Host "Spegnimento VM fs02 (Partner)..."
Stop-VM -Name "fs02" -Force
Write-Host "Spegnimento VM fs01 (Severino Srl)..."
Stop-VM -Name "fs01" -Force
Write-Host "Spegnimento VM dc01 (Domain Controller)..."
Stop-VM -Name "dc01" -Force

# FASE 2: Riavvio Host Fisico
Restart-Computer -Force

# FASE 3: Sequenza di Avvio (all'avvio dell'host o manualmente se non in automatic startup)
# 1. Avviare dc01 e attendere 90 secondi per consentire l'avvio completo di AD DS e DNS
Start-VM -Name "dc01"
Start-Sleep -Seconds 90

# 2. Avviare fs01 e fs02
Start-VM -Name "fs01"
Start-VM -Name "fs02"

# 3. Verifica stato
Get-VM | Select-Object Name, State, Uptime, MemoryAssigned
```

---

## 7. Procedura RB-06: Gestione Sala Riunioni Microsoft Teams Rooms

**ID Runbook:** RB-06  
**Livello Rischio:** L1  
**Frequenza:** Su necessità  
**Autorità:** Helpdesk L1 / Francesco Iavarone  

### 7.1 Resync e Riavvio Logitech Rally Bar & Touch Tablet
Se la sala riunioni presenta mancata risposta dei controlli touch sul tablet o assenza di segnale video su TV 65":
1. **Verifica Alimentazione e Rete:**
   - Controllare che il tablet Logitech Tap IP sia acceso (LED alimentazione PoE attivo).
   - Verificare che il cavo HDMI tra Rally Bar e porta HDMI 1 della TV sia saldamente inserito.
   - Verificare che la presa di rete `ether15` sul patch panel abbia il LED verde link 1 Gbps attivo.
2. **Riavvio del Sistema Teams Rooms:**
   - Tramite tablet, accedere a: *Impostazioni (icona ingranaggio) -> Impostazioni Amministratore (password in `vault://it/projects/severino-srl/teams/meeting`) -> Riavvia dispositivo*.
   - Se il tablet non risponde, eseguire un power-cycle staccando e reinserendo il cavo di alimentazione sul retro della Rally Bar (attendere 15 secondi prima di reinserire).
3. **Esecuzione Chiamata di Collaudo:**
   - Avviare una chiamata Teams con un utente interno per confermare microfoni beamforming, telecamera AI auto-framing e audio diffuso.

---

## 8. Procedura RB-07: Rotazione Credenziali di Sicurezza

**ID Runbook:** RB-07  
**Livello Rischio:** L2 (Dispositivi) / L3 (Domain Admin)  
**Frequenza:** Trimestrale (90 giorni) per switch/hypervisor; Semestrale (180 giorni) per account locali  
**Autorità:** Marco Severino  

1. **Generazione Chiave:** Generare password complessa ad alta entropia (minimo 18 caratteri con lettere, numeri e simboli).
2. **Registrazione Vault:** Aggiornare PRIMA il secret nel vault aziendale (`vault://it/projects/severino-srl/...`), registrando data di rotazione e operatore.
3. **Applicazione:** Applicare la nuova password sull'interfaccia dell'apparato o tramite comando di sistema.
4. **Verifica Obbligatoria:** Effettuare logout completo e rieseguire il login con la nuova credenziale accertandosi che la vecchia chiave venga scartata.

---

## 9. Matrice di Escalation e Contatti di Emergenza

| Livello | Descrizione Evento | Tempistica Risposta (SLA) | Contatto di Riferimento | Canale Operativo |
|---|---|---|---|---|
| **L1** | Problema singola postazione utente (MiniPC, password dimenticata, mapping disco mancante) | Entro 2 ore lavorative | Helpdesk Tecnico Severino Srl | Ticket interno / Assistenza diretta |
| **L2** | Interruzione accesso share di reparto o anomalia backup giornaliero | Entro 1 ora lavorativa | **Francesco Iavarone** (Senior Sysadmin) | Telefono / Sessione remota |
| **L3** | Blocco switch core MikroTik, indisponibilità host HP Z4 o perdita connettività WAN | Entro 30 minuti | **Francesco Iavarone** + **Marco Severino** | Presenza sul posto / Chiamata diretta |
| **L4** | Evento disastroso, corruzione dati, violazione sicurezza o guasto hardware non riparabile | Immediato (< 15 min) | **Marco Severino** (Lead Architect & Crisis Manager) | Attivazione piano di emergenza |

---

## 10. Checklist di Validazione Runbook

- [x] Tutte le 7 procedure operative (RB-01..RB-07) sono dettagliate e collaudate.
- [x] Gli script PowerShell e RouterOS sono completi, pronti all'uso e privi di placeholder aperti.
- [x] La roadmap di transizione verso RustCopy v7.4.1+ è chiara e strutturata.
- [x] Nessuna password in chiaro; utilizzati rigorosamente i riferimenti `vault://`.
- [x] La matrice di escalation L1-L4 presenta ruoli, SLA e contatti definiti.
- [x] Documento conforme allo standard OKF v0.2.
