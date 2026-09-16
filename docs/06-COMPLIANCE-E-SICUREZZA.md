---
okf_version: "0.2"
id: "specification-itinfra-compliance-security-01"
title: "Specifica dei Framework di Compliance e Resilienza Operativa — NIS2, ISO 27001:2022, DORA"
type: "specification"
domain: "IT Infrastructure Security & Regulatory Compliance"
tags: ["okf-v0.2", "specification", "compliance", "security", "nis2", "iso27001", "dora", "resilience"]

# Metadati estesi IT
project_id: "itinfra-core"
project_name: "ITInfra Compliance & Regulatory Architecture"
phase: 0
author: "matrixNeo76"
reviewer: "Cybersecurity & Compliance Officers"
approver: "Project Maintainer"
owner_team: "Security & Governance"
status: "approved"
version: "1.0.0"
created_at: "2026-09-16"
updated_at: "2026-09-16"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "specification-itinfra-assistant-v02"
  - "guide-itinfra-agentic-assistant-01"
  - "specification-itinfra-manifest-projects-01"
  - "guide-global-memory-system-test-01"
depends_on:
  - "specification-itinfra-assistant-v02"
classification: "public"
retention: "permanent"
lang: "it"

entities:
  - name: "NIS2 Directive"
    type: "specification"
    description: "Direttiva UE 2022/2555 sulla cibersicurezza di reti e sistemi informativi per enti critici"
  - name: "ISO/IEC 27001:2022"
    type: "specification"
    description: "Standard internazionale per l'Information Security Management System con controlli A.5-A.8"
  - name: "DORA Regulation"
    type: "specification"
    description: "Regolamento UE 2022/2554 per la resilienza operativa digitale del settore finanziario e ICT"
  - name: "Vault Security Protocol"
    type: "pattern"
    description: "Convenzione standard vault:// per eliminare credenziali in chiaro dalla documentazione"

relations:
  - targetTitle: "Indice e Navigazione della Documentazione"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Indice master della documentazione tecnica"
  - targetTitle: "Specifica Tecnica — Assistente Agentico ITInfra"
    targetId: "specification-itinfra-assistant-v02"
    relationType: "references"
    weight: 0.9
    description: "Specifica architetturale complessiva"
  - targetTitle: "Guida all'Uso dell'Assistente Agentico"
    targetId: "guide-itinfra-agentic-assistant-01"
    relationType: "governs"
    weight: 0.95
    description: "Istruzioni per l'intervista guidata sui requisiti di sicurezza"
  - targetTitle: "Specifica Registro Progetti e Manifest Condiviso"
    targetId: "specification-itinfra-manifest-projects-01"
    relationType: "references"
    weight: 0.85
    description: "Riferimento al manifest di progetto per parametri di retention e vault"
  - targetTitle: "Guida Operativa — Global Staging Memory & Enterprise System Test Suite"
    targetId: "guide-global-memory-system-test-01"
    relationType: "references"
    weight: 0.9
    description: "Politiche di sicurezza preventiva contro secret leakage e verifica automatica"
---

# Specifica dei Framework di Compliance e Resilienza Operativa

<!-- AI-INSTRUCTIONS:
  Questa specifica documenta l'integrazione dei requisiti NIS2, ISO 27001:2022 e DORA
  all'interno dei template di Assessment, Progettazione e Collaudo.
-->

## 1. Obiettivo della Conformità Integrata

Nelle moderne infrastrutture critiche ed enterprise, la conformità normativa e la sicurezza delle informazioni non possono essere considerate un'attività a valle, ma devono essere **integrate per progettazione (Security by Design & by Default)**.

I template del repository **ItInfra** incorporano in modo nativo i requisiti dei tre standard di riferimento europei e internazionali:
1. **NIS2 (Direttiva UE 2022/2555)**
2. **ISO/IEC 27001:2022**
3. **DORA (Regolamento UE 2022/2554)**

---

## 2. Direttiva NIS2 (UE 2022/2555)

La Direttiva NIS2 si applica ai soggetti essenziali e importanti operanti in settori critici (energia, trasporti, finanza, sanità, acqua potabile, infrastrutture digitali, gestione servizi ICT, pubblica amministrazione).

### Requisiti Chiave Mappati nei Template:
- **Gestione dei rischi e sicurezza delle reti (Art. 21):**
  - Mappato in [`01-RSD-URS.md`](../templates/01-RSD-URS.md) (Sezione 6) e [`02-HLD.md`](../templates/02-HLD.md) (Sezione 5.6).
  - Richiede micro-segmentazione, cifratura end-to-end e autenticazione multifattore (MFA) per accessi amministrativi.
- **Notifica tempestiva degli incidenti (Art. 23):**
  - **Early warning** entro 24 ore dalla rilevazione di incidenti significativi.
  - **Notifica dettagliata** entro 72 ore con valutazione iniziale della gravità.
  - Documentato nei requisiti di logging immutabile, SIEM centralizzato e Runbook operativo ([`08-SOP-Runbook.md`](../templates/08-SOP-Runbook.md)).
- **Sicurezza della catena di fornitura (Supply Chain Security):**
  - Mappato nell'inventario hardware e licenze software ([`09-Handover-Inventory.md`](../templates/09-Handover-Inventory.md)).

---

## 3. Standard ISO/IEC 27001:2022

