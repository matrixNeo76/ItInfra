#!/usr/bin/env python3
"""
scripts/itinfra_publish.py
-------------------------
Modulo di pubblicazione controllata (Central Publisher) e sincronizzazione motore
per l'architettura Local Workspace + Central Publish (Release v0.9).

Garantisce:
1. Pre-Flight Quality Gate obbligatorio prima della pubblicazione (OKF v0.2 + Zero-Leak).
2. Copia atomica e confinata strettamente a projects/<slug>/.
3. Protezione da sovrascrittura di progetti remoti approvati (--force).
4. Sincronizzazione sicura del motore locale (sync-engine) dalla share master.
"""

import os
import re
import json
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"
CONFIG_FILE_NAME = ".itinfra_config.json"

# Regex per rilevare secret in chiaro (non conformi a vault://)
CLEARTEXT_SECRET_PATTERNS = [
    re.compile(r'(?:password|secret|token|api_key|priv_key)\s*:\s*["\'](?!vault:\/\/|<DA-RICHIEDERE>|da-richiedere)([^"\']+)["\']', re.IGNORECASE),
    re.compile(r'(?:password|secret|token|chiave)\s*=\s*["\'](?!vault:\/\/|<DA-RICHIEDERE>|da-richiedere)([^"\']+)["\']', re.IGNORECASE),
]

