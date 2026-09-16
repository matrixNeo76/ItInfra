<#
  PowerShell Setup & Provisioning Script - Progetto: severino-srl
  Generato automaticamente da ItInfra Automation Suite
  Data generazione: 2026-09-16 09:55:39
#>

# --------------------------------------------------------------
# Estratto da: 08-SOP-Runbook.md
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Estratto da: 08-SOP-Runbook.md
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Estratto da: 08-SOP-Runbook.md
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Estratto da: 08-SOP-Runbook.md
# --------------------------------------------------------------
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

# --------------------------------------------------------------
# Estratto da: 08-SOP-Runbook.md
# --------------------------------------------------------------
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