L'aggiornamento 2022 dello standard ISO/IEC 27001 organizza i controlli di sicurezza (Annex A) in 4 categorie fondamentali, recepite nell'architettura documentale:

| Dominio ISO 27001:2022 | Controlli Rilevanti per l'Infrastruttura | Documento ITInfra Corrispondente |
|------------------------|------------------------------------------|----------------------------------|
| **A.5 Controlli Organizzativi** | Politiche di controllo accessi, gestione asset, segregazione compiti, gestione incidenti (A.5.24) | `01-RSD-URS.md`, `09-Handover-Inventory.md`, `10-RCA-Troubleshooting.md` |
| **A.6 Controlli Persone** | Screening, accordi di riservatezza, sensibilizzazione | `04-MOP.md` (ruoli ed escalation) |
| **A.7 Controlli Fisici** | Sicurezza perimetrale data center, cablaggio sicuro, manutenzione rack | `03-LLD.md` (Rack elevation e patch panel) |
| **A.8 Controlli Tecnologici** | Segregazione reti (A.8.20), sicurezza servizi di rete (A.8.21), segregazione in reti (A.8.22), PAM (A.8.2) | `02-HLD.md` (Zone trust), `03-LLD.md` (VLAN, ACL) |

---

## 4. Regolamento DORA (UE 2022/2554)

Il regolamento DORA (Digital Operational Resilience Act) stabilisce requisiti uniformi per la sicurezza dei sistemi di rete e informativi delle entità finanziarie e dei fornitori terzi critici di servizi TIC (ICT).

### Requisiti Chiave Mappati:
1. **ICT Risk Management Framework (Capitolo II):**
   - Strategie di ridondanza con RTO e RPO certificati per servizi mission-critical.
   - Presenza di data center secondario con sincronizzazione sincrona/asincrona.
2. **Test di Resilienza Operativa Digitale (Capitolo IV):**
   - Conduzione periodica di **Threat-Led Penetration Testing (TLPT)** su infrastrutture live o staging.
   - Piani di collaudo e validazione formalizzati in [`07-ATP.md`](../templates/07-ATP.md).
3. **Piani di Contingenza e Rollback:**
   - Obbligo di disporre di procedure di fallback validate prima di qualsiasi intervento su sistemi di produzione ([`05-Rollback.md`](../templates/05-Rollback.md)).

---

## 5. Protocollo di Sicurezza per le Credenziali & Local Encrypted Vault

In conformità ai requisiti di audit e riservatezza di NIS2 e ISO 27001:2022 (A.5.15, A.8.2):
- **È SEVERAMENTE VIETATO** inserire chiavi crittografiche, token API o password in chiaro all'interno dei documenti tecnici o repository Git.
- Tutti i riferimenti a credenziali DEVONO utilizzare l'URI standard:
  ```
  vault://it/projects/<slug>/<apparato_o_servizio>/<utenza>
  ```
  *Esempio:* `vault://it/projects/severino-srl/mikrotik/admin`

### 5.1 Motore Crittografico Locale (AES-256-GCM)
Il repository include il modulo `scripts/itinfra_vault.py` e il subparser CLI `vault`:
1. **Cifratura Autenticata:** I secret vengono cifrati localmente in `projects/<slug>/.vault.enc` tramite algoritmo simmetrico **AES-256-GCM** (12-byte nonce, 16-byte authentication tag).
2. **Derivazione della Chiave (KDF):** Master key derivata con **PBKDF2-HMAC-SHA256** (100.000 iterazioni con salt casuale a 16 byte).
3. **Concorrenza Sicura e Multi-Worktree:** Un context manager di **File Locking Atomico** (`.vault.lock`) garantisce l'accesso esclusivo al vault, prevenendo corruzioni dei dati durante l'esecuzione parallela di più subagenti AI su Git Worktree.
4. **Protezione Git Totale:** I file `.vault.enc`, `.vault.lock` e chiavi `.secret` sono tassativamente esclusi da Git via `.gitignore`.
5. **Audit di Coerenza Automatico:** Il comando `python scripts/itinfra.py vault audit <slug>` scansiona tutti i file Markdown del progetto, verifica la corrispondenza dei riferimenti `vault://` e rileva secret mancanti o orfani.

### 5.2 Prevenzione del Secret Leakage nella Memoria Globale (Release v0.8)
Nelle architetture multi-tenant, la condivisione di una memoria globale (`projects/_global_scratchpad.md`) comporta il rischio critico di propagazione involontaria di credenziali o riferimenti specifici del cliente tra diversi progetti.
Per soddisfare le policy Zero-Leakage:
1. **Sanitizer Preventivo (`validate_global_entry_safety`):** Il motore di persistenza in `scripts/itinfra_memory.py` analizza preventivamente qualsiasi annotazione destinata al pool globale. Se il testo contiene riferimenti a `vault://it/projects/` o stringhe di credenziali in chiaro (`password:`, `secret:`, token), l'operazione viene immediatamente abortita con `PermissionError`.
2. **Confinamento Ermetico dei Secret:** La conoscenza condivisa è circoscritta unicamente a vincoli architetturali generici, incompatibilità di apparati note e linee guida di vendor. Tutti i secret rimangono confinati nel `.vault.enc` di ciascun cliente.
3. **Collaudo Continuo:** Il modulo `MOD-03` e `MOD-07` dell'Enterprise System Test Suite (`scripts/itinfra_test_suite.py`) verifica costantemente l'assenza di leakage crittografico su tutti i file del repository.

