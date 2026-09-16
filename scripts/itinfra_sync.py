#!/usr/bin/env python3
"""
scripts/itinfra_sync.py
-----------------------
Client Startup Auto-Sync & Version Checker (Release v0.9.5).
Verifica lo stato di allineamento del workspace client locale rispetto
alla share master centrale e sincronizza in background i template e gli script.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"
CONFIG_FILE_NAME = ".itinfra_config.json"

class ClientSyncManager:
    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path.cwd()
        self.config_path = self.workspace_root / CONFIG_FILE_NAME
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if self.config_path.exists():
            try:
                return json.loads(self.config_path.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    def _save_config(self) -> None:
        try:
            self.config_path.write_text(json.dumps(self.config, indent=2), encoding="utf-8")
        except Exception:
            pass

    def check_updates(self, source_override: Optional[str] = None) -> Tuple[bool, List[str], str]:
        share_str = source_override or self.config.get("central_share", DEFAULT_CENTRAL_SHARE)
        share_path = Path(share_str)

        if not share_path.exists():
            return False, [], f"Share centrale '{share_str}' non raggiungibile (offline o senza VPN)."

        dirs_to_check = ["scripts", "templates", "docs"]
        root_files = ["README.md", "ROADMAP.md", "AGENTS.md", "CLAUDE.md", "INTEGRAZIONE-REPO.md", "00-INDEX.md"]

        files_to_update = []

        for d in dirs_to_check:
            rem_d = share_path / d
            if rem_d.exists() and rem_d.is_dir():
                for root, _, files in os.walk(rem_d):
                    for fname in files:
                        if fname.endswith(".pyc") or "__pycache__" in root:
                            continue
                        rem_f = Path(root) / fname
                        rel_f = rem_f.relative_to(share_path)
                        loc_f = self.workspace_root / rel_f
                        if not loc_f.exists() or rem_f.stat().st_mtime > loc_f.stat().st_mtime:
                            files_to_update.append(str(rel_f))

        for rf in root_files:
            rem_f = share_path / rf
            if rem_f.exists():
                loc_f = self.workspace_root / rf
                if not loc_f.exists() or rem_f.stat().st_mtime > loc_f.stat().st_mtime:
                    files_to_update.append(rf)

        msg = f"{len(files_to_update)} file aggiornabili rilevati sulla share master." if files_to_update else "Workspace locale gia' allineato all'ultima versione."
        return True, files_to_update, msg

    def sync(self, source_override: Optional[str] = None) -> Tuple[bool, str, int]:
        ok, files_to_update, msg = self.check_updates(source_override)
        if not ok:
            return False, msg, 0

        if not files_to_update:
            return True, "Workspace locale gia' aggiornato al 100%.", 0

        share_str = source_override or self.config.get("central_share", DEFAULT_CENTRAL_SHARE)
        share_path = Path(share_str)

        updated_count = 0
        try:
            for rel_str in files_to_update:
                rem_f = share_path / rel_str
                loc_f = self.workspace_root / rel_str
                loc_f.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(rem_f, loc_f)
                updated_count += 1

            self.config["last_sync_timestamp"] = datetime.now().isoformat()
            self._save_config()

            return True, f"Sincronizzazione completata: {updated_count} file aggiornati dalla share master.", updated_count
        except Exception as e:
            return False, f"Errore durante la sincronizzazione locale: {e}", updated_count

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Client Startup Auto-Sync & Version Checker")
    parser.add_argument("--check-only", action="store_true", help="Verifica solo se ci sono aggiornamenti senza applicarli")
    parser.add_argument("--source", default=None, help=f"Percorso share master (default: '{DEFAULT_CENTRAL_SHARE}')")
    parser.add_argument("--json", action="store_true", help="Output in formato JSON")
    args = parser.parse_args()

    mgr = ClientSyncManager()
    if args.check_only:
        ok, files, msg = mgr.check_updates(args.source)
        if args.json:
            print(json.dumps({"reachable": ok, "updates_available": len(files) > 0, "count": len(files), "files": files, "message": msg}))
        else:
            print(msg)
        sys.exit(0 if ok else 1)
    else:
        ok, msg, count = mgr.sync(args.source)
        if args.json:
            print(json.dumps({"success": ok, "updated_count": count, "message": msg}))
        else:
            print(msg)
        sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
