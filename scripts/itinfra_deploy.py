#!/usr/bin/env python3
"""
scripts/itinfra_deploy.py
------------------------
Continuous Deployment Engine per lo storage master centrale (Release v0.9.5).
Sincronizza in modo differenziale, atomico e sicuro il motore, i template,
le guide e le skill dal repository di sviluppo master verso la share centrale.
"""

import os
import sys
import shutil
import hashlib
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"

def sha256_file(file_path: Path) -> str:
    h = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

class CentralDeployer:
    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or Path(__file__).resolve().parent.parent

    def deploy(
        self,
        target_share: Optional[str] = None,
        dry_run: bool = False,
        quiet: bool = False
    ) -> Tuple[bool, str, Dict[str, Any]]:
        target_str = target_share or DEFAULT_CENTRAL_SHARE
        target_path = Path(target_str)

        stats = {
            "target": target_str,
            "files_scanned": 0,
            "files_updated": 0,
            "bytes_transferred": 0,
            "updated_files": [],
            "dry_run": dry_run,
            "status": "pending"
        }

        if not target_path.exists():
            msg = f["DEPLOYERRORE] La cartella master centrale '{target_str}' non e' raggiungibile."]
            stats["status"] = "target_unreachable"
            return False, msg, stats

        # Cartelle e file da distribuire (ESCLUSA STRICTLY projects/ e .git/)
        dirs_to_sync = ["scripts", "templates", "docs", "skills", ".agents", ".vscode"]
        root_files_to_sync = [
            "README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md",
            "INTEGRAZIONE-REPO.md", "00-INDEX.md", "update.cmd", "it.cmd"
        ]

        files_to_check: List[Tuple[Path, Path]] = []

        # 1. Scansione directory core
        for dir_name in dirs_to_sync:
            src_dir = self.repo_root / dir_name
            if src_dir.exists() and src_dir.is_dir():
                for root, _, files in os.walk(src_dir):
                    for fname in files:
                        if fname.endswith(".pyc") or "__pycache__" in root or fname.endswith(".tmp"):
                            continue
                        src_f = Path(root) / fname
                        rel_f = src_f.relative_to(self.repo_root)
                        dst_f = target_path / rel_f
                        files_to_check.append((src_f, dst_f))

        # 2. Scansione root files
        for rname in root_files_to_sync:
            src_f = self.repo_root / rname
            if src_f.exists():
                dst_f = target_path / rname
                files_to_check.append((src_f, dst_f))

        stats["files_scanned"] = len(files_to_check)

        # 3. Confronto differenziale
        files_to_copy: List[Tuple[Path, Path]] = []
        for src_f, dst_f in files_to_check:
            needs_update = False
            if not dst_f.exists():
                needs_update = True
            else:
                # Confronto prima per mtime / dimensione
                if src_f.stat().st_size != dst_f.stat().st_size or src_f.stat().st_mtime > dst_f.stat().st_mtime:
                    try:
                        if sha256_file(src_f) != sha256_file(dst_f):
                            needs_update = True
                    except Exception:
                        needs_update = True

            if needs_update:
                files_to_copy.append((src_f, dst_f))

        stats["files_updated"] = len(files_to_copy)
        stats["updated_files"] = [str(s.relative_to(self.repo_root)) for s, _ in files_to_copy]

        if dry_run:
            msg = (
                f"[DRY-RUN DEPLOY] Individuati {len(files_to_copy)} file da aggiornare su '{target_str}'.\n" +
                (f"File: {', '.join(stats['updated_files'][:10])}{'...' if len(files_to_copy) > 10 else ''}" if files_to_copy else "File gia' allineati.")
            )
            stats["status"] = "dry_run_success"
            return True, msg, stats

        if not files_to_copy:
            msg = f"[DEPLOY OK] Nessun file modificato. La share centrale '{target_str}' e' gia' allineata al 100%."
            stats["status"] = "already_up_to_date"
            return True, msg, stats

        # 4. Esecuzione effettiva del deploy
        try:
            for src_f, dst_f in files_to_copy:
                dst_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_f, dst_f)
                stats["bytes_transferred"] += src_f.stat().st_size

            msg = (
                f"[SUCCESSO DEPLOY] Share master '{target_str}' aggiornata con successo!\n"
                f"  File sincronizzati: {len(files_to_copy)} su {stats['files_scanned']} scansionati\n"
                f"  Volume trasferito: {stats['bytes_transferred'] / 1024:.1f} KB"
            )
            stats["status"] = "deployed"
            return True, msg, stats
        except Exception as e:
            msg = f"[ERRORE DEPLOY] Errore durante la copia verso '{target_str}': {e}"
            stats["status"] = "error"
            return False, msg, stats

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Continuous Deployment Engine verso Storage Master Centrale")
    parser.add_argument("--dest", default=None, help=f"Percorso della share centrale (default: '{DEFAULT_CENTRAL_SHARE}')")
    parser.add_argument("--dry-run", action="store_true", help="Simula il deploy senza copiare file")
    parser.add_argument("--quiet", action="store_true", help="Output sintetico per hook Git")
    args = parser.parse_args()

    deployer = CentralDeployer()
    ok, msg, stats = deployer.deploy(target_share=args.dest, dry_run=args.dry_run, quiet=args.quiet)
    if not args.quiet or not ok or stats.get("files_updated", 0) > 0:
        print(msg)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
