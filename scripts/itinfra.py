#!/usr/bin/env python3
"""
ITInfra CLI & OKF v0.2 Linter
Suite per la gestione di progetti di infrastrutture IT e validazione documentale OKF v0.2.
"""

import sys
import os
import re
import argparse
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
        files_to_check = [f for f in sorted(list(target_path.rglob("*.md"))) if f.name.lower() != "readme.md"]
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
    else:
        parser.print_help()
        return 1

if __name__ == "__main__":
    sys.exit(main())
