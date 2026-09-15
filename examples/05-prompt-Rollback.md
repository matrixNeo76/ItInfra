# Esempio prompt — Rollback / Fallback Plan

Scenario: piano di ripristino in caso di criticità bloccanti durante il deploy.

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: RSD/URS, HLD, LLD, MOP
- **Obiettivo**: definire le procedure di rollback per annullare le modifiche e tornare allo stato precedente

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un technical lead specializzato in contingency planning per interventi IT.
Il tuo compito è compilare il template Rollback/Fallback Plan, definendo:
- trigger oggettivi per attivare il rollback
- punti di non-ritorno (NRP) oltre i quali il rollback non è più sicuro
- procedure di ripristino passo-passo per ogni fase del MOP
- verifiche post-rollback per confermare il ripristino

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - MOP: /vault/projects/acme-milano-2026/04-MOP.md (id: guide-acme-milano-mop-01)
   - LLD: /vault/projects/acme-milano-2026/03-LLD.md (id: architecture-acme-milano-lld-01)
4. Concentrati sulle 9 fasi del MOP (A-I) e sui 7 gate (GATE-1 a GATE-7)

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (Tech Lead)
- reviewer: Giulia Bianchi
- approver: Luca Verdi (Sponsor Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — Rollback Plan

### Stato pre-intervento (baseline per il rollback)
- Infrastruttura legacy ancora operativa:
  - Server: 3x Dell R730xd (vecchi, ma funzionanti)
  - Storage: HPE MSA 2040
  - Switch: Cisco Catalyst 2960
  - VM in produzione: 28 VM su VMware ESXi 6.7
- DNS pubblico: A record app.acme.it → IP pubblico 1.2.3.4 (vecchio firewall)
- BGP route: ASN 65500, preferenza primaria via ISP-A
- Backup: Veeam su HPE StoreOnce (vecchio appliance)

### Snapshot baseline pre-intervento (già esistenti)
- Config firewall vecchio: vault://backups/legacy/fw-old-<snap_id>.cfg (SHA256: abc123...)
- Config switch vecchi: vault://backups/legacy/sw-old-<snap_id>.cfg
- VM backup: ultimo backup Veeam del 2026-03-15 (28 VM, 1.2 TB totali)
- DNS pubblico: export zone file in data 2026-03-09

### Decision authority
- Tech Lead (Mario Rossi): può proporre rollback
- PM (Mario Rossi): può autorizzare rollback fino a GATE-6
- Sponsor (Luca Verdi): può autorizzare rollback post-cutover
- Crisis Manager (Anna Neri, CISO Acme): override per situazioni critiche (DR)

### Comunicazioni durante rollback
- Canale: Teams "ACME-Milano-Deploy-2026"
- Email: deploy@acme.it + crisis@acme.it
- Utenti: comunicazione via email all-news@acme.it

### Vincoli / note
- Il rollback oltre NRP-3 (post-cutover) richiede piano di migrazione dati specifico
- In caso di compromissione confermata: attivare immediatamente DR plan (vedi SOP)
- Tolleranza massima finestra manutenzione: +4 ore oltre le 18:00 del giorno 3

## TEMPLATE DA COMPILARE

Template path: /download/templates/05-Rollback.md
Tipo documento: Rollback
Fase: 3

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Per ogni step del MOP, definire la procedura inversa
  * Trigger oggettivi e misurabili (no "se sembra che non funziona")
  * Decision Authority chiaramente identificata con SLA
  * Punti di non-ritorno (NRP) definiti e spiegati
  * Snapshot baseline con hash di verifica
  * Tempo massimo di rollback stimato per ogni fase
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [guide-acme-milano-mop-01]
- related_docs del nuovo Rollback:
  - guide-acme-milano-mop-01
  - architecture-acme-milano-lld-01
  - architecture-acme-milano-asbuilt-01 (placeholder)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft
- Versione: 0.1
- ID documento: guide-acme-milano-rollback-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe)
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/05-Rollback.md
   - ID: guide-acme-milano-rollback-01

Compila il documento ora.
```

---

## Output atteso

Documento Rollback Plan completo con:

- Scopo del documento chiaro
- Almeno 12 trigger oggettivi e misurabili (TR-01 a TR-12), suddivisi in tecnici/operativi/sicurezza
- Stato di riferimento (baseline pre-intervento) con snapshot e hash SHA256
- Decision Authority con catena decisionale (Tech Lead → PM → Sponsor → Crisis Manager)
- 3 punti di non-ritorno (NRP-1, NRP-2, NRP-3) chiaramente spiegati
- Piano comunicazioni durante rollback (T-0, ogni 30min, T-end, T+24h)
- Sequenza operativa di rollback per ogni fase del MOP (ROLL-H, ROLL-G, ROLL-F, ROLL-E, ROLL-D, ROLL-C, ROLL-B)
- Tempo massimo di rollback per fase
- Verifiche post-rollback tecniche (VPR-01 a VPR-06), funzionali e di sicurezza
- Post-mortem report template (RCA, differenze vs baseline, costo, azioni correttive)
- Tabella differenze pre/post rollback (audit)
- Appendice A: snippet operativi per restore config firewall, restore DNS pubblico, shutdown VM
- Checklist di validazione completa

---

## Tip & trucchi

### Per trigger oggettivi
Verifica che ogni trigger abbia:
- Una **soglia misurabile** (es. "> 30 min", "> 5% errori", "CVSS ≥ 9")
- Un **rilevamento automatico** (monitoring system, SIEM, APM)
- Non lasciare trigger vaghi come "se il sistema non funziona bene"

### Per coerenza con il MOP
Il Rollback DEVE coprire tutte le fasi del MOP. Verifica che per ogni fase A-I del MOP ci sia una procedura ROLL-X corrispondente.

### Per snapshot baseline
Gli snapshot baseline devono avere hash SHA256 verificabili. Se non hai l'hash, chiedi all'agente di proporre il comando per calcolarlo:

```text
Per ogni snapshot baseline, includi nel documento il comando shell per calcolare
l'hash SHA256 (es. sha256sum su Linux, Get-FileHash su PowerShell).
```

### Per i punti di non-ritorno
I NRP sono il momento in cui il rollback diventa problematico. Verifica che:
- Siano chiaramente identificati (es. "dopo GATE-4 storage config")
- Spieghino perché non è più sicuro tornare indietro
- Indichino un'azione alternativa (es. "ripristinare da backup legacy")

### Per progetti senza rollback possibile
Se il rollback non è tecnicamente possibile (es. migrazione dati one-way), il piano dovrebbe essere onesto e dichiarare:
- Quali fasi sono irreversibili
- Qual è il piano B in caso di fallimento (es. DR plan, ripristino da backup esterno)
- Quando attivare il Crisis Manager

### Validazione
Dopo la generazione, valida con:
```text
Verifica la coerenza tra questo Rollback Plan e il MOP: ogni fase del MOP deve avere
una procedura inversa corrispondente. Elenca eventuali fasi MOP senza rollback associato.
```
