---
okf_version: "0.2"
id: "guide-<project_slug>-rollback-01"
title: "Rollback Plan — <titolo progetto, es. Deploy Infrastruttura DC Milano>"
type: "guide"
domain: "IT Infrastructure & Contingency Planning"
tags: ["okf-v0.2", "rollback", "contingency", "fallback", "fase-3", "disaster-recovery"]

# Metadati estesi IT (preservati dal parser come rawFrontmatter)
project_id: "<PROJECT_ID>"
project_name: "<nome progetto>"
site: "<SITE_CODE>"
customer: "<cliente>"
phase: 3
author: "<nome>"
reviewer: "<nome>"
approver: "<nome>"
owner_team: "<team>"
status: "draft"
version: "0.1"
created_at: "<YYYY-MM-DD>"
updated_at: "<YYYY-MM-DD>"
related_docs:
  - "guide-<project_slug>-mop-01"
  - "architecture-<project_slug>-lld-01"
  - "architecture-<project_slug>-asbuilt-01"
depends_on:
  - "guide-<project_slug>-mop-01"
supersedes: null
superseded_by: null
classification: "confidential"
retention: "7y"
lang: "it"

entities:
  - name: "Rollback Trigger"
    type: "concept"
    description: "Condizione oggettiva e misurabile che attiva la procedura di ripristino"
  - name: "No-Return Point"
    type: "concept"
    description: "Punto dell'intervento oltre il quale il rollback non è più sicuro o possibile"
  - name: "Baseline Snapshot"
    type: "pattern"
    description: "Snapshot dello stato pre-intervento con hash SHA256 per verifica integrità"
  - name: "Decision Authority"
    type: "pattern"
    description: "Catena di autorità per approvare l'attivazione del rollback (Tech Lead → PM → Sponsor)"

relations:
  - targetTitle: "MOP — Method of Procedure"
    targetId: "guide-<project_slug>-mop-01"
    relationType: "depends_on"
    weight: 1.0
    description: "Il Rollback definisce le procedure inverse per ogni fase del MOP"
  - targetTitle: "LLD — Low-Level Design"
    targetId: "architecture-<project_slug>-lld-01"
    relationType: "references"
    weight: 0.85
    description: "Lo stato baseline pre-intervento fa riferimento all'LLD approvato"
  - targetTitle: "As-Built Documentation"
    targetId: "architecture-<project_slug>-asbuilt-01"
    relationType: "references"
    weight: 0.8
    description: "In caso di rollback parziale, l'As-Built documenta lo stato effettivamente raggiunto"
---

<!-- AI-INSTRUCTIONS:
  Ruolo: definire le procedure di ripristino per annullare le modifiche e tornare allo stato precedente.
  Input attesi: MOP approvato, snapshot/backup dello stato pre-intervento, runbook vendor.
  Regole di compilazione:
    1. Per ogni step del MOP, definire la procedura inversa corrispondente.
    2. Definire CHIARAMENTE i trigger che attivano il rollback (criteri oggettivi, non opinioni).
    3. Indicare chi ha l'autorità per decidere il rollback (Decision Authority).
    4. Specificare il tempo massimo entro cui è possibile eseguire rollback con successo.
    5. Definire i punti di non-ritorno (no-return points) oltre i quali il rollback non è più sicuro.
    6. Dettagliare le verifiche post-rollback per confermare il ripristino.
    7. Pianificare le comunicazioni a stakeholder durante l'evento.
    8. Registrare le differenze tra stato pre-intervento e stato post-rollback per audit.
    9. In `depends_on` deve figurare il MOP.
    10. Validare la checklist in fondo prima di `status: in-review`.
-->

# Rollback / Fallback Plan

**Progetto:** `<project_name>`
**Cliente:** `<customer>`
**Sito:** `<site>`
**Versione documento:** `<version>`
**Stato:** `<status>`

## 1. Scopo del Documento

