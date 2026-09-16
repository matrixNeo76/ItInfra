---
name: itinfra-vault
description: Gestione sicura del Local Encrypted Secret Vault (AES-256-GCM) per progetti IT. Utilizzare per inizializzare vault, cifrare credenziali, recuperare secret, condurre audit di sicurezza su riferimenti vault:// e garantire zero leak di credenziali su Git.
---

# ITInfra Secret Vault Skill — Gestione Credenziali Cifrate (AES-256-GCM)

Questa skill fornisce le linee guida operative per la gestione sicura e crittografata dei segreti aziendali, credenziali di rete, chiavi API e certificati nei progetti di infrastruttura gestiti con ItInfra.

---

## 1. Principi di Sicurezza Fondamentali

1. **DIVIETO ASSOLUTO di credenziali in chiaro:** Nessuna password, token API, pre-shared key o certificato privato deve mai essere committata o scritta in chiaro nei documenti Markdown (`.md`), nei file di configurazione (`.yaml`) o negli script.
2. **Standard di Cifratura Locale:** I segreti risiedono in un archivio cifrato locale `projects/<slug>/.vault.enc` protetto con:
   - Cifratura autenticata **AES-256-GCM** (12-byte nonce, 16-byte auth tag).
   - Derivazione della master key con **PBKDF2-HMAC-SHA256** (100.000 iterazioni con salt casuale a 16 byte).
3. **Concorrenza Sicura e Multi-Worktree:** L'accesso al vault è protetto da un meccanismo di **File Locking atomico** (`.vault.lock`) con context manager per prevenire corruzioni dei dati durante l'esecuzione parallela di subagenti su Git Worktree.
4. **Protezione Git Totale:** I file `.vault.enc`, `.vault.lock`, chiavi e file `.secret` sono tassativamente esclusi dal controllo versione tramite `.gitignore`.
5. **Protezione Preventiva da Secret Leakage Globale (Release v0.8):** È severamente vietato inserire credenziali o riferimenti `vault://it/projects/` nello Staging Scratchpad Globale (`projects/_global_scratchpad.md`). Il sanitizer preventivo (`validate_global_entry_safety`) blocca automaticamente tali tentativi sollevando `PermissionError`.

---

## 2. Riferimento delle Credenziali nei Documenti Markdown

Nei file tecnici (`01-RSD` ... `10-RCA`) e nello scratchpad locale (`_scratchpad.md`), le credenziali devono essere espresse esclusivamente tramite l'URI standard del vault aziendale:

```markdown
<!-- ESEMPIO CORRETTO NEI DOCUMENTI MARKDOWN -->
- **Username di amministrazione:** `admin`
- **Password:** Riferimento sicuro `vault://it/projects/<slug>/mikrotik/admin`
- **Master Passphrase BitLocker:** Riferimento sicuro `vault://it/projects/<slug>/hyperv/bitlocker-recovery`
```

---

## 3. Comandi Operativi CLI per il Vault

Tutte le operazioni sul vault sono gestite tramite il subparser `vault` di `scripts/itinfra.py`:

### Inizializzazione del Vault
Crea il contenitore cifrato per il progetto:
```powershell
python scripts/itinfra.py vault init <slug> [--passphrase "<passphrase>"] [--overwrite]
```

### Inserimento o Aggiornamento di un Secret
Aggiunge una chiave (se `--value` è omesso, viene richiesto in modo nascosto da terminale):
```powershell
python scripts/itinfra.py vault set <slug> mikrotik/admin --value "<password_segreta>"
python scripts/itinfra.py vault set <slug> zerotier/admin-token --value "<token_api>"
```

### Recupero di un Secret (Decifratura)
Stampa a video il valore decifrato (richiede la master passphrase):
```powershell
python scripts/itinfra.py vault get <slug> mikrotik/admin
```

### Elenco Chiavi Censite
Visualizza la mappa dei segreti registrati con relativi timestamp di aggiornamento (senza mai esporre i valori in chiaro):
```powershell
python scripts/itinfra.py vault list <slug>
```

### Audit dei Riferimenti Markdown vs Vault
Scansiona tutti i 10 documenti tecnici del progetto e lo scratchpad, estrae ogni occorrenza di `vault://` e verifica se corrisponde a un segreto effettivamente censito:
```powershell
python scripts/itinfra.py vault audit <slug> [--passphrase "<passphrase>"]
```
- Segnala **chiavi mancanti**: citate nei documenti tecnici ma non ancora inserite nel vault.
- Segnala **chiavi orfane**: presenti nel vault ma non referenziate in alcun documento.

### Collaudo Unificato di Sicurezza
Verifica la piena integrità crittografica e l'assenza di secret leaks tramite il modulo `MOD-03` dell'Enterprise Test Suite:
```powershell
python scripts/itinfra.py test-suite --report-html
```
