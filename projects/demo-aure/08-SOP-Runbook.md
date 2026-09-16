---
okf_version: "0.2"
id: "guide-demo-aure-sop-runbook-01"
title: "SOP/Runbook — Progetto Demo-aure"
type: "guide"
domain: "IT Infrastructure & Operations Runbook"
tags: ["okf-v0.2", "sop", "runbook", "operations", "fase-7", "procedures"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "demo-aure"
project_name: "Progetto Demo-aure"
site: "DC-MIL-01"
customer: "Cliente Demo-aure"
phase: 7
author: "Mario Rossi"
reviewer: "<nome>"
approver: "<nome>"
owner_team: "<team operations>"
status: "draft"
version: "0.1"
created_at: "2026-09-15"
updated_at: "2026-09-15"
related_docs:
  - "architecture-demo-aure-asbuilt-01"
  - "specification-demo-aure-atp-01"
  - "specification-demo-aure-handover-01"
depends_on:
  - "architecture-demo-aure-asbuilt-01"
supersedes: null
superseded_by: null
classification: "internal"
retention: "5y"
lang: "it"

entities:
  - name: "Standard Operating Procedure"
    type: "concept"
    description: "Procedura operativa standard con ID, prerequisiti, step-by-step, verifica, escalation"
  - name: "Runbook"
    type: "pattern"
    description: "Raccolta di procedure operativa per sistemisti primo e secondo livello"
  - name: "Disaster Recovery Runbook"
    type: "specification"
    description: "Procedura completa di attivazione DR con fasi, RTO/RPO, trigger"
  - name: "Escalation Path"
    type: "pattern"
    description: "Catena di escalation con SLA per livelli L1-L4 (NO → System Eng → Senior → Crisis)"
  - name: "Credential Rotation"
    type: "specification"
    description: "Procedura di rotazione credenziali ogni 90 giorni con riferimento al vault"

relations:
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-demo-aure-asbuilt-01"
    relationType: "depends_on"
    weight: 1.0
    description: "Il SOP usa l'As-Built come riferimento per hostname, IP e configurazioni"
  - targetTitle: "ATP — Acceptance Test Plan"
    targetId: "specification-demo-aure-atp-01"
    relationType: "references"
    weight: 0.85
    description: "Le procedure SOP incorporano le verifiche collaudate nell'ATP"
  - targetTitle: "Handover & Asset Inventory"
    targetId: "specification-demo-aure-handover-01"
    relationType: "references"
    weight: 0.95
    description: "L'handover include la consegna del SOP al team operations"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: produrre il manuale operativo di primo e secondo livello per i sistemisti che
    gestiranno l'infrastruttura in regime di operations.
  Input attesi: As-Built compilato, eventuali runbook vendor, struttura del team operations,
    policy aziendali di gestione change/incident.
  Regole di compilazione:
    1. Ogni procedura deve avere: ID univoco, scopo, prerequisiti, step-by-step,
       verifica finale, escalation in caso di anomalia.
    2. I comandi devono essere copia-incollabili (in blocchi di codice), con placeholder
       per i parametri variabili (es. <hostname>).
    3. Le credenziali NON vanno in chiaro: riferimento al vault.
    4. Indicare SEMPRE il livello di rischio (L1/L2/L3) e l'autorità richiesta.
    5. Per procedure distruttive o a rischio, indicare prerequisiti di backup/snapshot.
    6. Includere procedure di DR complete (richiamabili da agenti durante incidenti).
    7. Le procedure devono essere testate e firmate dal team che le eseguirà.
    8. Validare la checklist in fondo prima di `status: in-review`.
-->

# SOP / Runbook — Standard Operating Procedures

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`
**Proprietario documento:** `<owner_team>`

## 1. Scope Operativo

### 1.1 A chi è rivolto
Il presente runbook è rivolto al team operations del cliente (`<owner_team>`) e definisce le procedure operative standard per la gestione quotidiana dell'infrastruttura installata presso il sito `<site>`. Si applica sia al primo livello (NO — Network Operations, H24) sia al secondo livello (System Engineers, on-call).

### 1.2 Livelli di Rischio e Autorità

| Livello | Definizione | Esecutore | Approvazione richiesta |
|---------|-------------|-----------|-------------------------|
| L1 | Operazione standard, nessun impatto utente | NO (H24) | Nessuna |
| L2 | Operazione con impatto pianificato o modifica config | System Engineer | Team Lead |
| L3 | Operazione critica, possibile down di servizi | Senior Engineer + Team Lead | PM / Sponsor |
| L4 | Operazione di Disaster Recovery | DR Team + Crisis Manager | Crisis Manager |

### 1.3 Riferimenti
- As-Built: [[06-As-Built]]
- Rapporto di collaudo: [[07-ATP]]
- Verbale di handover: [[09-Handover-Inventory]]

## 2. Procedura — Creazione Nuovo Share File Server

**ID Runbook:** RB-001
**Livello rischio:** L2
**Frequenza tipica:** su richiesta
**Autorità richiesta:** Team Lead

### 2.1 Scopo
Creare un nuovo share SMB su FILE-SRV-01 con permessi per un dipartimento specifico, applicando le policy di quota e backup.

### 2.2 Prerequisiti
- [ ] Richiesta formale approvata (ticket `<ID>`)
- [ ] Gruppo AD per il dipartimento già esistente (es. `GRP-<dipartimento>-RW`)
- [ ] Quota confermata dal richiedente
- [ ] Backup del file server funzionante (verificare ultimo job)

### 2.3 Step-by-Step

```powershell
# 1. Connettersi a FILE-SRV-01 via jump host
Enter-PSSession -ComputerName FILE-SRV-01 -Credential (Get-Credential)

# 2. Creare la cartella
$sharePath = "D:\Shares\<nome_share>"
New-Item -Path $sharePath -ItemType Directory

# 3. Creare lo share SMB con permessi
New-SmbShare -Name "<nome_share>" `
             -Path $sharePath `
             -FullAccess "DOMAIN\Domain Admins" `
             -ChangeAccess "DOMAIN\GRP-<dipartimento>-RW" `
             -ReadAccess "DOMAIN\GRP-<dipartimento>-RO"

# 4. Impostare NTFS permissions
$acl = Get-Acl $sharePath
$acl.SetAccessRuleProtection($true, $false)  # disabilita inheritance
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule(
    "DOMAIN\GRP-<dipartimento>-RW", "Modify", "ContainerInherit,ObjectInherit", "None", "Allow"
)
$acl.AddAccessRule($rule)
Set-Acl -Path $sharePath -AclObject $acl

# 5. Impostare quota FSRM
Set-FsrmQuota -Path $sharePath -Size "<quota_GB>GB" -HardLimit

# 6. Aggiungere al job di backup Veeam
# (via console Veeam o PowerShell Veeam module)
Add-VBRJobObject -Job "Job-FILE" -Path $sharePath

# 7. Uscire
Exit-PSSession
```

### 2.4 Verifica Finale
- [ ] Da una macchina del dipartimento, navigare `\\FILE-SRV-01\<nome_share>`: deve richiedere auth e permettere scrittura
- [ ] Da una macchina non autorizzata: accesso negato
- [ ] Copiare un file di test > quota: deve fallire con errore di disco pieno
- [ ] Verificare che lo share compaia nel prossimo backup notturno

### 2.5 Escalation
- Se la quota non viene applicata: verificare servizio FSRM su FILE-SRV-01, contattare `<Storage Engineer>`
- Se i permessi non vengono rispettati: verificare trust AD, contattare `<AD admin>`
- Se lo share non viene aggiunto al backup Veeam: contattare `<Backup admin>`

## 3. Procedura — Provisioning Nuova VM

**ID Runbook:** RB-002
**Livello rischio:** L2
**Frequenza tipica:** su richiesta
**Autorità richiesta:** Team Lead

### 3.1 Scopo
Creare una nuova VM nel cluster CL-PROD-01 partendo da template, assegnando IP statico, join al dominio e includendola nel backup.

### 3.2 Prerequisiti
- [ ] Richiesta formale approvata (ticket `<ID>`) con specifiche: vCPU, RAM, disco, OS, applicazione, owner
- [ ] IP libero identificato in subnet della VLAN target (consultare IPAM)
- [ ] Template VM disponibile (TPL-WIN-2022-STD o TPL-DEB-12)
- [ ] Gruppo AD per la macchina già creato (se richiesto da policy)

### 3.3 Step-by-Step

```powershell
# 1. Connettersi a vCenter via PowerCLI
Connect-VIServer -Server vcenter.<domain> -User "<vault://it/projects/acme-milano-dc/vcenter/admin>"

# 2. Parametri VM
$vmName = "<SRV-APP-XX>"
$template = "TPL-WIN-2022-STD"  # o TPL-DEB-12
$cluster = "CL-PROD-01"
$datastore = "LUN-001"
$network = "PG-PROD-APP"  # o PG-PROD-DB, PG-MGMT in base a VLAN
$ip = "10.10.20.<XX>"
$gateway = "10.10.20.1"
$dns = "10.10.50.20,10.10.50.21"

# 3. Clonare da template
New-VM -Name $vmName `
       -Template $template `
       -ResourcePool $cluster `
       -Datastore $datastore

# 4. Configurare CPU/RAM (se diversi dal template)
Set-VM -VM $vmName -NumCpu <n> -MemoryGB <n> -Confirm:$false

# 5. Configurare network e IP
$nic = Get-NetworkAdapter -VM $vmName
Set-NetworkAdapter -NetworkAdapter $nic -NetworkName $network -Confirm:$false

# 6. Avviare e fare customization (cloud-init / sysprep)
Start-VM -VM $vmName
# Attendere che la VM sia pronta, poi configurare IP:
Invoke-VMScript -VM $vmName -ScriptText "
  netsh interface ip set address 'Ethernet' static $ip 255.255.255.0 $gateway
  netsh interface ip set dns 'Ethernet' static $dns
  netdom join %COMPUTERNAME% /domain:<domain> /userD:DOMAIN\joiner /passwordD:*
  shutdown /r /t 0
"

# 7. Aggiungere al backup Veeam
Add-VBRJobObject -Job "Job-VM-PROD" -Server $vmName

# 8. Registrare nel CMDB / IPAM
# (via API CMDB o manualmente)

Disconnect-VIServer -Server vcenter.<domain> -Confirm:$false
```

### 3.4 Verifica Finale
- [ ] VM accesa, ping risponde da jump host
- [ ] Login con credenziali di dominio OK
- [ ] DNS risolve `<SRV-APP-XX>.<domain>`
- [ ] Backup incluso nel job Job-VM-PROD
- [ ] CMDB/IPAM aggiornato

### 3.5 Escalation
- Se la customizzazione fallisce: verificare VMware Tools / open-vm-tools aggiornati
- Se il join AD fallisce: verificare DNS, account joiner nel vault, OU di destinazione
- Se il backup non si aggiunge: contattare `<Backup admin>`

## 4. Procedura — Rotazione Credenziali

**ID Runbook:** RB-003
**Livello rischio:** L2 (L3 per account critici: vCenter, storage, AD admin)
**Frequenza tipica:** ogni 90 giorni (180 giorni per UPS/PDU)
**Autorità richiesta:** Team Lead; per account critici PM/Sponsor

### 4.1 Scopo
Ruotare le credenziali admin degli apparati di infrastruttura secondo le policy di sicurezza aziendali.

### 4.2 Prerequisiti
- [ ] Elenco credenziali da ruotare (consultare vault `vault://it/projects/acme-milano-dc/`)
- [ ] Finestra di manutenzione programmata (per apparati critici)
- [ ] Backup configurazione apparato (per ripristino in caso di problemi)
- [ ] Co-presenza di due tecnici (four-eyes principle per account L3)

### 4.3 Step-by-Step (esempio per firewall fw-01)

```bash
# 1. Generare nuova password casuale
NEW_PW=$(openssl rand -base64 24 | tr -d '/+=' | head -c 20)

# 2. Salvare nel vault PRIMA di applicare
vault kv put vault://it/projects/acme-milano-dc/fw-01/admin \
  password="$NEW_PW" \
  rotated_at="$(date -Iseconds)" \
  rotated_by="$(whoami)"

# 3. Login al firewall via SSH (con vecchia password)
ssh admin@fw-01.<domain>

# 4. Cambiare la password
# (comandi vendor-specific, es. Fortinet:)
config system admin
  edit "admin"
    set password $NEW_PW
  next
end

# 5. Logout e rilogin con nuova password per verifica
exit
ssh admin@fw-01.<domain>
# (dovrebbe richiedere $NEW_PW)

# 6. Verificare che i monitoring / automation possano ancora loggare
# (eventuali script che usano credenziali fw-01 devono essere aggiornati)

# 7. Registrare nel logbook rotazione credenziali
echo "$(date -Iseconds) - fw-01 admin rotated by $(whoami)" >> /var/log/cred-rotation.log
```

### 4.4 Verifica Finale
- [ ] Login con nuova password OK
- [ ] Login con vecchia password FALLISCE (verifica obbligatoria)
- [ ] Monitoring/automation aggiornati e funzionanti
- [ ] Vault aggiornato con timestamp rotazione
- [ ] Logbook aggiornato

### 4.5 Escalation
- Se la rotazione fallisce e la vecchia password è ancora attiva: riprovare dopo verifica permessi
- Se la rotazione lascia l'apparato non accessibile: ripristinare config da backup (vedi [[05-Rollback]] sezione §7.1 ROLL-D), contattare vendor support
- Se il monitoring non si connette più: aggiornare secret nel monitoring system

## 5. Procedura — Riavvio Controllato di un Nodo Cluster

**ID Runbook:** RB-004
**Livello rischio:** L2 (L3 in finestra di produzione)
**Frequenza tipica:** su necessità (patching, manutenzione)
**Autorità richiesta:** Team Lead

### 5.1 Scopo
Riavviare un nodo hypervisor (SRV-01/02/03) senza impatto sulle VM in esecuzione, sfruttando vMotion/DRS.

### 5.2 Prerequisiti
- [ ] Finestra di manutenzione comunicata (anche fuori orario, comunicare 24h prima)
- [ ] Verificare DRS impostato su "Fully Automated"
- [ ] Verificare che gli altri nodi abbiano capacità sufficiente (CPU/RAM) per accogliere le VM
- [ ] Verificare che HA sia attivo sul cluster

### 5.3 Step-by-Step

```powershell
# 1. Mettere il nodo in maintenance mode
Connect-VIServer -Server vcenter.<domain>
Get-VMHost -Name SRV-01.<domain> | Set-VMHost -State Maintenance -Evacuate

# 2. Attendere che tutte le VM siano migrate (DRS)
# (monitorare via Get-VMHost o vCenter UI)
Get-VMHost -Name SRV-01.<domain> | Get-VM
# (deve restituire vuoto o solo VM spente)

# 3. Riavviare il nodo via iLO/iDRAC (più pulito di SSH reboot)
# (via API iLO - script vendor-specific)
Invoke-WebRequest -Uri "https://10.10.50.101/redfish/v1/Systems/1/Actions/ComputerSystem.Reset" `
  -Method POST `
  -Headers @{"X-Auth-Token"="<vault://iLO/token>"} `
  -Body '{"ResetType":"GracefulRestart"}'

# 4. Attendere che il nodo torni up (verifica via ping e vCenter)
do {
  Start-Sleep -Seconds 30
  $host_state = (Get-VMHost -Name SRV-01.<domain>).ConnectionState
} until ($host_state -eq "Connected")

# 5. Uscire dal maintenance mode
Get-VMHost -Name SRV-01.<domain> | Set-VMHost -State Connected

# 6. Verificare che DRS ribilanci le VM (opzionale, di solito automatico)
Disconnect-VIServer -Server vcenter.<domain> -Confirm:$false
```

### 5.4 Verifica Finale
- [ ] Nodo "Connected" in vCenter, no allarmi
- [ ] Tutte le VM originarie del nodo sono di nuovo running (anche se migrate)
- [ ] HA status: "OK" sul cluster
- [ ] Storage paths: tutti i path attivi (no dead paths)
- [ ] Network uplinks: entrambi attivi

### 5.5 Escalation
- Se il nodo non torna up entro 15 min: accedere iLO/iDRAC, controllare log hardware, contattare vendor (Dell/Cisco/HPE)
- Se le VM non migrano durante il maintenance mode: verificare DRS, eventualmente eseguire vMotion manuale
- Se dopo il riavvio le VM hanno alert storage: verificare iSCSI multipath, riavviare HBA se necessario

## 6. Procedura — Disaster Recovery (DR) Completo

**ID Runbook:** RB-DR-001
**Livello rischio:** L4
**Frequenza tipica:** solo in caso di disastro
**Autorità richiesta:** Crisis Manager

### 6.1 Scopo
Attivare il sito di Disaster Recovery in caso di indisponibilità totale del sito primario, secondo gli RTO/RPO definiti in [[01-RSD-URS]].

### 6.2 Trigger di Attivazione
- Perdita totale del sito primario (incendio, allagamento, blackout prolungato)
- Compromissione confermata dell'infrastruttura con impossibilità di isolare
- Decisione del Crisis Manager in accordo con sponsor

### 6.3 RTO/RPO Target
- **RTO ≤ 4 ore** dal trigger all'erogazione servizi
- **RPO ≤ 1 ora** (repliche async verso stor-dr ogni 15 min, RPO effettivo ~12 min)

### 6.4 Step-by-Step

```
FASE 1 — Attivazione (T+0 → T+30min)
[ ] 1.1 Conferma formale attivazione DR da Crisis Manager
[ ] 1.2 Convocazione DR team (chat / call)
[ ] 1.3 Comunicazione utenti: "Servizi temporaneamente non disponibili"

FASE 2 — Avvio Sito DR (T+30min → T+1h30min)
[ ] 2.1 Verificare stato repliche storage su stor-dr (ultima snapshot)
[ ] 2.2 Attivare snapshot stor-dr → LUN attivi su sito DR
[ ] 2.3 Avviare hypervisor sito DR (se spenti)
[ ] 2.4 Avviare VM in sequenza: AD → DNS → DB → APP → web (seguendo dependency tree)
[ ] 2.5 Verificare reachability interna: ping tra VM DR

FASE 3 — Reindirizzamento Traffico (T+1h30min → T+2h30min)
[ ] 3.1 Aggiornare DNS pubblico → IP DR (TTL 60s)
[ ] 3.2 Aggiornare BGP route preference (ANN DR > ANN primario)
[ ] 3.3 Attivare VPN verso siti remoti da sito DR
[ ] 3.4 Verificare servizi pubblici accessibili (HTTP/HTTPS check)

FASE 4 — Verifica Funzionale (T+2h30min → T+3h30min)
[ ] 4.1 Login test utente
[ ] 4.2 Transazione di prova
[ ] 4.3 Verifica integrazioni esterne (API)
[ ] 4.4 Verifica backup DR funzionante

FASE 5 — Comunicazione e Stabilizzazione (T+3h30min → T+4h)
[ ] 5.1 Comunicazione utenti: "Servizi ripristinati su sito DR"
[ ] 5.2 Monitoraggio intensivo 24h
[ ] 5.3 Pianificazione failback (post-emergenza, in separata sede)
```

### 6.5 Verifica Finale
- [ ] Tutti i servizi pubblici accessibili
- [ ] SLA rispettato (RTO ≤ 4h, RPO ≤ 1h)
- [ ] DR team ha completato logbook DR
- [ ] Comunicazione agli utenti inviata
- [ ] Post-mortem pianificato entro 72h

### 6.6 Escalation
- Se le repliche stor-dr non sono utilizzabili: ripristinare da backup cloud (RTO +4h)
- Se il DNS pubblico non si aggiorna: contattare provider DNS (NO iscritto a account)
- Se le VPN verso siti remoti non si attivano: verificare config firewall DR, contattare ISP

## 7. Procedura — Ripristino File da Backup

**ID Runbook:** RB-005
**Livello rischio:** L1
**Frequenza tipica:** su richiesta utente
**Autorità richiesta:** Nessuna

### 7.1 Scopo
Ripristinare un file o una cartella cancellata/modificata per errore, dal backup Veeam.

### 7.2 Prerequisiti
- [ ] Ticket utente con dettaglio: hostname, path file, data cancellazione o ultima modifica corretta
- [ ] Verificare retention job: il backup del giorno richiesto è disponibile

### 7.3 Step-by-Step

```powershell
# 1. Aprire Veeam Backup Console (o PowerShell)
Connect-VBRServer -Server bkp-01.<domain>

# 2. Identificare il restore point
$restore = Get-VBRBackup -Name "Job-FILE" | 
           Get-VBRRestorePoint -Name "FILE-SRV-01" |
           Where-Object {$_.CreationTime -ge "<data_richiesta>"} |
           Sort-Object CreationTime -Descending | Select-Object -First 1

# 3. Avviare restore file-level (FLR)
Start-VBRWindowsFileRestore -RestorePoint $restore -Path "<percorso_file>" -Destination "\\FILE-SRV-01\RestoreTemp\"

# 4. Verificare ripristino in \\FILE-SRV-01\RestoreTemp\
# (l'utente deve confermare il file)

# 5. Spostare il file in posizione finale (manualmente o via script)
Move-Item "\\FILE-SRV-01\RestoreTemp\<file>" "\\FILE-SRV-01\<percorso_originale>\"

# 6. Verificare permessi NTFS corretti
Get-Acl "\\FILE-SRV-01\<percorso_originale>\<file>"

Disconnect-VBRServer
```

### 7.4 Verifica Finale
- [ ] File ripristinato in posizione originale (o in path alternativo concordato)
- [ ] Permessi NTFS corretti
- [ ] Utente ha confermato integrità del file
- [ ] Ticket chiuso con nota "ripristinato da backup del `<data>`"

### 7.5 Escalation
- Se il file non è nel backup (oltre retention): comunicare impossibilità all'utente
- Se restore fallisce per errore Veeam: controllare job status, contattare `<Backup admin>`

## 8. Procedura — Aggiornamento Firmware Storage

**ID Runbook:** RB-006
**Livello rischio:** L3 (potenziale impatto storage)
**Frequenza tipica:** trimestrale o secondo vendor
**Autorità richiesta:** PM / Sponsor

### 8.1 Scopo
Applicare aggiornamento firmware storage array stor-01 mantenendo disponibilità servizio (controller failover).

### 8.2 Prerequisiti
- [ ] Compatibilità firmware verificata con hypervisor e switch (vendor HCL)
- [ ] Backup configurazione storage completo
- [ ] Snapshot di tutte le LUN (pre-aggiorrnamento)
- [ ] Finestra di manutenzione comunicata (notturna, fuori produzione)
- [ ] Vendor support contattato in caso di rollback (contratto attivo)

### 8.3 Step-by-Step (semplificato)

```
1. Verificare stato storage: controller A active, B standby
2. Scaricare firmware via vendor console
3. Pre-check: nessun job backup attivo, no replication in corso
4. Aggiornare controller B (standby)
   - firmware upgrade su B
   - wait completamento, verify B healthy
5. Failover: A → B (controller B diventa active)
   - verificare I/O continua, no drop
6. Aggiornare controller A (ora standby)
   - firmware upgrade su A
   - wait completamento, verify A healthy
7. Failback opzionale: B → A (per ribilanciare carico, se richiesto)
8. Verifica finale: entrambi i controller healthy, I/O OK
```

### 8.4 Verifica Finale
- [ ] Entrambi i controller su nuova versione firmware
- [ ] I/O storage senza errori (verifica via storage console e OS host)
- [ ] Snapshot pre-aggiornamento mantenuti (cancellabili dopo 7gg di stabilità)
- [ ] Tutte le repliche verso DR riprese

### 8.5 Escalation
- Se failover controller non riesce: NON proseguire, contattare vendor support
- Se dopo upgrade I/O presenta errori: rollback firmware (vedi procedura vendor), aprire ticket

## 9. Mappa Runbook e Frequenze

| ID | Titolo | Livello | Frequenza |
|----|--------|---------|-----------|
| RB-001 | Creazione share file server | L2 | su richiesta |
| RB-002 | Provisioning VM | L2 | su richiesta |
| RB-003 | Rotazione credenziali | L2/L3 | 90gg |
| RB-004 | Riavvio nodo cluster | L2 | su necessità |
| RB-DR-001 | DR completo | L4 | su disastro |
| RB-005 | Ripristino file da backup | L1 | su richiesta |
| RB-006 | Aggiornamento firmware storage | L3 | trimestrale |

## 10. Escalation Path Generale

| Livello | Trigger | Owner | SLA risposta |
|---------|---------|-------|--------------|
| L1 | Anomalia minore, runbook disponibile | NO | 15 min |
| L2 | Operazione pianificata | System Engineer | 30 min |
| L3 | Operazione critica / impatto servizi | Senior Engineer + Team Lead | 1h |
| L4 | Disaster / crisi | DR Team + Crisis Manager | immediato |

**Contatti:**

| Ruolo | Nome | Cell | Email |
|-------|------|------|-------|
| NO H24 | `<nome>` | `<phone>` | `<email>` |
| Team Lead Operations | `<nome>` | `<phone>` | `<email>` |
| System Engineer on-call | `<nome>` | `<phone>` | `<email>` |
| Storage Engineer | `<nome>` | `<phone>` | `<email>` |
| Network Engineer | `<nome>` | `<phone>` | `<email>` |
| Security Engineer | `<nome>` | `<phone>` | `<email>` |
| Vendor support (storage) | `<vendor>` | `<phone>` | `<email>` / ticket |
| Vendor support (hypervisor) | `<vendor>` | `<phone>` | `<email>` / ticket |

## 11. Riferimenti e Documenti Correlati

- As-Built: [[06-As-Built]]
- Rapporto di collaudo: [[07-ATP]]
- Handover: [[09-Handover-Inventory]]
- MOP (per procedure installazione iniziale): [[04-MOP]]
- Rollback Plan (per DR o ripristini estesi): [[05-Rollback]]

## Appendice A — Strumenti e Accessi Operativi

| Tool | Versione | URL / Endpoint | Accesso | Note |
|------|---------|-----------------|--------|------|
| vCenter | `<8.0 U2>` | `https://vcenter.<domain>` | SSO via AD | MFA obbligatoria |
| Veeam Console | `<12.1>` | `bkp-01.<domain>` | Vault cred. | Solo da jump host |
| Storage Console | `<vendor>` | `https://stor-01.<domain>` | Vault cred. | Solo da MGMT VLAN |
| Firewall Console | `<vendor>` | `https://fw-01.<domain>` | Vault cred. | Solo da MGMT VLAN |
| Vault | `<HashiCorp Vault>` | `https://vault.<domain>` | LDAP + MFA | Credenziali infrastruttura |
| IPAM | `<phpIPAM>` | `https://ipam.<domain>` | LDAP | Gestione IP |
| CMDB | `<piattaforma>` | `<URL>` | LDAP | Asset management |
| Monitoring | `<Zabbix>` | `https://monitor.<domain>` | LDAP | H24 dashboard |

---

## Checklist di Validazione

- [ ] Scope operativo e livelli di rischio definiti (§1)
- [ ] Almeno 5 procedure standard (RB-001 → RB-005) compilate
- [ ] Procedura DR completa (RB-DR-001) con fasi, RTO/RPO, trigger
- [ ] Per ogni procedura: scopo, prereq, step, verifica, escalation
- [ ] Comandi copia-incollabili in blocchi di codice
- [ ] Nessuna password in chiaro (riferimenti al vault)
- [ ] Mappa runbook con frequenze (§9)
- [ ] Escalation path con contatti (§10)
- [ ] Strumenti e accessi operativi documentati (Appendice A)
- [ ] `depends_on` contiene As-Built
- [ ] `owner_team` valorizzato (squadra che eseguirà le procedure)