Il presente piano definisce le procedure operative per annullare le modifiche apportate durante l'intervento descritto in [[04-MOP]] e ripristinare l'infrastruttura allo stato operativo precedente (snapshot di riferimento: §3).

L'obiettivo è minimizzare l'impatto su utenza e servizi qualora si manifestino criticità bloccanti durante il deploy.

## 2. Trigger di Rollback

Il rollback viene attivato quando SI VERIFICA ALMENO UNO dei seguenti eventi:

### 2.1 Trigger Tecnici

| ID | Condizione | Soglia | Rilevamento |
|----|-----------|--------|-------------|
| TR-01 | Servizio pubblico non accessibile | > 30 min da cutover | Monitor esterno (Pingdom/UptimeRobot) |
| TR-02 | Tasso di errore 5xx superiore | > 5% in 15 min | SIEM / APM |
| TR-03 | Latenza media HTTP | > 2s per 15 min | APM |
| TR-04 | Errore di configurazione bloccante non risolvibile on-site | Immediato | Esito Gate |
| TR-05 | Failover cluster hypervisor non riuscito | Dopo 3 tentativi | Logs hypervisor |
| TR-06 | Storage replication fallita | RPO > target x3 | Storage console |
| TR-07 | Penetration test rivela vulnerabilità critica (CVSS ≥ 9) | Immediato | Report pen-test |
| TR-08 | Data corruption verificato | Immediato | Checksum/validate |

### 2.2 Trigger Operativi
- TR-09: Finestra di manutenzione superata oltre tolleranza massima (MOP §4)
- TR-10: Comunicazione cliente/sponsor che richiede sospensione
- TR-11: Indisponibilità di membri chiave della squadra per eventi esterni

### 2.3 Trigger di Sicurezza
- TR-12: Sospetto compromissione in corso (indicatori di attacco attivo)
- TR-13: Violazione dati confermata o sospetta

## 3. Stato di Riferimento (Baseline Pre-Intervento)

### 3.1 Snapshot Configurazioni

| Componente | Snapshot ID | Data | Location | Verifica integrità |
|-----------|-------------|------|----------|---------------------|
| fw-01/02 | `<snap_id>` | `<YYYY-MM-DD HH:MM>` | `vault://backups/fw/` | SHA256 `<...>` |
| sw-core-01/02 | `<snap_id>` | `<YYYY-MM-DD HH:MM>` | `vault://backups/sw-core/` | SHA256 `<...>` |
| sw-tor-01/02 | `<snap_id>` | `<YYYY-MM-DD HH:MM>` | `vault://backups/sw-tor/` | SHA256 `<...>` |
| stor-01 config | `<snap_id>` | `<YYYY-MM-DD HH:MM>` | `vault://backups/stor/` | SHA256 `<...>` |
| hypervisor SRV-01/02/03 | `<snap_id>` | `<YYYY-MM-DD HH:MM>` | `vault://backups/hv/` | SHA256 `<...>` |
| VM DC/DNS | `<vm_backup_id>` | `<YYYY-MM-DD HH:MM>` | backup appliance bkp-01 | SHA256 `<...>` |

### 3.2 Stato di Rete Documentato

| Indirizzo | Hostname | Stato pre-intervento |
|-----------|----------|---------------------|
| `<IP pubblico vecchio>` | `<hostname>` | Diretto a server legacy |
| `<DNS A record>` | `<fqdn>` | TTL 300s, valore `<IP vecchio>` |
| `<BGP route>` | — | ASN primario `<...>`, preferenza 100 |

## 4. Decision Authority

### 4.1 Autorità Decisionali

| Ruolo | Persona | Autorità | Contatto |
|-------|---------|---------|----------|
| Tech Lead | `<nome>` | Può proporre rollback | `<phone>` |
| PM | `<nome>` | Può autorizzare rollback fino a GATE-6 | `<phone>` |
| Sponsor | `<nome>` | Può autorizzare rollback post-cutover | `<phone>` |
| Crisis Manager | `<nome>` | Override per situazioni critiche (DR) | `<phone>` |

