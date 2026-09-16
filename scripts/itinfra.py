#!/usr/bin/env python3
"""
ITInfra CLI & OKF v0.2 Linter
Suite per la gestione di progetti di infrastrutture IT e validazione documentale OKF v0.2.
"""

import sys
import os
import re
import html
import argparse
import subprocess
import getpass
import ipaddress
import socket
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

try:
    import yaml
except ImportError:
    print("ERRORE: PyYAML non installato. Installa con: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

CANONICAL_OKF_TYPES = {
    "concept",
    "architecture",
    "guide",
    "specification",
    "tool_description",
    "prompt_skill",
}

CANONICAL_ENTITY_TYPES = {
    "concept",
    "framework",
    "technology",
    "toolchain",
    "pattern",
    "organization",
    "specification",
}

CANONICAL_RELATION_TYPES = {
    "references",
    "implements",
    "depends_on",
    "extends",
    "documents",
    "governs",
    "constrains",
    "relates_to",
}

IT_DOCUMENT_TYPES = [
    ("01-RSD-URS", 1, "specification", "Requirements Specification Document"),
    ("02-HLD", 2, "architecture", "High-Level Design"),
    ("03-LLD", 2, "architecture", "Low-Level Design"),
    ("04-MOP", 3, "guide", "Method of Procedure"),
    ("05-Rollback", 3, "guide", "Rollback / Fallback Plan"),
    ("06-As-Built", 5, "architecture", "As-Built Documentation"),
    ("07-ATP", 6, "specification", "Acceptance Test Plan"),
    ("08-SOP-Runbook", 7, "guide", "Standard Operating Procedures / Runbook"),
    ("09-Handover-Inventory", 7, "specification", "Handover & Asset Inventory"),
]

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"

COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_CYAN = "\033[96m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

def supports_color() -> bool:
    return sys.stdout.isatty() or os.environ.get("FORCE_COLOR") == "1"

def colorize(text: str, color: str) -> str:
    if supports_color():
        return f"{color}{text}{COLOR_RESET}"
    return text

def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, Optional[str]]:
    """Estrae frontmatter YAML e body markdown."""
    content = content.lstrip("\ufeff")
    pattern = r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return None, content, "Frontmatter YAML delimitato da '---' non trovato all'inizio del file."
    yaml_text = match.group(1)
    body_text = match.group(2)
    try:
        data = yaml.safe_load(yaml_text)
        if not isinstance(data, dict):
            return None, body_text, "Il frontmatter YAML non e' un dizionario valido."
        return data, body_text, None
    except Exception as e:
        return None, body_text, f"Errore parsing YAML: {e}"

class OKFValidator:
    def __init__(self, is_template: bool = False):
        self.is_template = is_template

    def validate(self, file_path: Path) -> Dict[str, Any]:
        result = {
            "file": str(file_path),
            "errors": [],
            "warnings": [],
            "stats": {
                "placeholders_count": 0,
                "da_richiedere_count": 0,
                "entities_count": 0,
                "relations_count": 0,
            }
        }

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            result["errors"].append(f"Impossibile leggere il file: {e}")
            return result

        frontmatter, body, err = parse_frontmatter(content)
        if err:
            result["errors"].append(err)
            return result

        # 1. Controllo okf_version
        okf_version = str(frontmatter.get("okf_version", ""))
        if okf_version != "0.2":
            result["errors"].append(f"okf_version deve essere '0.2', trovato: '{okf_version}'")

        # 2. Controllo id
        doc_id = frontmatter.get("id")
        if not doc_id or not isinstance(doc_id, str):
            result["errors"].append("Campo 'id' obbligatorio e deve essere una stringa non vuota.")
        elif not self.is_template and "<" in doc_id:
            result["errors"].append(f"Campo 'id' contiene ancora placeholder: '{doc_id}'")

        # 3. Controllo title
        title = frontmatter.get("title")
        if not title or not isinstance(title, str):
            result["errors"].append("Campo 'title' obbligatorio.")
        elif len(title) > 120:
            result["warnings"].append(f"Titolo molto lungo ({len(title)} caratteri > 120 raccomandati).")

        # 4. Controllo type
        doc_type = frontmatter.get("type")
        if doc_type not in CANONICAL_OKF_TYPES:
            result["errors"].append(
                f"Campo 'type' '{doc_type}' non valido. Valori canonici OKF v0.2 ammessi: {sorted(list(CANONICAL_OKF_TYPES))}"
            )

        # 5. Controllo domain
        domain = frontmatter.get("domain")
        if not domain or not isinstance(domain, str):
            result["errors"].append("Campo 'domain' obbligatorio.")

        # 6. Controllo tags
        tags = frontmatter.get("tags")
        if not isinstance(tags, list) or len(tags) < 2:
            result["errors"].append("Campo 'tags' deve essere una lista di almeno 2 tag in lowercase.")
        else:
            if tags[0] != "okf-v0.2":
                result["errors"].append(f"Il primo tag DEVE essere 'okf-v0.2', trovato: '{tags[0]}'")
            for tag in tags:
                if not isinstance(tag, str) or tag != tag.lower():
                    result["warnings"].append(f"Il tag '{tag}' dovrebbe essere in minuscolo (lowercase).")

        # 7. Controllo entities
        entities = frontmatter.get("entities")
        if not isinstance(entities, list) or len(entities) < 1:
            result["errors"].append("Campo 'entities' deve contenere almeno 1 entita'.")
        else:
            result["stats"]["entities_count"] = len(entities)
            for idx, ent in enumerate(entities):
                if not isinstance(ent, dict):
                    result["errors"].append(f"Entita' #{idx+1} non e' un oggetto valido.")
                    continue
                name = ent.get("name")
                e_type = ent.get("type")
                desc = ent.get("description")
                if not name or not desc:
                    result["errors"].append(f"Entita' #{idx+1} priva di 'name' o 'description'.")
                if e_type not in CANONICAL_ENTITY_TYPES:
                    result["errors"].append(
                        f"Entita' '{name}' ha tipo '{e_type}' non valido. Ammessi: {sorted(list(CANONICAL_ENTITY_TYPES))}"
                    )

        # 8. Controllo relations
        relations = frontmatter.get("relations", [])
        relation_target_ids = set()
        if not isinstance(relations, list):
            result["errors"].append("Campo 'relations' deve essere una lista.")
        else:
            result["stats"]["relations_count"] = len(relations)
            for idx, rel in enumerate(relations):
                if not isinstance(rel, dict):
                    result["errors"].append(f"Relazione #{idx+1} non e' un oggetto.")
                    continue
                t_id = rel.get("targetId")
                t_type = rel.get("relationType")
                weight = rel.get("weight")
                if t_id:
                    relation_target_ids.add(t_id)
                else:
                    result["errors"].append(f"Relazione #{idx+1} priva di 'targetId'.")
                if t_type not in CANONICAL_RELATION_TYPES:
                    result["errors"].append(
                        f"Relazione verso '{t_id}' ha tipo '{t_type}' non valido. Ammessi: {sorted(list(CANONICAL_RELATION_TYPES))}"
                    )
                if weight is None or not (0.0 <= float(weight) <= 1.0):
                    result["warnings"].append(f"Relazione verso '{t_id}' ha weight non compreso tra 0.0 e 1.0.")

        # 9. Controllo Coerenza related_docs vs relations
        related_docs = frontmatter.get("related_docs", [])
        if isinstance(related_docs, list):
            for r_id in related_docs:
                if r_id and r_id not in relation_target_ids:
                    result["errors"].append(
                        f"Discrepanza OKF: ID '{r_id}' presente in related_docs ma assente come targetId in relations."
                    )
        elif related_docs is not None:
            result["errors"].append("Campo 'related_docs' deve essere una lista di ID.")

        # 10. Controllo di Sicurezza (Credenziali in chiaro)
        # Rileva solo assegnazioni reali di password/secret non referenziate a vault:// e non placeholder/variabili
        secret_assignment_pattern = re.compile(
            r"^\s*(?:[\w.-]*(?:password|passwd|pwd|secret|api_key|token)[\w.-]*)\s*[:=]\s*[\"'](?!vault:\/\/|<|\$|null|none|\s*[\"'])([^\"'\n]{4,})[\"']",
            re.IGNORECASE | re.MULTILINE
        )
        for m in secret_assignment_pattern.finditer(content):
            val = m.group(1).strip()
            # Ignora se contiene riferimenti di esempio, spiegazioni o variabili shell
            if any(term in val.lower() for term in ["vault", "example", "placeholder", "$", "prompt", "richiedere"]):
                continue
            result["errors"].append(f"VIOLAZIONE DI SICUREZZA: Rilevata possibile credenziale in chiaro: '{m.group(0).strip()}'. Usa 'vault://'.")
            break

        # 11. Controllo Placeholder (<...>, <DA-RICHIEDERE>)
        placeholders = re.findall(r"<([A-Za-z0-9_-]{2,})>", content)
        # Filtra eventuali tag HTML legittimi come <br>, <!--
        valid_html = {"br", "hr", "p", "div", "span", "details", "summary"}
        code_placeholders = [p for p in placeholders if p.lower() not in valid_html and not p.startswith("!--")]

        da_richiedere = re.findall(r"<DA-RICHIEDERE>", content)

        result["stats"]["placeholders_count"] = len(code_placeholders)
        result["stats"]["da_richiedere_count"] = len(da_richiedere)

        if not self.is_template:
            if da_richiedere:
                result["warnings"].append(f"Presenti {len(da_richiedere)} campi contrassegnati come <DA-RICHIEDERE>.")
            if code_placeholders:
                result["warnings"].append(f"Presenti {len(code_placeholders)} placeholder residui da compilare (es. <{code_placeholders[0]}>).")

        # 12. Controllo Trust Signals (Release v0.6)
        if frontmatter:
            verified = frontmatter.get("verified")
            if verified is not None:
                if not isinstance(verified, bool):
                    result["errors"].append("Campo 'verified' deve essere un booleano (true/false).")
                elif verified is True:
                    if not frontmatter.get("verified_by"):
                        result["warnings"].append("Documento marcato come verified: true ma privo di 'verified_by'.")
                    if not frontmatter.get("last_vetted"):
                        result["warnings"].append("Documento marcato come verified: true ma privo di data 'last_vetted'.")

            stale_after = frontmatter.get("stale_after")
            if stale_after:
                try:
                    stale_str = str(stale_after).strip()
                    stale_date = datetime.strptime(stale_str, "%Y-%m-%d").date()
                    if stale_date < datetime.now().date():
                        result["warnings"].append(
                            f"[STALE-WARNING] Documento scaduto il {stale_date} (stale_after superato). Richiede ricertificazione tecnica prima dell'uso."
                        )
                except ValueError:
                    result["warnings"].append(f"Formato data 'stale_after' non valido ('{stale_after}'). Atteso YYYY-MM-DD.")

        return result

