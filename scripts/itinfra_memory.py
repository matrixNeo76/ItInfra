#!/usr/bin/env python3
"""
ITInfra Hybrid Memory Manager (OKF v0.2)
Gestione della Memoria Locale Ibrida a 3 Livelli e Trust Signals per progetti ITInfra.
Supporta Staging Memory per-tenant e Global Enterprise Memory Pool (_global_scratchpad.md).
100% File-Based & Git-Native, privo di demoni o database esterni.
"""

import os
import re
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None


SCRATCHPAD_HEADER_TEMPLATE = """# ITInfra Memory Scratchpad — {slug}
<!-- Staging Memory semi-strutturata (Livello 2). Anti-inquinamento Git. -->
<!-- Note, requisiti aperti e decisioni confermate prima del consolidamento ufficiale nei documenti OKF v0.2. -->

## 1. Decisioni Tecniche Confermate
<!-- Voci validate durante l'intervista tecnica o la sessione operativa -->

## 2. Requisiti in Sospeso (<DA-RICHIEDERE>)
<!-- Punti aperti, parametri mancanti o decisioni in attesa di risposta dal cliente/team -->

## 3. Note Operative & Contatti
<!-- Credenziali referenziate vault://, contatti stakeholder, vincoli di manutenzione -->

## 4. Cronologia Consolidamenti
<!-- Registro dei consolidamenti verso documenti di Livello 3 -->
"""

GLOBAL_SCRATCHPAD_TEMPLATE = """---
okf_version: "0.2"
id: "guide-itinfra-global-memory-01"
title: "Global Enterprise Staging Memory & Architectural Best Practices — ITInfra"
type: "guide"
domain: "IT Infrastructure Knowledge Engineering"
tags: ["okf-v0.2", "memory", "global-scratchpad", "best-practices", "known-issues"]
project_id: "itinfra-core"
project_name: "ITInfra Enterprise Memory Pool"
phase: 0
author: "Enterprise Solutions Architect"
reviewer: "System Architecture Board"
approver: "Project Maintainer"
owner_team: "Infrastructure Architecture"
status: "in-review"
version: "1.0.0"
created_at: "{today}"
updated_at: "{today}"
related_docs:
  - "architecture-itinfra-docs-index-01"
  - "guide-memoria-ibrida-trust-signals-v02"
depends_on: []
classification: "internal"
retention: "permanent"
lang: "it"
entities:
  - name: "Global Enterprise Staging Memory"
    type: "framework"
    description: "Pool di memoria di secondo livello condivisa per best practice, pattern e lezioni apprese"
relations:
  - targetTitle: "Indice Generale della Documentazione"
    targetId: "architecture-itinfra-docs-index-01"
    relationType: "references"
    weight: 0.9
    description: "Hub documentale master ITInfra"
---

# ITInfra Global Enterprise Memory Scratchpad
<!-- Staging Memory Globale (Livello 2 Enterprise). 100% File-Based & Git-Native. -->
<!-- Raccoglie best practice architetturali, bug noti di vendor e linee guida trasversali a tutti i clienti. -->
<!-- Policy Zero-Leakage: VIETATO inserire secret, credenziali o IP di produzione specifici di un singolo tenant. -->

## 1. Best Practices & Design Patterns
<!-- Pattern architetturali collaudati e convenzioni approvate per reti, compute e storage -->

## 2. Known Issues & Hardware Limitations
<!-- Bug noti di firmware, incompatibilità transceiver, anomalie documentate nei post-mortem -->

## 3. Hardware & Vendor Guidelines
<!-- Requisiti minimi di BIOS, firmware di schede di rete e raccomandazioni di modelli -->

## 4. Open Architectural Questions
<!-- Punti di discussione trasversali per il board architetturale dell'organizzazione -->
"""

