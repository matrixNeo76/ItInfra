#!/usr/bin/env python3
"""
ITInfra Global Enterprise Inventory & Entity Intelligence Engine (OKF v0.2)
Permette la scansione, ricerca e interpolazione ontologica cross-progetto
del patrimonio hardware, software e delle entità tecnologiche del portfolio ITInfra.
100% File-Based & Git-Native.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

try:
    import yaml
except ImportError:
    yaml = None


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, Optional[str]]:
    content = content.lstrip("\ufeff")
    match = re.search(r"^---\r?\n(.*?)\r?\n---\r?\n(.*)$", content, re.DOTALL)
    if not match:
        return None, content, "No frontmatter"
    try:
        data = yaml.safe_load(match.group(1)) if yaml else None
        return (data if isinstance(data, dict) else None), match.group(2), None
    except Exception as e:
        return None, match.group(2), str(e)


# Regole e pattern euristici per il riconoscimento apparati e vendor
VENDOR_PATTERNS = [
    ("Dell", r"\b(?:dell\s+(?:poweredge|server|emc|r\d{3}|optiplex|latitude|precision)|poweredge|r630|r730|r740|r640|perc\s+h\d+)\b", re.IGNORECASE),
    ("MikroTik", r"\b(?:mikrotik|routeros|crs\d+|rb\d+|ccr\d+)\b", re.IGNORECASE),
    ("Cisco", r"\b(?:cisco|catalyst|nexus|meraki)\b", re.IGNORECASE),
    ("Fortinet", r"\b(?:fortinet|fortigate|fortiswitch)\b", re.IGNORECASE),
    ("HP / HPE", r"\b(?:hp|hpe|proliant|aruba)\b", re.IGNORECASE),
    ("Microsoft", r"\b(?:hyper-v|windows\s+server|active\s+directory)\b", re.IGNORECASE),
    ("ZeroTier", r"\b(?:zerotier|zt\d+)\b", re.IGNORECASE),
    ("Proxmox", r"\b(?:proxmox|pve)\b", re.IGNORECASE),
]

CATEGORY_PATTERNS = [
    ("Server", r"\b(?:server|poweredge|proliant|r\d{3}|host\s+hv|compute)\b", re.IGNORECASE),
    ("Switch", r"\b(?:switch|crs\d+|catalyst|leaf|spine|sw-core|patch\s+panel)\b", re.IGNORECASE),
    ("Router / GW", r"\b(?:router|gateway|rb\d+|ccr\d+|edge)\b", re.IGNORECASE),
    ("Firewall", r"\b(?:firewall|fortigate|pfsense|opnsense|utm)\b", re.IGNORECASE),
    ("Storage / Backup", r"\b(?:storage|nas|san|iscsi|synology|qnap|ssk|veeam|rustcopy)\b", re.IGNORECASE),
    ("Virtualization / OS", r"\b(?:hyper-v|proxmox|esxi|vmware|linux|windows)\b", re.IGNORECASE),
    ("SDN / Overlay", r"\b(?:zerotier|tailscale|wireguard|vpn|vxlan|evpn)\b", re.IGNORECASE),
]


class GlobalInventoryEngine:
    def __init__(self, repo_root: Optional[Path] = None):
        if repo_root is None:
            self.repo_root = Path(__file__).resolve().parent.parent
        else:
            self.repo_root = repo_root
        self.projects_dir = self.repo_root / "projects"
        self._cache: Optional[Dict[str, Any]] = None

    def scan_all_projects(self, force: bool = False) -> Dict[str, Any]:
        """Scansiona tutti i progetti e compila il database ontologico aggregato."""
        if self._cache is not None and not force:
            return self._cache

        projects_data = {}
        all_entities = []
        all_devices = []
        all_rcas = []

        if not self.projects_dir.exists():
            return {
                "projects": {}, "entities": [], "devices": [], "rcas": [],
                "stats": {"total_projects": 0, "total_docs": 0, "total_entities": 0, "total_devices": 0}
            }

        # Trova tutte le cartelle progetto (escludendo speciali)
        proj_dirs = [
            p for p in sorted(self.projects_dir.iterdir())
            if p.is_dir() and not p.name.startswith("_") and p.name not in ["configs", "exports"]
        ]

        total_docs = 0

        for p_dir in proj_dirs:
            slug = p_dir.name
            manifest_file = p_dir / "project-manifest.yaml"
            manifest_info = {}
            if manifest_file.exists():
                try:
                    manifest_info = yaml.safe_load(manifest_file.read_text(encoding="utf-8")) or {}
                except Exception:
                    pass

            customer = manifest_info.get("customer", slug.capitalize())
            proj_name = manifest_info.get("project_name", f"Progetto {slug}")

            proj_record = {
                "slug": slug,
                "customer": customer,
                "project_name": proj_name,
                "manifest": manifest_info,
                "documents": [],
            }

            md_files = [
                f for f in sorted(p_dir.glob("*.md"))
                if not f.name.startswith("_") and f.name.lower() != "readme.md"
            ]

            for md_file in md_files:
                try:
                    content = md_file.read_text(encoding="utf-8")
                except Exception:
                    continue

                total_docs += 1
                fm, body, _ = parse_frontmatter(content)
                fm = fm or {}

                doc_id = fm.get("id", md_file.stem)
                doc_title = fm.get("title", md_file.stem)
                doc_type = fm.get("type", "concept")
                phase = fm.get("phase", 0)
                entities = fm.get("entities", []) or []
                verified = fm.get("verified", False)
                verified_by = fm.get("verified_by", "")
                last_vetted = fm.get("last_vetted", "")
                stale_after = fm.get("stale_after", "")

                doc_entry = {
                    "filename": md_file.name,
                    "id": doc_id,
                    "title": doc_title,
                    "type": doc_type,
                    "phase": phase,
                    "verified": verified,
                    "verified_by": verified_by,
                    "last_vetted": last_vetted,
                    "stale_after": stale_after,
                    "entities_count": len(entities)
                }
                proj_record["documents"].append(doc_entry)

                # Raccogli entita ontologiche
                for ent in entities:
                    if isinstance(ent, dict):
                        e_name = ent.get("name", "").strip()
                        e_type = ent.get("type", "concept")
                        e_desc = ent.get("description", "").strip()
                        if e_name:
                            all_entities.append({
                                "name": e_name,
                                "type": e_type,
                                "description": e_desc,
                                "project_slug": slug,
                                "customer": customer,
                                "doc_file": md_file.name,
                                "doc_title": doc_title,
                                "doc_id": doc_id,
                            })

                # Riconoscimento ticket RCA
                if md_file.name.startswith("10-RCA-"):
                    inc_id = fm.get("incident_id", md_file.stem.replace("10-RCA-", ""))
                    sev = fm.get("severity", "P2-High")
                    status = fm.get("status", "resolved")
                    all_rcas.append({
                        "incident_id": inc_id,
                        "project_slug": slug,
                        "customer": customer,
                        "file": md_file.name,
                        "title": doc_title,
                        "severity": sev,
                        "status": status,
                        "content_snippet": body[:500] if body else ""
                    })

                # Estrazione apparati e hardware dal body (tabelle o testo)
                lines = content.splitlines()
                for line in lines:
                    if not ("|" in line or ":" in line):
                        continue
                    # Cerca match vendor
                    for vendor_name, v_pattern, v_flags in VENDOR_PATTERNS:
                        if re.search(v_pattern, line, v_flags):
                            # Identifica categoria
                            cat_found = "Hardware / Tech"
                            for c_name, c_pat, c_flags in CATEGORY_PATTERNS:
                                if re.search(c_pat, line, c_flags):
                                    cat_found = c_name
                                    break

                            # Estrai eventuale IP nella riga
                            ip_m = re.search(r"\b(?:192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+)\b", line)
                            ip_found = ip_m.group(0) if ip_m else None

                            # Estrai modello ripulito
                            clean_line = line.replace("|", " ").strip()
                            clean_line = re.sub(r"\s+", " ", clean_line)

                            all_devices.append({
                                "vendor": vendor_name,
                                "category": cat_found,
                                "context": clean_line[:120],
                                "ip": ip_found,
                                "project_slug": slug,
                                "customer": customer,
                                "doc_file": md_file.name,
                                "doc_title": doc_title
                            })
                            break

            projects_data[slug] = proj_record

        # Deduplicazione intelligente dei device per evitare rumore
        unique_devices = []
        seen_dev = set()
        for d in all_devices:
            sig = (d["project_slug"], d["vendor"], d["category"], d.get("ip"), d["context"][:40])
            if sig not in seen_dev:
                seen_dev.add(sig)
                unique_devices.append(d)

        self._cache = {
            "projects": projects_data,
            "entities": all_entities,
            "devices": unique_devices,
            "rcas": all_rcas,
            "stats": {
                "total_projects": len(projects_data),
                "total_docs": total_docs,
                "total_entities": len(all_entities),
                "total_devices": len(unique_devices),
                "total_rcas": len(all_rcas)
            }
        }
        return self._cache

    def find(self, term: str, entity_type: Optional[str] = None) -> Dict[str, Any]:
        """Cerca un termine (es. 'Dell R630', 'CRS326', 'ZeroTier') attraverso tutti i progetti."""
        db = self.scan_all_projects()
        t_clean = term.strip().lower()

        matched_entities = []
        for e in db["entities"]:
            if entity_type and e["type"].lower() != entity_type.lower():
                continue
            if t_clean in e["name"].lower() or t_clean in e["description"].lower():
                matched_entities.append(e)

        matched_devices = []
        for d in db["devices"]:
            if t_clean in d["vendor"].lower() or t_clean in d["context"].lower() or (d["ip"] and t_clean in d["ip"]):
                matched_devices.append(d)

        # Correlazione con ticket RCA (Cross-Client Incident Intelligence)
        rca_alerts = []
        for rca in db["rcas"]:
            if t_clean in rca["title"].lower() or t_clean in rca["content_snippet"].lower():
                rca_alerts.append(rca)

        # Raggruppa clienti/progetti impattati
        projects_involved = set()
        for item in matched_entities:
            projects_involved.add(f"{item['customer']} ({item['project_slug']})")
        for item in matched_devices:
            projects_involved.add(f"{item['customer']} ({item['project_slug']})")

        return {
            "term": term,
            "total_matches": len(matched_entities) + len(matched_devices),
            "projects_involved": sorted(list(projects_involved)),
            "entities": matched_entities,
            "devices": matched_devices,
            "rca_alerts": rca_alerts
        }

    def list_hardware(self, vendor_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Restituisce l'inventario consolidato di tutti gli apparati censiti."""
        db = self.scan_all_projects()
        v_clean = vendor_filter.strip().lower() if vendor_filter else None

        results = []
        for d in db["devices"]:
            if v_clean and v_clean not in d["vendor"].lower():
                continue
            results.append(d)

        return sorted(results, key=lambda x: (x["vendor"], x["category"], x["customer"]))

    def summary(self) -> Dict[str, Any]:
        """Restituisce una sintesi del portfolio tecnologico multi-cliente."""
        db = self.scan_all_projects()
        vendors_count = {}
        cats_count = {}
        for d in db["devices"]:
            v = d["vendor"]
            c = d["category"]
            vendors_count[v] = vendors_count.get(v, 0) + 1
            cats_count[c] = cats_count.get(c, 0) + 1

        return {
            "stats": db["stats"],
            "vendors_breakdown": dict(sorted(vendors_count.items(), key=lambda x: -x[1])),
            "categories_breakdown": dict(sorted(cats_count.items(), key=lambda x: -x[1])),
            "projects_list": [
                {"slug": s, "customer": p["customer"], "docs_count": len(p["documents"])}
                for s, p in db["projects"].items()
            ],
            "rcas_list": [
                {"id": r["incident_id"], "customer": r["customer"], "title": r["title"], "severity": r["severity"]}
                for r in db["rcas"]
            ]
        }
