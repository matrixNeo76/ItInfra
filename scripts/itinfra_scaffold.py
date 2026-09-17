#!/usr/bin/env python3
"""
scripts/itinfra_scaffold.py
--------------------------
Auto-Scaffolding Engine per ITInfra (Release v0.9.10).
Analizza il file 'project-manifest.yaml' di un progetto e propaga determinismo,
metadati estesi, parametri di rete, inventory hardware e riferimenti vault
all'interno dei 10 documenti OKF v0.2, azzerando il lavoro manuale iniziale
e preservando la politica Zero-Hallucination.
"""

import os
import re
import sys
import yaml
from pathlib import Path
from datetime import date
from typing import Dict, Any, List, Tuple, Optional

# Colori terminale ANSI
COLOR_RESET = "\033[0m"
COLOR_BOLD = "\033[1m"
COLOR_GREEN = "\033[32m"
COLOR_CYAN = "\033[36m"
COLOR_YELLOW = "\033[33m"
COLOR_RED = "\033[31m"

def colorize(text: str, color_code: str) -> str:
    return f"{color_code}{text}{COLOR_RESET}"

class ProjectScaffolder:
    """Motore di propagazione automatica dal manifesto di progetto ai template OKF v0.2."""

    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            self.repo_root = Path(__file__).resolve().parent.parent
        else:
            self.repo_root = Path(repo_root)

        self.templates_dir = self.repo_root / "templates"
        self.projects_dir = self.repo_root / "projects"

    def find_similar_slug(self, slug: str, cutoff: float = 0.70) -> List[str]:
        """Restituisce eventuali slug esistenti simili a quello richiesto per prevenire typo."""
        import difflib
        if not self.projects_dir.exists():
            return []
        existing = [
            d.name for d in self.projects_dir.iterdir()
            if d.is_dir() and not d.name.startswith(("_", ".")) and d.name != slug
        ]
        return difflib.get_close_matches(slug, existing, n=3, cutoff=cutoff)

    def scaffold(self, slug: str, dry_run: bool = False, force: bool = False) -> Tuple[bool, str, Dict[str, Any]]:
        """Esegue lo scaffolding dei 10 documenti OKF v0.2 per lo slug indicato."""
        project_dir = self.projects_dir / slug
        manifest_file = project_dir / "project-manifest.yaml"

        auto_initialized = False
        if not project_dir.exists() or not manifest_file.exists():
            # Typo Guard: se il progetto non esiste, verifica se ci sono progetti simili
            if not force and not project_dir.exists():
                similar = self.find_similar_slug(slug)
                if similar:
                    sim_str = ", ".join(f"'{s}'" for s in similar)
                    return (
                        False,
                        f"[TYPO GUARD] Il progetto '{slug}' non esiste, ma sono stati trovati progetti con nome simile: {sim_str}. "
                        f"Se intendevi lavorare su uno di essi, correggi il comando. "
                        f"Per forzare la creazione del nuovo progetto '{slug}', usa il flag --force.",
                        {"similar_projects": similar}
                    )

            auto_initialized = True
            if not dry_run:
                project_dir.mkdir(parents=True, exist_ok=True)
                template_manifest = self.repo_root / "projects" / "_template" / "project-manifest.yaml"
                client_name = f"Cliente {slug.capitalize()}"
                proj_name = f"Progetto {slug.capitalize()}"
                if template_manifest.exists():
                    text = template_manifest.read_text(encoding="utf-8")
                    text = re.sub(r'project_id:\s*"[^"]+"', f'project_id: "{slug}"', text)
                    text = re.sub(r'project_name:\s*"[^"]+"', f'project_name: "{proj_name}"', text)
                    text = re.sub(r'customer:\s*"[^"]+"', f'customer: "{client_name}"', text)
                    manifest_file.write_text(text, encoding="utf-8")
                else:
                    manifest_file.write_text(f"""project_id: "{slug}"
project_name: "{proj_name}"
customer: "{client_name}"
lead_architect: "System Architect"
status: "in-planning"
version: "0.1.0"
""", encoding="utf-8")
                try:
                    from itinfra_memory import MemoryManager
                    mem_mgr = MemoryManager(repo_root=self.repo_root)
                    mem_mgr.init_scratchpad(slug)
                except Exception:
                    pass

        # 1. Carica e valida il manifesto
        if auto_initialized and dry_run:
            manifest_data = {
                "project_id": slug,
                "project_name": f"Progetto {slug.capitalize()}",
                "customer": f"Cliente {slug.capitalize()}",
                "lead_architect": "System Architect",
                "owner_team": "IT Operations & Architecture",
                "status": "in-planning",
                "version": "0.1.0"
            }
        else:
            try:
                with open(manifest_file, "r", encoding="utf-8") as mf:
                    manifest_data = yaml.safe_load(mf) or {}
            except Exception as e:
                return False, f"Errore nel parsing YAML del manifesto: {e}", {}

        # 2. Estrai i dati certi (Ground Truth)
        project_id = str(manifest_data.get("project_id") or slug)
        project_name = str(manifest_data.get("project_name") or f"Progetto {slug.capitalize()}")
        customer = str(manifest_data.get("customer") or "Cliente Enterprise")
        lead_architect = str(manifest_data.get("lead_architect") or "System Architect")
        owner_team = str(manifest_data.get("owner_team") or "IT Operations & Architecture")
        today_str = date.today().isoformat()
        created_at = str(manifest_data.get("created_at") or today_str)

        sites = manifest_data.get("sites") or []
        site_code = "HQ-01"
        site_name = "Sede Principale"
        if sites and isinstance(sites, list) and len(sites) > 0 and isinstance(sites[0], dict):
            site_code = sites[0].get("code", "HQ-01")
            site_name = sites[0].get("name", "Sede Principale")

        net = manifest_data.get("network_baseline") or {}
        supernet_ipv4 = str(net.get("supernet_ipv4") or "")
        ad_domain = str(net.get("active_directory_domain") or "")
        dc_ip = str(net.get("dc_ip") or "")
        vault_prefix = str(net.get("vault_secret_prefix") or f"vault://it/projects/{slug}")
        core_switch = str(net.get("core_switch_model") or "")

        hw = manifest_data.get("hardware_baseline") or {}
        hypervisor_host = str(hw.get("hypervisor_host") or "")
        hypervisor_os = str(hw.get("hypervisor_os") or "")

        sla = manifest_data.get("sla_baseline") or {}
        tier1_rto = str(sla.get("tier1_rto") or "")
        tier1_rpo = str(sla.get("tier1_rpo") or "")

        # 3. Mappa dei template standard (1-10)
        template_files = sorted([
            f for f in self.templates_dir.glob("*.md")
            if re.match(r"^\d{2}-", f.name) and not f.name.startswith("00-") and not f.name.startswith("99-")
        ])

        if not template_files:
            return False, f"Nessun template numerato trovato in: {self.templates_dir}", {}

        stats = {
            "slug": slug,
            "auto_initialized": auto_initialized,
            "files_scaffolded": 0,
            "files_skipped": 0,
            "replacements_count": 0,
            "details": []
        }

        # 4. Processa ciascun documento
        for tpl in template_files:
            target_file = project_dir / tpl.name
            already_exists = target_file.exists()

            if already_exists and not force:
                # Modifica sul file esistente per completare i placeholder rimasti
                source_content = target_file.read_text(encoding="utf-8")
                action_label = "Aggiornato (in-place)"
            else:
                source_content = tpl.read_text(encoding="utf-8")
                action_label = "Creato da template" if not already_exists else "Sovrascritto (force)"

            modified_content, count = self._apply_replacements(
                source_content,
                slug=slug,
                project_id=project_id,
                project_name=project_name,
                customer=customer,
                lead_architect=lead_architect,
                owner_team=owner_team,
                site_code=site_code,
                site_name=site_name,
                created_at=created_at,
                today_str=today_str,
                supernet_ipv4=supernet_ipv4,
                ad_domain=ad_domain,
                dc_ip=dc_ip,
                vault_prefix=vault_prefix,
                core_switch=core_switch,
                hypervisor_host=hypervisor_host,
                hypervisor_os=hypervisor_os,
                tier1_rto=tier1_rto,
                tier1_rpo=tier1_rpo
            )

            if not dry_run:
                target_file.write_text(modified_content, encoding="utf-8")

            stats["files_scaffolded"] += 1
            stats["replacements_count"] += count
            stats["details"].append({
                "file": tpl.name,
                "action": action_label,
                "replacements": count
            })

        # 5. Aggiorna lo stato dei documenti nel manifesto
        if not dry_run:
            try:
                doc_map = manifest_data.get("documents") or {}
                for detail in stats["details"]:
                    doc_key = detail["file"].replace(".md", "")
                    if doc_map.get(doc_key) in ("missing", None):
                        doc_map[doc_key] = "draft"
                manifest_data["documents"] = doc_map
                manifest_data["updated_at"] = today_str

                with open(manifest_file, "w", encoding="utf-8") as mf:
                    yaml.safe_dump(manifest_data, mf, allow_unicode=True, sort_keys=False)
            except Exception:
                pass

        msg = f"Scaffolding completato per '{slug}': {stats['files_scaffolded']} documenti processati ({stats['replacements_count']} sostituzioni)."
        return True, msg, stats

    def _apply_replacements(
        self,
        text: str,
        slug: str,
        project_id: str,
        project_name: str,
        customer: str,
        lead_architect: str,
        owner_team: str,
        site_code: str,
        site_name: str,
        created_at: str,
        today_str: str,
        supernet_ipv4: str,
        ad_domain: str,
        dc_ip: str,
        vault_prefix: str,
        core_switch: str,
        hypervisor_host: str,
        hypervisor_os: str,
        tier1_rto: str,
        tier1_rpo: str
    ) -> Tuple[str, int]:
        """Applica le sostituzioni di ground truth sui token del template."""
        total_replacements = 0

        replacements = [
            # Frontmatter univoci
            (r"<project_slug>", slug),
            (r"<PROJECT_ID>", project_id),
            (r"<nome progetto>", project_name),
            (r"<SITE_CODE>", site_code),
            (r"<cliente>", customer),
            (r"<nome autore>", lead_architect),
            (r'author:\s*"<nome>"', f'author: "{lead_architect}"'),
            (r'owner_team:\s*"<team>"', f'owner_team: "{owner_team}"'),
            (r"<team responsabile>", owner_team),
            (r"<incident_id>", "01"),
            (r"<YYYY-MM-DD>", created_at),
            (r'title:\s*"([^"]*)<titolo progetto[^>]*>([^"]*)"', rf'title: "\1{project_name}\2"'),
            (r'title:\s*"([^"]*)<nome progetto>([^"]*)"', rf'title: "\1{project_name}\2"'),
            
            # Vault
            (r"vault://it/<project>/", f"{vault_prefix}/"),
            (r"vault://it/<PROJECT_ID>/", f"{vault_prefix}/"),
            (r"vault://it/projects/<slug>/", f"{vault_prefix}/"),
        ]

        if supernet_ipv4:
            replacements.extend([
                (r"<IP_SUBNET>", supernet_ipv4),
                (r"<supernet_ipv4>", supernet_ipv4),
            ])

        if ad_domain:
            replacements.extend([
                (r"<DOMINIO_AD>", ad_domain),
                (r"<active_directory_domain>", ad_domain),
            ])

        if dc_ip:
            replacements.extend([
                (r"<DC_IP>", dc_ip),
            ])

        if core_switch:
            replacements.extend([
                (r"<SWITCH_CORE_MODEL>", core_switch),
            ])

        if hypervisor_host:
            replacements.extend([
                (r"<HYPERVISOR_HOST>", hypervisor_host),
            ])

        if hypervisor_os:
            replacements.extend([
                (r"<HYPERVISOR_OS>", hypervisor_os),
            ])

        if tier1_rto:
            replacements.extend([
                (r"<RTO_TARGET>", tier1_rto),
            ])

        if tier1_rpo:
            replacements.extend([
                (r"<RPO_TARGET>", tier1_rpo),
            ])

        for pattern, repl in replacements:
            new_text, count = re.subn(pattern, repl, text)
            if count > 0:
                text = new_text
                total_replacements += count

        return text, total_replacements

