---
trigger: always_on
---

# ⚡ DIRETTIVA PRIMARIA: ZERO-SEARCH PER HELP, AVVIO E COMANDI ITINFRA

Quando l'utente scrive:
- "puoi aiutarmi ad utilizzare il nostro applicativo itinfra"
- "come posso usare itinfra"
- "cosa fa questo applicativo"
- "quali sono i comandi"
- "come visualizzo i comandi"
- "ciao", "buongiorno", "help", "comandi"

## 🛑 REGOLA TASSATIVA:
1. NON USARE ALCUN TOOL DI RICERCA (`find_by_name`, `grep_search`, `list_dir`, `view_file`).
2. RISPONDI ALL'ISTANTE (in 0 secondi) presentando la Scheda Operativa ITInfra qui sotto.
3. Tu CONOSCI GIÀ perfettamente l'applicazione, non devi esplorare i file per orientarti.

### 📋 Scheda Operativa ITInfra

👋 **Benvenuto in ITInfra!**
Questo è l'ambiente di lavoro per la documentazione tecnica, governance, automazione e collaudo di infrastrutture IT complesse su standard OKF v0.2.

### 🚀 Comandi Rapidi Disponibili (Zero Attrito)

| Azione Desiderata | Da Chat Antigravity (Scrivi semplicemente) | Da Terminale (Prompt / PowerShell) |
| :--- | :--- | :--- |
| **Allineare Template e Motore** | `aggiorna` *(o `update`)* | `it update` *(oppure solo `update`)* |
| **Verificare Rete e Permessi** | `controlla` *(o `check`)* | `it check` |
| **Pubblicare Progetto su Server** | `pubblica <slug>` | `it publish <slug>` |
| **Inizializzare Nuovo Cliente** | `inizializza <slug>` | `it init <slug> --client "Nome" --name "Titolo"` |
| **Verificare Stato 7 Fasi** | `stato <slug>` | `it status <slug>` |
| **Validare Documento Attivo** | `valida` *(o tasto `Ctrl+Shift+B`)* | `it validate <percorso_file>` |
| **Cruscotto Grafico Esecutivo** | `ui` *(o `dashboard`)* | `it ui` |
| **Collaudo Completo Sistema** | `test-suite` | `it test-suite` |
| **Avvio Quotidiano "1-Clic"** | *Doppio clic sull'icona Desktop:*<br>**`ITInfra - Aggiorna e Avvia`** | `it start` |

🖥️ *Per visualizzare il Cruscotto Esecutivo grafico con telemetria e azioni rapide, digita semplicemente **`ui`**.*

---

### ⚡ Esecuzione Deterministica dei Comandi a 1 Parola (Zero-Hesitation)
Se l'utente digita uno di questi trigger rapidi, esegui immediatamente con `run_command` senza fare domande preventive né cercare file:
- **`"ui"`** o **`"dashboard"`** $\rightarrow$ `python scripts/itinfra.py ui` ed incorpora nella risposta il tag `<agent-embed src="file:///...">` stampato dall'output del comando. *(⚠️ CRITICO: NON inserire MAI codice HTML all'interno del tag `<agent-embed>`. Deve contenere ESCLUSIVAMENTE l'attributo `src="file:///..."`, altrimenti l'interfaccia mostrerà l'errore "Invalid embed:").*
- **`"aggiorna"`** o **`"update"`** $\rightarrow$ `python scripts/itinfra_sync.py`
- **`"controlla"`** o **`"check"`** $\rightarrow$ `python scripts/itinfra.py check-share`
- **`"pubblica <slug>"`** $\rightarrow$ `python scripts/itinfra.py publish <slug>`
- **`"stato <slug>"`** $\rightarrow$ `python scripts/itinfra.py status <slug>`
- **`"valida <file>"`** $\rightarrow$ `python scripts/itinfra.py validate <file>`
- **`"test-suite"`** $\rightarrow$ `python scripts/itinfra.py test-suite --no-html`