### 4.2 Catena Decisionale
1. Rilevamento trigger da chiunque → segnalazione a `<Tech Lead>`
2. `<Tech Lead>` valuta entro `<15 min>` → proposta formale a `<PM>`
3. `<PM>` decide entro `<30 min>` (oppure `<Sponsor>` se oltre GATE-6)
4. Comunicazione START rollback a tutti gli stakeholder (canale §6)
5. Esecuzione rollback (sequenza §7)
6. Verifica post-rollback (§8)
7. Decisione formale: mantenere stato precedente o pianificare retry

## 5. Punti di Non-Ritorno (No-Return Points)

| Punto | Quando | Perché non ritornabile | Azione alternativa |
|-------|--------|------------------------|---------------------|
| NRP-1 | Dopo GATE-4 (storage config) | Dati su storage nuovo | Ripristinare da backup legacy |
| NRP-2 | Dopo GATE-6 (pre-cutover) | Snapshot baseline non più applicabile ai nuovi dati | Migrazione dati reversibile via export/import |
| NRP-3 | Dopo GATE-7 (cutover) | Servizi già esposti su nuova infrastruttura, utenti hanno avuto accesso | Rollback DNS + riallineamento dati bidirezionale |

**Oltre NRP-3 il rollback è possibile solo con piano di migrazione dati specifico: consultare `<Crisis Manager>`.**

## 6. Comunicazioni durante Rollback

| Quando | Canale | Mittente | Destinatari | Contenuto |
|--------|--------|----------|-------------|-----------|
| T-0 (decisione) | chat + email | `<PM>` | Sponsor, NO, utenti | "Rollback IN CORSO — motivazione breve" |
| Ogni 30 min | chat | `<Tech Lead>` | PM, Sponsor | Stato avanzamento rollback |
| T-end | chat + email | `<PM>` | Sponsor, NO, utenti | "Rollback COMPLETATO — stato ripristinato" |
| T+24h | email | `<Tech Lead>` | Sponsor, NO | Post-mortem report con RCA |

## 7. Sequenza Operativa di Rollback

### 7.1 Rollback per Fase MOP

Per ogni fase del MOP (A-I), la procedura di rollback inversa è la seguente:

#### Rollback Fase H (Cutover) — ROLL-H
| Step | Attività | Durata | Owner | Verifica |
|------|----------|--------|-------|---------|
| ROLL-H.1 | Notifica rollback agli utenti | 0.1h | `<PM>` | Acknowledged |
| ROLL-H.2 | Restore DNS pubblico → IP vecchio | 0.25h | `<Sysadmin>` | Resolve test OK |
| ROLL-H.3 | Restore BGP route pref. | 0.25h | `<Net Eng>` | Routing table OK |
| ROLL-H.4 | Verifica servizi legacy UP | 1h | `<QA>` | Health-check PASS |

#### Rollback Fase G (Verifiche Pre-Cutover) — ROLL-G
| Step | Attività | Durata | Owner | Verifica |
|------|----------|--------|-------|---------|
| ROLL-G.1 | Disattiva tunnel VPN/replica nuovi | 0.25h | `<Net Eng>` | Tunnel down |
| ROLL-G.2 | Pulizia snapshot di test | 0.25h | `<Storage Eng>` | No snapshot test |

#### Rollback Fase F (Virtualizzazione) — ROLL-F
| Step | Attività | Durata | Owner | Verifica |
|------|----------|--------|-------|---------|
| ROLL-F.1 | Shutdown VM nuove | 0.5h | `<Hypervisor Eng>` | VM spente |
| ROLL-F.2 | Remove host da cluster CL-PROD-01 | 0.5h | `<Hypervisor Eng>` | Cluster ridotto |
| ROLL-F.3 | Reinstall hypervisor da baseline | 2h | `<Hypervisor Eng>` | Host ready (legacy) |

