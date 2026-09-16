---
okf_version: "0.2"
id: "guide-local-workspace-central-publish-01"
title: "Guida Operativa — Architettura Local Workspace & Central Publish con Quality Gate (Release v0.9)"
type: "guide"
domain: "IT Infrastructure Knowledge Engineering"
tags: ["okf-v0.2", "guide", "publish", "quality-gate", "local-workspace", "central-share", "deployment"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Documentation Suite"
phase: 0
author: "Enterprise Solutions Architect"
reviewer: "System Architecture Board"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture & DevOps"
status: "approved"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "specification-itinfra-assistant-v02"
  - "guide-itinfra-cli-manual-01"
  - "guide-global-memory-system-test-01"
depends_on:
  - "guide-global-memory-system-test-01"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "Local Workspace Architecture"
    type: "pattern"
    description: "Pattern operativo che isola l'ambiente di lavoro dell'agente AI su disco SSD locale del client"
  - name: "Central Share Master Hub"
    type: "technology"
    description: "Repository e archivio master condiviso su storage di rete SMB per la distribuzione e raccolta della conoscenza"
  - name: "Pre-Flight Quality Gate"
    type: "framework"
    description: "Insieme di verifiche automatiche bloccanti (linter OKF v0.2, strict grounding e zero-leak) prima della pubblicazione"
  - name: "Atomic Project Publisher"
    type: "toolchain"
    description: "Modulo di sincronizzazione atomica e confinata del singolo slug di progetto verso la share centrale"
  - name: "Engine Synchronization Mechanism"
    type: "toolchain"
    description: "Strumento di aggiornamento unidirezionale della copia locale di script e template scaricati dal master"

relations:
  - targetTitle: "Indice Generale della Documentazione ITInfra"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Indice master della documentazione tecnica"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 1.0
    description: "Attuazione esecutiva della Sezione 2.15 per l'architettura Local Workspace & Central Publish"
  - targetTitle: "Manuale Operativo CLI ITInfra"
    targetId: "guide-itinfra-cli-manual-01"
    relationType: "extends"
    weight: 0.95
    description: "Documentazione dei comandi CLI publish e sync-engine"
  - targetTitle: "Guida Operativa — Global Staging Memory & Unified Verification Dashboard"
    targetId: "guide-global-memory-system-test-01"
    relationType: "depends_on"
    weight: 0.85
    description: "Integrazione con la suite di collaudo e la memoria globale"
---

# Guida Operativa: Architettura Local Workspace & Central Publish (Release v0.9)

<!-- AI-INSTRUCTIONS:
  Questa guida definisce lo standard architetturale per la distribuzione e l'utilizzo multi-operatore
  della suite ITInfra. Istruisce tecnici e agenti AI a lavorare su workspace locali veloci su SSD
  e a pubblicare progetti verso lo storage master centrale esclusivamente previo superamento del Quality Gate.
-->

## 1. Obiettivi e Visione Architetturale

L'architettura **Local Workspace & Central Publish** (Release v0.9) risolve alla radice le complessità tipiche degli ambienti multi-operatore in rete locale:
1. **Prestazioni Native SSD:** Gli agenti AI (come Antigravity) operano su file system locale ad altissima velocità, eliminando le latenze SMB e i timeout dei file watcher di Windows su percorsi di rete UNC.
2. **Inviolabilità del Motore Centrale:** I file sorgente (`scripts/`), i template normativi (`templates/`), le guide (`docs/`) e il repository `.git/` rimangono protetti sulla macchina di sviluppo master e non sono esposti a modifiche accidentali da parte dei client secondari.
3. **Quality Gate Prima della Condivisione:** Nessun progetto può essere riversato nello storage centrale se presenta errori formali OKF v0.2, placeholder illegali o credenziali in chiaro.
4. **Isolamento Multi-Tenant Totale:** Ciascun operatore lavora esclusivamente sulla cartella del cliente assegnato (`projects/<slug>/`), senza alcun rischio di sovrascrivere o corrompere i progetti dei colleghi.

---

## 2. Topologia del Flusso di Lavoro

```mermaid
sequenceDiagram
    autonumber
    actor Tecnico as Tecnico / Agente AI (Client LAN)
    participant Local as SSD Locale (C:\itinfra\)
    participant Gate as Pre-Flight Quality Gate
    participant Central as Central Share (\\fileserv01\dati01\workaure)

    Note over Tecnico,Local: Setup Iniziale (One-Click)
    Central->>Local: setup_client_workspace.ps1 (Sync engine & templates)
    
    Note over Tecnico,Local: Fase di Redazione & Validazione
    Tecnico->>Local: itinfra.py init acme-roma
    Tecnico->>Local: Antigravity redige 01-RSD .. 09-Handover
    Tecnico->>Local: itinfra.py validate projects/acme-roma/

    Note over Tecnico,Central: Fase di Pubblicazione Controllata
    Tecnico->>Gate: itinfra.py publish acme-roma
    Gate->>Gate: 1. Linter OKF v0.2 (0 errori)
    Gate->>Gate: 2. Strict Grounding Audit
    Gate->>Gate: 3. Scansione Zero-Leak Secret in chiaro
    alt Quality Gate Superato
        Gate->>Central: Copia atomica di projects/acme-roma/
        Central-->>Tecnico: Pubblicazione riuscita (100% Conforme)
    else Rilevato Errore o Secret Leak
        Gate-->>Tecnico: BLOCCO: Pubblicazione respinta con elenco anomalie
    end
```

---

## 3. Guida per l'Amministratore Master (Setup Storage Centrale)

Sulla macchina di sviluppo master (utente `auresystem`):

1. **Inizializzazione della Share Master:**
   Eseguire lo script PowerShell per allestire e allineare la cartella condivisa:
   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/init_central_share.ps1
   ```
   Lo script:
   - Crea le cartelle `scripts/`, `templates/`, `docs/` e `projects/` su `\\fileserv01\dati01\workaure`.
   - Sincronizza tutti gli script Python, i template OKF v0.2 e le guide ufficiali.
   - Allinea i file di governance (`README.md`, `ROADMAP.md`, `AGENTS.md`).

---

## 4. Guida per i Tecnici LAN (Allestimento Client Windows 11)

Su qualsiasi workstation client della rete LAN o VPN:

1. **Setup One-Click del Workspace Locale:**
   Aprire PowerShell ed eseguire:
   ```powershell
   powershell -ExecutionPolicy Bypass -File \\fileserv01\dati01\workaure\scripts\setup_client_workspace.ps1
   ```
   L'automazione:
   - Crea la cartella di lavoro su disco locale `C:\itinfra\`.
   - Scarica la copia più recente del motore, dei template e delle guide.
   - Crea il file di configurazione `.itinfra_config.json` con puntamento predefinito a `\\fileserv01\dati01\workaure`.
   - Verifica la presenza dell'interprete Python nel sistema.

2. **Inizializzare un Nuovo Progetto Cliente:**
   ```powershell
   cd C:\itinfra
   python scripts/itinfra.py init <slug> --client "<Nome Cliente>" --name "<Titolo Progetto>"
   ```

3. **Lavorare con l'Agente AI:**
   - Aprire la cartella `C:\itinfra` in Antigravity.
   - Condurre l'intervista tecnica guidata per compilare i documenti OKF v0.2 in `projects/<slug>/`.

---

## 5. Comando `publish`: Meccanismo di Pubblicazione e Quality Gate

Quando la documentazione di un cliente è completata (o al passaggio di milestone):

### Sintassi del Comando
```powershell
python scripts/itinfra.py publish <slug> [--dest <path>] [--dry-run] [--force]
```

### Parametri e Opzioni
| Parametro | Descrizione |
|---|---|
| `<slug>` | Nome univoco della cartella progetto in `projects/` da pubblicare |
| `--dest` | *(Opzionale)* Sovrascrive il percorso della share centrale configurata in `.itinfra_config.json` |
| `--dry-run` | Esegue il Quality Gate completo e mostra l'elenco dei file pronti senza copiare nulla sul server |
| `--force` | Forza la sovrascrittura nel caso in cui il progetto remoto contenga documenti già in stato `approved` |

### I 3 Controlli del Pre-Flight Quality Gate
1. **Linter OKF v0.2:** Tutti i documenti markdown in `projects/<slug>/` vengono analizzati con `OKFValidator`. Se viene rilevato anche un solo errore di schema, `id`, `tags` o formattazione, la pubblicazione viene respinta.
2. **Strict Grounding Audit:** Verifica semantica dell'assenza di placeholder illegali o parametri di rete incongruenti.
3. **Scansione Anti-Leak:** Ispezione di tutte le righe dei documenti alla ricerca di password in chiaro (es. `admin_password: "..."`). Le credenziali DEVONO essere referenziate tramite schema `vault://it/projects/<slug>/...` oppure valorizzate come `<DA-RICHIEDERE>`.

### Esempio di Risultato di Successo
```
[SUCCESSO] Progetto 'severino-srl' pubblicato con successo!
  Sorgente: C:\itinfra\projects\severino-srl
  Destinazione centrale: \\fileserv01\dati01\workaure\projects\severino-srl
  File sincronizzati: 19 (481.6 KB)
  Quality Gate OKF v0.2: 100% CONFORME (0 errori)
```

---

## 6. Comando `sync-engine`: Aggiornamento del Motore Locale

Quando l'amministratore rilascia nuovi template normativi, aggiornamenti alla CLI o guide operative:

```powershell
python scripts/itinfra.py sync-engine [--source <path>] [--dry-run]
```

- Esegue la scansione differenziale tra la share centrale e il workspace locale.
- Aggiorna automaticamente i file di `templates/`, `scripts/` e `docs/` che presentano una data di modifica più recente sul server master.
- Lascia **ermeticamente intatti** tutti i file di lavoro presenti nella cartella locale `projects/`.

---

## 7. Matrice di Sicurezza & Conformità Operativa

| Risorsa | Posizione Locale (`C:\itinfra`) | Posizione Centrale (`\\fileserv01\...`) | Protezione Applicata |
|---|---|---|---|
| **Sorgenti Python (`scripts/`)** | Esecuzione locale veloce | Storage protetto | Modificabile solo dal Developer master |
| **Template OKF v0.2** | Copia di lavoro | Standard ufficiale | Immutabili durante le sessioni di compilazione |
| **Progetti Cliente (`projects/`)** | Cartella del singolo tenant | Raccolta progetti aziendali | Sincronizzati solo via Quality Gate atomico |
| **Secret Vault (`.vault.enc`)** | Cifrato in AES-256-GCM locale | Escluso dalla pubblicazione | Zero credenziali in chiaro trasmesse in rete |
