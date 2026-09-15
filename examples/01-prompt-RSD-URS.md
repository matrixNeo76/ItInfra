# Esempio prompt — RSD/URS (Requirements Specification Document)

Scenario: progetto di sostituzione infrastruttura datacenter legacy per cliente mid-market.

---

## Scenario di esempio

- **Cliente**: Acme S.p.A. (cliente manifatturiero, 600 dipendenti, sede a Milano)
- **Sito**: MIL-01 — Datacenter Milano, via Verdi 10
- **Progetto**: Sostituzione completa infrastruttura datacenter legacy (server, storage, networking) con stack moderno HA
- **Driver**: hardware in end-of-life, costo manutenzione crescente, necessità SLA 99.9%, compliance GDPR

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un system engineer senior specializzato in infrastrutture IT enterprise.
Il tuo compito è compilare il template RSD/URS (Requirements Specification Document)
partendo dai dati forniti in questo prompt.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md se sei Claude Code)
2. Leggi /download/templates/00-INDEX.md
3. Conferma di averli letti con un riepilogo di 3 righe

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01
- customer: Acme S.p.A.
- author: Mario Rossi (System Engineer, Integratore)
- reviewer: Giulia Bianchi (Tech Lead)
- approver: Luca Verdi (Sponsor Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — RSD/URS

### Contesto e obiettivi business
- Sostituire infrastruttura datacenter esistente (Dell R730xd, HPE MSA 2040, Cisco Catalyst 2960) in end-of-life
- Driver di business: ridurre TCO del 25% in 36 mesi, migliorare SLA a 99.9%, conformità GDPR
- Vincolo: budget approvato 180k€ (capex), 25k€/anno (opex)

### Stakeholder
- Sponsor: Luca Verdi (CFO Acme)
- PM: Mario Rossi (Integratore)
- Tech Lead: Giulia Bianchi (Integratore)
- Security Officer: Anna Neri (Acme CISO)
- NO Lead: Marco Conti (Acme Operations)

### Requisiti funzionali (input utente)
- RF-001: integrazione con Active Directory esistente (dominio acme.local)
- RF-002: supporto quota storage per dipartimento
- RF-003: esposizione API REST per monitoring (Prometheus-compatible)
- RF-004: gestione centralizzata backup con deduplicazione
- RF-005: supporto VM Windows Server e Linux
- RF-006: gestione storage multi-protocollo (iSCSI, NFS, SMB3)
- RF-007: rete SD-WAN per connessione a 3 sedi remote

### Requisiti non funzionali
- SLA disponibilità: 99.9%
- RTO sistemi mission-critical: ≤ 4h
- RPO sistemi mission-critical: ≤ 1h
- RTO file server: ≤ 24h
- RPO file server: ≤ 12h
- Capacità storage iniziale: 30 TB (crescita 20% annua)
- Compute: 3 nodi hypervisor, ~50 VM previste anno 1
- Throughput rete LAN: 10 Gbps minimo ToR

### Compliance
- GDPR (trattamento dati clienti)
- ISO/IEC 27001 (certificazione aziendale Acme)

### Sito di DR
- Sito secondario: Bergamo (BG-01), distanza 60 km
- Capacità: 1 rack, link WAN 1 Gbps dedicato

### Criteri di accettazione
- SLA misurato per 30 giorni consecutivi ≥ 99.9%
- DR test con RTO ≤ 4h e RPO ≤ 1h
- Pen-test annuale senza vulnerabilità critiche
- Formazione team Acme completata

## TEMPLATE DA COMPILARE

Template path: /download/templates/01-RSD-URS.md
Tipo documento: RSD-URS
Fase: 1

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter del template
- Rispetta TUTTE le regole elencate
- Sostituisci TUTTI i placeholder <...> con valori reali
- NON inventare requisiti non forniti: usa <DA-RICHIEDERE> e segnala in Open Issues

## DOCUMENTI CORRELATI (depends_on)

Nessun documento depends_on per questo template (è il primo del ciclo).
In related_docs, indicare placeholder per i documenti che verranno generati:
- 02-HLD (da compilare)
- 04-MOP (da compilare)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft
- Versione: 0.1
- NO password in chiaro
- ID documento: specification-acme-milano-rsd-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe)
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/01-RSD-URS.md
   - ID: specification-acme-milano-rsd-01

Compila il documento ora.
```

---

## Output atteso

L'agente dovrebbe restituire un documento RSD/URS completo con:

- Frontmatter YAML popolato (id: `specification-acme-milano-rsd-01`, project_id, status: draft, related_docs con placeholder per HLD e MOP)
- Tutte le 12 sezioni compilate
- Tabelle requisiti con ID univoci (RF-001..RF-007, RNF-xxx)
- Requisiti non funzionali quantificati (RTO/RPO, capacità, SLA)
- Compliance GDPR e ISO 27001 spuntate
- Criteri di accettazione mappati a test futuri
- Stakeholder con ruoli e contatti
- Sezione Open Issues (se mancano dati)
- Checklist di validazione completa

---

## Tip & trucchi

### Per ottenere requisiti più precisi
Se i requisiti forniti sono vaghi, chiedi all'agente di **proporre requisiti aggiuntivi** basati sul contesto, specificando che vanno approvati:

```text
Per i requisiti non funzionali dove mancano dettagli, proponi valori ragionevoli
basati su best practice per clienti mid-market manifatturieri. Marca ogni proposta
con [PROPOSTA - DA APPROVARE] in modo che io possa validarla.
```

### Per gestire più stakeholder
Se il cliente ha molti stakeholder, fornisci all'agente una tabella strutturata invece di una lista:

```text
Stakeholder:
| Ruolo | Nome | Org | Email | Responsabilità |
| Sponsor | Luca Verdi | Acme CFO | luca.verdi@acme.it | Budget |
| PM | Mario Rossi | Integratore | m.rossi@integ.it | Coordinamento |
| ...
```

### Per progetti complessi
Se il progetto ha many compliance framework (GDPR + ISO 27001 + NIS2 + DORA), forniscili in lista e chiedi all'agente di documentare per ognuno le implicazioni specifiche nella sezione §6 del template.