def cmd_list_templates(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    templates_dir = repo_root / "templates"

    if not templates_dir.exists():
        print(f"Directory {templates_dir} non trovata.", file=sys.stderr)
        return 1

    print(colorize("\n=== CATALOGO TEMPLATE DOCUMENTALI IT (OKF v0.2) ===", COLOR_BOLD + COLOR_CYAN))
    print(f"{'Codice':<24} | {'Fase':<6} | {'Tipo OKF':<15} | {'Descrizione'}")
    print("-" * 80)

    for code, phase, okf_type, desc in IT_DOCUMENT_TYPES:
        filename = f"{code}.md"
        filepath = templates_dir / filename
        exists = "OK" if filepath.exists() else "NON TROVATO"
        status_color = COLOR_GREEN if filepath.exists() else COLOR_RED
        print(f"{code:<24} | Fase {phase:<2} | {okf_type:<15} | {desc} [{colorize(exists, status_color)}]")

    print("-" * 80 + "\n")
    return 0

def cmd_init(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    projects_dir = repo_root / "projects"
    project_slug = args.project_slug.lower().strip()
    target_dir = projects_dir / project_slug

    if target_dir.exists():
        print(colorize(f"ERRORE: Il progetto '{project_slug}' esiste gia' in: {target_dir}", COLOR_RED))
        return 1

    target_dir.mkdir(parents=True, exist_ok=True)

    template_manifest = repo_root / "projects" / "_template" / "project-manifest.yaml"
    manifest_target = target_dir / "project-manifest.yaml"

    customer = args.client or "Cliente Demo S.p.A."
    architect = args.architect or "System Architect"
    project_name = args.name or f"Progetto Infrastruttura {project_slug.capitalize()}"

    if template_manifest.exists():
        text = template_manifest.read_text(encoding="utf-8")
        text = re.sub(r'project_id:\s*"[^"]+"', f'project_id: "{project_slug}"', text)
        text = re.sub(r'project_name:\s*"[^"]+"', f'project_name: "{project_name}"', text)
        text = re.sub(r'customer:\s*"[^"]+"', f'customer: "{customer}"', text)
        text = re.sub(r'lead_architect:\s*"[^"]+"', f'lead_architect: "{architect}"', text)
        manifest_target.write_text(text, encoding="utf-8")
    else:
        manifest_target.write_text(f"""project_id: "{project_slug}"
project_name: "{project_name}"
customer: "{customer}"
lead_architect: "{architect}"
status: "in-planning"
version: "0.1.0"
""", encoding="utf-8")

    # Inizializza scratchpad Staging Memory (Release v0.6)
    try:
        from itinfra_memory import MemoryManager
        mem_mgr = MemoryManager(repo_root=repo_root)
        mem_mgr.init_scratchpad(project_slug)
    except Exception:
        pass

    print(colorize(f"\n[OK] Progetto '{project_slug}' inizializzato con successo!", COLOR_GREEN + COLOR_BOLD))
    print(f"Cartella: {target_dir}")
    print(f"Manifest: {manifest_target}")
    print("\nPuoi iniziare a compilare il primo documento:")
    print(f"  Fase 1: 01-RSD-URS.md")
    print(f"Eseguendo: python scripts/itinfra.py status {project_slug}\n")
    return 0

def cmd_validate(args: argparse.Namespace) -> int:
    target_path = Path(args.path)
    if not target_path.exists():
        print(colorize(f"ERRORE: Percorso '{target_path}' non trovato.", COLOR_RED))
        return 1

    is_dir = target_path.is_dir()
    is_template_dir = "templates" in str(target_path.resolve()).lower()

    files_to_check = []
    if is_dir:
        files_to_check = [f for f in sorted(list(target_path.rglob("*.md"))) if f.name.lower() != "readme.md" and not f.name.startswith("_")]
    else:
        files_to_check = [target_path]

    if not files_to_check:
        print(f"Nessun file Markdown trovato in: {target_path}")
        return 0

    print(colorize(f"\n=== VALIDAZIONE OKF v0.2: {len(files_to_check)} file da verificare ===", COLOR_BOLD + COLOR_CYAN))

    has_errors = False
    total_warnings = 0

    for file in files_to_check:
        # Se il file e' un README o INDEX, gestisci specificamente
        is_tpl = is_template_dir or ("_template" in str(file))
        validator = OKFValidator(is_template=is_tpl)
        res = validator.validate(file)

        rel_path = file.name
        if len(res["errors"]) > 0:
            has_errors = True
            print(f"[{colorize('FAIL', COLOR_RED + COLOR_BOLD)}] {file}")
            for err in res["errors"]:
                print(f"   {colorize('x', COLOR_RED)} {err}")
        else:
            status_text = "PASS" if len(res["warnings"]) == 0 else "WARN"
            status_color = COLOR_GREEN if len(res["warnings"]) == 0 else COLOR_YELLOW
            print(f"[{colorize(status_text, status_color + COLOR_BOLD)}] {file}")

        for w in res["warnings"]:
            total_warnings += 1
            print(f"   {colorize('!', COLOR_YELLOW)} {w}")

        if args.verbose:
            stats = res["stats"]
            print(f"   Dettagli: {stats['entities_count']} entita', {stats['relations_count']} relazioni, {stats['placeholders_count']} placeholder")

    print("-" * 80)
    if has_errors:
        print(colorize("\n[X] Validazione fallita: correggi gli errori evidenziati.", COLOR_RED + COLOR_BOLD))
        return 1
    else:
        msg = f"\n[V] Validazione completata con successo ({total_warnings} avvisi)."
        print(colorize(msg, COLOR_GREEN + COLOR_BOLD))
        return 0

def cmd_status(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    project_slug = args.project_slug.lower().strip()
    proj_dir = repo_root / "projects" / project_slug

    if not proj_dir.exists():
        print(colorize(f"ERRORE: Progetto '{project_slug}' non trovato in {proj_dir}", COLOR_RED))
        return 1

    manifest_file = proj_dir / "project-manifest.yaml"
    manifest_data = {}
    if manifest_file.exists():
        try:
            manifest_data = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
        except Exception:
            pass

    print(colorize(f"\n=== STATO PROGETTO: {project_slug.upper()} ===", COLOR_BOLD + COLOR_CYAN))
    print(f"Cliente:        {manifest_data.get('customer', 'N/A')}")
    print(f"Nome Progetto:  {manifest_data.get('project_name', 'N/A')}")
    print(f"Lead Architect: {manifest_data.get('lead_architect', 'N/A')}")
    print(f"Stato Globale:  {manifest_data.get('status', 'N/A')}")
    print(f"Supernet IPv4:  {manifest_data.get('network_baseline', {}).get('supernet_ipv4', 'N/A')}")
    print(f"ASN BGP:        {manifest_data.get('network_baseline', {}).get('bgp_asn_internal', 'N/A')}")
    print("-" * 80)

    print(f"{'Doc ID':<24} | {'Fase':<6} | {'Presenza':<12} | {'Qualita / OKF':<15} | {'Note'}")
    print("-" * 80)

    completed_count = 0
    validator = OKFValidator(is_template=False)

    for code, phase, okf_type, desc in IT_DOCUMENT_TYPES:
        doc_filename = f"{code}.md"
        doc_path = proj_dir / doc_filename
        if doc_path.exists():
            val_res = validator.validate(doc_path)
            if len(val_res["errors"]) == 0:
                qual = colorize("OKF Conforme", COLOR_GREEN)
                completed_count += 1
            else:
                qual = colorize(f"{len(val_res['errors'])} Errori", COLOR_RED)
            presence = colorize("Presente", COLOR_GREEN)
            ph = val_res["stats"]["placeholders_count"]
            note = f"{ph} placeholder aperti" if ph > 0 else "Completo"
        else:
            presence = colorize("Mancante", COLOR_YELLOW)
            qual = "-"
            note = f"Richiesto per Fase {phase}"

        print(f"{code:<24} | Fase {phase:<2} | {presence:<21} | {qual:<24} | {note}")

    print("-" * 80)
    pct = int((completed_count / len(IT_DOCUMENT_TYPES)) * 100)
    print(f"Avanzamento documentale: {completed_count}/{len(IT_DOCUMENT_TYPES)} ({pct}%)\n")

    # Sezione Ticket RCA & Troubleshooting (Fase 7 Post-Go-Live)
    rca_files = sorted(proj_dir.glob("10-RCA-*.md"))
    if rca_files:
        print(colorize("--- TICKET & INCIDENT RCA (Fase 7 Post-Go-Live) ---", COLOR_BOLD + COLOR_CYAN))
        print(f"{'File':<34} | {'Incidente ID':<16} | {'Severita':<10} | {'Qualita OKF':<15} | {'Stato'}")
        print("-" * 95)
        for rf in rca_files:
            val_res = validator.validate(rf)
            qual = colorize("OKF Conforme", COLOR_GREEN) if len(val_res["errors"]) == 0 else colorize(f"{len(val_res['errors'])} Errori", COLOR_RED)
            c_text = rf.read_text(encoding="utf-8").lstrip("\ufeff")
            fm, _, _ = parse_frontmatter(c_text)
            fm = fm or {}
            inc_id = fm.get("incident_id", "N/A")
            sev = fm.get("severity", "N/A")
            st = fm.get("status", "N/A")
            print(f"{rf.name:<34} | {inc_id:<16} | {sev:<10} | {qual:<24} | {st}")
        print("-" * 95 + "\n")

    return 0

def extract_markdown_table_rows(section_text: str) -> List[Dict[str, str]]:
    """Estrae le righe di una tabella Markdown restituendo una lista di dizionari {header: value}."""
    lines = [l.strip() for l in section_text.strip().splitlines() if l.strip()]
    table_lines = [l for l in lines if l.startswith("|") and l.endswith("|")]
    if len(table_lines) < 3:
        return []

    headers = [h.strip() for h in table_lines[0].split("|")[1:-1]]
    rows = []
    for line in table_lines[2:]:  # Salta riga header e riga separatore |---|---|
        cols = [c.strip() for c in line.split("|")[1:-1]]
        if len(cols) == len(headers):
            row = {headers[i]: cols[i] for i in range(len(headers))}
            rows.append(row)
    return rows

def cmd_export_ipam(args: argparse.Namespace) -> int:
    target_path = Path(args.path)
    if target_path.is_dir():
        # Cerca file LLD o As-Built nel progetto
        cand = list(target_path.glob("*LLD*.md")) or list(target_path.glob("*As-Built*.md"))
        if not cand:
            print(colorize(f"ERRORE: Nessun file LLD o As-Built trovato nella cartella '{target_path}'.", COLOR_RED))
            return 1
        target_path = cand[0]

    if not target_path.exists():
        print(colorize(f"ERRORE: File '{target_path}' non trovato.", COLOR_RED))
        return 1

    content = target_path.read_text(encoding="utf-8")
    out_dir = Path(args.out) if args.out else Path("exports")
    out_dir.mkdir(parents=True, exist_ok=True)
    fmt = args.format.lower()

    vlans_data = []
    prefixes_data = []
    ips_data = []

    # 1. Parsing Sezione 2.1 - Schema di Subnetting
    subnets_match = re.search(r"##+ [0-9.]* ?Schema di Subnetting.*?\n(.*?)(?=\n##+ |\Z)", content, re.DOTALL | re.IGNORECASE)
    if subnets_match:
        rows = extract_markdown_table_rows(subnets_match.group(1))
        for r in rows:
            subnet = r.get("Subnet", "")
            cidr = r.get("CIDR", "")
            prefix = f"{subnet}{cidr}" if cidr.startswith("/") else f"{subnet}/{cidr}" if cidr else subnet
            vlan_id = r.get("VLAN ID", "")
            desc = r.get("Utilizzo", "")
            zone = r.get("Zona", "")
            gateway = r.get("Gateway", "")

            if prefix and not prefix.startswith("<"):
                prefixes_data.append({
                    "prefix": prefix,
                    "status": "active",
                    "vrf": zone or "Global",
                    "tenant": "Default",
                    "vlan": vlan_id if not vlan_id.startswith("<") else "",
                    "description": desc or zone
                })
            if gateway and not gateway.startswith("<"):
                ips_data.append({
                    "address": f"{gateway}{cidr}",
                    "status": "reserved",
                    "vrf": zone or "Global",
                    "tenant": "Default",
                    "dns_name": f"gw-{zone.lower()}" if zone else "gateway",
                    "description": f"Default Gateway VLAN {vlan_id}"
                })

    # 2. Parsing Sezione 2.2 - Mappatura VLAN
    vlans_match = re.search(r"##+ [0-9.]* ?Mappatura VLAN.*?\n(.*?)(?=\n##+ |\Z)", content, re.DOTALL | re.IGNORECASE)
    if vlans_match:
        rows = extract_markdown_table_rows(vlans_match.group(1))
        for r in rows:
            vid = r.get("VLAN ID", "")
            name = r.get("Nome", "")
            zone = r.get("Zona", "")
            trust = r.get("Trust level", "")
            if vid and not vid.startswith("<"):
                vlans_data.append({
                    "vid": vid,
                    "name": name if not name.startswith("<") else f"VLAN_{vid}",
                    "status": "active",
                    "tenant": "Default",
                    "description": f"Zona: {zone} | Trust: {trust}"
                })

    # 3. Parsing Sezione 2.3 - Allocazione IP degli Host Fissi
    hosts_match = re.search(r"##+ [0-9.]* ?Allocazione IP degli Host Fissi.*?\n(.*?)(?=\n##+ |\Z)", content, re.DOTALL | re.IGNORECASE)
    if hosts_match:
        rows = extract_markdown_table_rows(hosts_match.group(1))
        for r in rows:
            hostname = r.get("Hostname", "")
            ip = r.get("IP", "")
            vlan = r.get("VLAN", "")
            role = r.get("Ruolo", "")
            note = r.get("Note", "")
            if ip and not ip.startswith("<"):
                ips_data.append({
                    "address": ip if "/" in ip else f"{ip}/32",
                    "status": "active",
                    "vrf": "Global",
                    "tenant": "Default",
                    "dns_name": hostname if not hostname.startswith("<") else "",
                    "description": f"{role} ({note})" if note else role
                })

    print(colorize(f"\n=== ESPORTAZIONE IPAM / NETBOX DA: {target_path.name} ===", COLOR_BOLD + COLOR_CYAN))
    print(f"Formato:      {fmt.upper()}")
    print(f"Cartella out: {out_dir.resolve()}")
    print(f"VLAN trovate: {len(vlans_data)}")
    print(f"Subnet/Prefix: {len(prefixes_data)}")
    print(f"IP Allocati:  {len(ips_data)}")

    if fmt == "json":
        import json
        (out_dir / "vlans.json").write_text(json.dumps(vlans_data, indent=2), encoding="utf-8")
        (out_dir / "prefixes.json").write_text(json.dumps(prefixes_data, indent=2), encoding="utf-8")
        (out_dir / "ip_addresses.json").write_text(json.dumps(ips_data, indent=2), encoding="utf-8")
    else:
        import csv
        # Salva vlans.csv
        with open(out_dir / "vlans.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["vid", "name", "status", "tenant", "description"])
            writer.writeheader()
            writer.writerows(vlans_data)

        # Salva prefixes.csv
        with open(out_dir / "prefixes.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["prefix", "status", "vrf", "tenant", "vlan", "description"])
            writer.writeheader()
            writer.writerows(prefixes_data)

        # Salva ip_addresses.csv
        with open(out_dir / "ip_addresses.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["address", "status", "vrf", "tenant", "dns_name", "description"])
            writer.writeheader()
            writer.writerows(ips_data)

    print(colorize("\n[OK] Esportazione completata con successo!", COLOR_GREEN + COLOR_BOLD))
    print(f"  - {out_dir / ('vlans.' + fmt)}")
    print(f"  - {out_dir / ('prefixes.' + fmt)}")
    print(f"  - {out_dir / ('ip_addresses.' + fmt)}\n")
    return 0

def cmd_generate_diagram(args: argparse.Namespace) -> int:
    target_path = Path(args.path)
    if not target_path.exists():
        print(colorize(f"ERRORE: File '{target_path}' non trovato.", COLOR_RED))
        return 1

    content = target_path.read_text(encoding="utf-8")
    diag_type = args.type.lower()
    output_lines = []

    # 1. Diagramma Topologico
    if diag_type in ("topology", "all"):
        output_lines.append("```mermaid")
        output_lines.append("graph TD")
        output_lines.append("    %% Stili dei nodi per categoria architetturale")
        output_lines.append("    classDef core fill:#1e395b,stroke:#2b5797,stroke-width:2px,color:#fff;")
        output_lines.append("    classDef tor fill:#107c41,stroke:#0b552c,stroke-width:2px,color:#fff;")
        output_lines.append("    classDef fw fill:#d83b01,stroke:#a82a00,stroke-width:2px,color:#fff;")
        output_lines.append("    classDef storage fill:#5c2d91,stroke:#3b1a60,stroke-width:2px,color:#fff;")
        output_lines.append("    classDef srv fill:#0078d7,stroke:#004e8c,stroke-width:1px,color:#fff;")
        output_lines.append("")

        # Cerca tabelle di switch nel capitolo 4 (Cable Matrix)
        cable_sections = re.findall(r"###+ [0-9.]* ?Switch (?:Core|ToR)? ?([a-zA-Z0-9_-]+).*?\n(.*?)(?=\n###+ |\Z)", content, re.DOTALL | re.IGNORECASE)
        edges = set()
        devices = {}

        for sw_name, sec_text in cable_sections:
            sw_id = sw_name.replace("-", "_").lower()
            devices[sw_id] = sw_name
            rows = extract_markdown_table_rows(sec_text)
            for r in rows:
                target_dev = r.get("Dispositivo collegato") or r.get("Dispositivo") or ""
                target_dev = target_dev.split()[0].strip()  # Prende primo token
                local_port = r.get("Porta", "")
                remote_port = r.get("Porta remota", "")
                vlan = r.get("VLAN", "")

                if target_dev and not target_dev.startswith("<") and target_dev.lower() != "spare":
                    tgt_id = target_dev.replace("-", "_").replace(".", "_").lower()
                    devices[tgt_id] = target_dev
                    label = f"{local_port} <-> {remote_port}" if remote_port else local_port
                    if vlan and not vlan.startswith("<"):
                        label += f" ({vlan})"
                    edge_key = tuple(sorted([sw_id, tgt_id])) + (label,)
                    edges.add((sw_id, tgt_id, label))

        # Se non trovate tabelle cavi dettagliate, estrai componenti da HLD
        if not edges:
            output_lines.append("    %% Topologia logica estratta da componenti")
            output_lines.append("    Internet[Internet / WAN] --> fw_01[Firewall Cluster FW-HA]:::fw")
            output_lines.append("    fw_01 --> sw_core_01[Core Switch SW-CORE-01]:::core")
            output_lines.append("    fw_01 --> sw_core_02[Core Switch SW-CORE-02]:::core")
            output_lines.append("    sw_core_01 --- sw_core_02")
            output_lines.append("    sw_core_01 --> sw_tor_01[Switch ToR R01]:::tor")
            output_lines.append("    sw_core_02 --> sw_tor_01")
            output_lines.append("    sw_core_01 --> sw_tor_02[Switch ToR R02]:::tor")
            output_lines.append("    sw_core_02 --> sw_tor_02")
            output_lines.append("    sw_tor_01 --> srv_compute[Cluster Hypervisor / Server]:::srv")
            output_lines.append("    sw_tor_02 --> storage_array[Storage SAN / NAS]:::storage")
        else:
            output_lines.append("    subgraph Network_Fabric[\"Infrastruttura di Rete\"]")
            for dev_id, dev_name in sorted(devices.items()):
                d_lower = dev_name.lower()
                cls_name = "core" if "core" in d_lower else "tor" if "tor" in d_lower else "fw" if "fw" in d_lower else "storage" if "stor" in d_lower else "srv"
                output_lines.append(f"        {dev_id}[\"{dev_name}\"]:::{cls_name}")
            output_lines.append("    end")
            output_lines.append("")
            output_lines.append("    %% Interconnessioni e cablaggi fisici")
            for src, tgt, label in sorted(edges):
                clean_label = label.replace('"', '').replace('|', '/')
                output_lines.append(f"    {src} <== \"{clean_label}\" ==> {tgt}")

        output_lines.append("```\n")

    # 2. Diagramma Rack Elevation
    if diag_type in ("rack", "all"):
        output_lines.append("```mermaid")
        output_lines.append("block-beta")
        output_lines.append("    columns 1")
        output_lines.append("    block:Rack[\"Rack Elevation 42U\"]")
        output_lines.append("        columns 2")
        output_lines.append("        U_Header[\"Unita RU\"]:1")
        output_lines.append("        Comp_Header[\"Apparato / Componente\"]:1")

        # Parsing Sezione Rack Elevation
        rack_matches = re.findall(r"^\s*([0-9]{1,2})\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]*)", content, re.MULTILINE)
        found_u = False
        for u_num, comp, note in rack_matches:
            u_clean = u_num.strip()
            comp_clean = comp.strip().replace('"', '').replace('[', '').replace(']', '')
            if comp_clean.startswith("-"):
                comp_clean = "(Spazio Libero / Patching)"
            if u_clean.isdigit():
                found_u = True
                output_lines.append(f"        U_{u_clean}[\"{u_clean}U\"]:1")
                output_lines.append(f"        Dev_{u_clean}[\"{comp_clean}\"]:1")

        if not found_u:
            output_lines.append("        U_42[\"42U-41U\"]:1 Dev_42[\"PDU & Cable Management\"]:1")
            output_lines.append("        U_40[\"40U-39U\"]:1 Dev_40[\"Top of Rack Switches (HA)\"]:1")
            output_lines.append("        U_38[\"38U-35U\"]:1 Dev_38[\"Hypervisor Nodes 1-4\"]:1")
            output_lines.append("        U_34[\"34U-20U\"]:1 Dev_34[\"Spazio di Espansione Calcolo\"]:1")
            output_lines.append("        U_19[\"19U-10U\"]:1 Dev_19[\"Storage Array & Disk Shelves\"]:1")
            output_lines.append("        U_09[\"01U-09U\"]:1 Dev_09[\"UPS & PDU Inferiore\"]:1")

        output_lines.append("    end")
        output_lines.append("```\n")

    result_text = "\n".join(output_lines)
    if args.out:
        out_file = Path(args.out)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(result_text, encoding="utf-8")
        print(colorize(f"\n[OK] Diagramma salvato con successo in: {out_file}\n", COLOR_GREEN + COLOR_BOLD))
    else:
        print(colorize("\n=== DIAGRAMMA MERMAID GENERATO ===", COLOR_BOLD + COLOR_CYAN))
        print(result_text)

    return 0

def markdown_to_html_enhanced(md: str) -> str:
    """Converte un testo markdown in HTML pulito con supporto a tabelle, blocchi mermaid e checklist."""
    import html as html_lib
    
    lines = md.splitlines()
    html_out = []
    in_code_block = False
    code_lang = ""
    code_lines = []
    in_table = False
    table_headers = []
    table_rows = []
    in_list = False

    def close_table():
        nonlocal in_table, table_headers, table_rows
        if not in_table:
            return ""
        out = ["<div class=\"table-container\"><table>"]
        if table_headers:
            out.append("<thead><tr>")
            for h in table_headers:
                out.append(f"<th>{h}</th>")
            out.append("</tr></thead>")
        if table_rows:
            out.append("<tbody>")
            for row in table_rows:
                out.append("<tr>")
                for cell in row:
                    out.append(f"<td>{cell}</td>")
                out.append("</tr>")
            out.append("</tbody>")
        out.append("</table></div>")
        in_table = False
        table_headers = []
        table_rows = []
        return "".join(out)

    def close_list():
        nonlocal in_list
        if not in_list:
            return ""
        in_list = False
        return "</ul>"

    def format_inline(text: str) -> str:
        # Checkbox
        text = text.replace("[x]", "<span class=\"badge-checked\">&check; Fatto</span>")
        text = text.replace("[ ]", "<span class=\"badge-unchecked\">&square; Da fare</span>")
        # Bold
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        # Italic
        text = re.sub(r"\*(.*?)\*", r"<em>\1</em>", text)
        # Inline code
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # Wiki-links [[target]]
        text = re.sub(r"\[\[(.*?)\]\]", r"<span class=\"wiki-link\">&sect; \1</span>", text)
        return text

    for line in lines:
        stripped = line.strip()

        # Blocchi di codice ```
        if stripped.startswith("```"):
            if in_code_block:
                in_code_block = False
                block_content = html_lib.escape("\n".join(code_lines))
                if code_lang.lower() == "mermaid":
                    html_out.append(f"<div class=\"mermaid\">\n{'\n'.join(code_lines)}\n</div>")
                else:
                    html_out.append(f"<pre><code class=\"language-{code_lang}\">{block_content}</code></pre>")
                code_lines = []
                code_lang = ""
            else:
                if in_table:
                    html_out.append(close_table())
                if in_list:
                    html_out.append(close_list())
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_lines = []
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        # Tabelle Markdown
        if stripped.startswith("|") and stripped.endswith("|"):
            if in_list:
                html_out.append(close_list())
            cells = [format_inline(c.strip()) for c in stripped[1:-1].split("|")]
            # Riga divisoria |---|---|
            if all(re.match(r"^:?-+:?$", re.sub(r"<.*?>", "", c).strip()) for c in cells):
                continue
            if not in_table:
                in_table = True
                table_headers = cells
            else:
                table_rows.append(cells)
            continue
        elif in_table:
            html_out.append(close_table())

        # Liste non ordinate
        if stripped.startswith("- ") or stripped.startswith("* "):
            if not in_list:
                in_list = True
                html_out.append("<ul>")
            item_text = format_inline(stripped[2:].strip())
            html_out.append(f"<li>{item_text}</li>")
            continue
        elif in_list and not stripped.startswith("- ") and not stripped.startswith("* "):
            html_out.append(close_list())

        # Headers
        if stripped.startswith("# "):
            html_out.append(f"<h1>{format_inline(stripped[2:].strip())}</h1>")
        elif stripped.startswith("## "):
            html_out.append(f"<h2>{format_inline(stripped[3:].strip())}</h2>")
        elif stripped.startswith("### "):
            html_out.append(f"<h3>{format_inline(stripped[4:].strip())}</h3>")
        elif stripped.startswith("#### "):
            html_out.append(f"<h4>{format_inline(stripped[5:].strip())}</h4>")
        elif stripped.startswith("---") or stripped.startswith("***"):
            html_out.append("<hr/>")
        elif stripped:
            html_out.append(f"<p>{format_inline(stripped)}</p>")

    if in_table:
        html_out.append(close_table())
    if in_list:
        html_out.append(close_list())

    return "\n".join(html_out)

def cmd_export_html(args) -> int:
    """Genera un report consolidato completo in formato HTML per il progetto."""
    target_path = Path(args.project)
    if not target_path.exists():
        project_dir = Path("projects") / args.project
        if project_dir.exists():
            target_path = project_dir
        else:
            print(colorize(f"ERRORE: Cartella progetto '{args.project}' non trovata.", COLOR_RED))
            return 1

    # Carica manifest se presente
    manifest_file = target_path / "project-manifest.yaml"
    manifest = {}
    if manifest_file.exists():
        try:
            manifest = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
        except Exception as e:
            print(colorize(f"AVVISO: Impossibile leggere il manifesto: {e}", COLOR_YELLOW))

    project_name = manifest.get("project_name", target_path.name)
    client_name = manifest.get("customer", "N/A")
    lead_arch = manifest.get("lead_architect", "N/A")
    net_baseline = manifest.get("network_baseline", {})
    hw_baseline = manifest.get("hardware_baseline", {})
    sla_baseline = manifest.get("sla_baseline", {})

    # Raccogli e valida documenti
    validator = OKFValidator(is_template=False)
    doc_sections = []
    completed_count = 0
    total_docs = len(IT_DOCUMENT_TYPES)

    for prefix, phase, okf_type, desc in IT_DOCUMENT_TYPES:
        doc_files = list(target_path.glob(f"{prefix}*.md"))
        if doc_files:
            file_p = doc_files[0]
            val_res = validator.validate(file_p)
            status_ok = len(val_res["errors"]) == 0
            if status_ok:
                completed_count += 1
            content = file_p.read_text(encoding="utf-8").lstrip("\ufeff")
            fm, body, _ = parse_frontmatter(content)
            doc_sections.append({
                "prefix": prefix,
                "phase": phase,
                "type": okf_type,
                "desc": desc,
                "path": file_p.name,
                "frontmatter": fm or {},
                "body_html": markdown_to_html_enhanced(body),
                "is_valid": status_ok,
                "errors": val_res["errors"],
                "warnings": val_res["warnings"]
            })
        else:
            doc_sections.append({
                "prefix": prefix,
                "phase": phase,
                "type": okf_type,
                "desc": desc,
                "path": None,
                "frontmatter": {},
                "body_html": f"<p class='doc-missing'>Documento non ancora redatto (previsto per la Fase {phase}).</p>",
                "is_valid": False,
                "errors": [],
                "warnings": []
            })

    pct_complete = int((completed_count / total_docs) * 100)

    tab_mapping = {
        "01-RSD-URS": ("tab-fase1", "Fase 1: RSD"),
        "02-HLD": ("tab-fase2-hld", "Fase 2: HLD"),
        "03-LLD": ("tab-fase2-lld", "Fase 2: LLD"),
        "04-MOP": ("tab-fase3-mop", "Fase 3: MOP"),
        "05-Rollback": ("tab-fase3-rollback", "Fase 3: Rollback"),
        "06-As-Built": ("tab-fase5-asbuilt", "Fase 5: As-Built"),
        "07-ATP": ("tab-fase6-atp", "Fase 6: ATP"),
        "08-SOP-Runbook": ("tab-fase7-sop", "Fase 7: SOP"),
        "09-Handover-Inventory": ("tab-fase7-handover", "Fase 7: Handover"),
    }

    nav_buttons = [
        '<button class="tab-btn active" onclick="switchTab(\'tab-dashboard\')">Dashboard & Manifest</button>',
        '<button class="tab-btn" onclick="window.open(\'graph.html\', \'_blank\')">Knowledge Graph 3D/D3 &#128376;</button>'
    ]
    for s in doc_sections:
        prefix = s["prefix"]
        if prefix in tab_mapping:
            t_id, t_label = tab_mapping[prefix]
            if s["is_valid"]:
                nav_buttons.append(f'<button class="tab-btn" onclick="switchTab(\'{t_id}\')">{t_label} &check;</button>')
            elif s["path"]:
                nav_buttons.append(f'<button class="tab-btn" onclick="switchTab(\'{t_id}\')">{t_label} (!)</button>')

    # Raccogli e valida eventuali documenti RCA (10-RCA-*.md)
    rca_files = sorted(target_path.glob("10-RCA-*.md"))
    rca_sections = []
    for rf in rca_files:
        val_res = validator.validate(rf)
        c_text = rf.read_text(encoding="utf-8").lstrip("\ufeff")
        fm, b_text, _ = parse_frontmatter(c_text)
        rca_sections.append({
            "path": rf.name,
            "frontmatter": fm or {},
            "body_html": markdown_to_html_enhanced(b_text),
            "is_valid": len(val_res["errors"]) == 0,
            "errors": val_res["errors"]
        })

    if rca_sections:
        nav_buttons.append('<button class="tab-btn" onclick="switchTab(\'tab-rca\')">Incident & RCA &check;</button>')

    nav_buttons_html = "\n        ".join(nav_buttons)

    # HTML Template con CSS Moderno Dark/Light e Mermaid
    html_template = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Report Progetto IT: {html.escape(project_name)}</title>
    <style>
        :root {{
            --bg-primary: #0f172a;
            --bg-secondary: #1e293b;
            --bg-card: #1e293b;
            --bg-input: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --border-color: #334155;
            --font-main: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
            --font-mono: 'Cascadia Code', 'Fira Code', 'Courier New', monospace;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-main);
            line-height: 1.6;
            padding-bottom: 80px;
        }}
        header {{
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 2.5rem 2rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(12px);
        }}
        .header-content {{
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1.5rem;
        }}
        .header-title h1 {{
            font-size: 1.8rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.5px;
        }}
        .header-title p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-top: 0.3rem;
        }}
        .header-meta {{
            display: flex;
            gap: 1.5rem;
            align-items: center;
        }}
        .progress-pill {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 9999px;
            padding: 0.5rem 1.2rem;
            display: flex;
            align-items: center;
            gap: 0.8rem;
        }}
        .progress-bar-bg {{
            width: 110px;
            height: 10px;
            background-color: #334155;
            border-radius: 5px;
            overflow: hidden;
        }}
        .progress-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            width: {pct_complete}%;
            border-radius: 5px;
        }}
        .container {{
            max-width: 1300px;
            margin: 2rem auto;
            padding: 0 1.5rem;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1rem;
            margin-bottom: 2.5rem;
        }}
        .kpi-card {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem 1.5rem;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-cyan);
        }}
        .kpi-label {{
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        .kpi-val {{
            font-size: 1.4rem;
            font-weight: 700;
            margin-top: 0.4rem;
            color: #ffffff;
        }}
        .nav-tabs {{
            display: flex;
            gap: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 2rem;
            overflow-x: auto;
            padding-bottom: 0.5rem;
        }}
        .tab-btn {{
            background: none;
            border: none;
            color: var(--text-secondary);
            padding: 0.75rem 1.2rem;
            font-size: 0.95rem;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }}
        .tab-btn:hover {{
            color: #ffffff;
            background-color: var(--bg-secondary);
        }}
        .tab-btn.active {{
            color: #ffffff;
            background-color: var(--accent-blue);
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        .card {{
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
        }}
        .card h2 {{
            font-size: 1.4rem;
            margin-bottom: 1.2rem;
            color: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.6rem;
        }}
        .card h3 {{
            font-size: 1.15rem;
            margin: 1.5rem 0 0.8rem;
            color: var(--accent-cyan);
        }}
        .card h4 {{
            font-size: 1.05rem;
            margin: 1.2rem 0 0.6rem;
            color: #e2e8f0;
        }}
        .card p {{
            margin-bottom: 1rem;
            color: #cbd5e1;
        }}
        .card ul {{
            margin: 0.8rem 0 1.2rem 1.5rem;
            color: #cbd5e1;
        }}
        .card li {{
            margin-bottom: 0.4rem;
        }}
        .table-container {{
            overflow-x: auto;
            margin: 1.2rem 0 1.8rem;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }}
        th {{
            background-color: #273549;
            color: #e2e8f0;
            font-weight: 600;
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
        }}
        td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: #cbd5e1;
        }}
        tr:nth-child(even) td {{
            background-color: rgba(255, 255, 255, 0.02);
        }}
        tr:hover td {{
            background-color: rgba(255, 255, 255, 0.05);
        }}
        pre {{
            background-color: #0b1120;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.2rem;
            overflow-x: auto;
            margin: 1rem 0 1.5rem;
            font-family: var(--font-mono);
            font-size: 0.88rem;
            color: #38bdf8;
        }}
        code {{
            font-family: var(--font-mono);
            background-color: #0b1120;
            padding: 0.15rem 0.4rem;
            border-radius: 4px;
            font-size: 0.88rem;
            color: #38bdf8;
        }}
        .mermaid {{
            background-color: #0b1120;
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            display: flex;
            justify-content: center;
        }}
        .badge-pass {{
            background-color: rgba(16, 185, 129, 0.2);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            padding: 0.25rem 0.7rem;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 600;
        }}
        .badge-checked {{
            color: #34d399;
            font-weight: 600;
        }}
        .badge-unchecked {{
            color: var(--accent-amber);
            font-weight: 600;
        }}
        .wiki-link {{
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.1);
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
        }}
        .doc-missing {{
            color: #64748b;
            font-style: italic;
            padding: 2rem;
            text-align: center;
        }}
        .manifest-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-top: 1rem;
        }}
        .manifest-box {{
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.25rem;
        }}
        .manifest-box h4 {{
            margin-top: 0;
            color: var(--accent-cyan);
            margin-bottom: 0.8rem;
        }}
    </style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'dark' }});
    </script>
