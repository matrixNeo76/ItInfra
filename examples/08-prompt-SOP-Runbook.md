# Esempio prompt — SOP / Runbook (Standard Operating Procedures)

Scenario: manuale operativo di primo e secondo livello per il team operations del cliente.

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: As-Built, ATP
- **Obiettivo**: produrre il manuale operativo che il team Acme utilizzerà quotidianamente

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un system engineer senior specializzato in documentazione operativa IT.
Il tuo compito è compilare il template SOP/Runbook, manuale operativo di
primo e secondo livello per i sistemisti che gestiranno l'infrastruttura.

Le procedure devono essere testabili, con comandi copia-incollabili,
verifiche finali e escalation in caso di anomalia.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - As-Built: /vault/projects/acme-milano-2026/06-As-Built.md (hostname, IP, topologia)
   - ATP: /vault/projects/acme-milano-2026/07-ATP.md (limitazioni note, warning)

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (System Engineer, Integratore)
- reviewer: Giulia Bianchi
- approver: Marco Conti (NO Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — SOP/Runbook

### Team operations Acme (per definire escalation)
- NO H24: Marco Conti (rotazione 3 persone: Marco, Luca, Paolo)
- System Engineer: Marco Conti + Paolo Ferri
- Storage Engineer: Paolo Ferri (con support vendor NetApp)
- Network Engineer: Luca Bruni (con support vendor Cisco)
- Security Engineer: Anna Neri (CISO)
- Backup admin: Paolo Ferri

### Strumenti e accessi (per Appendice A)
- vCenter: https://vcenter.acme.local, versione 8.0 U2, SSO via AD, MFA obbligatoria
- Veeam Console: https://bkp-01.acme.local, versione 12.1, credenziali in vault
- NetApp ONTAP console: https://stor-01.acme.local, ONTAP 9.13.1
- FortiGate console: https://fw-01.acme.local, FortiOS 7.4.3
- HashiCorp Vault: https://vault.acme.local, LDAP + MFA
- phpIPAM: https://ipam.acme.local, LDAP auth
- iTop CMDB: https://cmdb.acme.local, LDAP
- Zabbix: https://monitor.acme.local, LDAP, dashboard H24

### Procedure da documentare (richieste utente)

#### RB-001 — Creazione nuovo share file server
- File server: FILE-SRV-01 (VM Windows Server 2022, IP 10.10.20.50)
- Software: Windows Server 2022 + FSRM (File Server Resource Manager)
- Backup: Veeam Job-FILE

#### RB-002 — Provisioning nuova VM
- Cluster: CL-PROD-01 (3 nodi SRV-01/02/03)
- vCenter: vcenter.acme.local
- Template disponibili: TPL-WIN-2022-STD, TPL-DEB-12
- Datastore: LUN-001 / LUN-002 (iSCSI)
- Backup: Veeam Job-VM-PROD

#### RB-003 — Rotazione credenziali
- Frequenza: 90 giorni per apparati, 180 giorni per UPS/PDU
- Vault: HashiCorp Vault, path vault://it/acme-milano-2026/
- Apparati da ruotare: fw-01/02, sw-core-01/02, sw-tor-01/02, stor-01, bkp-01, vCenter, UPS/PDU

#### RB-004 — Riavvio controllato nodo cluster
- Cluster: CL-PROD-01
- DRS: fully automated
- HA: enabled
- iLO: 10.10.50.101/102/103 per SRV-01/02/03

#### RB-DR-001 — DR completo
- Sito DR: BG-01 (Bergamo, 60 km)
- Storage DR: stor-dr (NetApp FAS8700, IP 10.20.50.20)
- RTO target: ≤ 4 ore
- RPO target: ≤ 1 ora
- Replica: SnapMirror async ogni 15 min (Tier1), ogni 1h (Tier2)
- Runbook DR completo: 5 fasi (Attivazione, Avvio sito DR, Reindirizzamento traffico, Verifica, Comunicazione)

#### RB-005 — Ripristino file da backup
- Software: Veeam Backup & Replication 12.1
- Appliance: bkp-01 (10.10.50.40)
- Restore path temporaneo: \\FILE-SRV-01\RestoreTemp\

#### RB-006 — Aggiornamento firmware storage
- Storage: stor-01 (NetApp FAS8700, ONTAP 9.13.1)
- Modalità: controller failover (A→B→A)
- Supporto: NetApp Premium 24x7, contratto CTR-003
- Snapshot pre-aggiornamento obbligatorio

### Policy di escalation Acme
- L1 (NO H24): anomalia minore, runbook disponibile — SLA risposta 15 min
- L2 (System Engineer): operazione pianificata — SLA 30 min
- L3 (Senior + Team Lead): operazione critica — SLA 1h
- L4 (DR Team + Crisis Manager): disastro — SLA immediato

### Contatti Acme
- Marco Conti (NO Lead): +39 333 1234567, marco.conti@acme.it
- Paolo Ferri (Storage/Backup): +39 333 2345678, paolo.ferri@acme.it
- Luca Bruni (Network): +39 333 3456789, luca.bruni@acme.it
- Anna Neri (CISO): +39 333 4567890, anna.neri@acme.it
- Acme Facility (accesso fisico): +39 02 1234567

### Contatti vendor support
- Dell ProSupport Plus: 800 870 090 (CTR-001, 24x7 NBD)
- Cisco SMARTnet: 800 123 456 (CTR-002, 24x7x4)
- NetApp Premium: 800 789 012 (CTR-003, 24x7)
- Fortinet FortiCare: 800 345 678 (CTR-004, 24x7)
- Veeam Premium: 800 456 789 (CTR-005, 24x7)
- APC Standard: 800 567 890 (CTR-006, 24x7)

## TEMPLATE DA COMPILARE

Template path: /download/templates/08-SOP-Runbook.md
Tipo documento: SOP-Runbook
Fase: 7

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Ogni procedura: scopo, prereq, step-by-step, verifica finale, escalation
  * Comandi copia-incollabili in blocchi di codice, con placeholder <...>
  * NO password in chiaro (riferimento al vault)
  * Indicare SEMPRE il livello di rischio (L1/L2/L3/L4) e l'autorità richiesta
  * Per procedure distruttive o a rischio: prerequisiti di backup/snapshot
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-asbuilt-01]
- related_docs del nuovo SOP:
  - architecture-acme-milano-asbuilt-01
  - specification-acme-milano-atp-01
  - specification-acme-milano-handover-01 (placeholder)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft
- Versione: 0.1
- ID documento: guide-acme-milano-sop-runbook-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe) incluso il numero di runbook prodotti
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/08-SOP-Runbook.md
   - ID: guide-acme-milano-sop-runbook-01

Compila il documento ora. Sarà lungo (550+ righe).
```

---

## Output atteso

Documento SOP/Runbook completo con:

- Scope operativo e livelli di rischio (L1-L4) definiti
- 6 procedure standard (RB-001 a RB-006) + 1 procedura DR completa (RB-DR-001)
- Per ogni procedura: ID, scopo, prerequisiti, step-by-step con comandi, verifica finale, escalation
- Comandi copia-incollabili in blocchi PowerShell/bash
- Mappa runbook con frequenze
- Escalation path con contatti Acme e vendor
- Strumenti e accessi operativi (Appendice A)
- Checklist di validazione completa

---

## Tip & trucchi

### Per i comandi copia-incollabili
I comandi devono essere **pronti all'uso**: l'operatore deve poterli copiare e incollare con modifiche minime (sostituire solo i parametri variabili). Verifica che:
- Siano in blocchi di codice con syntax highlighting corretto (`powershell`, `bash`, ecc.)
- I placeholder siano evidenziati con `<>` (es. `<hostname>`, `<IP>`)
- I commenti spieghino ogni passo
- Le variabili siano dichiarate all'inizio dello script

### Per le procedure DR
La procedura DR (RB-DR-001) è la più critica. Verifica che:
- Sia divisa in 5 fasi chiare (Attivazione, Avvio sito DR, Reindirizzamento traffico, Verifica, Comunicazione)
- I tempi stimati per ogni fase siano realistici
- RTO e RPO target siano ripetuti più volte nel documento
- L'escalation al Crisis Manager sia chiara

### Per coerenza con As-Built
Tutti gli hostname, IP, e configurazioni nel SOP DEVONO corrispondere a quanto dichiarato nell'As-Built. Verifica che:
- I server citati (FILE-SRV-01, DC-01, DC-02, ecc.) esistano nell'inventario As-Built
- Gli IP management siano corretti
- I nomi dei job di backup siano coerenti con l'As-Built §9.1

### Per testabilità delle procedure
Ogni procedura deve essere testabile in ambiente di test o con impatto minimo. Verifica che:
- Le procedure L1 siano eseguibili senza impatto produzione
- Le procedure L2/L3 indichino chiaramente l'impatto e la finestra consigliata
- Le procedure distruttive (RB-006 firmware storage) indichino i prerequisiti di snapshot/backup

### Per lingua e tono
Il manuale operativo è rivolto a tecnici italiani. Mantieni:
- Italiano per il body e le spiegazioni
- Inglese per i comandi e i termini tecnici (hostname, IPs, parametri)
- Tono diretto, non accademico
- Frasi brevi e azioni chiare

### Per versioning delle procedure
Le procedure operative cambiano nel tempo. Verifica che:
- Ogni procedura abbia un ID univoco (RB-xxx) stabile nel tempo
- La `version` del documento si incrementi a ogni modifica sostanziale
- Le modifiche sostanziali siano tracciate in una sezione "Changelog" (puoi aggiungerla)