def cmd_scaffold(args) -> int:
    """Handler CLI per il comando scaffold."""
    scaffolder = ProjectScaffolder()
    ok, msg, stats = scaffolder.scaffold(
        slug=args.slug.strip().lower(),
        dry_run=getattr(args, "dry_run", False),
        force=getattr(args, "force", False)
    )

    if ok:
        print(colorize("\n" + "=" * 65, COLOR_BOLD + COLOR_GREEN))
        print(f"  [OK] AUTO-SCAFFOLDING COMPLETATO PER: '{args.slug}'")
        print("=" * 65)
        if stats.get("auto_initialized"):
            print(colorize(f"  [AUTO-INIT] Progetto '{args.slug}' non presente: manifesto inizializzato automaticamente.", COLOR_CYAN + COLOR_BOLD))
        print(f"  Documenti generati/allineati: {stats['files_scaffolded']}")
        print(f"  Sostituzioni totali:          {stats['replacements_count']}")
        if getattr(args, "dry_run", False):
            print(colorize("  MODALITÀ: SIMULAZIONE DRY-RUN (Nessun file scritto)", COLOR_YELLOW + COLOR_BOLD))
        print("\nDettaglio per file:")
        for det in stats["details"]:
            print(f"  • {det['file']:<28} | {det['action']:<22} | {det['replacements']} sostituzioni")
        print("=" * 65 + "\n")
        return 0
    else:
        print(colorize(f"\n[ERRORE SCAFFOLD] {msg}\n", COLOR_RED + COLOR_BOLD))
        return 1

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Auto-Scaffolding Engine per ITInfra")
    parser.add_argument("slug", help="Slug del progetto da scaffoldare")
    parser.add_argument("--dry-run", action="store_true", help="Simula lo scaffolding senza scrivere su disco")
    parser.add_argument("--force", action="store_true", help="Forza la riscrittura dei template esistenti")
    args = parser.parse_args()
    sys.exit(cmd_scaffold(args))