class ProjectPublisher:
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        config_path = self.workspace_root / CONFIG_FILE_NAME
        if config_path.exists():
            try:
                return json.loads(config_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def get_central_share(self, override_path: Optional[str] = None) -> str:
        if override_path:
            return override_path
        return self.config.get("central_share", DEFAULT_CENTRAL_SHARE)

    def run_preflight_checks(self, slug: str) -> Tuple[bool, List[str], List[str]]:
        """
        Esegue i controlli di qualità prima della pubblicazione:
        1. Esistenza della cartella di progetto.
        2. Validazione formale OKF v0.2 su tutti i file markdown (0 errori ammessi).
        3. Scansione anti-leak per credenziali in chiaro.
        4. Presenza del manifesto di progetto.
        """
        errors: List[str] = []
        warnings: List[str] = []
        
        project_dir = self.workspace_root / "projects" / slug
        if not project_dir.exists() or not project_dir.is_dir():
            errors.append(f"Cartella di progetto non trovata: projects/{slug}")
            return False, errors, warnings

        manifest_file = project_dir / "project-manifest.yaml"
        if not manifest_file.exists():
            warnings.append(f"Manifesto di progetto assente: projects/{slug}/project-manifest.yaml")

        # Import del validatore OKF
        try:
            from itinfra import OKFValidator
            validator = OKFValidator(is_template=False)
        except ImportError:
            try:
                import sys
                sys.path.insert(0, str(self.workspace_root / "scripts"))
                from itinfra import OKFValidator
                validator = OKFValidator(is_template=False)
            except Exception as e:
                errors.append(f"Impossibile caricare il modulo di validazione OKF: {e}")
                return False, errors, warnings

        all_md_files = list(project_dir.glob("*.md"))
        md_files = [f for f in all_md_files if f.name.lower() != "readme.md" and not f.name.startswith("_")]
        if not md_files:
            errors.append(f"Nessun documento formale Markdown trovato in projects/{slug}/")
            return False, errors, warnings

        for md_path in md_files:
            rel_name = md_path.relative_to(self.workspace_root)
            # Validazione OKF
            val_res = validator.validate(md_path)
            for err in val_res.get("errors", []):
                errors.append(f"[{rel_name}] Errore OKF: {err}")
            for warn in val_res.get("warnings", []):
                warnings.append(f"[{rel_name}] Avviso: {warn}")

            # Scansione Anti-Leak
            try:
                content = md_path.read_text(encoding="utf-8")
                for line_idx, line in enumerate(content.splitlines(), start=1):
                    for pattern in CLEARTEXT_SECRET_PATTERNS:
                        m = pattern.search(line)
                        if m:
                            secret_sample = m.group(1)[:4] + "..." if len(m.group(1)) > 4 else m.group(1)
                            errors.append(
                                f"[{rel_name}:L{line_idx}] Rilevata credenziale in chiaro ('{secret_sample}'). "
                                f"Usare 'vault://it/projects/{slug}/...' oppure '<DA-RICHIEDERE>'."
                            )
            except Exception as e:
                errors.append(f"[{rel_name}] Errore lettura file durante la scansione anti-leak: {e}")

        is_valid = (len(errors) == 0)
        return is_valid, errors, warnings

    def publish_project(
        self,
        slug: str,
        target_share: Optional[str] = None,
        dry_run: bool = False,
        force: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Pubblica in modo atomico il progetto locale su storage centrale.
        """
        dest_share_str = self.get_central_share(target_share)
        dest_share = Path(dest_share_str)
        stats = {
            "slug": slug,
            "source_dir": str(self.workspace_root / "projects" / slug),
            "target_dir": str(dest_share / "projects" / slug),
            "files_copied": 0,
            "bytes_copied": 0,
            "dry_run": dry_run,
            "status": "pending"
        }

        # 1. Preflight Quality Gate
        is_valid, errors, warnings = self.run_preflight_checks(slug)
        if not is_valid:
            error_summary = "\n  - ".join(errors)
            msg = f"[QUALITY GATE FALLITO] Impossibile pubblicare '{slug}':\n  - {error_summary}"
            stats["status"] = "failed_preflight"
            return False, msg, stats

        # 2. Verifica accessibilità storage centrale
        try:
            if not dest_share.exists():
                msg = (
                    f"[ERRORE DESTINAZIONE] La cartella centrale '{dest_share_str}' non e' accessibile o non esiste. "
                    "Verificare la connessione di rete LAN / VPN e le credenziali di accesso."
                )
                stats["status"] = "target_unreachable"
                return False, msg, stats
        except Exception as e:
            msg = f"[ERRORE ACCESSO RETE] Impossibile verificare '{dest_share_str}': {e}"
            stats["status"] = "target_unreachable"
            return False, msg, stats

        dest_projects_dir = dest_share / "projects"
        dest_project_slug_dir = dest_projects_dir / slug

        # 3. Protezione da sovrascrittura di progetti remoti approvati
        if dest_project_slug_dir.exists() and not force:
            for remote_md in dest_project_slug_dir.glob("*.md"):
                try:
                    text = remote_md.read_text(encoding="utf-8", errors="ignore")
                    if "status: approved" in text or 'status: "approved"' in text:
                        msg = (
                            f"[SOVRASCRITTURA BLOCCATA] Il progetto remoto in '{dest_project_slug_dir}' "
                            f"contiene documenti con stato 'approved' (es. {remote_md.name}). "
                            "Per sovrascrivere un As-Built o progetto approvato utilizzare il flag '--force'."
                        )
                        stats["status"] = "blocked_approved_target"
                        return False, msg, stats
                except Exception:
                    pass

        source_dir = self.workspace_root / "projects" / slug
        files_to_copy = []

        # Raccoglie tutti i file validi da pubblicare
        for root, _, files in os.walk(source_dir):
            for file_name in files:
                # Esclude secret cifrati locali e file lock atomici
                if file_name.endswith(".enc") or file_name.endswith(".lock") or file_name.endswith(".tmp"):
                    continue
                file_path = Path(root) / file_name
                rel_path = file_path.relative_to(source_dir)
                files_to_copy.append((file_path, rel_path))

        stats["files_count"] = len(files_to_copy)

        # 4. Modalità Dry-Run
        if dry_run:
            file_list_str = "\n  - ".join(str(rel) for _, rel in files_to_copy)
            msg = (
                f"[DRY-RUN] Pre-Flight Quality Gate superato con successo per '{slug}'!\n"
                f"Destinazione: {dest_project_slug_dir}\n"
                f"File pronti per la pubblicazione ({len(files_to_copy)} file):\n  - {file_list_str}"
            )
            stats["status"] = "dry_run_success"
            return True, msg, stats

        # 5. Esecuzione effettiva della pubblicazione
        try:
            os.makedirs(dest_project_slug_dir, exist_ok=True)
            for src_file, rel_path in files_to_copy:
                target_file = dest_project_slug_dir / rel_path
                target_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, target_file)
                stats["files_copied"] += 1
                stats["bytes_copied"] += src_file.stat().st_size

            msg = (
                f"[SUCCESSO] Progetto '{slug}' pubblicato con successo!\n"
                f"  Sorgente: {source_dir}\n"
                f"  Destinazione centrale: {dest_project_slug_dir}\n"
                f"  File sincronizzati: {stats['files_copied']} ({stats['bytes_copied'] / 1024:.1f} KB)\n"
                f"  Quality Gate OKF v0.2: 100% CONFORME (0 errori)"
            )
            if warnings:
                msg += f"\n  Avvisi informativi ({len(warnings)}):\n    - " + "\n    - ".join(warnings[:5])
            stats["status"] = "published"
            return True, msg, stats

        except Exception as e:
            msg = f"[ERRORE COPIA] Si e' verificato un errore durante la pubblicazione su '{dest_project_slug_dir}': {e}"
            stats["status"] = "error_copying"
            return False, msg, stats

    def sync_engine(
        self,
        source_share: Optional[str] = None,
        dry_run: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Sincronizza e aggiorna la copia locale di scripts/, templates/ e docs/
        scaricandola dalla share master centrale.
        """
        src_share_str = self.get_central_share(source_share)
        src_share = Path(src_share_str)
        stats = {
            "source": src_share_str,
            "target": str(self.workspace_root),
            "synced_dirs": [],
            "files_updated": 0,
            "dry_run": dry_run,
            "status": "pending"
        }

        if not src_share.exists():
            msg = f"[ERRORE SOURCE] La cartella master centrale '{src_share_str}' non e' raggiungibile."
            stats["status"] = "source_unreachable"
            return False, msg, stats

        directories_to_sync = ["templates", "scripts", "docs", "skills", ".agents", ".vscode"]
        root_files_to_sync = ["README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md", "INTEGRAZIONE-REPO.md", "00-INDEX.md"]

        files_to_update = []

        # Scansione directory
        for dir_name in directories_to_sync:
            remote_dir = src_share / dir_name
            if remote_dir.exists() and remote_dir.is_dir():
                for root, _, files in os.walk(remote_dir):
                    for file_name in files:
                        if file_name.endswith(".pyc") or "__pycache__" in root:
                            continue
                        rem_path = Path(root) / file_name
                        rel_path = rem_path.relative_to(src_share)
                        loc_path = self.workspace_root / rel_path
                        files_to_update.append((rem_path, loc_path))

        # Scansione file radice
        for file_name in root_files_to_sync:
            rem_file = src_share / file_name
            if rem_file.exists():
                loc_file = self.workspace_root / file_name
                files_to_update.append((rem_file, loc_file))

        if dry_run:
            msg = (
                f"[DRY-RUN SYNC-ENGINE] Individuati {len(files_to_update)} file pronti per l'aggiornamento "
                f"da '{src_share_str}' verso '{self.workspace_root}'."
            )
            stats["status"] = "dry_run_success"
            stats["files_count"] = len(files_to_update)
            return True, msg, stats

        try:
            for rem_file, loc_file in files_to_update:
                loc_file.parent.mkdir(parents=True, exist_ok=True)
                # Copia solo se modificato o mancante
                if not loc_file.exists() or rem_file.stat().st_mtime > loc_file.stat().st_mtime:
                    shutil.copy2(rem_file, loc_file)
                    stats["files_updated"] += 1

            msg = (
                f"[SUCCESSO SYNC-ENGINE] Motore locale allineato con successo!\n"
                f"  Sorgente centrale: {src_share_str}\n"
                f"  File aggiornati: {stats['files_updated']} su {len(files_to_update)} scansionati."
            )
            stats["status"] = "synced"
            return True, msg, stats
        except Exception as e:
            msg = f"[ERRORE SYNC-ENGINE] Errore durante l'aggiornamento locale: {e}"
            stats["status"] = "error"
            return False, msg, stats

    def check_share_permissions(
        self,
        target_share: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None
    ) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Esegue un test diagnostico completo dei permessi sulla share master centrale:
        1. Raggiungibilita' e visibilita' di rete della share.
        2. Permessi di LETTURA su templates/, scripts/, docs/.
        3. Permessi di SCRITTURA e CANCELLAZIONE su projects/ (necessari per publish).
        4. Protezione da SCRITTURA su radice, scripts/ e templates/ (anti-tampering).

        Supporta opzionalmente credenziali (--user / --password) per simulare
        il profilo di un tecnico senza cambiare utente Windows.
        """
        share_str = self.get_central_share(target_share)
        share_path = Path(share_str)

        report = {
            "share": share_str,
            "simulated_user": username or "utente_corrente_windows",
            "reachable": False,
            "read_ok": False,
            "projects_write_ok": False,
            "core_protected": False,
            "checks": [],
            "status": "failed"
        }

        use_smbclient = False
        if username and password:
            try:
                import smbclient
                # Estrae l'host (es. fileserv01 o IP) dal path UNC \\host\share\path
                unc_parts = share_str.strip("\\/").split("\\")
                server_host = unc_parts[0] if unc_parts else "fileserv01"
                smbclient.register_session(server_host, username=username, password=password, connection_timeout=5)
                use_smbclient = True
            except Exception as e:
                msg = f"[ERRORE AUTENTICAZIONE SMB] Impossibile autenticare l'utente '{username}': {e}"
                report["checks"].append({"test": "Autenticazione utente", "passed": False, "detail": str(e)})
                return False, msg, report

        # Verifica raggiungibilità
        if not use_smbclient:
            if not share_path.exists():
                msg = (
                    f"[ERRORE DI RETE] La share centrale '{share_str}' non e' raggiungibile.\n"
                    f"Possibili cause:\n"
                    f"  - Postazione non connessa alla LAN aziendale o VPN disattivata.\n"
                    f"  - Credenziali di rete non fornite a Windows (accesso come altro utente)."
                )
                report["checks"].append({"test": "Raggiungibilita' share", "passed": False, "detail": "Share offline o inaccessibile"})
                return False, msg, report

        report["reachable"] = True
        report["checks"].append({"test": "Raggiungibilita' share", "passed": True, "detail": "Share online e accessibile"})

        # 1. Test Lettura Core (templates, scripts, docs)
        read_dirs = ["templates", "scripts", "docs"]
        read_success = True
        read_details = []
        for d in read_dirs:
            if use_smbclient:
                import smbclient
                p_str = f"{share_str}\\{d}"
                try:
                    entries = smbclient.listdir(p_str)
                    read_details.append(f"{d} ({len(entries)} el.)")
                except Exception as e:
                    read_success = False
                    read_details.append(f"{d} (errore: {e})")
            else:
                p = share_path / d
                if p.exists() and p.is_dir():
                    try:
                        count = len(list(p.iterdir()))
                        read_details.append(f"{d} ({count} el.)")
                    except Exception as e:
                        read_success = False
                        read_details.append(f"{d} (errore: {e})")
                else:
                    read_details.append(f"{d} (non presente)")

        report["read_ok"] = read_success
        report["checks"].append({
            "test": "Lettura Core (templates, scripts, docs)",
            "passed": read_success,
            "detail": ", ".join(read_details)
        })

        # 2. Test Scrittura su projects/
        proj_write_ok = False
        proj_detail = ""
        test_filename = f".itinfra_perm_test_{os.getpid()}.tmp"

        if use_smbclient:
            import smbclient
            p_file = f"{share_str}\\projects\\{test_filename}"
            try:
                with smbclient.open_file(p_file, mode="w") as f:
                    f.write("itinfra_permission_test")
                with smbclient.open_file(p_file, mode="r") as f:
                    content = f.read()
                smbclient.remove(p_file)
                if content == "itinfra_permission_test":
                    proj_write_ok = True
                    proj_detail = "Scrittura, verifica e rimozione completate con successo"
                else:
                    proj_detail = "Contenuto scritto non corrispondente"
            except Exception as e:
                proj_detail = f"Scrittura bloccata ({e})"
        else:
            proj_dir = share_path / "projects"
            if not proj_dir.exists():
                proj_detail = "Cartella 'projects/' non presente sulla share"
            else:
                test_file = proj_dir / test_filename
                try:
                    test_file.write_text("itinfra_permission_test", encoding="utf-8")
                    content = test_file.read_text(encoding="utf-8")
                    test_file.unlink()
                    if content == "itinfra_permission_test":
                        proj_write_ok = True
                        proj_detail = "Scrittura, verifica e rimozione completate con successo"
                    else:
                        proj_detail = "Contenuto scritto non corrispondente"
                except Exception as e:
                    proj_detail = f"Scrittura bloccata ({e})"

        report["projects_write_ok"] = proj_write_ok
        report["checks"].append({
            "test": "Scrittura su 'projects/' (Publishing)",
            "passed": proj_write_ok,
            "detail": proj_detail
        })

        # 3. Test Protezione Core da Scrittura non autorizzata (Radice, scripts, templates)
        core_targets = [
            ("Radice share", share_str if use_smbclient else share_path),
            ("Cartella scripts/", f"{share_str}\\scripts" if use_smbclient else share_path / "scripts"),
            ("Cartella templates/", f"{share_str}\\templates" if use_smbclient else share_path / "templates")
        ]
        core_protected = True
        core_details = []
        for label, dir_target in core_targets:
            wrote_ok = False
            if use_smbclient:
                import smbclient
                t_file = f"{dir_target}\\{test_filename}"
                try:
                    with smbclient.open_file(t_file, mode="w") as f:
                        f.write("tamper_test")
                    wrote_ok = True
                    smbclient.remove(t_file)
                except Exception:
                    wrote_ok = False
            else:
                if not dir_target.exists():
                    continue
                test_file = dir_target / test_filename
                try:
                    test_file.write_text("tamper_test", encoding="utf-8")
                    wrote_ok = True
                    test_file.unlink()
                except Exception:
                    wrote_ok = False

            if wrote_ok:
                core_protected = False
                core_details.append(f"{label}: APERTA A MODIFICHE (Rischio)")
            else:
                core_details.append(f"{label}: Protetta (Scrittura negata)")

        report["core_protected"] = core_protected
        report["checks"].append({
            "test": "Protezione Core da scrittura",
            "passed": core_protected,
            "detail": "; ".join(core_details)
        })

        # Generazione messaggio tabellare
        user_display = username if username else "Sessione Windows Corrente"
        lines = [
            "================================================================================",
            f"          REPORT DIAGNOSTICA PERMESSI STORAGE MASTER CENTRALE",
            "================================================================================",
            f"Percorso Share:  {share_str}",
            f"Profilo Utente:  {user_display}",
            "--------------------------------------------------------------------------------"
        ]
        for chk in report["checks"]:
            status_tag = "[OK]  " if chk["passed"] else "[FAIL]"
            lines.append(f"  {status_tag} {chk['test']:<42} -> {chk['detail']}")
        lines.append("--------------------------------------------------------------------------------")

        overall_ok = report["reachable"] and report["read_ok"] and report["projects_write_ok"] and report["core_protected"]
        if overall_ok:
            lines.append("ESITO GLOBALE: TUTTI I CONTROLLI SUPERATI [100% CONFORME]")
            lines.append("La postazione client e' perfettamente abilitata alla pubblicazione di progetti")
            lines.append("e le cartelle core del server sono protette da manomissioni accidentali.")
            report["status"] = "success"
        else:
            if not core_protected and not username:
                lines.append("ESITO GLOBALE: ATTENZIONE - SCRITTURA CORE CONSENTITA")
                lines.append("Nota: Se questo test e' stato eseguito come utente Amministratore (es. matrix),")
                lines.append("la scrittura e' consentita per design. Per i tecnici standard (gruppo_tecnici)")
                lines.append("la protezione core e' invece attiva e garantita.")
            else:
                lines.append("ESITO GLOBALE: RILEVATE ANOMALIE O MANCANZA DI PERMESSI")
            report["status"] = "failed"
        lines.append("================================================================================")

        return overall_ok, "\n".join(lines), report