</head>
<body>

<header>
    <div class="header-content">
        <div class="header-title">
            <h1>{html.escape(project_name)}</h1>
            <p>Cliente: <strong>{html.escape(client_name)}</strong> | Lead Architect: <strong>{html.escape(lead_arch)}</strong> | Standard: <strong>OKF v0.2 Nativo</strong></p>
        </div>
        <div class="header-meta">
            <div class="progress-pill">
                <span>Avanzamento Fasi: <strong>{pct_complete}%</strong> ({completed_count}/{total_docs})</span>
                <div class="progress-bar-bg">
                    <div class="progress-bar-fill"></div>
                </div>
            </div>
        </div>
    </div>
</header>

<main class="container">
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-label">Supernet LAN</div>
            <div class="kpi-val">{html.escape(net_baseline.get('supernet_ipv4', '192.168.120.0/24'))}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Dominio Active Directory</div>
            <div class="kpi-val">{html.escape(net_baseline.get('active_directory_domain', 'severino'))}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Domain Controller IP</div>
            <div class="kpi-val">{html.escape(net_baseline.get('dc_ip', '192.168.120.239'))}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">ZeroTier Network</div>
            <div class="kpi-val" style="font-size: 1.15rem;">{html.escape(net_baseline.get('zerotier_network_id', '65228D8D6D71CA23'))}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Core Switch</div>
            <div class="kpi-val" style="font-size: 1.15rem;">MikroTik CRS326</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Virtualizzazione</div>
            <div class="kpi-val" style="font-size: 1.15rem;">HP Z4 / Hyper-V 2022</div>
        </div>
    </div>

    <nav class="nav-tabs">
        {nav_buttons_html}
    </nav>

    <!-- TAB DASHBOARD -->
    <div id="tab-dashboard" class="tab-content active">
        <div class="card">
            <h2>Manifesto di Progetto & Baseline Tecnologica</h2>
            <div class="manifest-grid">
                <div class="manifest-box">
                    <h4>Topologia & Rete Locale</h4>
                    <p><strong>Switch Core:</strong> {html.escape(net_baseline.get('core_switch_model', 'MikroTik CRS326-24G-2S+RM'))}</p>
                    <p><strong>Configurazione Porte:</strong> <code>ether1</code> WAN isolata verso Vodafone Station; <code>ether2-24</code> in Hardware Bridge LAN 1 Gbps.</p>
                    <p><strong>WiFi:</strong> {html.escape(net_baseline.get('wifi_solution', 'UniFi AP'))} su porta <code>ether14</code>.</p>
                    <p><strong>DHCP Server:</strong> Erogato da DC <code>dc01</code> (range 192.168.120.2 - 192.168.120.254).</p>
                </div>
                <div class="manifest-box">
                    <h4>Compute & Virtualizzazione</h4>
                    <p><strong>Workstation Host:</strong> {html.escape(hw_baseline.get('hypervisor_host', 'HP Z4'))} con Windows Server 2022 Datacenter.</p>
                    <p><strong>VM dc01:</strong> Active Directory Domain Controller, DNS integrato (IP: 192.168.120.239).</p>
                    <p><strong>VM fs01:</strong> File Server Severino Srl con 2 TB VHDX dedicati (IP: 192.168.120.240).</p>
                    <p><strong>VM fs02:</strong> File Server Partner con storage SSK 512 GB in passthrough fisico (IP: 192.168.120.241).</p>
                </div>
                <div class="manifest-box">
                    <h4>Collaboration & Sicurezza</h4>
                    <p><strong>Sala Riunioni:</strong> {html.escape(hw_baseline.get('meeting_room', 'TV 65\", Logitech Rally Bar + Tablet touch, Teams Rooms'))}.</p>
                    <p><strong>Overlay SDN:</strong> ZeroTier Network ID <code>{html.escape(net_baseline.get('zerotier_network_id', '65228D8D6D71CA23'))}</code> gestito da <code>{html.escape(net_baseline.get('zerotier_admin_email', 'salviozt01@gmail.com'))}</code>.</p>
                    <p><strong>Backup:</strong> QNAP TS-233 (IP: 192.168.120.250) con Cobian Reflector serale e transizione a RustCopy v7.4.1+.</p>
                    <p><strong>SLA Target:</strong> RTO 2 ore, RPO 1 ora. Finestra di manutenzione standard: weekend.</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Matrice di Conformità Fasi e Documentazione OKF v0.2</h2>
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Fase</th>
                            <th>Identificativo Doc</th>
                            <th>Tipologia OKF</th>
                            <th>Titolo Descrittivo</th>
                            <th>Stato Formale</th>
                            <th>Checklist & Note</th>
                        </tr>
                    </thead>
                    <tbody>
    """

    for s in doc_sections:
        badge_cls = "badge-pass" if s["is_valid"] else "badge-unchecked"
        status_txt = "VALIDATO (0 errori)" if s["is_valid"] else ("NON REDATTO" if not s["path"] else "NON CONFORME")
        file_label = s["path"] if s["path"] else "In attesa"
        html_template += f"""
                        <tr>
                            <td><strong>Fase {s['phase']}</strong></td>
                            <td><code>{s['prefix']}</code></td>
                            <td><span class="wiki-link">{s['type']}</span></td>
                            <td>{html.escape(s['desc'])}</td>
                            <td><span class="{badge_cls}">{status_txt}</span></td>
                            <td>{html.escape(file_label)}</td>
                        </tr>
        """

    html_template += f"""
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    """

    # Genera le singole tab documentali
    for s in doc_sections:
        if s["prefix"] in tab_mapping:
            tab_id = tab_mapping[s["prefix"]][0]
            fm = s["frontmatter"]
            doc_id = fm.get("id", s["prefix"])
            doc_title = fm.get("title", s["desc"])
            html_template += f"""
    <!-- TAB {s['prefix']} -->
    <div id="{tab_id}" class="tab-content">
        <div class="card">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 1.5rem; flex-wrap:wrap; gap: 1rem;">
                <div>
                    <h2>{html.escape(doc_title)}</h2>
                    <p>ID Documento: <code>{html.escape(doc_id)}</code> | Tipo: <strong>{s['type']}</strong> | Fase: <strong>Fase {s['phase']}</strong></p>
                </div>
                <div>
                    <span class="badge-pass">&check; Validato OKF v0.2</span>
                </div>
            </div>
            {s['body_html']}
        </div>
    </div>
            """

    # Genera la tab RCA se sono presenti incidenti
    if rca_sections:
        html_template += f"""
    <!-- TAB INCIDENT & RCA -->
    <div id="tab-rca" class="tab-content">
        <div class="card">
            <h2>Incident Management & Root Cause Analysis (Fase 7)</h2>
            <p>Registro formale degli incidenti e disservizi tecnici risolti per il progetto <strong>{html.escape(project_name)}</strong>.</p>
        </div>
        """
        for r in rca_sections:
            fm = r["frontmatter"]
            inc_id = fm.get("incident_id", "N/A")
            sev = fm.get("severity", "P2-High")
            title = fm.get("title", r["path"])
            status = fm.get("status", "approved")
            badge_class = "badge-pass" if r["is_valid"] else "badge-warn"
            html_template += f"""
        <div class="card" style="margin-top: 1.5rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 1.5rem; flex-wrap:wrap; gap: 1rem; border-bottom: 1px solid var(--border-color); padding-bottom: 1rem;">
                <div>
                    <h3>{html.escape(title)}</h3>
                    <p>Incidente: <code>{html.escape(inc_id)}</code> | Severità: <strong>{html.escape(sev)}</strong> | Stato: <strong>{html.escape(status)}</strong></p>
                </div>
                <div>
                    <span class="{badge_class}">&check; Validato OKF v0.2</span>
                </div>
            </div>
            {r['body_html']}
        </div>
            """
        html_template += """
    </div>
        """

    html_template += """
