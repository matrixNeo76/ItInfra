# Esempio prompt — MOP (Method of Procedure)

Scenario: piano operativo passo-passo per l'intervento di deploy.

---

## Scenario di esempio

- **Progetto**: acme-milano-2026
- **Documento precedente già compilato**: RSD/URS, HLD, LLD
- **Obiettivo**: definire la sequenza operativa dell'intervento (chi fa cosa, quando, con quali verifiche)

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un project manager + technical lead specializzato in interventi IT complessi.
Il tuo compito è compilare il template MOP (Method of Procedure) partendo dall'LLD
già approvato.

Il MOP descrive la sequenza operativa passo-passo dell'intervento di deploy,
con finestre di manutenzione, responsabilità (RACI), gate di verifica intermedia,
comunicazioni e piano di rollback.

Prima di iniziare:
1. Leggi /download/templates/AGENTS.md (o CLAUDE.md)
2. Leggi /download/templates/00-INDEX.md
3. Leggi i documenti già compilati:
   - RSD/URS: /vault/projects/acme-milano-2026/01-RSD-URS.md
   - HLD: /vault/projects/acme-milano-2026/02-HLD.md
   - LLD: /vault/projects/acme-milano-2026/03-LLD.md
4. Conferma con un riepilogo di 5 righe dei componenti principali da installare

## INPUT DATI — Progetto

- project_id: acme-milano-2026
- project_name: Sostituzione Infrastruttura Datacenter Milano
- site: MIL-01 (Datacenter Milano, via Verdi 10)
- customer: Acme S.p.A.
- author: Mario Rossi (PM + Tech Lead)
- reviewer: Giulia Bianchi (Tech Lead)
- approver: Luca Verdi (Sponsor Acme)
- owner_team: Acme Operations

## DATI SPECIFICI — MOP

### Squadra tecnica
- Mario Rossi (Tech Lead, integratore) — coordina e supervisiona
- Giulia Bianchi (Network Engineer, integratore) — switch, firewall, routing
- Carlo Neri (Storage Engineer, integratore) — storage, backup
- Sara Villa (Hypervisor/Sysadmin, integratore) — vSphere, VM, AD
- Marco Conti (NO Acme) — presa in carico, testing utente
- Anna Neri (CISO Acme) — review security

### Finestra di manutenzione
- Inizio: 2026-03-16 08:00 (Europe/Rome, lunedì)
- Fine prevista: 2026-03-18 18:00 (mercoledì)
- Durata stimata: 3 giorni (24h lavoro)
- Tolleranza massima: +4 ore
- Cutover: sera del giorno 3 (2026-03-18 20:00-23:00)
- Impatto utenti: nessuno giorni 1-2 (sala server offline per ops), ridotto giorno 3 (cutover)

### Prerequisiti (verificati T-7gg)
- Hardware ricevuto e staged (firmware aggiornato a banco)
- Credenziali admin in vault: vault://it/acme-milano-2026/
- Licenze software caricate (VMware vSphere, NetApp ONTAP, FortiGate UTM, Veeam)
- Accesso fisico al sito: badge nominale rilasciato da Acme Facility
- Jump host: VPN aziendale integratore + MFA
- Backup configurazioni esistenti (vecchio DC) completato in data 2026-03-09
- Comunicazione utenti inviata T-7gg

### Comunicazioni
- Canale chat emergenze: Teams "ACME-Milano-Deploy-2026"
- Email distribuzione: deploy@acme.it
- War room fisica: sala riunioni Acme Milano, via Verdi 10, piano 1

### Criteri di blocco / rollback (richiamo a Rollback Plan separato)
- Servizio pubblico down > 30 min dal cutover → rollback
- Tasso errore 5xx > 5% in 15 min → rollback
- Vuln critica emersa durante pen-test → rollback
- Rollback plan completo: /vault/projects/acme-milano-2026/05-Rollback.md

### Output attesi
- Infrastruttura installata fisicamente e cablata (certificata)
- Configurazioni caricate su tutti gli apparati
- Cluster hypervisor operativo, VM base (DC, DNS, NTP) attive
- Repliche storage verso DR (BG-01) attive
- Cutover eseguito con esito positivo
- Documento As-Built compilato e approvato
- Verbale di collaudo (ATP) firmato
- Handover al team Acme firmato

## TEMPLATE DA COMPILARE

Template path: /download/templates/04-MOP.md
Tipo documento: MOP
Fase: 3