#### Rollback Fase E (Storage) — ROLL-E
| Step | Attività | Durata | Owner | Verifica |
|------|----------|--------|-------|---------|
| ROLL-E.1 | Stop replication verso DR | 0.1h | `<Storage Eng>` | Replica down |
| ROLL-E.2 | Unmount LUN dagli host | 0.5h | `<Storage Eng>` | LUN unmounted |
| ROLL-E.3 | Restore config storage da snapshot | 0.5h | `<Storage Eng>` | Config match SHA256 |

#### Rollback Fase D (Rete) — ROLL-D
| Step | Attività | Durata | Owner | Verifica |
|------|----------|--------|-------|---------|
| ROLL-D.1 | Restore config firewall da snapshot | 0.25h | `<Sec Eng>` | Config match SHA256 |
| ROLL-D.2 | Restore config switch ToR | 0.25h | `<Net Eng>` | Config match SHA256 |
| ROLL-D.3 | Restore config switch core | 0.25h | `<Net Eng>` | Config match SHA256 |
| ROLL-D.4 | Verifica routing e reachability legacy | 0.5h | `<Net Eng>` | Test PASS |

#### Rollback Fase C (Cablaggio) — ROLL-C
- Generalmente non necessario disfare il cablaggio: lasciare cavi in loco, smarcare etichette e registrare come "spare" se l'infrastruttura legacy verrà rimossa in fase successiva.
- **Solo se richiesto da cliente**: smontare cavi e restituire patch panel.

#### Rollback Fase B (Installazione fisica) — ROLL-B
- Mantenere hardware montato (spento) per eventuale retry.
- In caso di decisione di rimozione completa: pianificare activity di smontaggio dedicata.

### 7.2 Tempo Massimo di Rollback

| Fase | Tempo massimo rollback |
|------|------------------------|
| H (Cutover) | ≤ 2 ore |
| G + F + E + D | ≤ 4 ore |
| Totale dal cutover a stato baseline | ≤ 6 ore |

## 8. Verifiche Post-Rollback

Dopo aver completato la sequenza di rollback, verificare che lo stato sia coerente con la baseline §3:

### 8.1 Verifiche Tecniche

| ID | Verifica | Metodo | Esito atteso | Owner |
|----|----------|--------|--------------|-------|
| VPR-01 | Servizi pubblici raggiungibili | HTTP/HTTPS check da 3 locazioni esterne | 200 OK | `<QA>` |
| VPR-02 | Routing conforme a baseline | `show ip route` comparato | Match | `<Net Eng>` |
| VPR-03 | Config apparati = snapshot | Diff SHA256 | Match | `<Tech Lead>` |
| VPR-04 | Backup legacy funzionante | Restore test di 1 file random | OK | `<Sysadmin>` |
| VPR-05 | DNS pubblico risolve legacy | dig/nslookup | `<IP vecchio>` | `<Sysadmin>` |
| VPR-06 | SLA monitoring attivo | Sensori UP | 100% | `<NOC>` |

### 8.2 Verifiche Funzionali (business)
- [ ] Login applicativi possibile per utenti test
- [ ] Transazioni di esempio completate con successo
- [ ] Reportistica giornaliera generata correttamente
- [ ] Integrazioni esterne (API) funzionanti

### 8.3 Verifiche di Sicurezza
- [ ] Log security coerenti con baseline
- [ ] Nessun allarme IDS/IPS nuovo
- [ ] Sessioni utente attive coerenti

## 9. Documentazione Post-Rollback

### 9.1 Post-Mortem Report

Devono essere compilati entro 72 ore dalla conclusione del rollback:

