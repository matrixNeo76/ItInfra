---
okf_version: "0.2"
id: "guide-itinfra-cli-manual-01"
title: "Manuale Operativo e Guida di Riferimento — ITInfra CLI (scripts/itinfra.py)"
type: "guide"
domain: "IT Infrastructure & Automation Tooling"
tags: ["okf-v0.2", "guide", "cli", "itinfra", "manual", "linter", "netbox", "mermaid"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Automation Suite"
phase: 0
author: "matrixNeo76"
reviewer: "DevOps & System Engineers"
approver: "Project Maintainer"
owner_team: "DevOps Engineering"
status: "approved"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "specification-itinfra-assistant-v02"
  - "specification-itinfra-manifest-projects-01"
  - "guide-itinfra-agentic-assistant-01"
depends_on:
  - "specification-itinfra-assistant-v02"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "ITInfra CLI"
    type: "toolchain"
    description: "Script Python scripts/itinfra.py per automazione, validazione OKF v0.2, export IPAM e diagrammi"
  - name: "NetBox Integration"
    type: "technology"
    description: "Formato di esportazione CSV e JSON compatibile con import bulk NetBox IPAM"
  - name: "Mermaid Visualizer"
    type: "toolchain"
    description: "Generatore di diagrammi di topologia di rete e rack elevation in sintassi Mermaid"

relations:
  - targetTitle: "Indice e Navigazione della Documentazione"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Indice master della documentazione tecnica"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "implements"
    weight: 1.0
    description: "Implementa le funzionalità architetturali della specifica"
  - targetTitle: "Specifica Registro Progetti e Manifest Condiviso"
    targetId: "specification-itinfra-manifest-projects-01"
    relationType: "depends_on"
    weight: 0.95
    description: "Utilizza la struttura della cartella projects e il manifesto YAML"
  - targetTitle: "Guida all'Uso con Agenti AI e Framework Agentici"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "relates_to"
    weight: 0.9
    description: "Fornisce la base di comandi eseguibili dagli agenti AI"
---

# Manuale Operativo: ITInfra CLI (`scripts/itinfra.py`)

<!-- AI-INSTRUCTIONS:
  Questa guida fornisce il riferimento operativo dettagliato per ogni comando
  della CLI scripts/itinfra.py, con parametri, esempi pratici e spiegazione degli output.
-->

## 1. Introduzione e Requisiti

La CLI **`scripts/itinfra.py`** è lo strumento centrale di automazione, controllo qualità e generazione per il repository **ItInfra**. È scritta in Python 3 standard (compatibile con Python 3.10+) con l'unica dipendenza di `pyyaml`.

### Prerequisiti
```bash
# Verifica installazione Python 3:
python --version

# Installa PyYAML:
pip install pyyaml
```

---

## 2. Sintassi Generale

```bash
python scripts/itinfra.py <comando> [opzioni]
```

I comandi disponibili sono:
- **`list-templates`**: Elenca tutti i 9 template documentali e le 7 fasi del ciclo IT.
- **`init`**: Inizializza un nuovo progetto creando la cartella e il manifesto precompilato.
- **`status`**: Visualizza la dashboard dell'avanzamento documentale e della qualità OKF per un progetto.
- **`validate`**: Esegue il linter formale OKF v0.2, verifica i link e controlla la sicurezza.
- **`export-ipam`**: Estrae le tabelle di indirizzamento da documenti LLD/As-Built in formati CSV/JSON per NetBox.
- **`generate-diagram`**: Produce diagrammi Mermaid (topologia di rete o elevazione rack) a partire dai file LLD.

---

## 3. Guida Dettagliata ai Comandi

### 3.1 `list-templates`
Mostra il catalogo completo dei template disponibili in `templates/`, indicando codice, fase del ciclo di vita, tipo canonico OKF v0.2 e presenza su disco.

```bash
python scripts/itinfra.py list-templates
```

**Esempio di output:**
```
=== CATALOGO TEMPLATE DOCUMENTALI IT (OKF v0.2) ===
Codice                   | Fase   | Tipo OKF        | Descrizione
--------------------------------------------------------------------------------
01-RSD-URS               | Fase 1 | specification   | Requirements Specification Document [OK]
02-HLD                   | Fase 2 | architecture    | High-Level Design [OK]
03-LLD                   | Fase 2 | architecture    | Low-Level Design [OK]
...
```

---

### 3.2 `init`
Crea una cartella di progetto in `projects/<project_slug>/` e genera un file `project-manifest.yaml` pronto per essere compilato.

```bash
python scripts/itinfra.py init <project_slug> [--client "<Cliente>"] [--name "<Nome Progetto>"] [--architect "<Lead>"]
```

**Parametri:**
- `<project_slug>` *(obbligatorio)*: Identificativo in minuscolo con trattini (es. `acme-milano-dc`).
- `--client`: Nome del cliente o committente (default: `Cliente Demo S.p.A.`).
- `--name`: Titolo esteso dell'iniziativa.
- `--architect`: Nominativo del Lead Systems/Network Architect responsabile.

**Esempio:**
```bash
python scripts/itinfra.py init tele-torino-dc --client "Telecom Torino" --name "Nuovo DC Leaf-Spine" --architect "Laura Bianchi"
```

---

### 3.3 `status`
Legge il file `project-manifest.yaml` e analizza tutti i file presenti nella cartella di progetto, controllandone l'esistenza, la conformità OKF v0.2 e il numero di placeholder residui (`<...>`).

```bash
python scripts/itinfra.py status <project_slug>
```

**Esempio di output:**
```
=== STATO PROGETTO: DEMO-ACME ===
Cliente:        Acme Corporation
Nome Progetto:  Modernizzazione Rete Datacenter
Lead Architect: Mario Rossi
Stato Globale:  in-planning
Supernet IPv4:  10.100.0.0/16
ASN BGP:        65100
--------------------------------------------------------------------------------
Doc ID                   | Fase   | Presenza     | Qualita / OKF   | Note
--------------------------------------------------------------------------------
01-RSD-URS               | Fase 1 | Presente     | OKF Conforme    | Completo
02-HLD                   | Fase 2 | Mancante     | -               | Richiesto per Fase 2
...
Avanzamento documentale: 1/9 (11%)
```

---

### 3.4 `validate`
Esegue il controllo di qualità formale e ontologico OKF v0.2 su un singolo file Markdown o ricorsivamente su un'intera cartella.

```bash
python scripts/itinfra.py validate <percorso> [-v]
```

**Controlli eseguiti dal linter:**
1. **Header OKF v0.2:** Presenza di `okf_version: "0.2"`, `id` non vuoto, `title` <= 120 caratteri, `type` canonico OKF.
2. **Tag e Tassonomia:** Minimo 2 tag lowercase, primo tag tassativamente `okf-v0.2`.
3. **Entità:** Minimo 1 entità con tipo canonico (`concept`, `framework`, `technology`, `toolchain`, `pattern`, `organization`, `specification`).
4. **Relazioni:** Oggetti `{targetTitle, targetId, relationType, weight, description}` con tipi di relazione ammessi.
5. **Biunivocità `related_docs` vs `relations`:** Ogni ID presente in `related_docs` DEVE avere una corrispondente riga in `relations` con `targetId` coincidente.
6. **Rilevamento Password in Chiaro:** Intercetta qualsiasi assegnazione di credenziale in chiaro che non usi il protocollo sicuro `vault://` o variabili shell.
7. **Controllo Placeholder:** Monitora e segnala la presenza di campi `<DA-RICHIEDERE>` e placeholder non valorizzati.

**Esempi:**
```bash
# Valida tutti i template ufficiali:
python scripts/itinfra.py validate templates/

# Valida un singolo documento di progetto con dettagli:
python scripts/itinfra.py validate projects/demo-acme/01-RSD-URS.md -v
```

---

### 3.5 `export-ipam`
Analizza le tabelle di indirizzamento IP e VLAN da un file LLD o As-Built ed esporta i dati in formato CSV standard per **NetBox** o in formato JSON strutturato.

```bash
python scripts/itinfra.py export-ipam <percorso_file_o_progetto> [--format csv|json] [--out <cartella>]
```

**File generati:**
- **`vlans.csv`**: Colonne: `vid,name,status,tenant,description`
- **`prefixes.csv`**: Colonne: `prefix,status,vrf,tenant,vlan,description`
- **`ip_addresses.csv`**: Colonne: `address,status,vrf,tenant,dns_name,description`

**Esempio:**
```bash
# Esportazione NetBox CSV:
python scripts/itinfra.py export-ipam templates/03-LLD.md --format csv --out ./exports/netbox/

# Esportazione JSON:
python scripts/itinfra.py export-ipam projects/demo-acme/ --format json --out ./exports/json/
```

---

### 3.6 `generate-diagram`
Legge la matrice dei cablaggi fisici e l'elevazione rack dal Low-Level Design (o As-Built) e genera codice **Mermaid** formattato e pronto da includere nella documentazione.

```bash
python scripts/itinfra.py generate-diagram <file_lld> [--type topology|rack|all] [--out <file_output>]
```

**Opzioni `--type`:**
- `topology`: Genera il diagramma di rete (Mermaid `graph TD`) raggruppando i nodi per tipologia (`core`, `tor`, `fw`, `storage`, `srv`) ed etichettando le connessioni con porte fisiche e VLAN.
- `rack`: Genera il diagramma di layout rack (Mermaid `block-beta`) riproducendo visivamente le 42U dall'alto verso il basso.
- `all`: Genera entrambi i diagrammi sequenzialmente.

**Esempio:**
```bash
# Stampa a video il diagramma topologico:
python scripts/itinfra.py generate-diagram templates/03-LLD.md --type topology

# Salva i diagrammi in un file markdown:
python scripts/itinfra.py generate-diagram templates/03-LLD.md --type all --out ./diagrams.md
```
