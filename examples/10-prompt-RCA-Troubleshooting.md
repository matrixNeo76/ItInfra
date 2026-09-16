# Esempio prompt — RCA & Troubleshooting (Root Cause Analysis)

Scenario: risoluzione formale e post-mortem di un incidente tecnico post-go-live per il cliente.

---

## Scenario di esempio

- **Progetto**: `acme-milano-2026`
- **Documenti precedenti già compilati**: `03-LLD.md`, `06-As-Built.md`, `08-SOP-Runbook.md`
- **Obiettivo**: isolare l'anomalia con l'albero a 7 strati OSI (L1-L7), determinare la causa radice con i 5 Perché, applicare il fix definitivo e stilare il documento OKF v0.2 `10-RCA-INC-2026-001.md`.

---

## Prompt completo (copia e personalizza)

```text
## RUOLO E CONTESTO

Sei un Lead Infrastructure Architect & Troubleshooter specializzato in analisi post-mortem di disservizi di rete e sistemi.
Il tuo compito è compilare la scheda di Root Cause Analysis (RCA) secondo lo standard OKF v0.2, applicando il metodo rigorosamente deterministico a 7 strati OSI (L1-L7) e la tecnica dei 5 Perché.

Regole vincolanti:
1. STRICT GROUNDING: Divieto assoluto di inventare dati, log, orari o parametri tecnici. Se un dato non è noto, usa tassativamente <DA-RICHIEDERE>.
2. CREDENZIALI SICURE: Nessun secret in chiaro. Usa sempre riferimenti vault://it/projects/<slug>/...
3. FEED-FORWARD CAPA: Esplicita quali documenti di progetto (LLD, As-Built, Runbook, ATP) devono essere allineati.

Prima di iniziare:
1. Leggi AGENTS.md (o CLAUDE.md) e templates/00-INDEX.md
2. Consulta projects/acme-milano-2026/06-As-Built.md e 03-LLD.md

## INPUT DATI — Incidente

- ID Incidente: INC-2026-001
- Progetto / Slug: acme-milano-2026
- Cliente: Acme S.p.A.
- Data e Ora Rilevamento: 2026-03-24 09:15 CET
- Data e Ora Risoluzione: 2026-03-24 11:45 CET (Risolto in 2.5h, SLA target 4.0h, sla_breached: false)
- Severità: P2-High
- Apparati Impattati: File Server FS01 (IP LAN 192.168.120.10, VPN 10.147.19.10), Router Core RB5009 (192.168.120.1)
- Servizio: Condivisione File SMB su share di rete

## EVIDENZE RACCOLTE DAI SISTEMISTI (Telemetria Reale)

- Sintomo: 4 utenti in smart working via VPN non riescono ad aprire file CAD superiori a 1 MB (errore 0x8007003B). In sede LAN il problema non esiste.
- Strato L1 (Fisico): Link 10G SFP+ UP, 0 errori CRC (PASS).
- Strato L2 (Data Link): VLAN 10 Server corretta, MAC address presente (PASS).
- Strato L3 (Network): Ping verso 10.147.19.10 OK (28 ms). Ping con DF e payload > 1372 byte: Richiesta scaduta 100% loss (FAIL - PMTU Black Hole).
- Strato L4 (Transport): Test TCP porta 445: SYN/ACK ricevuto con successo (PASS).
- Strato L7 (Applicativo): Timeout su trasferimento dati SMB dovuto allo scarto silenzioso dei pacchetti di dimensione eccedente MTU WAN (1500 byte).

## RISOLUZIONE APPLICATA

1. Fix Server FS01: Impostazione persistente MTU 1400 su scheda virtuale VPN con PowerShell:
   netsh interface ipv4 set subinterface "VPN-Interface" mtu=1400 store=persistent
2. Fix Router MikroTik: Aggiunta regola firewall Mangle per TCP MSS Clamping su sessioni SYN:
   /ip firewall mangle add chain=forward action=change-mss new-mss=clamp-to-pmtu protocol=tcp tcp-flags=syn
3. Collaudo TR-01..TR-04: Test download file CAD da 145 MB riuscito con transfer rate di 27.8 MB/s (PASS).

Compila il template 10-RCA-Troubleshooting.md e restituiscimi il documento completo pronto per essere salvato in projects/acme-milano-2026/10-RCA-INC-2026-001.md.
```

---

## Output atteso dall'agente

L'agente AI restituirà:
1. Il documento completo in blocco Markdown con frontmatter canonico OKF v0.2 (`type: guide`), metadati estesi (`incident_id`, `sla_target_hours`, `resolution_time_hours`, `sla_breached: false`).
2. Diagramma flowchart Mermaid con la sequenza cronologica.
3. Tabella comparativa dei 7 strati OSI (L1-L7).
4. Albero logico dei 5 Perché che identifica la mancata applicazione del MSS clamping come causa radice primaria.
5. Script di fix con credenziali referenziate in modo sicuro tramite `vault://`.
6. Piano delle azioni correttive e preventive (CAPA) con owner e scadenze.
7. Comandi di validazione suggeriti: `python scripts/itinfra.py validate <file>`.