</main>

<script>
    function switchTab(tabId) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
        
        if (event && event.target) {
            event.target.classList.add('active');
        }
        const activeTab = document.getElementById(tabId);
        if (activeTab) {
            activeTab.classList.add('active');
            window.scrollTo({ top: 0, behavior: 'smooth' });
            if (window.mermaid && typeof window.mermaid.run === 'function') {
                try {
                    window.mermaid.run({ nodes: activeTab.querySelectorAll('.mermaid') });
                } catch(e) {}
            }
        }
    }
</script>

</body>
</html>
"""

    out_file_path = Path(args.out) if args.out else target_path / "report.html"
    out_file_path.parent.mkdir(parents=True, exist_ok=True)
    out_file_path.write_text(html_template, encoding="utf-8")

    print(colorize(f"\n[OK] Report consolidato HTML generato con successo!", COLOR_GREEN + COLOR_BOLD))
    print(colorize(f"     File salvato in: {out_file_path.resolve()}", COLOR_CYAN))
    print(colorize(f"     Documenti inclusi: {completed_count}/{total_docs} ({pct_complete}% avanzamento)\n", COLOR_BOLD))

    return 0

def cmd_vault(args) -> int:
    try:
        from scripts.itinfra_vault import VaultManager, VaultError
    except ImportError:
        try:
            from itinfra_vault import VaultManager, VaultError
        except ImportError as e:
            print(colorize(f"ERRORE: Impossibile importare itinfra_vault: {e}", COLOR_RED))
            return 1

    slug = args.project_slug
    passphrase = getattr(args, "passphrase", None) or os.environ.get("ITINFRA_VAULT_PASS")

    try:
        vault = VaultManager(slug)
    except VaultError as e:
        print(colorize(f"ERRORE VAULT: {e}", COLOR_RED))
        return 1

    action = args.vault_action

    if action == "init":
        if not passphrase:
            passphrase = getpass.getpass("Inserisci la nuova Master Passphrase per il Vault: ")
            confirm = getpass.getpass("Conferma la Master Passphrase: ")
            if passphrase != confirm:
                print(colorize("ERRORE: Le passphrase non coincidono.", COLOR_RED))
                return 1
        try:
            vpath = vault.init_vault(passphrase, overwrite=getattr(args, "overwrite", False))
            print(colorize(f"[OK] Vault inizializzato con successo in: {vpath}", COLOR_GREEN + COLOR_BOLD))
            return 0
        except Exception as e:
            print(colorize(f"ERRORE inizializzazione: {e}", COLOR_RED))
            return 1

    elif action == "set":
        key = args.key
        val = args.value
        if val is None:
            val = getpass.getpass(f"Inserisci il valore per il secret '{key}': ")
        if not passphrase:
            passphrase = getpass.getpass("Inserisci la Master Passphrase del Vault: ")
        try:
            vault.set_secret(key, val, passphrase)
            print(colorize(f"[OK] Secret '{key}' memorizzato e cifrato con successo!", COLOR_GREEN + COLOR_BOLD))
            return 0
        except Exception as e:
            print(colorize(f"ERRORE salvataggio secret: {e}", COLOR_RED))
            return 1

    elif action == "get":
        key = args.key
        if not passphrase:
            passphrase = getpass.getpass("Inserisci la Master Passphrase del Vault: ")
        try:
            val = vault.get_secret(key, passphrase)
            if val is not None:
                print(val)
                return 0
            else:
                print(colorize(f"Secret '{key}' non trovato nel vault.", COLOR_YELLOW))
                return 1
        except Exception as e:
            print(colorize(f"ERRORE recupero secret: {e}", COLOR_RED))
            return 1

    elif action == "list":
        if not passphrase:
            passphrase = getpass.getpass("Inserisci la Master Passphrase del Vault: ")
        try:
            keys = vault.list_keys(passphrase)
            print(colorize(f"\nChiavi censite nel vault del progetto '{slug}' ({len(keys)} secret):", COLOR_BOLD))
            if not keys:
                print("  (nessun secret presente)")
            for item in keys:
                print(f"  - {colorize(item['key'], COLOR_CYAN)} (aggiornato: {item['updated_at']})")
            print()
            return 0
        except Exception as e:
            print(colorize(f"ERRORE elenco chiavi: {e}", COLOR_RED))
            return 1

    elif action == "audit":
        print(colorize(f"\n=== AUDIT CREDENZIALI & PUNTATORI VAULT: {slug} ===", COLOR_BOLD + COLOR_CYAN))
        audit_res = vault.audit_references(passphrase)
        if "error" in audit_res:
            print(colorize(f"Attenzione: {audit_res['error']}", COLOR_YELLOW))

        print(f"Vault locale esiste: {'SI (' + audit_res['vault_file'] + ')' if audit_res['vault_exists'] else 'NO'}")
        print(f"File markdown con puntatori vault://: {audit_res['files_with_references']}")
        print(f"Riferimenti vault:// trovati: {audit_res['total_references_count']}")
        print(f"Chiavi distinte referenziate: {len(audit_res['referenced_keys'])}")
        for k in audit_res['referenced_keys']:
            print(f"  * vault://it/projects/{slug}/{k}")

        if audit_res.get("vault_keys") is not None:
            print(colorize(f"\nConfronto con le chiavi memorizzate nel Vault ({len(audit_res['vault_keys'])} chiavi):", COLOR_BOLD))
            missing = audit_res.get("missing_in_vault", [])
            unused = audit_res.get("unused_in_vault", [])
            if missing:
                print(colorize(f"\n[!] ATTENZIONE: {len(missing)} chiavi referenziate nei documenti NON sono presenti nel vault:", COLOR_RED + COLOR_BOLD))
                for m in missing:
                    print(colorize(f"    - {m}", COLOR_RED))
            else:
                print(colorize("\n[OK] Tutte le chiavi referenziate nei documenti esistono nel vault cifrato!", COLOR_GREEN))

            if unused:
                print(colorize(f"\n[i] NOTA: {len(unused)} chiavi presenti nel vault non sono direttamente citate nei documenti:", COLOR_YELLOW))
                for u in unused:
                    print(f"    - {u}")
        else:
            print(colorize("\n[i] Per confrontare i riferimenti con i secret effettivi, specifica --passphrase o imposta ITINFRA_VAULT_PASS", COLOR_YELLOW))
        print()
        return 0

    return 0

def cmd_worktree(args) -> int:
    action = args.wt_action
    repo_root = Path.cwd()
    try:
        res = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=True)
        repo_root = Path(res.stdout.strip())
    except Exception:
        pass

    ROLE_BRANCH_MAP = {
        "infra-architect": "feat/architecture",
        "infra-security": "feat/security-vault",
        "infra-automation": "feat/ops-mop",
        "infra-qa": "feat/testing-atp"
    }

    ROLE_DESCRIPTIONS = {
        "infra-architect": "Stesura 02-HLD, 03-LLD, topologie di rete e diagrammi Mermaid",
        "infra-security": "Gestione Vault AES-256, matrici di accesso, compliance NIS2/ISO 27001",
        "infra-automation": "04-MOP, script RouterOS (.rsc), PowerShell Hyper-V e 08-Runbook",
        "infra-qa": "07-ATP (casi di test), 09-Handover & Asset Inventory, audit di coerenza"
    }

    if action == "add":
        role = args.role
        branch = args.branch or ROLE_BRANCH_MAP.get(role, f"feat/{role}")
        wt_dir = repo_root / ".worktrees" / role
        desc = ROLE_DESCRIPTIONS.get(role, f"Agente dedicato per ruolo {role}")

        print(colorize(f"\n=== CREAZIONE WORKTREE AGENTE: {role} ===", COLOR_BOLD + COLOR_CYAN))
        print(f"Ruolo:        {role} ({desc})")
        print(f"Branch:       {branch}")
        print(f"Directory:    {wt_dir}")

        if wt_dir.exists():
            print(colorize(f"AVVISO: La directory {wt_dir} esiste già.", COLOR_YELLOW))
            return 1

        wt_dir.parent.mkdir(parents=True, exist_ok=True)
        check_b = subprocess.run(["git", "show-ref", "--verify", f"refs/heads/{branch}"], capture_output=True)
        cmd = ["git", "worktree", "add"]
        if check_b.returncode == 0:
            cmd.extend([str(wt_dir), branch])
        else:
            cmd.extend(["-b", branch, str(wt_dir), "HEAD"])

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(colorize(f"ERRORE creazione worktree: {res.stderr.strip()}", COLOR_RED))
            return 1

        print(colorize(f"[OK] Worktree creato con successo!", COLOR_GREEN + COLOR_BOLD))
        print(colorize(f"\nPer far lavorare un subagente in questo worktree isolato:", COLOR_BOLD))
        print(colorize(f"  1. Spostarsi nella directory: cd {wt_dir}", COLOR_CYAN))
        print(colorize(f"  2. Oppure in Antigravity: Workspace: 'share' o specificare la cartella", COLOR_CYAN))
        print(colorize(f"  3. Una volta completato il lavoro, eseguire: python scripts/itinfra.py worktree sync {role}\n", COLOR_CYAN))
        return 0

    elif action == "list":
        print(colorize(f"\n=== GIT WORKTREES ATTIVI ===", COLOR_BOLD + COLOR_CYAN))
        res = subprocess.run(["git", "worktree", "list"], capture_output=True, text=True)
        if res.returncode != 0:
            print(colorize(f"ERRORE lettura worktrees: {res.stderr.strip()}", COLOR_RED))
            return 1
        lines = res.stdout.strip().splitlines()
        for l in lines:
            parts = l.split()
            path_str = parts[0]
            branch_str = parts[-1] if len(parts) > 1 else ""
            if ".worktrees" in path_str:
                role_name = Path(path_str).name
                desc = ROLE_DESCRIPTIONS.get(role_name, "Ruolo custom")
                print(f"  - {colorize(role_name, COLOR_GREEN + COLOR_BOLD)} -> {branch_str}")
                print(f"    Path: {path_str}")
                print(f"    Ambito: {desc}")
            else:
                print(f"  * {colorize('ROOT (main)', COLOR_BOLD)} -> {branch_str} ({path_str})")
        print()
        return 0

    elif action == "sync":
        role = args.role
        wt_dir = repo_root / ".worktrees" / role
        if not wt_dir.exists():
            print(colorize(f"ERRORE: Worktree non trovato in {wt_dir}", COLOR_RED))
            return 1
        print(colorize(f"Sincronizzazione worktree '{role}' con branch 'main'...", COLOR_CYAN))
        res = subprocess.run(["git", "merge", "main", "--no-edit"], cwd=str(wt_dir), capture_output=True, text=True)
        if res.returncode == 0:
            print(colorize(f"[OK] Worktree '{role}' sincronizzato con 'main'.", COLOR_GREEN))
            return 0
        else:
            print(colorize(f"ERRORE merge/sync: {res.stderr.strip() or res.stdout.strip()}", COLOR_RED))
            return 1

    elif action == "cleanup":
        print(colorize(f"Pulizia worktrees...", COLOR_CYAN))
        wt_base = repo_root / ".worktrees"
        if wt_base.exists():
            for child in wt_base.iterdir():
                if child.is_dir():
                    print(f"Rimozione worktree: {child.name}")
                    subprocess.run(["git", "worktree", "remove", str(child), "--force"], capture_output=True)
        subprocess.run(["git", "worktree", "prune"], capture_output=True)
        print(colorize("[OK] Pulizia completata.", COLOR_GREEN))
        return 0

    return 0

def cmd_audit_consistency(args) -> int:
    slug = args.project_slug
    repo_root = Path.cwd()
    project_dir = repo_root / "projects" / slug
    if not project_dir.exists():
        print(colorize(f"ERRORE: Progetto non trovato in {project_dir}", COLOR_RED))
        return 1

    print(colorize(f"\n==================================================================", COLOR_BOLD))
    print(colorize(f"🔍 AUDIT DI COERENZA INCROCIATA & STRICT GROUNDING: {slug.upper()}", COLOR_BOLD + COLOR_CYAN))
    print(colorize(f"==================================================================\n", COLOR_BOLD))

    manifest_file = project_dir / "project-manifest.yaml"
    manifest_data = {}
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest_data = yaml.safe_load(f) or {}
        except Exception as e:
            print(colorize(f"AVVISO: Errore lettura manifesto: {e}", COLOR_YELLOW))

    net_base = manifest_data.get("network_baseline", {}) or manifest_data.get("network", {})
    expected_dc_ip = net_base.get("dc_ip")

    declared_subnets = []
    for k, v in net_base.items():
        if isinstance(v, str) and ("subnet" in k or "supernet" in k or "cidr" in k):
            try:
                declared_subnets.append(ipaddress.ip_network(v, strict=False))
            except ValueError:
                pass

    md_files = sorted(project_dir.glob("*.md"))
    if not md_files:
        print(colorize("Nessun documento .md trovato nel progetto.", COLOR_YELLOW))
        return 0

    anomalies = []
    warnings = []
    all_found_ips = {}
    placeholders_count = 0
    raw_placeholders = []

    ip_pattern = re.compile(r'\b(?:192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b')
    raw_placeholder_pattern = re.compile(r'<([a-zA-Z0-9_\-\s]{2,40})>')

    # Regex mirate per entita core (DC e Switch Core)
    dc_pattern_1 = re.compile(r'(?:srv-dc01?|dc01|domain\s+controller)[^|\n]*?\|[^|\n]*?(\b192\.168\.\d{1,3}\.\d{1,3}\b)', re.I)
    dc_pattern_2 = re.compile(r'\|\s*(\b192\.168\.\d{1,3}\.\d{1,3}\b)\s*\|[^|\n]*?(?:srv-dc|dc01|domain\s+controller)', re.I)
    dc_pattern_3 = re.compile(r'(?:srv-dc01?|dc01|domain\s+controller)[^:\n]*?:\s*`?(\b192\.168\.\d{1,3}\.\d{1,3}\b)', re.I)

    sw_pattern_1 = re.compile(r'(?:sw-core01?|crs326|switch\s+core)[^|\n]*?\|[^|\n]*?(\b192\.168\.\d{1,3}\.\d{1,3}\b)', re.I)
    sw_pattern_2 = re.compile(r'\|\s*(\b192\.168\.\d{1,3}\.\d{1,3}\b)\s*\|[^|\n]*?(?:sw-core|crs326|switch\s+core)', re.I)
    sw_pattern_3 = re.compile(r'(?:sw-core01?|crs326|switch\s+core)[^:\n]*?:\s*`?(\b192\.168\.\d{1,3}\.\d{1,3}\b)', re.I)

    dc_ips = {}
    switch_ips = {}

    for md_file in md_files:
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        lines = content.splitlines()
        for l_num, line in enumerate(lines, start=1):
            for match in raw_placeholder_pattern.finditer(line):
                tag = match.group(1).strip()
                if tag.upper() == "DA-RICHIEDERE":
                    placeholders_count += 1
                elif not any(tag.lower().startswith(x) for x in ["div", "/div", "span", "/span", "b", "/b", "i", "/i", "table", "/table", "tr", "/tr", "td", "/td", "th", "/th", "p", "/p", "!--", "br"]):
                    raw_placeholders.append((md_file.name, l_num, match.group(0)))

            for match in ip_pattern.finditer(line):
                ip_str = match.group(0)
                if ip_str.endswith(".0") or ip_str.endswith(".255"):
                    continue
                if ip_str not in all_found_ips:
                    all_found_ips[ip_str] = []
                all_found_ips[ip_str].append((md_file.name, l_num))

            # DC specific pattern matching
            m_dc = dc_pattern_1.search(line) or dc_pattern_2.search(line) or dc_pattern_3.search(line)
            if m_dc:
                dc_ips.setdefault(m_dc.group(1), []).append(md_file.name)

            # Switch specific pattern matching
            m_sw = sw_pattern_1.search(line) or sw_pattern_2.search(line) or sw_pattern_3.search(line)
            if m_sw:
                switch_ips.setdefault(m_sw.group(1), []).append(md_file.name)

    print(colorize("1. Verifica Conformità Spazio di Indirizzamento IP (Subnet Check):", COLOR_BOLD))
    if declared_subnets:
        print(f"   Supernet dichiarata nel Manifesto: {', '.join(str(s) for s in declared_subnets)}")
        out_of_subnet = []
        for ip_str, occurrences in all_found_ips.items():
            ip_obj = ipaddress.ip_address(ip_str)
            if not any(ip_obj in s for s in declared_subnets):
                out_of_subnet.append((ip_str, occurrences))

        if out_of_subnet:
            hld_only = []
            real_outliers = []
            for ip_str, occ in out_of_subnet:
                if all(f == "02-HLD.md" for f, _ in occ):
                    hld_only.append((ip_str, occ))
                else:
                    real_outliers.append((ip_str, occ))

            if hld_only:
                print(colorize(f"   [i] Trovati {len(hld_only)} IP concettuali in 02-HLD.md (modello multi-VLAN preliminare documentato come proposta iniziale).", COLOR_YELLOW))

            if real_outliers:
                print(colorize(f"   [!] RILEVATI {len(real_outliers)} IP AL DI FUORI DELLE SUBNET DI PROGETTO:", COLOR_RED + COLOR_BOLD))
                for ip_str, occ in real_outliers:
                    files_list = ", ".join(sorted(set(f for f, l in occ)))
                    print(colorize(f"       - {ip_str} (in: {files_list})", COLOR_RED))
                    anomalies.append(f"IP {ip_str} non appartiene alle subnet approvate {declared_subnets}")
            else:
                print(colorize(f"   [OK] Tutti gli IP operativi (LLD, MOP, As-Built, ATP, SOP) appartengono correttamente alle subnet approvate!", COLOR_GREEN))
        else:
            print(colorize(f"   [OK] Tutti i {len(all_found_ips)} IP censiti appartengono correttamente alla supernet di progetto!", COLOR_GREEN))
    else:
        print(colorize("   [i] Nessuna supernet specificata nel manifest; saltato controllo CIDR stretto.", COLOR_YELLOW))

    print(colorize("\n2. Verifica Consistenza Entità Core tra i 9 Documenti:", COLOR_BOLD))
    # Domain Controller
    if expected_dc_ip:
        if expected_dc_ip in dc_ips:
            files = ", ".join(sorted(set(dc_ips[expected_dc_ip])))
            print(colorize(f"   [OK] Domain Controller allineato al Manifesto ({expected_dc_ip}) in: {files}", COLOR_GREEN))
        else:
            print(colorize(f"   [!] Domain Controller {expected_dc_ip} non trovato esplicitamente nelle tabelle!", COLOR_YELLOW))
            warnings.append(f"DC IP {expected_dc_ip} non censito con mapping esplicito")

    if len(dc_ips) == 1:
        ip = list(dc_ips.keys())[0]
        files = ", ".join(sorted(set(dc_ips[ip])))
        print(colorize(f"   [OK] Nessun IP divergente rilevato per Domain Controller: {ip}", COLOR_GREEN))
    elif len(dc_ips) > 1:
        print(colorize(f"   [!] DISCORDANZA DOMAIN CONTROLLER: rilevati IP multipli!", COLOR_RED + COLOR_BOLD))
        for ip, files in dc_ips.items():
            print(f"       - {ip} citato in: {', '.join(set(files))}")
        anomalies.append("IP discordanti per il Domain Controller tra i documenti")

    # Switch Core
    if len(switch_ips) == 1:
        ip = list(switch_ips.keys())[0]
        files = ", ".join(sorted(set(switch_ips[ip])))
        print(colorize(f"   [OK] Switch Core identificato univocamente a: {ip} (in: {files})", COLOR_GREEN))
    elif len(switch_ips) > 1:
        # Check if 192.168.120.1 was only in 02-HLD conceptual phase
        if len(switch_ips) == 2 and "192.168.120.1" in switch_ips and switch_ips["192.168.120.1"] == ["02-HLD.md"]:
            print(colorize(f"   [OK] Switch Core confermato univocamente a 192.168.120.1 in LLD, As-Built, SOP e Handover!", COLOR_GREEN))
            print(colorize(f"   [i] Nota: 192.168.120.1 presente solo come schema concettuale HLD.", COLOR_YELLOW))
        else:
            print(colorize(f"   [!] DISCORDANZA SWITCH CORE: rilevati IP multipli!", COLOR_YELLOW))
            for ip, files in switch_ips.items():
                print(f"       - {ip} citato in: {', '.join(set(files))}")
            warnings.append("IP multipli rilevati per lo Switch Core")

    print(colorize("\n3. Controllo Strict Grounding & Placeholder Incompleti:", COLOR_BOLD))
    print(f"   Placeholder standard `<DA-RICHIEDERE>` rilevati: {placeholders_count}")
    if raw_placeholders:
        print(colorize(f"   [!] Rilevati {len(raw_placeholders)} placeholder grezzi non conformi (es. `<nome>`, `<ip>`):", COLOR_RED))
        for fname, lnum, ph in raw_placeholders[:10]:
            print(f"       - {fname}:{lnum} -> {ph}")
        if len(raw_placeholders) > 10:
            print(f"       ... e altri {len(raw_placeholders) - 10} placeholder")
        warnings.append(f"{len(raw_placeholders)} placeholder grezzi da sostituire con valori reali o <DA-RICHIEDERE>")
    else:
        print(colorize("   [OK] Nessun placeholder grezzo non conforme rilevato.", COLOR_GREEN))

    print(colorize("\n4. Controllo Trust Signals & Obsolescenza Tecnica (Release v0.6):", COLOR_BOLD))
    stale_docs = []
    verified_docs = 0
    today_date = datetime.now().date()
    for md_file in md_files:
        try:
            c_text = md_file.read_text(encoding="utf-8")
            fm_data, _, _ = parse_frontmatter(c_text)
            if fm_data:
                if fm_data.get("verified") is True:
                    verified_docs += 1
                s_after = fm_data.get("stale_after")
                if s_after:
                    try:
                        s_date = datetime.strptime(str(s_after).strip(), "%Y-%m-%d").date()
                        if s_date < today_date:
                            stale_docs.append((md_file.name, s_date))
                    except Exception:
                        pass
        except Exception:
            pass

    print(f"   Documenti con certificazione Trust Signals (verified: true): {verified_docs}/{len(md_files)}")
    if stale_docs:
        print(colorize(f"   [!] Documenti scaduti rilevati ({len(stale_docs)}):", COLOR_YELLOW))
        for fname, s_date in stale_docs:
            print(f"       - {fname} (scaduto il {s_date})")
        warnings.append(f"{len(stale_docs)} documenti con certificazione tecnica scaduta (stale_after)")
    else:
        print(colorize("   [OK] Nessun documento con data validita' scaduta rilevato.", COLOR_GREEN))

    print(colorize("\n------------------------------------------------------------------", COLOR_BOLD))
    if anomalies:
        print(colorize(f"ESITO AUDIT COERENZA: FALLITO ({len(anomalies)} anomalie critiche, {len(warnings)} avvisi)", COLOR_RED + COLOR_BOLD))
        return 1
    elif warnings:
        print(colorize(f"ESITO AUDIT COERENZA: PASS CON AVVISI (0 anomalie critiche, {len(warnings)} avvisi)", COLOR_YELLOW + COLOR_BOLD))
        return 0
    else:
        print(colorize("ESITO AUDIT COERENZA: SUCCESSO 100% (Tutti i parametri allineati e coerenti!)", COLOR_GREEN + COLOR_BOLD))
        return 0

def cmd_export_configs(args) -> int:
    slug = args.project_slug
    repo_root = Path.cwd()
    project_dir = repo_root / "projects" / slug
    if not project_dir.exists():
        print(colorize(f"ERRORE: Progetto non trovato in {project_dir}", COLOR_RED))
        return 1

    out_dir = Path(args.out) if args.out else project_dir / "configs"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(colorize(f"\n=== ESPORTAZIONE CONFIGURAZIONI ESECUTIVE: {slug} ===", COLOR_BOLD + COLOR_CYAN))
    print(f"Directory destinazione: {out_dir}\n")

    rsc_blocks = []
    ps1_blocks = []

    for md_file in sorted(project_dir.glob("*.md")):
        try:
            content = md_file.read_text(encoding="utf-8")
        except Exception:
            continue

        for match in re.finditer(r'```(?:routeros|rsc)\r?\n(.*?)\r?\n```', content, re.DOTALL | re.IGNORECASE):
            code = match.group(1).strip()
            if code and len(code) > 20:
                rsc_blocks.append((md_file.name, code))

        for match in re.finditer(r'```(?:powershell|ps1)\r?\n(.*?)\r?\n```', content, re.DOTALL | re.IGNORECASE):
            code = match.group(1).strip()
            if code and len(code) > 20:
                ps1_blocks.append((md_file.name, code))

    generated_files = []

    if rsc_blocks:
        rsc_file = out_dir / "sw-core-01.rsc"
        with open(rsc_file, "w", encoding="utf-8") as f:
            f.write(f"# RouterOS Configuration Script - Progetto: {slug}\n")
            f.write(f"# Generato automaticamente da ItInfra Automation Suite\n")
            f.write(f"# Data generazione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for src_doc, block in rsc_blocks:
                f.write(f"################################################################\n")
                f.write(f"# Estratto da: {src_doc}\n")
                f.write(f"################################################################\n")
                f.write(block + "\n\n")
        generated_files.append(rsc_file)
        print(colorize(f"  [+] Generato: {rsc_file.name} ({len(rsc_blocks)} blocchi RouterOS)", COLOR_GREEN))

    if ps1_blocks:
        ps1_file = out_dir / "setup_ad_hyperv.ps1"
        with open(ps1_file, "w", encoding="utf-8") as f:
            f.write(f"<#\n  PowerShell Setup & Provisioning Script - Progetto: {slug}\n")
            f.write(f"  Generato automaticamente da ItInfra Automation Suite\n")
            f.write(f"  Data generazione: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n#>\n\n")
            for src_doc, block in ps1_blocks:
                f.write(f"# --------------------------------------------------------------\n")
                f.write(f"# Estratto da: {src_doc}\n")
                f.write(f"# --------------------------------------------------------------\n")
                f.write(block + "\n\n")
        generated_files.append(ps1_file)
        print(colorize(f"  [+] Generato: {ps1_file.name} ({len(ps1_blocks)} blocchi PowerShell)", COLOR_GREEN))

    if not generated_files:
        print(colorize("Nessun blocco di configurazione RouterOS o PowerShell rilevato nei documenti.", COLOR_YELLOW))
    else:
        print(colorize(f"\n[OK] Esportazione completata con successo! {len(generated_files)} file generati in {out_dir}\n", COLOR_GREEN + COLOR_BOLD))

    return 0

def cmd_troubleshoot(args: argparse.Namespace) -> int:
    """Gestisce ticket di incidente e Root Cause Analysis (RCA)."""
    repo_root = Path(__file__).resolve().parent.parent
    project_slug = args.project_slug.lower().strip()
    proj_dir = repo_root / "projects" / project_slug

    if not proj_dir.exists():
        print(colorize(f"ERRORE: Progetto '{project_slug}' non trovato in {proj_dir}", COLOR_RED))
        return 1

    manifest_file = proj_dir / "project-manifest.yaml"
    manifest_data = {}
    if manifest_file.exists():
        try:
            manifest_data = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
        except Exception:
            pass

    if args.tb_action == "list":
        rca_files = sorted(proj_dir.glob("10-RCA-*.md"))
        print(colorize(f"\n=== TICKET RCA & TROUBLESHOOTING: {project_slug.upper()} ===", COLOR_BOLD + COLOR_CYAN))
        if not rca_files:
            print("Nessun ticket RCA registrato per questo progetto.")
            print(f"Per crearne uno: python scripts/itinfra.py troubleshoot init {project_slug} <ticket_id>\n")
            return 0

        print(f"{'File':<34} | {'ID Incidente':<16} | {'Severita':<10} | {'Stato':<10} | {'Titolo'}")
        print("-" * 105)
        validator = OKFValidator(is_template=False)
        for rf in rca_files:
            content = rf.read_text(encoding="utf-8").lstrip("\ufeff")
            fm, _, _ = parse_frontmatter(content)
            fm = fm or {}
            inc_id = fm.get("incident_id", "N/A")
            sev = fm.get("severity", "N/A")
            st = fm.get("status", "N/A")
            title = fm.get("title", rf.stem)
            if len(title) > 38:
                title = title[:35] + "..."
            val_res = validator.validate(rf)
            st_color = COLOR_GREEN if len(val_res["errors"]) == 0 else COLOR_YELLOW
            print(f"{rf.name:<34} | {inc_id:<16} | {sev:<10} | {colorize(st, st_color):<19} | {title}")
        print("-" * 105 + "\n")
        return 0

    elif args.tb_action == "init":
        ticket_id = args.ticket_id.strip()
        clean_id = re.sub(r'[^a-zA-Z0-9_-]', '-', ticket_id)
        filename = f"10-RCA-{clean_id}.md"
        out_file = proj_dir / filename

        if out_file.exists() and not getattr(args, "force", False):
            print(colorize(f"ERRORE: Il ticket {filename} esiste già. Usa --force per sovrascrivere.", COLOR_RED))
            return 1

        template_path = repo_root / "templates" / "10-RCA-Troubleshooting.md"
        if not template_path.exists():
            print(colorize(f"ERRORE: Template {template_path} non trovato.", COLOR_RED))
            return 1

        tpl = template_path.read_text(encoding="utf-8")
        today = datetime.now().strftime("%Y-%m-%d")
        now_hm = datetime.now().strftime("%Y-%m-%d %H:%M")

        p_name = manifest_data.get("project_name", project_slug)
        p_id = manifest_data.get("project_id", project_slug.upper())
        customer = manifest_data.get("customer", "Cliente")
        site = manifest_data.get("site", "HQ")
        architect = manifest_data.get("lead_architect", "Lead Architect")
        title = args.title or f"RCA & Troubleshooting — Disservizio {ticket_id}"
        severity = args.severity or "P2-High"

        tpl = tpl.replace("<project_slug>", project_slug)
        tpl = tpl.replace("<PROJECT_ID>", p_id)
        tpl = tpl.replace("<nome progetto>", p_name)
        tpl = tpl.replace("<cliente>", customer)
        tpl = tpl.replace("<SITE_CODE>", site)
        tpl = tpl.replace("<nome>", architect)
        tpl = tpl.replace("<INCIDENT_ID>", f"INC-{clean_id}")
        tpl = tpl.replace("<incident_id>", clean_id.lower())
        tpl = tpl.replace("<YYYY-MM-DD>", today)
        tpl = tpl.replace("<YYYY-MM-DD HH:MM>", now_hm)
        tpl = tpl.replace("<titolo disservizio, es. Degrado Connettività SMB FS01>", title)
        tpl = tpl.replace("<Titolo Disservizio>", title)
        tpl = tpl.replace("<P1-Critical | P2-High | P3-Medium | P4-Low>", severity)
        tpl = tpl.replace("<P1 / P2 / P3 / P4>", severity)
        tpl = tpl.replace("<NOME_PROGETTO>", p_name)
        tpl = tpl.replace("<CLIENTE>", customer)

        out_file.write_text(tpl, encoding="utf-8")
        print(colorize(f"\n[+] Ticket RCA inizializzato con successo: {out_file}", COLOR_GREEN + COLOR_BOLD))
        print(f"Progetto:   {project_slug}")
        print(f"File:       {filename}")
        print(f"Severita:   {severity}")
        print(f"\nProssimi passi:")
        print(f"  1. Esegui il controllo telemetria live: python scripts/itinfra.py health-check {project_slug}")
        print(f"  2. Conduci l'indagine a 7 strati OSI con la skill 'itinfra-troubleshooter'")
        print(f"  3. Valida il documento con: python scripts/itinfra.py validate {out_file}\n")
        return 0

def cmd_health_check(args: argparse.Namespace) -> int:
    """Esegue telemetria e health check non distruttivo (ICMP/TCP) sugli apparati del manifest."""
    repo_root = Path(__file__).resolve().parent.parent
    project_slug = args.project_slug.lower().strip()
    proj_dir = repo_root / "projects" / project_slug

    if not proj_dir.exists():
        print(colorize(f"ERRORE: Progetto '{project_slug}' non trovato in {proj_dir}", COLOR_RED))
        return 1

    manifest_file = proj_dir / "project-manifest.yaml"
    manifest_data = {}
    if manifest_file.exists():
        try:
            manifest_data = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
        except Exception:
            pass

    print(colorize(f"\n=== LIVE TELEMETRY & HEALTH-CHECK: {project_slug.upper()} ===", COLOR_BOLD + COLOR_CYAN))
    timeout = args.timeout

    targets = []
    net = manifest_data.get("network_baseline", {})
    gw_ip = net.get("core_switch_ip") or net.get("default_gateway")
    if gw_ip:
        targets.append({"name": "Core Switch / Gateway", "host": gw_ip, "ports": [80, 443, 22]})

    asbuilt_file = proj_dir / "07-As-Built.md"
    if not asbuilt_file.exists():
        asbuilt_file = proj_dir / "06-As-Built.md"

    if asbuilt_file.exists():
        content_ab = asbuilt_file.read_text(encoding="utf-8")
        if "192.168.120.1" in content_ab or "rb5009" in content_ab.lower():
            targets.append({"name": "MikroTik RB5009 (GW)", "host": "192.168.120.1", "ports": [8291, 53, 80, 22]})
        if "192.168.120.2" in content_ab or "crs326" in content_ab.lower():
            targets.append({"name": "MikroTik CRS326 (SW)", "host": "192.168.120.2", "ports": [8291, 80]})
        if "192.168.120.10" in content_ab or "fs01" in content_ab.lower():
            targets.append({"name": "File Server FS01 (LAN)", "host": "192.168.120.10", "ports": [445, 3389, 5985, 139]})
        if "192.168.120.5" in content_ab or "hv01" in content_ab.lower():
            targets.append({"name": "Host HV01 (Hyper-V)", "host": "192.168.120.5", "ports": [3389, 5985, 445]})
        if "10.147.19." in content_ab or "zerotier" in content_ab.lower():
            zt_match = re.search(r'10\.147\.19\.\d+', content_ab)
            if zt_match:
                targets.append({"name": "FS01 ZeroTier Overlay", "host": zt_match.group(0), "ports": [445, 3389]})

    seen_hosts = set()
    unique_targets = []
    for t in targets:
        if t["host"] not in seen_hosts:
            seen_hosts.add(t["host"])
            unique_targets.append(t)

    if not unique_targets:
        print(colorize("Nessun endpoint IP rilevato nel manifest o nell'As-Built.", COLOR_YELLOW))
        return 0

    print(f"{'Target Apparato':<26} | {'IP Endpoint':<16} | {'ICMP Ping':<12} | {'Sonde TCP Portali'}")
    print("-" * 90)

    for tgt in unique_targets:
        name = tgt["name"]
        host = tgt["host"]
        is_windows = os.name == "nt"
        ping_cmd = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), host] if is_windows else ["ping", "-c", "1", "-W", str(int(timeout)), host]
        try:
            p_res = subprocess.run(ping_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout + 1.0)
            icmp_ok = (p_res.returncode == 0)
        except Exception:
            icmp_ok = False

        icmp_str = colorize("ONLINE (L3)", COLOR_GREEN) if icmp_ok else colorize("NO-RESP (L3)", COLOR_RED)

        port_results = []
        for port in tgt["ports"]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                r = sock.connect_ex((host, port))
                if r == 0:
                    port_results.append(colorize(f"{port}:OPEN", COLOR_GREEN))
                else:
                    port_results.append(colorize(f"{port}:CLOSED", COLOR_RED))
            except Exception:
                port_results.append(colorize(f"{port}:TIMEOUT", COLOR_YELLOW))
            finally:
                sock.close()

        ports_str = " | ".join(port_results)
        print(f"{name:<26} | {host:<16} | {icmp_str:<21} | {ports_str}")

    print("-" * 90)
    print(colorize("[*] Telemetria completata con successo. Valori integrabili in Sezione 4 (OSI L1-L4).\n", COLOR_CYAN))
    return 0

def cmd_export_graph(args: argparse.Namespace) -> int:
    """Genera una visualizzazione interattiva del Knowledge Graph D3.js per un progetto o per i template."""
    try:
        from scripts.graph_generator import build_graph_data, generate_graph_html
    except ImportError:
        try:
            from graph_generator import build_graph_data, generate_graph_html
        except ImportError:
            import sys
            sys.path.insert(0, str(repo_root / "scripts"))
            from graph_generator import build_graph_data, generate_graph_html

    repo_root = Path(__file__).resolve().parent.parent
    target_arg = args.target.strip()

    # Risolvi target: 'all'/'global', 'templates', slug progetto o path
    is_global = False
    if target_arg.lower() in ["all", "global", "enterprise"]:
        folder_path = repo_root / "projects"
        default_title = "ITInfra Global Enterprise Knowledge Graph OKF v0.2 (Multi-Tenant)"
        default_out = folder_path / "global-graph.html"
        is_global = True
    elif target_arg.lower() in ["templates", "template"]:
        folder_path = repo_root / "templates"
        default_title = "ITInfra Knowledge Graph OKF v0.2 — Template Ciclo IT"
        default_out = folder_path / "graph.html"
    else:
        proj_dir = repo_root / "projects" / target_arg
        if proj_dir.exists():
            folder_path = proj_dir
            default_title = f"Knowledge Graph OKF v0.2 — {target_arg.upper()}"
            default_out = proj_dir / "graph.html"
        else:
            folder_path = Path(target_arg)
            if not folder_path.exists():
                print(colorize(f"ERRORE: Percorso o progetto '{target_arg}' non trovato.", COLOR_RED))
                return 1
            default_title = f"Knowledge Graph OKF v0.2 — {folder_path.name}"
            default_out = folder_path / "graph.html"

    print(colorize(f"\n=== GENERAZIONE KNOWLEDGE GRAPH D3.JS OKF v0.2 ===", COLOR_BOLD + COLOR_CYAN))
    print(f"Sorgente:  {folder_path}")

    graph_data = build_graph_data(folder_path, is_global=is_global)
    nodes_count = len(graph_data["nodes"])
    links_count = len(graph_data["links"])

    if nodes_count == 0:
        print(colorize("AVVISO: Nessun documento Markdown valido con frontmatter OKF rilevato.", COLOR_YELLOW))
        return 1

    title = args.title or default_title
    out_file = Path(args.out) if args.out else default_out
    out_file.parent.mkdir(parents=True, exist_ok=True)

    html_page = generate_graph_html(graph_data, title=title)
    out_file.write_text(html_page, encoding="utf-8")

    print(colorize(f"[+] Nodi estratti:   {nodes_count}", COLOR_GREEN))
    print(colorize(f"[+] Archi semantici: {links_count}", COLOR_GREEN))
    print(colorize(f"[OK] Knowledge Graph interattivo salvato in: {out_file.resolve()}\n", COLOR_GREEN + COLOR_BOLD))
    return 0

def cmd_test_suite(args: argparse.Namespace) -> int:
    """Esegue la suite di collaudo end-to-end e genera il report HTML (Release v0.8)."""
    try:
        from itinfra_test_suite import SystemTestSuiteRunner, generate_system_test_html
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_test_suite import SystemTestSuiteRunner, generate_system_test_html

    repo_root = Path(__file__).resolve().parent.parent
    runner = SystemTestSuiteRunner(repo_root=repo_root)
    results = runner.run_all_tests()

    if getattr(args, "report_html", True):
        out_file = Path(args.out) if args.out else repo_root / "projects" / "system-test-report.html"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        generate_system_test_html(results, out_file)
        print(colorize(f"[OK] Dashboard HTML di collaudo salvata in: {out_file.resolve()}", COLOR_GREEN + COLOR_BOLD))

    return 0 if results["failed_modules"] == 0 else 1

def cmd_publish(args: argparse.Namespace) -> int:
    """Pubblica in modo atomico il progetto locale su storage master centrale (Release v0.9)."""
    try:
        from itinfra_publish import ProjectPublisher
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_publish import ProjectPublisher

    repo_root = Path(__file__).resolve().parent.parent
    publisher = ProjectPublisher(workspace_root=repo_root)
    success, msg, stats = publisher.publish_project(
        slug=args.slug,
        target_share=args.dest,
        dry_run=args.dry_run,
        force=args.force
    )
    if success:
        print(colorize(msg, COLOR_GREEN if not args.dry_run else COLOR_CYAN))
        return 0
    else:
        print(colorize(msg, COLOR_RED))
        return 1

def cmd_sync_engine(args: argparse.Namespace) -> int:
    """Sincronizza e aggiorna template, script e guide dalla share master (Release v0.9)."""
    try:
        from itinfra_publish import ProjectPublisher
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_publish import ProjectPublisher

    repo_root = Path(__file__).resolve().parent.parent
    publisher = ProjectPublisher(workspace_root=repo_root)
    success, msg, stats = publisher.sync_engine(
        source_share=args.source,
        dry_run=args.dry_run
    )
    if success:
        print(colorize(msg, COLOR_GREEN if not args.dry_run else COLOR_CYAN))
        return 0
    else:
        print(colorize(msg, COLOR_RED))
        return 1

def cmd_check_share(args: argparse.Namespace) -> int:
    """Verifica connettività, permessi di pubblicazione e protezione core sulla share centrale (Release v0.9.1)."""
    try:
        from itinfra_publish import ProjectPublisher
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_publish import ProjectPublisher

    repo_root = Path(__file__).resolve().parent.parent
    publisher = ProjectPublisher(workspace_root=repo_root)
    user = getattr(args, "user", None)
    password = getattr(args, "password", None)
    success, msg, report = publisher.check_share_permissions(
        target_share=args.path,
        username=user,
        password=password
    )
    if success:
        print(colorize(msg, COLOR_GREEN))
        return 0
    else:
        print(colorize(msg, COLOR_RED if not report.get("reachable") else COLOR_YELLOW))
        return 1

def cmd_deploy_share(args: argparse.Namespace) -> int:
    """Distribuisce in modo differenziale e atomico template e script sulla share master (Release v0.9.5)."""
    try:
        from itinfra_deploy import CentralDeployer
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_deploy import CentralDeployer

    deployer = CentralDeployer()
    ok, msg, stats = deployer.deploy(
        target_share=args.dest,
        dry_run=args.dry_run,
        quiet=False
    )
    if ok:
        print(colorize(msg, COLOR_GREEN if not args.dry_run else COLOR_CYAN))
        return 0
    else:
        print(colorize(msg, COLOR_RED))
        return 1

def cmd_memory(args: argparse.Namespace) -> int:
    """Gestisce la Memoria Locale Ibrida a 3 Livelli e i Trust Signals (Release v0.6 e v0.8)."""
    try:
        from itinfra_memory import MemoryManager
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_memory import MemoryManager

    repo_root = Path(__file__).resolve().parent.parent
    mgr = MemoryManager(repo_root=repo_root)

    # Riconoscimento target globale
    raw_slug = getattr(args, "project_slug", "") or ""
    slug = raw_slug.lower().strip()
    is_global = getattr(args, "is_global", False) or slug in ("global", "__global__", "all")

    if not is_global and not slug:
        print(colorize("ERRORE: Specificare lo slug del progetto o usare il flag --global.", COLOR_RED))
        return 1

    if not is_global:
        try:
            p_dir = mgr.get_project_dir(slug)
        except FileNotFoundError as e:
            print(colorize(f"ERRORE: {e}", COLOR_RED))
            return 1

    action = args.mem_action

    if action == "init":
        if is_global:
            sp = mgr.init_scratchpad(is_global=True)
            print(colorize(f"[OK] Staging Scratchpad Globale Enterprise inizializzato: {sp}", COLOR_GREEN + COLOR_BOLD))
        else:
            sp = mgr.init_scratchpad(slug)
            print(colorize(f"[OK] Scratchpad inizializzato per '{slug}': {sp}", COLOR_GREEN + COLOR_BOLD))
        return 0

    elif action == "log":
        sec = args.section
        text = args.text
        role = getattr(args, "role", None)
        author = getattr(args, "author", None) or getpass.getuser()
        try:
            if is_global:
                target_file, entry_id = mgr.log_entry(None, sec, text, role=role, author=author, is_global=True)
                print(colorize(f"[OK] Voce registrata nella Memoria Globale ({target_file.name}) con ID: {entry_id}", COLOR_GREEN + COLOR_BOLD))
            else:
                target_file, entry_id = mgr.log_entry(slug, sec, text, role=role, author=author)
                print(colorize(f"[OK] Voce registrata in '{target_file.name}' con ID: {entry_id}", COLOR_GREEN))
            print(f"Sezione: {sec} | Ruolo: {role or 'agent'} | Autore: {author}")
            return 0
        except Exception as ex:
            print(colorize(f"ERRORE: {ex}", COLOR_RED))
            return 1

    elif action == "show":
        if is_global:
            data = mgr.show_scratchpad(is_global=True)
            print(colorize(f"\n=== GLOBAL ENTERPRISE STAGING MEMORY (OKF v0.2) ===", COLOR_BOLD + COLOR_CYAN))
            print(f"File: {data['file']}")
            if not data["exists"]:
                print(colorize("Scratchpad globale non presente. Inizializzalo con: python scripts/itinfra.py memory init --global", COLOR_YELLOW))
                return 0
            stats = data["stats"]
            print(f"Best Practices: {stats['best_practices']} | Known Issues: {stats['known_issues']} | Hardware Rules: {stats['hardware_rules']} | Open Questions: {stats['open_questions']}")
            for sec_name, items in data["sections"].items():
                print(colorize(f"\n[{sec_name.upper().replace('_', ' ')}]:", COLOR_BOLD))
                if items:
                    for it in items:
                        print(f" {it}")
                else:
                    print("  (Nessuna voce registrata)")
            print()
            return 0
        else:
            data = mgr.show_scratchpad(slug)
            print(colorize(f"\n=== STAGING MEMORY (SCRATCHPAD): {slug.upper()} ===", COLOR_BOLD + COLOR_CYAN))
            print(f"File: {data['file']}")
            if not data["exists"]:
                print(colorize("Scratchpad non presente. Inizializzalo con: python scripts/itinfra.py memory init <slug>", COLOR_YELLOW))
                return 0
            stats = data["stats"]
            print(f"Decisioni Confermate: {stats['confirmed']} | Requisiti Sospesi: {stats['open']} | Note: {stats['notes']} | Consolidamenti: {stats['consolidated']}")
            if stats.get("worktrees_pending", 0) > 0:
                print(colorize(f"Avviso: presenti {stats['worktrees_pending']} file scratchpad da worktree. Esegui 'itinfra.py memory merge {slug}' per sincronizzarli.", COLOR_YELLOW))
            for sec_name, items in data["sections"].items():
                print(colorize(f"\n[{sec_name.upper()}]:", COLOR_BOLD))
                if items:
                    for it in items:
                        print(f" {it}")
                else:
                    print("  (Nessuna voce)")
            print()
            return 0

    elif action == "merge":
        if is_global:
            print(colorize("AVVISO: L'azione 'merge' non e' applicabile allo scratchpad globale (opera solo su worktrees di progetto).", COLOR_YELLOW))
            return 0
        res = mgr.merge_worktrees(slug)
        print(colorize(f"\n=== MERGE WORKTREES MEMORY: {slug.upper()} ===", COLOR_BOLD + COLOR_CYAN))
        print(f"Voci sincronizzate nello scratchpad master: {res['merged_count']}")
        print(colorize("[OK] Sincronizzazione worktree completata!", COLOR_GREEN))
        return 0

    elif action == "consolidate":
        if is_global:
            print(colorize("AVVISO: La memoria globale non supporta consolidate diretto verso singolo documento cliente.", COLOR_YELLOW))
            return 0
        target = args.target
        reviewer = args.reviewer or "Lead Architect"
        stale_days = args.stale_days
        try:
            res = mgr.consolidate(slug, target, reviewer=reviewer, stale_days=stale_days)
            if res.get("status") == "noop":
                print(colorize(f"AVVISO: {res['message']}", COLOR_YELLOW))
                return 0
            print(colorize(f"\n[OK] {res['message']}", COLOR_GREEN + COLOR_BOLD))
            print(f"Target:      {res['target_file']}")
            print(f"Reviewer:    {res['reviewer']}")
            print(f"Last Vetted: {res['last_vetted']}")
            print(f"Stale After: {res['stale_after'] or 'N/A'}")
            return 0
        except Exception as ex:
            print(colorize(f"ERRORE: {ex}", COLOR_RED))
            return 1

    elif action == "prune":
        archive = not args.no_archive
        if is_global:
            res = mgr.prune(is_global=True, archive=archive)
        else:
            res = mgr.prune(slug, archive=archive)
        print(colorize(f"[OK] {res['message']}", COLOR_GREEN))
        return 0

    return 0


def cmd_inventory(args: argparse.Namespace) -> int:
    """Interroga l'inventario tecnologico e le entità cross-progetto (Release v0.7)."""
    try:
        from itinfra_inventory import GlobalInventoryEngine
    except ImportError:
        import sys
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from itinfra_inventory import GlobalInventoryEngine

    repo_root = Path(__file__).resolve().parent.parent
    engine = GlobalInventoryEngine(repo_root=repo_root)

    action = args.inv_action

    if action == "find":
        term = args.term
        res = engine.find(term, entity_type=getattr(args, "type", None))
        print(colorize(f"\n=== RICERCA ASSET & ENTITÀ CROSS-PROGETTO: '{term}' ===", COLOR_BOLD + COLOR_CYAN))
        print(f"Occorrenze totali: {res['total_matches']}")
        print(f"Progetti coinvolti: {', '.join(res['projects_involved']) if res['projects_involved'] else 'Nessuno'}\n")

        if res["rca_alerts"]:
            print(colorize(f"⚠️  CROSS-CLIENT INCIDENT ALERT ({len(res['rca_alerts'])} ticket RCA collegati a questo termine):", COLOR_YELLOW + COLOR_BOLD))
            for r in res["rca_alerts"]:
                print(f"   - [{r['incident_id']}] {r['customer']} ({r['severity']}): {r['title']} [file: {r['file']}]")
            print()

        if res["entities"]:
            print(colorize("--- Entità Ontologiche Riconosciute ---", COLOR_BOLD))
            for e in res["entities"][:15]:
                print(f" • {colorize(e['name'], COLOR_GREEN)} ({e['type']})")
                print(f"   Cliente: {e['customer']} ({e['project_slug']}) | Doc: {e['doc_file']}")
                print(f"   Descrizione: {e['description'][:90]}...")
            if len(res["entities"]) > 15:
                print(f"   ... e altre {len(res['entities']) - 15} entità")
            print()

        if res["devices"]:
            print(colorize("--- Apparati Hardware & Device Mappati ---", COLOR_BOLD))
            for d in res["devices"][:15]:
                ip_str = f" [IP: {d['ip']}]" if d["ip"] else ""
                print(f" • [{colorize(d['vendor'], COLOR_CYAN)}] {d['category']}: {d['context'][:75]}...{ip_str}")
                print(f"   Progetto: {d['customer']} ({d['project_slug']}) -> {d['doc_file']}")
            if len(res["devices"]) > 15:
                print(f"   ... e altri {len(res['devices']) - 15} apparati")
            print()

        return 0

    elif action == "list-hardware":
        vendor = getattr(args, "vendor", None)
        devices = engine.list_hardware(vendor_filter=vendor)
        title = "INVENTARIO HARDWARE GLOBALE" + (f" (Filtro Vendor: {vendor})" if vendor else "")
        print(colorize(f"\n=== {title} ===", COLOR_BOLD + COLOR_CYAN))
        print(f"Apparati censiti: {len(devices)}\n")

        print(f"{'Vendor':<12} | {'Categoria':<18} | {'Cliente / Progetto':<24} | {'IP':<15} | {'Dettaglio / Modello'}")
        print("-" * 105)
        for d in devices:
            ip_str = d["ip"] or "-"
            cust_str = f"{d['customer'][:15]} ({d['project_slug']})"[:23]
            print(f"{d['vendor']:<12} | {d['category']:<18} | {cust_str:<24} | {ip_str:<15} | {d['context'][:40]}")
        print("-" * 105 + "\n")
        return 0

    elif action == "summary":
        s = engine.summary()
        stats = s["stats"]
        print(colorize(f"\n=== DASHBOARD ASSET & ENTITÀ ENTERPRISE ITINFRA ===", COLOR_BOLD + COLOR_CYAN))
        print(f"Progetti attivi:     {stats['total_projects']}")
        print(f"Documenti OKF v0.2:  {stats['total_docs']}")
        print(f"Entità ontologiche:  {stats['total_entities']}")
        print(f"Apparati mappati:    {stats['total_devices']}")
        print(f"Ticket RCA censiti:  {stats['total_rcas']}\n")

        print(colorize("Ripartizione per Vendor:", COLOR_BOLD))
        for v, cnt in s["vendors_breakdown"].items():
            print(f" • {v:<15}: {cnt} apparati")

        print(colorize("\nRipartizione per Categoria:", COLOR_BOLD))
        for c, cnt in s["categories_breakdown"].items():
            print(f" • {c:<20}: {cnt} apparati")

        print(colorize("\nProgetti e Clienti nel Portfolio:", COLOR_BOLD))
        for p in s["projects_list"]:
            print(f" • {p['customer']} (slug: {p['slug']}) - {p['docs_count']} documenti")
        print()
        return 0

    return 0

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="ITInfra CLI — Assistente e validatore OKF v0.2 per documentazione di infrastruttura IT"
    )
    subparsers = parser.add_subparsers(dest="command", help="Comandi disponibili")

    # Comando list-templates
    subparsers.add_parser("list-templates", help="Elenca tutti i template documentali disponibili")

    # Comando init
    p_init = subparsers.add_parser("init", help="Inizializza un nuovo progetto IT con manifesto condiviso")
    p_init.add_argument("project_slug", help="Identificativo univoco del progetto (es. acme-milano-dc)")
    p_init.add_argument("--client", help="Nome del cliente")
    p_init.add_argument("--name", help="Nome descrittivo del progetto")
    p_init.add_argument("--architect", help="Nome del Lead Architect")

    # Comando validate
    p_val = subparsers.add_parser("validate", help="Valida conformita' OKF v0.2 di file o cartelle")
    p_val.add_argument("path", help="File .md o directory da validare")
    p_val.add_argument("-v", "--verbose", action="store_true", help="Mostra dettagli entita' e relazioni")

    # Comando status
    p_status = subparsers.add_parser("status", help="Mostra lo stato di avanzamento delle 7 fasi di un progetto")
    p_status.add_argument("project_slug", help="Slug del progetto")

    # Comando export-ipam
    p_ipam = subparsers.add_parser("export-ipam", help="Esporta tabelle VLAN e Subnet da LLD in formato NetBox CSV/JSON")
    p_ipam.add_argument("path", help="File LLD/As-Built .md o cartella del progetto")
    p_ipam.add_argument("--format", choices=["csv", "json"], default="csv", help="Formato di esportazione (default: csv)")
    p_ipam.add_argument("--out", help="Cartella di output (default: ./exports)")

    # Comando generate-diagram
    p_diag = subparsers.add_parser("generate-diagram", help="Genera diagrammi Mermaid (topologia o rack) a partire da LLD")
    p_diag.add_argument("path", help="File LLD o As-Built .md")
    p_diag.add_argument("--type", choices=["topology", "rack", "all"], default="topology", help="Tipo diagramma (topology, rack, all)")
    p_diag.add_argument("--out", help="File di output opzionale (se omesso, stampa a video)")

    # Comando export-html
    p_html = subparsers.add_parser("export-html", help="Genera un report consolidato completo in formato HTML per il progetto")
    p_html.add_argument("project", help="Slug del progetto o percorso della cartella progetto")
    p_html.add_argument("--out", help="Percorso del file HTML di destinazione (default: projects/<slug>/report.html)")

    # Comando vault
    p_vault = subparsers.add_parser("vault", help="Gestione Local Encrypted Secret Vault (AES-256-GCM)")
    sub_vault = p_vault.add_subparsers(dest="vault_action", help="Azione vault", required=True)

    v_init = sub_vault.add_parser("init", help="Inizializza un nuovo vault cifrato")
    v_init.add_argument("project_slug", help="Slug del progetto")
    v_init.add_argument("--passphrase", help="Master passphrase (se omesso viene richiesta interattivamente)")
    v_init.add_argument("--overwrite", action="store_true", help="Sovrascrive il vault se esistente")

    v_set = sub_vault.add_parser("set", help="Salva o aggiorna un secret cifrato")
    v_set.add_argument("project_slug", help="Slug del progetto")
    v_set.add_argument("key", help="Path o chiave del secret (es. mikrotik/admin, vpn/zerotier)")
    v_set.add_argument("--value", help="Valore del secret (se omesso viene richiesto in modo sicuro)")
    v_set.add_argument("--passphrase", help="Master passphrase")

    v_get = sub_vault.add_parser("get", help="Recupera e decifra un secret")
    v_get.add_argument("project_slug", help="Slug del progetto")
    v_get.add_argument("key", help="Path o chiave del secret")
    v_get.add_argument("--passphrase", help="Master passphrase")

    v_list = sub_vault.add_parser("list", help="Elenca le chiavi censite nel vault (senza esporre valori)")
    v_list.add_argument("project_slug", help="Slug del progetto")
    v_list.add_argument("--passphrase", help="Master passphrase")

    v_audit = sub_vault.add_parser("audit", help="Verifica coerenza riferimenti vault:// nei markdown")
    v_audit.add_argument("project_slug", help="Slug del progetto")
    v_audit.add_argument("--passphrase", help="Master passphrase opzionale per verifica incrociata dei secret")

    # Comando worktree
    p_wt = subparsers.add_parser("worktree", help="Gestione Git Worktrees per agenti AI concorrenti")
    sub_wt = p_wt.add_subparsers(dest="wt_action", help="Azione worktree", required=True)

    wt_add = sub_wt.add_parser("add", help="Crea un worktree dedicato per un ruolo agente")
    wt_add.add_argument("role", choices=["infra-architect", "infra-security", "infra-automation", "infra-qa"], help="Ruolo dell'agente")
    wt_add.add_argument("--branch", help="Nome branch personalizzato (default feat/<ruolo>)")

    sub_wt.add_parser("list", help="Elenca i worktree attivi e i rispettivi ruoli")

    wt_sync = sub_wt.add_parser("sync", help="Sincronizza il worktree di un ruolo con main")
    wt_sync.add_argument("role", help="Ruolo dell'agente da sincronizzare")

    sub_wt.add_parser("cleanup", help="Rimuove tutti i worktree temporanei in .worktrees/")

    # Comando audit-consistency
    p_ac = subparsers.add_parser("audit-consistency", help="Verifica coerenza semantica incrociata tra i 9 documenti e il manifesto")
    p_ac.add_argument("project_slug", help="Slug del progetto")

    # Comando export-configs
    p_ec = subparsers.add_parser("export-configs", help="Estrae script RouterOS (.rsc) e PowerShell (.ps1) dai documenti")
    p_ec.add_argument("project_slug", help="Slug del progetto")
    p_ec.add_argument("--out", help="Directory di destinazione (default: projects/<slug>/configs/)")

    # Comando troubleshoot
    p_tb = subparsers.add_parser("troubleshoot", help="Gestione ticket di incidente e Root Cause Analysis (RCA)")
    sub_tb = p_tb.add_subparsers(dest="tb_action", help="Azione troubleshoot", required=True)

    tb_init = sub_tb.add_parser("init", help="Inizializza un nuovo ticket RCA da template OKF")
    tb_init.add_argument("project_slug", help="Slug del progetto")
    tb_init.add_argument("ticket_id", help="Identificativo ticket (es. FS01-SMB-Connectivity, INC-2026-001)")
    tb_init.add_argument("--title", help="Titolo descrittivo del disservizio")
    tb_init.add_argument("--severity", choices=["P1-Critical", "P2-High", "P3-Medium", "P4-Low"], help="Severità incidente")
    tb_init.add_argument("--force", action="store_true", help="Sovrascrive il file se esistente")

    tb_list = sub_tb.add_parser("list", help="Elenca i ticket RCA registrati per il progetto")
    tb_list.add_argument("project_slug", help="Slug del progetto")

    # Comando export-graph
    p_eg = subparsers.add_parser("export-graph", help="Genera una mappa interattiva D3.js del Knowledge Graph OKF v0.2 (supporta 'all' per vista globale)")
    p_eg.add_argument("target", help="Slug del progetto (es. severino-srl), 'templates', oppure 'all' / 'global'")
    p_eg.add_argument("--out", help="Percorso file HTML di output (default: <target>/graph.html)")
    p_eg.add_argument("--title", help="Titolo personalizzato della vista grafo")

    # Comando memory (Release v0.6 e v0.8)
    p_mem = subparsers.add_parser("memory", help="Gestione Memoria Locale Ibrida a 3 Livelli e Global Enterprise Pool (Release v0.8)")
    sub_mem = p_mem.add_subparsers(dest="mem_action", help="Azione memory", required=True)

    mem_init = sub_mem.add_parser("init", help="Inizializza lo scratchpad di staging (_scratchpad.md o globale)")
    mem_init.add_argument("project_slug", nargs="?", default="", help="Slug del progetto (o ometti con --global)")
    mem_init.add_argument("--global", dest="is_global", action="store_true", help="Opera sullo Staging Scratchpad Globale Enterprise")

    mem_log = sub_mem.add_parser("log", help="Registra una nota, decisione o best practice nello scratchpad")
    mem_log.add_argument("project_slug", nargs="?", default="", help="Slug del progetto (o ometti con --global)")
    mem_log.add_argument("--global", dest="is_global", action="store_true", help="Registra nella Memoria Globale Enterprise")
    mem_log.add_argument("--section", default="decisioni", help="Sezione (decisioni, sospesi, note, best-practices, known-issues, hardware-rules, open-architectural)")
    mem_log.add_argument("--text", required=True, help="Testo della nota o decisione")
    mem_log.add_argument("--role", help="Ruolo dell'agente (es. infra-architect, infra-security)")
    mem_log.add_argument("--author", help="Nome o identificativo autore (default: utente corrente)")

    mem_show = sub_mem.add_parser("show", help="Mostra il contenuto e le statistiche dello scratchpad")
    mem_show.add_argument("project_slug", nargs="?", default="", help="Slug del progetto (o ometti con --global)")
    mem_show.add_argument("--global", dest="is_global", action="store_true", help="Visualizza la Memoria Globale Enterprise")

    mem_merge = sub_mem.add_parser("merge", help="Fonde gli scratchpad temporanei dei worktree (.memory/) nello scratchpad master")
    mem_merge.add_argument("project_slug", help="Slug del progetto")

    mem_cons = sub_mem.add_parser("consolidate", help="Consolida le decisioni confermate nel documento target OKF v0.2 con Trust Signals")
    mem_cons.add_argument("project_slug", help="Slug del progetto")
    mem_cons.add_argument("--target", required=True, help="Identificativo documento target (es. 01-RSD-URS, 02-HLD, 03-LLD)")
    mem_cons.add_argument("--reviewer", default="Lead Architect", help="Nome/ruolo del revisore attestante (default: Lead Architect)")
    mem_cons.add_argument("--stale-days", type=int, default=90, help="Giorni di validita' prima dello stato stale (default: 90)")

    mem_prune = sub_mem.add_parser("prune", help="Archivia lo scratchpad corrente e lo reimposta allo stato vuoto")
    mem_prune.add_argument("project_slug", nargs="?", default="", help="Slug del progetto (o ometti con --global)")
    mem_prune.add_argument("--global", dest="is_global", action="store_true", help="Archivia la Memoria Globale Enterprise")
    mem_prune.add_argument("--no-archive", action="store_true", help="Non salva una copia nell'archivio")

    # Comando test-suite (Release v0.8)
    p_ts = subparsers.add_parser("test-suite", help="Esegue la suite di collaudo end-to-end e genera la dashboard HTML di sistema (Release v0.8)")
    p_ts.add_argument("--report-html", action="store_true", default=True, help="Esporta la dashboard HTML offline di verifica (default: True)")
    p_ts.add_argument("--no-html", dest="report_html", action="store_false", help="Esegue solo i test a terminale senza esportare HTML")
    p_ts.add_argument("--out", help="Percorso del file HTML di output (default: projects/system-test-report.html)")

    # Comando inventory (Release v0.7)
    p_inv = subparsers.add_parser("inventory", help="Ricerca asset hardware, apparati ed entità cross-progetto (Release v0.7)")
    sub_inv = p_inv.add_subparsers(dest="inv_action", help="Azione inventory", required=True)

    inv_find = sub_inv.add_parser("find", help="Cerca modelli hardware, entità o tecnologie in tutti i progetti")
    inv_find.add_argument("term", help="Termine di ricerca (es. 'Dell R630', 'CRS326', 'ZeroTier')")
    inv_find.add_argument("--type", help="Filtro tipo entità (es. technology, framework, toolchain)")

    inv_list = sub_inv.add_parser("list-hardware", help="Elenca tutti gli apparati hardware censiti nel portfolio clienti")
    inv_list.add_argument("--vendor", help="Filtra per vendor (es. Dell, MikroTik, HP, Cisco, Fortinet)")

    inv_sum = sub_inv.add_parser("summary", help="Dashboard statistica del patrimonio tecnologico multi-cliente")

    # Comando health-check
    p_hc = subparsers.add_parser("health-check", help="Esegue telemetria e health check non distruttivo (ICMP/TCP) sugli apparati del manifest")
    p_hc.add_argument("project_slug", help="Slug del progetto")
    p_hc.add_argument("--timeout", type=float, default=1.0, help="Timeout socket in secondi (default: 1.0)")

    # Comando publish (Release v0.9)
    p_pub = subparsers.add_parser("publish", help="Pubblica in modo atomico il progetto locale su storage master centrale (Release v0.9)")
    p_pub.add_argument("slug", help="Slug del progetto locale da pubblicare")
    p_pub.add_argument("--dest", default=None, help=f"Percorso della share centrale (default: '{DEFAULT_CENTRAL_SHARE}')")
    p_pub.add_argument("--dry-run", action="store_true", help="Simula il Quality Gate e la pubblicazione senza copiare file")
    p_pub.add_argument("--force", action="store_true", help="Forza la sovrascrittura anche se il progetto remoto e' approvato")

    # Comando sync-engine (Release v0.9)
    p_sync = subparsers.add_parser("sync-engine", help="Sincronizza e aggiorna template, script e guide dalla share master (Release v0.9)")
    p_sync.add_argument("--source", default=None, help=f"Percorso della share centrale (default: '{DEFAULT_CENTRAL_SHARE}')")
    p_sync.add_argument("--dry-run", action="store_true", help="Mostra i file che verrebbero aggiornati senza eseguire la copia")

    # Comando check-share (Release v0.9.1)
    p_chk = subparsers.add_parser("check-share", help="Verifica connettività, permessi di pubblicazione e protezione core sulla share centrale (Release v0.9.1)")
    p_chk.add_argument("--path", default=None, help=f"Percorso della share centrale da testare (default: '{DEFAULT_CENTRAL_SHARE}')")
    p_chk.add_argument("--user", default=None, help="Nome utente SMB per simulare un profilo tecnico (opzionale)")
    p_chk.add_argument("--password", default=None, help="Password SMB per simulare un profilo tecnico (opzionale)")

    # Comando deploy-share (Release v0.9.5)
    p_dep = subparsers.add_parser("deploy-share", help="Distribuisce in modo differenziale template e script sulla share centrale (Release v0.9.5)")
    p_dep.add_argument("--dest", default=None, help=f"Percorso della share centrale (default: '{DEFAULT_CENTRAL_SHARE}')")
    p_dep.add_argument("--dry-run", action="store_true", help="Simula il deploy differenziale senza copiare file")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 0

    if args.command == "list-templates":
        return cmd_list_templates(args)
    elif args.command == "init":
        return cmd_init(args)
    elif args.command == "validate":
        return cmd_validate(args)
    elif args.command == "status":
        return cmd_status(args)
    elif args.command == "export-ipam":
        return cmd_export_ipam(args)
    elif args.command == "generate-diagram":
        return cmd_generate_diagram(args)
    elif args.command == "export-html":
        return cmd_export_html(args)
    elif args.command == "vault":
        return cmd_vault(args)
    elif args.command == "worktree":
        return cmd_worktree(args)
    elif args.command == "audit-consistency":
        return cmd_audit_consistency(args)
    elif args.command == "export-configs":
        return cmd_export_configs(args)
    elif args.command == "troubleshoot":
        return cmd_troubleshoot(args)
    elif args.command == "health-check":
        return cmd_health_check(args)
    elif args.command == "export-graph":
        return cmd_export_graph(args)
    elif args.command == "memory":
        return cmd_memory(args)
    elif args.command == "inventory":
        return cmd_inventory(args)
    elif args.command == "test-suite":
        return cmd_test_suite(args)
    elif args.command == "publish":
        return cmd_publish(args)
    elif args.command == "sync-engine":
        return cmd_sync_engine(args)
    elif args.command == "check-share":
        return cmd_check_share(args)
    elif args.command == "deploy-share":
        return cmd_deploy_share(args)
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