SECTION_MAP = {
    # Mappatura tenant-specific
    "decisioni": "## 1. Decisioni Tecniche Confermate",
    "decision": "## 1. Decisioni Tecniche Confermate",
    "confirmed": "## 1. Decisioni Tecniche Confermate",
    "sospesi": "## 2. Requisiti in Sospeso (<DA-RICHIEDERE>)",
    "open": "## 2. Requisiti in Sospeso (<DA-RICHIEDERE>)",
    "da-richiedere": "## 2. Requisiti in Sospeso (<DA-RICHIEDERE>)",
    "note": "## 3. Note Operative & Contatti",
    "operativo": "## 3. Note Operative & Contatti",
    "contacts": "## 3. Note Operative & Contatti",
}

GLOBAL_SECTION_MAP = {
    "best-practices": "## 1. Best Practices & Design Patterns",
    "best_practices": "## 1. Best Practices & Design Patterns",
    "patterns": "## 1. Best Practices & Design Patterns",
    "pattern": "## 1. Best Practices & Design Patterns",
    "decisioni": "## 1. Best Practices & Design Patterns",
    "known-issues": "## 2. Known Issues & Hardware Limitations",
    "known_issues": "## 2. Known Issues & Hardware Limitations",
    "issues": "## 2. Known Issues & Hardware Limitations",
    "limitations": "## 2. Known Issues & Hardware Limitations",
    "bug": "## 2. Known Issues & Hardware Limitations",
    "sospesi": "## 2. Known Issues & Hardware Limitations",
    "hardware-rules": "## 3. Hardware & Vendor Guidelines",
    "hardware_rules": "## 3. Hardware & Vendor Guidelines",
    "hardware": "## 3. Hardware & Vendor Guidelines",
    "vendor": "## 3. Hardware & Vendor Guidelines",
    "guidelines": "## 3. Hardware & Vendor Guidelines",
    "note": "## 3. Hardware & Vendor Guidelines",
    "open-architectural": "## 4. Open Architectural Questions",
    "open_architectural": "## 4. Open Architectural Questions",
    "open": "## 4. Open Architectural Questions",
    "questions": "## 4. Open Architectural Questions",
}


class AtomicFileLock:
    """Lock atomico basato su filesystem per evitare race condition in ambiente multi-processo/multi-agente."""
    def __init__(self, lock_path: Path, timeout: float = 10.0, poll_interval: float = 0.1):
        self.lock_path = lock_path
        self.timeout = timeout
        self.poll_interval = poll_interval
        self.acquired = False
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)

    def __enter__(self):
        start = time.time()
        while True:
            try:
                fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"pid:{os.getpid()}:{time.time()}".encode("utf-8"))
                os.close(fd)
                self.acquired = True
                return self
            except FileExistsError:
                # Se il lock e' stantio (> 120s), rimuovilo
                try:
                    if time.time() - os.path.getmtime(self.lock_path) > 120.0:
                        os.remove(self.lock_path)
                except OSError:
                    pass
                if time.time() - start >= self.timeout:
                    raise TimeoutError(f"Timeout ({self.timeout}s) acquisizione lock su {self.lock_path}")
                time.sleep(self.poll_interval)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired and self.lock_path.exists():
            try:
                os.remove(self.lock_path)
            except OSError:
                pass


def validate_global_entry_safety(text: str) -> None:
    """
    Verifica che il testo destinato alla memoria globale non contenga riferimenti
    a secret di specifici progetti o password in chiaro (Zero-Leakage Multi-Tenant Policy).
    """
    # Blocco riferimenti a secret di specifici tenant
    if re.search(r"vault://it/projects/[^/\s]+/", text, re.IGNORECASE):
        raise PermissionError(
            "[SECURITY BLOCKED] Violazione Multi-Tenant: La memoria globale non ammette riferimenti "
            "a vault o secret di singoli clienti (trovato: vault://it/projects/...)."
        )
    
    # Blocco credenziali in chiaro
    if re.search(r'(password|pwd|secret|token)\s*[:=]\s*["\']?[A-Za-z0-9!@#$%^&*()_+]{4,}', text, re.IGNORECASE):
        raise PermissionError(
            "[SECURITY BLOCKED] Violazione di Sicurezza: Rilevate credenziali in chiaro nel testo della memoria globale."
        )


