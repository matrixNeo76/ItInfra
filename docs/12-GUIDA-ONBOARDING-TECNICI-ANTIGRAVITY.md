---
okf_version: "0.2"
id: "guide-onboarding-tecnici-antigravity-01"
title: "Guida Operativa — Onboarding Client Windows 11 & Configurazione Rapida per Antigravity (Release v0.9)"
type: "guide"
domain: "IT Infrastructure Knowledge Engineering"
tags: ["okf-v0.2", "guide", "onboarding", "antigravity", "windows-11", "setup", "skills"]

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
  - "guide-local-workspace-central-publish-01"
  - "guide-itinfra-agentic-assistant-01"
  - "specification-itinfra-assistant-v02"
depends_on:
  - "guide-local-workspace-central-publish-01"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "Antigravity Agentic IDE"
    type: "technology"
    description: "Ambiente di sviluppo e pair-programming assistito da agenti AI autonomi di Google DeepMind"
  - name: "Client Bootstrapper Skill"
    type: "toolchain"
    description: "Skill agentica itinfra-setup che diagnostica l'ambiente e auto-configura il workspace client"
  - name: "One-Click Setup Automation"
    type: "toolchain"
    description: "Script setup_client_workspace.ps1 per allestire in 5 secondi il workspace su SSD locale"
  - name: "Zero-Configuration Architecture"
    type: "pattern"
    description: "Pattern in cui l'agente eredita regole e istruzioni semplicemente aprendo la cartella del progetto"

relations:
  - targetTitle: "Indice Generale della Documentazione ITInfra"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Indice master della documentazione tecnica"
  - targetTitle: "Guida all'Architettura Local Workspace & Central Publish"
    targetId: "guide-local-workspace-central-publish-01"
    relationType: "depends_on"
    weight: 1.0
    description: "Architettura di pubblicazione controllata su storage master centrale"
  - targetTitle: "Guida per Assistente Agentico ITInfra"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "references"
    weight: 0.95
    description: "Istruzioni per l'interazione via prompt e interviste strutturate"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 0.9
    description: "Specifica tecnica del sistema agentico e delle skill integrate"
---

# Guida Operativa: Onboarding Client Windows 11 & Configurazione per Antigravity

<!-- AI-INSTRUCTIONS:
  Questa guida spiega passo-passo come configurare una nuova postazione client Windows 11
  per lavorare con la suite ITInfra tramite Google Antigravity, sfruttando la skill itinfra-setup
  oppure lo script di installazione One-Click dalla share di rete centrale.
-->

## 1. Panoramica e Requisiti Minimi

Questa guida è destinata ai **tecnici di rete, sistemisti e architetti IT** che devono iniziare a redigere documentazione tecnica di infrastruttura con il supporto dell'agente AI **Google Antigravity**.