- Leggi attentamente il blocco <!-- AI-INSTRUCTIONS --> nel frontmatter
- Rispetta TUTTE le regole, in particolare:
  * Ogni step ha: ID univoco, descrizione, durata, owner, prereq, output atteso
  * Indicare la finestra di manutenzione (inclusi fusi orari)
  * Definire i punti di verifica intermedia (gate)
  * In caso di bloccante, riferimento al [[05-Rollback]]
  * Matrice RACI per ogni fase significativa
- Sostituisci TUTTI i placeholder <...>

## DOCUMENTI CORRELATI (depends_on)

- depends_on: [architecture-acme-milano-lld-01, guide-acme-milano-rollback-01]
- related_docs del nuovo MOP:
  - specification-acme-milano-rsd-01
  - architecture-acme-milano-hld-01
  - architecture-acme-milano-lld-01
  - guide-acme-milano-rollback-01
  - architecture-acme-milano-asbuilt-01 (placeholder)

## VINCOLI DI OUTPUT

- Lingua: italiano (lang: it)
- Status: draft
- Versione: 0.1
- ID documento: guide-acme-milano-mop-01

## FORMATO DI OUTPUT ATTESO

Restituisci:
1. Documento completo in blocco Markdown (```markdown ... ```)
2. Riepilogo sintetico (3-5 righe)
3. Path e id suggeriti:
   - Path: /vault/projects/acme-milano-2026/04-MOP.md
   - ID: guide-acme-milano-mop-01

Compila il documento ora. Il documento sarà lungo (300+ righe).
```

---

## Output atteso

Documento MOP completo con:

- Obiettivo e scope dell'intervento
- Prerequisiti HW/LOG/OP completi
- Finestra di manutenzione con date, orari, fuso orario
- Matrice RACI per ogni attività chiave (Responsabile, Accountable, Consultato, Informato)
- Sequenza temporale in 9 fasi (A: Preparazione, B: Installazione fisica, C: Cablaggio, D: Configurazione rete, E: Storage, F: Virtualizzazione, G: Verifiche pre-cutover, H: Cutover, I: Post-cutover)
- Ogni step ha: ID, durata stimata, owner, prerequisiti, output atteso
- 7 gate di verifica intermedia (GATE-1 a GATE-7) con criteri di passaggio
- Piano comunicazioni (T-7gg, T-1gg, T-0 start, ogni gate, T+0 end, T+1gg post)
- Criteri di blocco e rollback richiamati
- Escalation path con SLA (L1 15min, L2 30min, L3 1h, L4 immediato)
- Modalità di accesso fisico/logico
- 8 output attesi quantificati
- Appendice A: pre-flight checklist + logbook template

---

## Tip & trucchi

### Per la stima delle durate
L'agente dovrebbe basarsi su best practice del settore. Se hai dati storici da progetti simili, forniscili:

```text
DURATE STIMATE DA PROGETTI SIMILI (riferimento):
- Mount server in rack: 30 min per unità
- Configurazione switch L3: 2h per unità
- Certificazione Fluke: 5 min per cavo rame, 15 min per fibra
- ...
```

### Per i gate di verifica
I gate sono critici: nessuno può procedere allo step successivo senza esito positivo. Verifica che ogni gate abbia:
- Un criterio di passaggio oggettivo e misurabile
- Un decision maker identificato
- Un'azione in caso di FAIL (generalmente: sospendere o rollback)

### Per la matrice RACI
Verifica che:
- Ogni attività abbia ESATTAMENTE un Accountable (più di uno = confusione)
- Il Responsible sia colui che esegue materialmente
- Il Consultato sia chi deve essere interpellato prima
- L'Informato sia chi deve sapere ma non decide

### Per progetti multi-site
Se l'intervento coinvolge più siti, includi nel prompt un'ulteriore sezione con i fusi orari:

```text
Siti coinvolti:
- MIL-01 (Milano) — Europe/Rome — installazione principale
- BG-01 (Bergamo) — Europe/Rome — sito DR, attivato solo in fase I (post-cutover)
- ROM-01 (Roma) — Europe/Rome — site remote via SD-WAN, attivato in fase successiva
```

### Per sicurezza operativa
Aggiungi al prompt eventuali vincoli di sicurezza aziendali:

```text
VINCOLI SICUREZZA OPERATIVA:
- Four-eyes principle per qualsiasi modifica a firewall/AD/storage
- Session recording attivo su jump host
- Tutti i comandi di config devono essere registrati in logbook (timestamp + operatore)
```