class MemoryManager:
    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            self.repo_root = Path(__file__).resolve().parent.parent
        else:
            self.repo_root = repo_root
        self.projects_dir = self.repo_root / "projects"

    def get_project_dir(self, slug: str) -> Path:
        p_dir = self.projects_dir / slug.lower().strip()
        if not p_dir.exists():
            raise FileNotFoundError(f"Directory di progetto non trovata: {p_dir}")
        return p_dir

    def get_global_scratchpad_path(self) -> Path:
        return self.projects_dir / "_global_scratchpad.md"

    def get_global_lock_path(self) -> Path:
        return self.projects_dir / "_global_scratchpad.lock"

    def get_scratchpad_path(self, slug: Optional[str], role: Optional[str] = None, is_global: bool = False) -> Path:
        if is_global or slug in ("__global__", "global", "all"):
            return self.get_global_scratchpad_path()
        if not slug:
            raise ValueError("Specificare uno slug di progetto oppure usare is_global=True.")
        
        p_dir = self.get_project_dir(slug)
        if role:
            # Isolamento multi-agente / worktree
            mem_dir = p_dir / ".memory"
            mem_dir.mkdir(parents=True, exist_ok=True)
            return mem_dir / f"scratchpad.{role.strip().lower()}.md"
        return p_dir / "_scratchpad.md"

    def init_scratchpad(self, slug: Optional[str] = None, is_global: bool = False, force: bool = False) -> Path:
        """Inizializza lo scratchpad del progetto o lo scratchpad globale se non esistente."""
        if is_global or slug in ("__global__", "global", "all"):
            target_file = self.get_global_scratchpad_path()
            if target_file.exists() and not force:
                return target_file
            
            with AtomicFileLock(self.get_global_lock_path()):
                today_str = datetime.now().strftime("%Y-%m-%d")
                content = GLOBAL_SCRATCHPAD_TEMPLATE.format(today=today_str)
                target_file.write_text(content, encoding="utf-8")
            return target_file

        target_file = self.get_scratchpad_path(slug)
        if target_file.exists() and not force:
            return target_file

        lock_path = self.get_project_dir(slug) / ".scratchpad.lock"
        with AtomicFileLock(lock_path):
            header = SCRATCHPAD_HEADER_TEMPLATE.format(slug=slug)
            target_file.write_text(header, encoding="utf-8")
        return target_file

    def _generate_entry_id(self, text: str, timestamp: str) -> str:
        h = hashlib.sha256(f"{timestamp}:{text}".encode("utf-8")).hexdigest()[:8]
        return f"mem-{h}"

    def log_entry(
        self,
        slug: Optional[str],
        section_key: str,
        text: str,
        role: Optional[str] = None,
        author: Optional[str] = None,
        is_global: bool = False,
    ) -> Tuple[Path, str]:
        """Appende una voce strutturata nello scratchpad di progetto o globale con atomic file locking."""
        is_glob = is_global or slug in ("__global__", "global", "all")

        if is_glob:
            # Controllo di sicurezza preventivo multi-tenant
            validate_global_entry_safety(text)
            sec_header = GLOBAL_SECTION_MAP.get(section_key.lower().strip())
            if not sec_header:
                valid_keys = ", ".join(sorted(list(set(GLOBAL_SECTION_MAP.keys()))))
                raise ValueError(f"Sezione globale '{section_key}' non valida. Ammesse: {valid_keys}")

            target_file = self.get_global_scratchpad_path()
            lock_path = self.get_global_lock_path()
            if not target_file.exists():
                self.init_scratchpad(is_global=True)
        else:
            sec_header = SECTION_MAP.get(section_key.lower().strip())
            if not sec_header:
                valid_keys = ", ".join(sorted(list(set(SECTION_MAP.keys()))))
                raise ValueError(f"Sezione '{section_key}' non valida. Sezioni ammesse: {valid_keys}")

            target_file = self.get_scratchpad_path(slug, role=role)
            lock_path = self.get_project_dir(slug) / ".scratchpad.lock"
            if not target_file.exists():
                self.init_scratchpad(slug)
                if role:
                    target_file.write_text(
                        f"# Scratchpad Staging Role: {role} — {slug}\n\n"
                        + SCRATCHPAD_HEADER_TEMPLATE.format(slug=slug),
                        encoding="utf-8"
                    )

        ts = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry_id = self._generate_entry_id(text, ts)
        role_label = f"[{role}]" if role else "[agent]"
        author_label = f"({author})" if author else ""
        entry_line = f"- [{ts}] {role_label} {author_label} {text.strip()} <!-- id:{entry_id} -->\n"

        with AtomicFileLock(lock_path):
            content = target_file.read_text(encoding="utf-8")
            if sec_header not in content:
                content += f"\n\n{sec_header}\n"

            # Inserimento sotto l'intestazione della sezione
            pattern = re.escape(sec_header) + r"(.*?)(?=\n## |\Z)"
            match = re.search(pattern, content, re.DOTALL)
            if match:
                sub_content = match.group(0)
                new_sub_content = sub_content.rstrip() + "\n" + entry_line
                content = content.replace(sub_content, new_sub_content)
            else:
                content += f"\n{sec_header}\n{entry_line}"

            target_file.write_text(content, encoding="utf-8")

        return target_file, entry_id

    def show_scratchpad(self, slug: Optional[str] = None, is_global: bool = False) -> Dict[str, Any]:
        """Estrae e analizza le sezioni dello scratchpad (locale o globale)."""
        is_glob = is_global or slug in ("__global__", "global", "all")
        if is_glob:
            target_file = self.get_global_scratchpad_path()
            if not target_file.exists():
                return {
                    "file": str(target_file),
                    "is_global": True,
                    "exists": False,
                    "sections": {},
                    "stats": {"best_practices": 0, "known_issues": 0, "hardware_rules": 0, "open_questions": 0}
                }
            
            content = target_file.read_text(encoding="utf-8")
            sections_data: Dict[str, List[str]] = {
                "best_practices": [],
                "known_issues": [],
                "hardware_rules": [],
                "open_questions": [],
            }
            current_sec = None
            for line in content.splitlines():
                line_str = line.strip()
                if "## 1. Best Practices" in line:
                    current_sec = "best_practices"
                elif "## 2. Known Issues" in line:
                    current_sec = "known_issues"
                elif "## 3. Hardware & Vendor" in line:
                    current_sec = "hardware_rules"
                elif "## 4. Open Architectural" in line:
                    current_sec = "open_questions"
                elif line_str.startswith("## "):
                    current_sec = None
                elif current_sec and line_str.startswith("- ["):
                    sections_data[current_sec].append(line_str)

            return {
                "file": str(target_file),
                "is_global": True,
                "exists": True,
                "sections": sections_data,
                "stats": {
                    "best_practices": len(sections_data["best_practices"]),
                    "known_issues": len(sections_data["known_issues"]),
                    "hardware_rules": len(sections_data["hardware_rules"]),
                    "open_questions": len(sections_data["open_questions"]),
                }
            }

        target_file = self.get_scratchpad_path(slug)
        if not target_file.exists():
            return {
                "file": str(target_file),
                "is_global": False,
                "exists": False,
                "sections": {},
                "stats": {"confirmed": 0, "open": 0, "notes": 0, "worktrees_pending": 0}
            }

        content = target_file.read_text(encoding="utf-8")
        sections_data: Dict[str, List[str]] = {
            "decisioni": [],
            "sospesi": [],
            "note": [],
            "consolidamenti": [],
        }

        current_sec = None
        for line in content.splitlines():
            line_str = line.strip()
            if "## 1. Decisioni" in line:
                current_sec = "decisioni"
            elif "## 2. Requisiti in Sospeso" in line:
                current_sec = "sospesi"
            elif "## 3. Note Operative" in line:
                current_sec = "note"
            elif "## 4. Cronologia" in line:
                current_sec = "consolidamenti"
            elif line_str.startswith("## "):
                current_sec = None
            elif current_sec and line_str.startswith("- ["):
                sections_data[current_sec].append(line_str)

        # Rileva worktree pendenti
        p_dir = self.get_project_dir(slug)
        mem_dir = p_dir / ".memory"
        pending_worktrees = 0
        if mem_dir.exists():
            pending_worktrees = len(list(mem_dir.glob("scratchpad.*.md")))

        return {
            "file": str(target_file),
            "is_global": False,
            "exists": True,
            "sections": sections_data,
            "stats": {
                "confirmed": len(sections_data["decisioni"]),
                "open": len(sections_data["sospesi"]),
                "notes": len(sections_data["note"]),
                "consolidated": len(sections_data["consolidamenti"]),
                "worktrees_pending": pending_worktrees
            }
        }

    def merge_worktrees(self, slug: str) -> Dict[str, Any]:
        """Esegue il merge degli scratchpad dei subagenti worktree nello scratchpad principale del progetto."""
        p_dir = self.get_project_dir(slug)
        mem_dir = p_dir / ".memory"
        if not mem_dir.exists():
            return {"merged_count": 0, "files_processed": 0, "status": "noop"}

        main_scratch = self.get_scratchpad_path(slug)
        if not main_scratch.exists():
            self.init_scratchpad(slug)

        main_content = main_scratch.read_text(encoding="utf-8")
        existing_ids = set(re.findall(r"<!-- id:(mem-[a-f0-9]+) -->", main_content))

        merged_count = 0
        files_processed = 0

        lock_path = p_dir / ".scratchpad.lock"
        with AtomicFileLock(lock_path):
            for role_file in mem_dir.glob("scratchpad.*.md"):
                files_processed += 1
                role_content = role_file.read_text(encoding="utf-8")
                
                # Estrai tutte le righe con id
                for line in role_content.splitlines():
                    match = re.search(r"<!-- id:(mem-[a-f0-9]+) -->", line)
                    if match:
                        entry_id = match.group(1)
                        if entry_id not in existing_ids:
                            # Determina la sezione di appartenenza
                            target_sec = "## 3. Note Operative & Contatti"
                            if "## 1. Decisioni" in role_content:
                                target_sec = "## 1. Decisioni Tecniche Confermate"
                            elif "## 2. Requisiti" in role_content:
                                target_sec = "## 2. Requisiti in Sospeso (<DA-RICHIEDERE>)"

                            pattern = re.escape(target_sec) + r"(.*?)(?=\n## |\Z)"
                            m = re.search(pattern, main_content, re.DOTALL)
                            if m:
                                sub = m.group(0)
                                new_sub = sub.rstrip() + "\n" + line.strip() + "\n"
                                main_content = main_content.replace(sub, new_sub)
                            else:
                                main_content += f"\n{target_sec}\n{line.strip()}\n"

                            existing_ids.add(entry_id)
                            merged_count += 1

            main_scratch.write_text(main_content, encoding="utf-8")

        return {
            "merged_count": merged_count,
            "files_processed": files_processed,
            "status": "success"
        }

    def consolidate(
        self,
        slug: str,
        target_doc_id_or_prefix: str,
        reviewer: str,
        stale_days: int = 90
    ) -> Dict[str, Any]:
        """Consolida le decisioni confermate nello scratchpad verso un documento target OKF v0.2."""
        p_dir = self.get_project_dir(slug)
        scratch_path = self.get_scratchpad_path(slug)
        if not scratch_path.exists():
            raise FileNotFoundError(f"Scratchpad non trovato per il progetto: {slug}")

        # Trova il documento target
        target_path = None
        prefix_clean = target_doc_id_or_prefix.strip().upper()
        for cand in p_dir.glob("*.md"):
            if cand.name.startswith(prefix_clean) or target_doc_id_or_prefix.lower() in cand.name.lower():
                target_path = cand
                break

        if not target_path:
            raise FileNotFoundError(f"Documento target '{target_doc_id_or_prefix}' non trovato in {p_dir}")

        scratch_content = scratch_path.read_text(encoding="utf-8")
        
        # Estrai decisioni confermate
        dec_pattern = r"## 1\. Decisioni Tecniche Confermate(.*?)(?=\n## |\Z)"
        dec_match = re.search(dec_pattern, scratch_content, re.DOTALL)
        if not dec_match:
            return {"status": "noop", "message": "Nessuna decisione confermata trovata."}

        confirmed_lines = []
        for line in dec_match.group(1).splitlines():
            line_str = line.strip()
            if line_str.startswith("- ["):
                confirmed_lines.append(line_str)

        if not confirmed_lines:
            return {"status": "noop", "message": "Nessuna voce da consolidare nella Sezione 1."}

        # 1. Modifica Documento Target
        target_content = target_path.read_text(encoding="utf-8")
        if not target_content.startswith("---"):
            raise ValueError(f"Il file target {target_path.name} non ha frontmatter OKF v0.2 valido.")

        parts = target_content.split("---", 2)
        if len(parts) < 3:
            raise ValueError(f"Struttura frontmatter non valida in {target_path.name}.")

        fm_text = parts[1]
        body_text = parts[2]

        today_str = datetime.now().strftime("%Y-%m-%d")
        stale_date_str = (datetime.now() + timedelta(days=stale_days)).strftime("%Y-%m-%d") if stale_days > 0 else None

        # Aggiorna campi Trust Signals
        if "verified:" in fm_text:
            fm_text = re.sub(r"verified:\s*(true|false)", "verified: true", fm_text)
        else:
            fm_text += "\nverified: true"

        if "verified_by:" in fm_text:
            fm_text = re.sub(r'verified_by:\s*"[^"]*"', f'verified_by: "{reviewer}"', fm_text)
        else:
            fm_text += f'\nverified_by: "{reviewer}"'

        if "last_vetted:" in fm_text:
            fm_text = re.sub(r'last_vetted:\s*"[^"]*"', f'last_vetted: "{today_str}"', fm_text)
        else:
            fm_text += f'\nlast_vetted: "{today_str}"'

        if stale_date_str:
            if "stale_after:" in fm_text:
                fm_text = re.sub(r'stale_after:\s*"[^"]*"', f'stale_after: "{stale_date_str}"', fm_text)
            else:
                fm_text += f'\nstale_after: "{stale_date_str}"'

        if "updated_at:" in fm_text:
            fm_text = re.sub(r'updated_at:\s*"[^"]*"', f'updated_at: "{today_str}"', fm_text)

        # 2. Iniezione nel body del documento target
        consolidation_section = (
            f"\n\n## Decisioni Tecniche Consolidate da Staging Memory\n"
            f"> Consolidato dallo Scratchpad il `{today_str}` con attestazione di confidenza da parte di `{reviewer}`.\n"
            f"> Certificazione valida fino al: `{stale_date_str or 'N/D'}`.\n\n"
        )
        for item in confirmed_lines:
            consolidation_section += f"{item}\n"

        new_target_content = f"---{fm_text.strip()}\n---\n{body_text.rstrip()}{consolidation_section}"
        target_path.write_text(new_target_content, encoding="utf-8")

        # 3. Aggiorna lo scratchpad con lock
        log_entry = f"\n### Consolidamento verso [{target_path.name}] — {today_str} ({reviewer})\n"
        for item in confirmed_lines:
            log_entry += f"{item}\n"

        new_sec1 = "## 1. Decisioni Tecniche Confermate\n<!-- Voci validate durante l'intervista tecnica o la sessione operativa -->\n"
        scratch_content = re.sub(r"## 1\. Decisioni Tecniche Confermate.*?(?=\n## |\Z)", new_sec1, scratch_content, flags=re.DOTALL)

        sec4_header = "## 4. Cronologia Consolidamenti"
        if sec4_header in scratch_content:
            scratch_content += log_entry
        else:
            scratch_content += f"\n\n{sec4_header}\n{log_entry}"

        lock_path = p_dir / ".scratchpad.lock"
        with AtomicFileLock(lock_path):
            scratch_path.write_text(scratch_content, encoding="utf-8")

        return {
            "target_file": str(target_path),
            "consolidated_count": len(confirmed_lines),
            "status": "success",
            "reviewer": reviewer,
            "last_vetted": today_str,
            "stale_after": stale_date_str,
            "message": f"Consolidate {len(confirmed_lines)} decisioni con Trust Signals applicati con successo!"
        }

    def prune(self, slug: Optional[str] = None, is_global: bool = False, archive: bool = True) -> Dict[str, Any]:
        """Archivia il contenuto dello scratchpad corrente e ne ripristina la struttura pulita."""
        is_glob = is_global or slug in ("__global__", "global", "all")
        if is_glob:
            scratch_path = self.get_global_scratchpad_path()
            if not scratch_path.exists():
                return {"status": "noop", "message": "Nessuno scratchpad globale da ripulire."}

            today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            today_short = datetime.now().strftime("%Y-%m-%d")
            with AtomicFileLock(self.get_global_lock_path()):
                content = scratch_path.read_text(encoding="utf-8")
                if archive:
                    arch_file = self.projects_dir / "_global_scratchpad.archive.md"
                    arch_entry = f"\n\n---\n# ARCHIVIO MEMORIA GLOBALE DEL {today_str}\n---\n{content}\n"
                    if arch_file.exists():
                        existing = arch_file.read_text(encoding="utf-8")
                        arch_file.write_text(existing + arch_entry, encoding="utf-8")
                    else:
                        arch_file.write_text(f"# Archivio Global Staging Memory\n" + arch_entry, encoding="utf-8")

                clean_content = GLOBAL_SCRATCHPAD_TEMPLATE.format(today=today_short)
                scratch_path.write_text(clean_content, encoding="utf-8")

            return {
                "status": "success",
                "message": "Scratchpad globale ripulito con successo. Dati archiviati in: _global_scratchpad.archive.md"
            }

        scratch_path = self.get_scratchpad_path(slug)
        if not scratch_path.exists():
            return {"status": "noop", "message": "Nessuno scratchpad da ripulire."}

        p_dir = self.get_project_dir(slug)
        lock_path = p_dir / ".scratchpad.lock"
        with AtomicFileLock(lock_path):
            content = scratch_path.read_text(encoding="utf-8")
            today_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if archive:
                arch_file = p_dir / "_scratchpad.archive.md"
                arch_entry = f"\n\n---\n# ARCHIVIO MEMORIA DEL {today_str}\n---\n{content}\n"
                if arch_file.exists():
                    existing = arch_file.read_text(encoding="utf-8")
                    arch_file.write_text(existing + arch_entry, encoding="utf-8")
                else:
                    arch_file.write_text(f"# Archivio Staging Memory — {slug}\n" + arch_entry, encoding="utf-8")

            clean_content = SCRATCHPAD_HEADER_TEMPLATE.format(slug=slug)
            scratch_path.write_text(clean_content, encoding="utf-8")

        return {
            "status": "success",
            "message": "Scratchpad ripulito con successo. Dati archiviati in: _scratchpad.archive.md"
        }
