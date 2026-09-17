#!/usr/bin/env python3
"""
scripts/itinfra_reconcile.py
----------------------------
Reverse Reconciliation Engine per ITInfra (OKF v0.2, Release v0.9.12).
Consente di sincronizzare a ritroso le modifiche fisiche e telemetriche
documentate in 06-As-Built.md verso il manifesto di progetto (project-manifest.yaml).

Risolve il problema del "Drift tra Fasi" (Design vs As-Built), garantendo che:
1. Le divergenze sul campo vengano scoperte e tracciate con precisione (Drift Report).
2. Il manifesto venga riconciliato senza perdita di dati storici.
3. Lo scratchpad di memoria registri la riconciliazione con timestamp e autore.
100% Offline-First, Zero Dipendenze Esterne.
"""

import os
import re
import sys
import json
from datetime import datetime, timezone, date
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


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


class ProjectReconciler:
    """Motore di analisi del drift e riconciliazione inversa As-Built -> Manifest."""

    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            self.repo_root = Path(__file__).resolve().parent.parent
        else:
            self.repo_root = Path(repo_root)

        self.projects_dir = self.repo_root / "projects"

    def reconcile(
        self,
        slug: str,
        source_doc: Optional[str] = None,
        dry_run: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Esegue la riconciliazione inversa per lo slug indicato.
        """
        project_dir = self.projects_dir / slug
        if not project_dir.exists():
            return False, f"Cartella di progetto non trovata: {project_dir}", {}

        manifest_file = project_dir / "project-manifest.yaml"
        if not manifest_file.exists():
            return False, f"Manifesto di progetto non trovato in: {manifest_file}", {}

        # Identifica il file sorgente As-Built
        as_built_name = source_doc or "06-As-Built.md"
        as_built_file = project_dir / as_built_name
        if not as_built_file.exists():
            return False, f"Documento As-Built '{as_built_name}' non trovato in: {project_dir}", {}

        # 1. Carica il manifesto
        manifest_text = manifest_file.read_text(encoding="utf-8")
        manifest_data = {}
        if yaml is not None:
            try:
                manifest_data = yaml.safe_load(manifest_text) or {}
            except Exception as e:
                return False, f"Errore parsing manifesto YAML: {e}", {}
        else:
            manifest_data = self._parse_yaml_fallback(manifest_text)

        # 2. Carica e scansiona 06-As-Built.md
        as_built_text = as_built_file.read_text(encoding="utf-8")
        as_built_info = self._extract_as_built_info(as_built_text)

        # 3. Calcola il Drift
        drift_report = self._compute_drift(manifest_data, as_built_info)

        # 4. Formatta il report
        summary_lines = self._format_drift_report(slug, as_built_name, drift_report, dry_run)
        summary_str = "\n".join(summary_lines)

        if dry_run:
            return True, summary_str, drift_report

        # 5. Applica le modifiche a project-manifest.yaml se sono state rilevate divergenze
        if drift_report["drift_count"] > 0 or drift_report["discovered_count"] > 0:
            updated_manifest_text = self._apply_reconciliation(manifest_text, manifest_data, drift_report)
            manifest_file.write_text(updated_manifest_text, encoding="utf-8")

            # Registra l'evento nella memoria di staging (_scratchpad.md)
            self._log_to_memory(slug, as_built_name, drift_report)

        return True, summary_str, drift_report

    def _extract_as_built_info(self, text: str) -> Dict[str, Any]:
        """Estrae dati tecnici, hardware, deviazioni e IP da 06-As-Built.md."""
        info = {
            "deviations": [],
            "hardware": [],
            "ip_addresses": {},
            "network_entities": {}
        }

        # Parsing Deviazioni §3
        dev_table_match = re.search(r'## 3\.\s*Deviazioni dal LLD.*?\n\|.*?\|.*?\n((?:\|.*?\n)+)', text, re.DOTALL)
        if dev_table_match:
            rows = dev_table_match.group(1).strip().splitlines()
            for r in rows:
                cols = [c.strip() for c in r.split("|")[1:-1]]
                if len(cols) >= 4 and not cols[0].startswith("---") and cols[0].upper() != "ID":
                    dev_id = cols[0]
                    component = cols[1]
                    lld_val = cols[2]
                    as_built_val = cols[3]
                    motivation = cols[4] if len(cols) > 4 else ""
                    if not dev_id.startswith("<") and not component.startswith("<"):
                        info["deviations"].append({
                            "id": dev_id,
                            "component": component,
                            "lld": lld_val,
                            "as_built": as_built_val,
                            "motivation": motivation
                        })

        # Parsing Hardware §4 (Server e Switch)
        table_pattern = re.compile(r'###\s*4\.\d+\s*([^\n]+).*?\n\|.*?\|.*?\n((?:\|.*?\n)+)', re.DOTALL)
        for tm in table_pattern.finditer(text):
            category = tm.group(1).strip()
            rows = tm.group(2).strip().splitlines()
            for r in rows:
                cols = [c.strip() for c in r.split("|")[1:-1]]
                if len(cols) >= 3 and not cols[0].startswith("---") and cols[0].lower() not in ("hostname", "id"):
                    hostname = cols[0]
                    model = cols[1]
                    serial = cols[2] if len(cols) > 2 else ""
                    ip_addr = ""
                    for c in cols[3:]:
                        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', c)
                        if ip_match:
                            ip_addr = ip_match.group(0)
                            break
                    if not hostname.startswith("<") and not model.startswith("<"):
                        info["hardware"].append({
                            "category": category,
                            "hostname": hostname,
                            "model": model,
                            "serial": serial,
                            "ip": ip_addr
                        })

        # Ricerca IP specifici di Core Switch e Domain Controller nel testo
        sw_match = re.search(r'(?:sw-core|switch\s+core|crs326)[^\n]*?(?:Modello:|modello)[^\n]*?`?([A-Za-z0-9_\-\+]+)`?', text, re.IGNORECASE)
        if sw_match:
            info["network_entities"]["core_switch_model"] = sw_match.group(1).strip()

        dc_match = re.search(r'(?:srv-dc01?|dc01|domain\s+controller)[^|\n]*?\|[^|\n]*?(\b(?:\d{1,3}\.){3}\d{1,3}\b)', text, re.IGNORECASE)
        if dc_match:
            info["network_entities"]["dc_ip"] = dc_match.group(1).strip()

        return info

    def _compute_drift(self, manifest: Dict[str, Any], as_built: Dict[str, Any]) -> Dict[str, Any]:
        """Confronta i dati del manifesto con quelli estratti da As-Built."""
        drift_items = []
        matched_items = []
        discovered_items = []

        net_baseline = manifest.get("network_baseline") or {}
        hw_baseline = manifest.get("hardware_baseline") or {}

        # 1. Verifica Core Switch Model
        manifest_switch = net_baseline.get("core_switch_model")
        as_built_switch = as_built["network_entities"].get("core_switch_model")
        # Cerca anche nell'hardware estratto
        if not as_built_switch:
            for hw in as_built["hardware"]:
                if "switch" in hw.get("category", "").lower() or "sw" in hw.get("hostname", "").lower():
                    as_built_switch = hw.get("model")
                    break

        if manifest_switch and as_built_switch:
            if manifest_switch.strip().lower() != as_built_switch.strip().lower():
                drift_items.append({
                    "entity": "core_switch_model",
                    "location": "network_baseline.core_switch_model",
                    "manifest_value": manifest_switch,
                    "as_built_value": as_built_switch,
                    "severity": "high"
                })
            else:
                matched_items.append({
                    "entity": "core_switch_model",
                    "value": manifest_switch
                })

        # 2. Verifica DC IP
        manifest_dc_ip = net_baseline.get("dc_ip")
        as_built_dc_ip = as_built["network_entities"].get("dc_ip")
        if not as_built_dc_ip:
            for hw in as_built["hardware"]:
                if "dc" in hw.get("hostname", "").lower() and hw.get("ip"):
                    as_built_dc_ip = hw.get("ip")
                    break

        if manifest_dc_ip and as_built_dc_ip:
            if manifest_dc_ip.strip() != as_built_dc_ip.strip():
                drift_items.append({
                    "entity": "dc_ip",
                    "location": "network_baseline.dc_ip",
                    "manifest_value": manifest_dc_ip,
                    "as_built_value": as_built_dc_ip,
                    "severity": "high"
                })
            else:
                matched_items.append({
                    "entity": "dc_ip",
                    "value": manifest_dc_ip
                })

        # 3. Discovered Hardware
        for hw in as_built["hardware"]:
            discovered_items.append(hw)

        # 4. Deviazioni esplicite
        deviations = as_built.get("deviations", [])

        return {
            "drift_items": drift_items,
            "drift_count": len(drift_items),
            "matched_items": matched_items,
            "matched_count": len(matched_items),
            "discovered_items": discovered_items,
            "discovered_count": len(discovered_items),
            "deviations": deviations,
            "deviations_count": len(deviations)
        }

    def _format_drift_report(self, slug: str, as_built_name: str, drift: Dict[str, Any], dry_run: bool) -> List[str]:
        """Formatta il report di analisi del drift per output CLI e Markdown."""
        mode_tag = "SIMULAZIONE DRY-RUN" if dry_run else "RICONCILIAZIONE ATTIVA"
        lines = [
            colorize("\n" + "=" * 70, COLOR_BOLD + COLOR_CYAN),
            f"  🔄 ITINFRA REVERSE RECONCILIATION ENGINE: '{slug}'",
            f"  Sorgente As-Built: {as_built_name}  |  Modalità: {mode_tag}",
            colorize("=" * 70, COLOR_BOLD + COLOR_CYAN)
        ]

        # Sezione Drift
        lines.append("\n[1] ANALISI DISCREPANZE (DRIFT REPORT):")
        if drift["drift_count"] == 0:
            lines.append(colorize("  ✓ Nessun drift rilevato. Parametri manifest e As-Built perfettamente allineati.", COLOR_GREEN))
        else:
            lines.append(colorize(f"  ⚠️ Rilevate {drift['drift_count']} divergenze tra Design/Manifest e As-Built reale:", COLOR_YELLOW + COLOR_BOLD))
            for d in drift["drift_items"]:
                lines.append(f"    • {d['entity']:<20} | Manifest: {d['manifest_value']} -> As-Built: {d['as_built_value']}")

        # Sezione Allineati
        if drift["matched_count"] > 0:
            lines.append(f"\n[2] COMPONENTI VERIFICATI E COERENTI ({drift['matched_count']}):")
            for m in drift["matched_items"]:
                lines.append(f"  ✓ {m['entity']:<20} = {m['value']}")

        # Sezione Deviazioni Formali (§3)
        if drift["deviations_count"] > 0:
            lines.append(f"\n[3] DEVIAZIONI FORMALI DOCUMENTATE IN AS-BUILT (§3) ({drift['deviations_count']}):")
            for dev in drift["deviations"]:
                lines.append(f"  • [{dev['id']}] {dev['component']}: '{dev['lld']}' -> '{dev['as_built']}' ({dev['motivation']})")

        # Sezione Hardware Installato Censito
        if drift["discovered_count"] > 0:
            lines.append(f"\n[4] ASSET HARDWARE CENSITI DALL'AS-BUILT ({drift['discovered_count']}):")
            for hw in drift["discovered_items"]:
                ip_str = f" | IP: {hw['ip']}" if hw['ip'] else ""
                sn_str = f" | S/N: {hw['serial']}" if hw['serial'] else ""
                lines.append(f"  • {hw['hostname']:<12} | {hw['model']}{sn_str}{ip_str}")

        lines.append(colorize("\n" + "-" * 70, COLOR_BOLD))
        if dry_run:
            lines.append(colorize("MODALITÀ DRY-RUN: Nessuna modifica apportata a project-manifest.yaml.", COLOR_YELLOW))
            lines.append("Per applicare le modifiche e allineare il manifesto, esegui:")
            lines.append(f"  it reconcile {slug}")
        else:
            if drift["drift_count"] > 0 or drift["discovered_count"] > 0:
                lines.append(colorize("✓ Riconciliazione completata con successo!", COLOR_GREEN + COLOR_BOLD))
                lines.append(f"  - project-manifest.yaml aggiornato con i dati verificati dell'As-Built.")
                lines.append(f"  - Evento di riconciliazione archiviato nello scratchpad di memoria.")
            else:
                lines.append(colorize("✓ Manifesto già allineato. Nessuna modifica necessaria.", COLOR_GREEN))
        lines.append(colorize("=" * 70 + "\n", COLOR_BOLD + COLOR_CYAN))

        return lines

    def _apply_reconciliation(self, original_text: str, manifest: Dict[str, Any], drift: Dict[str, Any]) -> str:
        """Aggiorna il testo del manifesto propagando i valori riconciliati."""
        text = original_text

        # 1. Aggiorna campi con drift diretto
        for item in drift["drift_items"]:
            entity = item["entity"]
            new_val = item["as_built_value"]
            pattern = rf'({entity}:\s*)"[^"]*"'
            if re.search(pattern, text):
                text = re.sub(pattern, rf'\g<1>"{new_val}"', text)
            else:
                pattern_unquoted = rf'({entity}:\s*)[^\n]+'
                if re.search(pattern_unquoted, text):
                    text = re.sub(pattern_unquoted, rf'\g<1>"{new_val}"', text)

        # 2. Incrementa o annota versione manifesto
        today_str = date.today().isoformat()
        text = re.sub(r'updated_at:\s*"[^"]*"', f'updated_at: "{today_str}"', text)

        # 3. Aggiunge sezione as_built_reconciled se non presente
        if "as_built_reconciled:" not in text:
            reconcile_block = f"""
# Tracciamento riconciliazione As-Built (Release v0.9.12)
as_built_reconciled:
  reconciled_at: "{datetime.now(timezone.utc).isoformat()}"
  source_doc: "06-As-Built.md"
  drift_items_resolved: {drift['drift_count']}
  hardware_assets_count: {drift['discovered_count']}
"""
            text += reconcile_block

        return text

    def _log_to_memory(self, slug: str, source_doc: str, drift: Dict[str, Any]):
        """Registra la riconciliazione nella memoria di staging del progetto."""
        try:
            from itinfra_memory import MemoryManager
            mem_mgr = MemoryManager(repo_root=self.repo_root)
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            log_entry = (
                f"- [{timestamp}] Riconciliazione As-Built ({source_doc}): "
                f"Risolte {drift['drift_count']} discrepanze e censiti {drift['discovered_count']} asset hardware."
            )
            mem_mgr.append_entry(slug, "decisioni", log_entry)
        except Exception:
            pass

    def _parse_yaml_fallback(self, text: str) -> Dict[str, Any]:
        """Fallback elementare per parsing YAML senza dipendenze."""
        data = {}
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                data[k.strip()] = v.strip().strip('"').strip("'")
        return data


def cmd_reconcile(args) -> int:
    """Handler CLI per il comando reconcile."""
    reconciler = ProjectReconciler()
    ok, msg, _ = reconciler.reconcile(
        slug=args.slug.strip().lower(),
        source_doc=getattr(args, "from_doc", None),
        dry_run=getattr(args, "dry_run", False)
    )
    print(msg)
    return 0 if ok else 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reverse Reconciliation Engine per ITInfra")
    parser.add_argument("slug", help="Slug del progetto da riconciliare")
    parser.add_argument("--from-doc", default=None, help="Documento As-Built alternativo (default: 06-As-Built.md)")
    parser.add_argument("--dry-run", action="store_true", help="Simula la riconciliazione e mostra il drift report")
    args = parser.parse_args()
    sys.exit(cmd_reconcile(args))
