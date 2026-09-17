#!/usr/bin/env python3
"""
scripts/itinfra_interview.py
----------------------------
Modular Checkpointed Interview Manager per ITInfra (Release v0.9.12).
Gestisce l'intervista tecnica per la raccolta requisiti suddivisa in 5 blocchi atomici:
  1. scope    - Ambito, Stakeholder, Sedi e SLA
  2. network  - Indirizzamento IP, Supernet, AD, Switch Core, ZeroTier
  3. compute  - Hypervisor, Workstation Host, Macchine Virtuali e Storage
  4. security - Firewall, Matrice Accessi, Segmentazione e Backup
  5. atp      - Criteri di Accettazione, Finestra di Cutover e Rollback

Risolve la saturazione della finestra di contesto (Context Window Saturation)
salvando progressivamente le risposte su disco (_scratchpad.md e project-manifest.yaml).
100% Offline-First, Zero Dipendenze Esterne.
"""

import os
import re
import sys
import json
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"

def colorize(text: str, color_code: str) -> str:
    if sys.platform == "win32" and not os.environ.get("WT_SESSION") and not os.environ.get("ANSICON"):
        return text
    return f"{color_code}{text}{COLOR_RESET}"


INTERVIEW_BLOCKS = {
    "scope": {
        "title": "Blocco 1: Ambito, Stakeholder e SLA (RTO/RPO)",
        "phase": "1. Assessment & URS",
        "description": "Definizione perimetro del progetto, sedi fisiche, lead architect e requisiti di continuità di servizio.",
        "fields": [
            ("customer", "Nome Azienda / Cliente finale"),
            ("project_name", "Titolo esteso del progetto"),
            ("lead_architect", "System Architect / Lead Engineer responsabile"),
            ("primary_site", "Codice e ubicazione della sede principale (es. HQ-01, Milano)"),
            ("secondary_site", "Codice e ubicazione eventuale sede secondaria o DR"),
            ("tier1_rto", "Recovery Time Objective target (es. 2 ore, 15 minuti)"),
            ("tier1_rpo", "Recovery Point Objective target (es. 1 ora, RPO zero)")
        ],
        "prompt_template": """### 📋 INTERVISTA GUIDATA ITINFRA — BLOCCO 1: SCOPE, SEDI E SLA
Per favore fornisci le seguenti informazioni chiave sul progetto:
1. **Cliente finale:** (Ragione sociale completa)
2. **Titolo Progetto:** (Nome descrittivo dell'infrastruttura)
3. **Lead Architect / Referente Tecnico:** (Nome e ruolo)
4. **Sede/i coinvolte:** (Codice sede e indirizzo per ciascun sito, es. HQ Milano)
5. **Requisiti SLA:** RTO massimo tollerabile e RPO desiderato per i servizi critici.

*(Rispondi anche solo per punti elenco numerati. I dati verranno salvati su disco).*"""
    },
    "network": {
        "title": "Blocco 2: Rete, Indirizzamento IP e Connettività",
        "phase": "2. Network Baseline",
        "description": "Supernet IPv4, indirizzo Domain Controller, modello Core Switch, subnet e Overlay SDN.",
        "fields": [
            ("supernet_ipv4", "Supernet IPv4 assegnata alla sede (es. 192.168.120.0/24 o 10.10.0.0/16)"),
            ("dc_ip", "Indirizzo IP statico del Domain Controller primario (es. 192.168.120.239)"),
            ("ad_domain", "Nome FQDN del dominio Active Directory (es. azienda.local o azienda.lan)"),
            ("gateway_ip", "Indirizzo IP del Gateway / Router / Firewall (es. 192.168.120.1)"),
            ("core_switch_model", "Modello dello Switch di Centro Stella (es. MikroTik CRS326-24G-2S+RM)"),
            ("zerotier_network_id", "Eventuale Network ID ZeroTier SDN (o <DA-RICHIEDERE> se assente)")
        ],
        "prompt_template": """### 📋 INTERVISTA GUIDATA ITINFRA — BLOCCO 2: RETE E INDIRIZZAMENTO IP
Per favore indica i parametri di rete essenziali:
1. **Supernet / Subnet LAN principale:** (es. 192.168.120.0/24)
2. **IP Domain Controller (DNS primario):** (es. 192.168.120.239)
3. **Dominio Active Directory (FQDN):** (es. severino.local)
4. **Gateway predefinito / Firewall:** (IP e modello apparato)
5. **Switch Core / Accesso:** (Vendor e modello, es. MikroTik CRS326-24G-2S+RM)
6. **Overlay SDN / VPN remota:** (es. ZeroTier Network ID o WireGuard)"""
    },
    "compute": {
        "title": "Blocco 3: Compute, Virtualizzazione e Storage",
        "phase": "2. Infrastructure Design",
        "description": "Host fisico hypervisor, sistema operativo host, macchine virtuali e allocazione storage.",
        "fields": [
            ("hypervisor_host", "Hardware server fisico / workstation host (es. HP Z4 G4, Dell R750)"),
            ("hypervisor_os", "Sistema operativo hypervisor (es. Windows Server 2022 Hyper-V, Proxmox VE, ESXi)"),
            ("vm_list", "Elenco delle VM previste con ruolo e IP (es. dc01, fs01, app01)"),
            ("storage_type", "Tipologia storage (es. NVMe RAID1, SSD Dedicated VHDX, NAS QNAP)"),
            ("backup_storage", "Destinazione backup secondario (es. QNAP TS-233 su IP .250)")
        ],
        "prompt_template": """### 📋 INTERVISTA GUIDATA ITINFRA — BLOCCO 3: COMPUTE E VIRTUALIZZAZIONE
Fornisci i dettagli sull'infrastruttura di virtualizzazione:
1. **Server Fisico / Host:** (Vendor, modello, CPU e RAM, es. HP Z4 Xeon 64GB)
2. **Hypervisor / OS Host:** (es. Windows Server 2022 Datacenter Hyper-V)
3. **Macchine Virtuali (VM):** Quali VM sono previste? (Nome, ruolo e IP dedicato)
4. **Storage Dati:** (Capacità VHDX, dischi fisici passthrough o LUN dedicate)
5. **Storage di Backup:** (Appliance NAS o repository locale, es. QNAP TS-233)"""
    },
    "security": {
        "title": "Blocco 4: Sicurezza, Matrice Accessi e Vault",
        "phase": "2. Security & Compliance",
        "description": "Segmentazione, policy perimetrali, protezione credenziali vault:// e retention backup.",
        "fields": [
            ("vault_prefix", "Prefisso URI per credenziali protette (es. vault://it/projects/<slug>)"),
            ("firewall_policies", "Regole di ingresso/uscita WAN e isolamento VLAN ospiti/IoT"),
            ("backup_retention", "Politica di retention backup (es. 14 giorni locali, replica settimanale off-site)"),
            ("antivirus_edr", "Soluzione EDR / Endpoint Security adottata (es. Defender for Endpoint)")
        ],
        "prompt_template": """### 📋 INTERVISTA GUIDATA ITINFRA — BLOCCO 4: SICUREZZA E CREDENZIALI
Indica i requisiti di sicurezza e governance:
1. **Prefisso Vault Secrets:** (Usa il formato sicuro `vault://it/projects/<slug>/...`)
2. **Segmentazione di Rete:** (VLAN separate per gestione, dati, ospiti o telecamere?)
3. **Policy di Backup:** Frequenza di esecuzione e giorni di retention dei dati.
4. **Sicurezza Endpoint:** (Soluzione antivirus / EDR prevista)"""
    },
    "atp": {
        "title": "Blocco 5: Collaudo (ATP), Rollback e Cutover",
        "phase": "3-6. Procurement, ATP & Cutover",
        "description": "Criteri di accettazione, piano di cutover e condizioni per eventuale rollback immediato.",
        "fields": [
            ("cutover_window", "Finestra oraria di cutover (es. Sabato dalle 14:00 alle 20:00)"),
            ("atp_critical_tests", "Test critici obbligatori (es. Ping gateway, Join dominio AD, Accesso share SMB, DNS lookup)"),
            ("rollback_trigger", "Condizione scatenante per attivare il rollback (es. Mancato boot host entro 1h, perdita connettività WAN)")
        ],
        "prompt_template": """### 📋 INTERVISTA GUIDATA ITINFRA — BLOCCO 5: COLLAUDO (ATP) E ROLLBACK
Definisci le modalità di transizione e accettazione:
1. **Finestra di Cutover:** (Giorno e orario pianificato per il passaggio in produzione)
2. **Test di Collaudo Critici:** Quali verifiche devono avere esito POSITIVO al 100% per accettare il rilascio?
3. **Trigger di Rollback:** Qual è la condizione per cui si annulla il cutover e si ripristina lo stato precedente?"""
    }
}