| Sezione | Contenuto | Owner |
|---------|-----------|-------|
| Timeline | Eventi chiave con timestamp | `<Tech Lead>` |
| Root Cause Analysis (RCA) | Causa radice del fallimento | `<Tech Lead>` + `<vendor>` |
| Differenze vs baseline | Elementi non ripristinati o alterati | `<QA>` |
| Costo dell'evento | Ore lavoro, materiale, business impact | `<PM>` |
| Azioni correttive | Piani per evitare ripetizione | `<Tech Lead>` |
| Decisione retry | Sì/no, quando, piano aggiornato | `<PM>` + `<Sponsor>` |

### 9.2 Aggiornamento Documenti Correlati

- [ ] Aggiornare [[04-MOP]] con lezioni apprese
- [ ] Aggiornare [[06-As-Built]] solo se parzialmente completato
- [ ] Creare documento "Post-Mortem Rollback `<data>`" e linkarlo in `related_docs`

## 10. Differenze Pre/Post Rollback (Audit)

Elenco delle eventuali differenze residue rispetto allo stato pre-intervento. Devono essere approvate da `<Sponsor>` prima di considerare chiuso l'evento:

| ID | Componente | Differenza | Motivo | Approvazione |
|----|-----------|-----------|--------|--------------|
| DIFF-001 | `<es. cavi di rete nuovi lasciati in loco (spenti)>` | `<cablaggio spare aggiunto>` | `<costo di smontaggio non giustificato>` | `<Sponsor nome>` in data `<...>` |
| DIFF-002 | `<...>` | `<...>` | `<...>` | `<...>` |

## 11. Riferimenti e Documenti Correlati

- MOP: [[04-MOP]]
- LLD: [[03-LLD]]
- As-Built: [[06-As-Built]] (se compilato parzialmente)

## Appendice A — Snippet Operativi per il Rollback

### A.1 Restore config firewall (vendor-agnostic)
```bash
# Recupera snapshot da vault
vault pull vault://backups/fw/fw-01-<snap_id>.cfg
# Verifica integrità
sha256sum fw-01-<snap_id>.cfg
# Restore su apparato (via SSH/API)
fw-cli restore --file fw-01-<snap_id>.cfg --confirm
# Verifica
fw-cli show config | diff - fw-01-<snap_id>.cfg
```

### A.2 Restore DNS pubblico (Route 53 / Azure DNS / ecc.)
```bash
# Save current (per audit)
dns-cli record get --name <fqdn> --type A > /tmp/dns-after-rollback.json
# Restore
dns-cli record set --name <fqdn> --type A --value <IP legacy> --ttl 300
# Verify
dig +short <fqdn> @8.8.8.8
```

### A.3 Shutdown pulito VM nuove
```bash
# Lista VM create durante il deploy
vm-cli list --cluster CL-PROD-01 --created-after "<deploy-start-time>" \
  > /tmp/vm-to-shutdown.txt
# Shutdown graceful
for vm in $(cat /tmp/vm-to-shutdown.txt); do
  vm-cli shutdown --name $vm --timeout 300
done
# Verify
vm-cli list --state running --cluster CL-PROD-01
```

## Appendice B — Acronimi

| Acronimo | Espansione |
|----------|------------|
| RCA | Root Cause Analysis |
| NRP | No-Return Point |
| TR | Trigger |
| GATE | Punto di verifica intermedia (MOP) |
| DR | Disaster Recovery |
| SHA | Secure Hash Algorithm |

---

## Checklist di Validazione

- [ ] Trigger oggettivi e misurabili (almeno 10)
- [ ] Decision Authority chiaramente identificata con SLA
- [ ] Punti di non-ritorno (NRP) definiti e spiegati
- [ ] Snapshot baseline documentati con hash di verifica
- [ ] Per ogni fase del MOP esiste la procedura inversa
- [ ] Tempo massimo di rollback stimato per ogni fase
- [ ] Verifiche post-rollback tecniche e funzionali
- [ ] Piano comunicazioni durante rollback
- [ ] Template post-mortem incluso
- [ ] Tabella differenze pre/post (audit) presente
- [ ] `depends_on` contiene MOP