### Requisiti Minimi del PC Client
- **Sistema Operativo:** Windows 11 (o Windows 10 x64 aggiornato).
- **Runtime:** Python 3.10 o superiore (scaricabile da [python.org](https://www.python.org) o dal Microsoft Store).
- **Rete:** Connessione alla LAN aziendale o VPN attiva con visibilità su `\\fileserv01\dati01\workaure`.
- **Applicazione:** Google Antigravity installato.

---

## 2. Metodo 1: Setup Rapido "One-Click" da PowerShell (Consigliato)

È il metodo più veloce in assoluto per i tecnici collegati alla rete aziendale:

1. Premi `Win + X` e apri **Terminale Windows** (PowerShell).
2. Incolla ed esegui questo comando singolo:
   ```powershell
   powershell -ExecutionPolicy Bypass -File \\fileserv01\dati01\workaure\scripts\setup_client_workspace.ps1
   ```
3. In circa 5 secondi l'automazione:
   - Crea la cartella locale `C:\itinfra\`.
   - Sincronizza il motore, tutti i 10 template OKF v0.2, le guide e le skill per Antigravity.
   - Genera il file `.itinfra_config.json` con puntamento predefinito alla share master.
   - Verifica che Python sia pronto.

---

## 3. Metodo 2: Configurazione via Git (per Sviluppatori o Lavoro Remoto)

Se lavori da remoto o preferisci usare Git:

1. Apri PowerShell e clona il repository in locale:
   ```powershell
   git clone https://github.com/matrixNeo76/ItInfra.git C:\itinfra
   cd C:\itinfra
   ```
2. Installa le librerie minime:
   ```powershell
   pip install pyyaml cryptography
   ```

---

## 4. Apertura del Workspace in Google Antigravity

Una volta allestita la cartella `C:\itinfra`:

1. Avvia l'applicazione **Antigravity**.
2. Dal menu principale seleziona **File → Open Folder** (oppure premi `Ctrl + K, Ctrl + O`).
3. Seleziona la cartella locale **`C:\itinfra`**.

### Come Antigravity riconosce automaticamente l'ambiente:
Appena aperta la cartella, Antigravity attiva in modo del tutto trasparente:
- **`AGENTS.md`**: Regola di sistema primaria con divieto assoluto di allucinazioni e standard OKF v0.2.
- **Skill `itinfra-setup`**: Diagnostica e verifica integrità del workspace.
- **Skill `itinfra-assistant`**: Motore di intervista guidata per blocchi logici (Scope, Rete, Compute, Sicurezza, ATP).
- **Skill `itinfra-vault`**: Gestore crittografico locale AES-256 per credenziali e secret.
- **Skill `itinfra-troubleshooter`**: Diagnostica deterministica disservizi e schede post-mortem 10-RCA.

---

## 5. Come Iniziare a Lavorare: I Prompt Consigliati

Per interagire con Antigravity è sufficiente scrivere messaggi in linguaggio naturale nella finestra di chat:

### Caso A: Verifica Iniziale dell'Ambiente
> *"Verifica se il mio ambiente di lavoro ITInfra e' configurato correttamente e pronto all'uso."*
- Antigravity attiverà la skill `itinfra-setup`, collauderà le dipendenze e confermerà lo stato di salute.

### Caso B: Creazione di un Nuovo Progetto Cliente
> *"Ciao, dobbiamo redigere la documentazione di progetto per un nuovo cliente 'Banca del Nord' relativo al rinnovo dei firewall di perimetro."*
- Antigravity inizializzerà il manifesto con `itinfra.py init banca-del-nord`, creerà la cartella `projects/banca-del-nord/` e avvierà l'intervista guidata blocco per blocco.

### Caso C: Consultazione dell'Inventario Hardware Esistente
> *"Quali clienti del nostro catalogo utilizzano switch MikroTik CRS326 o server Dell R630?"*
- Antigravity interrogherà l'inventario cross-progetto (`itinfra.py inventory find`) e risponderà con apparati, IP e modelli correlati.

### Caso D: Pubblicazione del Progetto sullo Storage Master Centrale
Quando il progetto o una sua milestone è completa:
> *"Il progetto 'banca-del-nord' e' pronto. Esegui il quality gate e pubblicalo sulla share centrale."*
- Antigravity eseguirà:
  ```powershell
  python scripts/itinfra.py publish banca-del-nord
  ```
  sincronizzando in modo sicuro e atomico il progetto sul server `\\fileserv01\dati01\workaure\projects\banca-del-nord\`.

### Caso E: Diagnostica Connettività e Permessi Share Master
In qualsiasi momento per verificare se la postazione client può leggere i template e pubblicare su `projects/`:
> *"Verifica se ho i permessi corretti sulla share master centrale."*
- Antigravity eseguirà la diagnostica automatica:
  ```powershell
  python scripts/itinfra.py check-share
  ```
  restituendo un report tabellare con la conferma dell'abilitazione alla pubblicazione e della protezione del core.

---

## 6. Risoluzione dei Problemi Comuni (Troubleshooting)

| Sintomo | Causa Probabile | Soluzione Rapida |
|---|---|---|
| `python non e' riconosciuto come comando interno` | Python non è nel `PATH` di Windows | Scaricare Python 3.11 dal Microsoft Store spuntando *"Add python.exe to PATH"* |
| `Share \\fileserv01\... non raggiungibile` | PC non connesso alla rete aziendale o VPN staccata | Connettersi alla VPN aziendale o impostare un percorso alternativo in `.itinfra_config.json` |
| `SOVRASCRITTURA BLOCCATA durante il publish` | Sul server esiste già un progetto approvato (`status: approved`) | Chiedere ad Antigravity di pubblicare con il flag `--force` se si è certi di voler aggiornare l'As-Built ufficiale |
| `ModuleNotFoundError: No module named 'yaml'` | Libreria PyYAML mancante | Eseguire da terminale: `pip install pyyaml cryptography` |