class InterviewManager:
    """Gestore progressivo dell'intervista tecnica su standard OKF v0.2."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent
        self.projects_dir = self.repo_root / "projects"

    def _get_state_file(self, slug: str) -> Path:
        return self.projects_dir / slug / "_interview_state.json"

    def load_state(self, slug: str) -> Dict[str, Any]:
        sf = self._get_state_file(slug)
        if sf.exists():
            try:
                return json.loads(sf.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "slug": slug,
            "completed_blocks": [],
            "answers": {},
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    def save_state(self, slug: str, state: Dict[str, Any]):
        sf = self._get_state_file(slug)
        sf.parent.mkdir(parents=True, exist_ok=True)
        state["last_updated"] = datetime.now(timezone.utc).isoformat()
        sf.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    def get_status_report(self, slug: str) -> str:
        project_dir = self.projects_dir / slug
        if not project_dir.exists():
            return colorize(f"Progetto '{slug}' non trovato in {project_dir}", COLOR_RED)

        state = self.load_state(slug)
        completed = set(state.get("completed_blocks", []))

        lines = [
            colorize("\n" + "=" * 68, COLOR_BOLD + COLOR_CYAN),
            f"  🎙️ ITINFRA CHECKPOINTED INTERVIEW: '{slug}'",
            colorize("=" * 68, COLOR_BOLD + COLOR_CYAN),
            "Avanzamento Raccolta Requisiti a Blocchi Atomici:\n"
        ]

        total_blocks = len(INTERVIEW_BLOCKS)
        completed_count = 0

        for block_id, binfo in INTERVIEW_BLOCKS.items():
            is_done = block_id in completed
            if is_done:
                completed_count += 1
                status_icon = colorize("[COMPLETATO] ", COLOR_GREEN + COLOR_BOLD)
            else:
                status_icon = colorize("[IN ATTESA]   ", COLOR_YELLOW + COLOR_BOLD)

            lines.append(f"  {status_icon} {binfo['title']:<48} (ID: {block_id})")

        pct = int((completed_count / total_blocks) * 100)
        lines.append(colorize("\n" + "-" * 68, COLOR_BOLD))
        lines.append(f"Stato complessivo intervista: {completed_count}/{total_blocks} blocchi ({pct}%)")

        # Suggerimento prossimo blocco
        next_block = None
        for b_id in INTERVIEW_BLOCKS.keys():
            if b_id not in completed:
                next_block = b_id
                break

        if next_block:
            lines.append(f"\nProssimo blocco da affrontare:")
            lines.append(colorize(f"  it interview {slug} --prompt {next_block}", COLOR_CYAN + COLOR_BOLD))
        else:
            lines.append(colorize("\n✓ Intervista completa al 100%! Tutti i 5 blocchi sono stati acquisiti.", COLOR_GREEN + COLOR_BOLD))
            lines.append(f"Puoi procedere allo scaffolding o alla revisione: it status {slug}")

        lines.append(colorize("=" * 68 + "\n", COLOR_BOLD + COLOR_CYAN))
        return "\n".join(lines)

    def get_prompt_for_block(self, slug: str, block_id: str) -> str:
        b = INTERVIEW_BLOCKS.get(block_id.lower())
        if not b:
            return colorize(f"Blocco '{block_id}' non valido. Opzioni: {list(INTERVIEW_BLOCKS.keys())}", COLOR_RED)
        return b["prompt_template"]

    def record_answers(
        self,
        slug: str,
        block_id: str,
        answers: Dict[str, str],
        mark_completed: bool = True
    ) -> Tuple[bool, str]:
        """Salva le risposte su disco (_scratchpad.md, manifesto e stato)."""
        project_dir = self.projects_dir / slug
        if not project_dir.exists():
            return False, f"Progetto '{slug}' non trovato."

        b = INTERVIEW_BLOCKS.get(block_id.lower())
        if not b:
            return False, f"Blocco '{block_id}' non riconosciuto."

        # 1. Aggiorna lo stato JSON
        state = self.load_state(slug)
        if "answers" not in state:
            state["answers"] = {}
        state["answers"].setdefault(block_id, {}).update(answers)
        if mark_completed and block_id not in state["completed_blocks"]:
            state["completed_blocks"].append(block_id)
        self.save_state(slug, state)

        # 2. Aggiorna lo scratchpad di memoria (_scratchpad.md)
        try:
            from itinfra_memory import MemoryManager
            mem_mgr = MemoryManager(repo_root=self.repo_root)
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            lines = [f"\n### Intervista Checkpoint: {b['title']} [{timestamp}]"]
            for k, v in answers.items():
                lines.append(f"- **{k}**: {v}")
            mem_mgr.append_entry(slug, "decisioni", "\n".join(lines))
        except Exception:
            pass

        # 3. Propaga chiavi note nel manifesto
        self._propagate_to_manifest(slug, answers)

        return True, f"Risposte per il blocco '{block_id}' salvate con successo nello scratchpad e nel manifesto."

    def _propagate_to_manifest(self, slug: str, answers: Dict[str, str]):
        manifest_file = self.projects_dir / slug / "project-manifest.yaml"
        if not manifest_file.exists():
            return

        text = manifest_file.read_text(encoding="utf-8")

        for key, val in answers.items():
            if not val or val.startswith("<"):
                continue
            # Regex per sostituire valori esistenti
            pattern = rf'({key}:\s*)"[^"]*"'
            if re.search(pattern, text):
                text = re.sub(pattern, rf'\g<1>"{val}"', text)

        manifest_file.write_text(text, encoding="utf-8")


def cmd_interview(args) -> int:
    """Handler CLI per il comando interview."""
    manager = InterviewManager()
    slug = args.slug.strip().lower()

    if getattr(args, "status", False) or (not getattr(args, "block", None) and not getattr(args, "prompt", None) and not getattr(args, "set", None)):
        print(manager.get_status_report(slug))
        return 0

    if getattr(args, "prompt", None):
        print(manager.get_prompt_for_block(slug, args.prompt))
        return 0

    if getattr(args, "block", None) and not getattr(args, "set", None):
        print(manager.get_prompt_for_block(slug, args.block))
        return 0

    if getattr(args, "set", None):
        block_id = getattr(args, "block", None) or "scope"
        raw_kvs = args.set
        parsed_kvs = {}
        for kv in raw_kvs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                parsed_kvs[k.strip()] = v.strip()
            else:
                parsed_kvs[kv.strip()] = "true"

        ok, msg = manager.record_answers(slug, block_id, parsed_kvs, mark_completed=True)
        if ok:
            print(colorize(f"\n[OK] {msg}\n", COLOR_GREEN + COLOR_BOLD))
            return 0
        else:
            print(colorize(f"\n[ERRORE] {msg}\n", COLOR_RED + COLOR_BOLD))
            return 1

    return 0


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Modular Checkpointed Interview Manager per ITInfra")
    parser.add_argument("slug", help="Slug del progetto")
    parser.add_argument("--status", action="store_true", help="Mostra lo stato di completamento dei 5 blocchi")
    parser.add_argument("--prompt", choices=list(INTERVIEW_BLOCKS.keys()), help="Genera il prompt per l'agente o il tecnico per lo specifico blocco")
    parser.add_argument("--block", choices=list(INTERVIEW_BLOCKS.keys()), help="Seleziona il blocco attivo")
    parser.add_argument("--set", nargs="+", help="Salva una o più risposte nel formato chiave=valore")
    args = parser.parse_args()
    sys.exit(cmd_interview(args))
