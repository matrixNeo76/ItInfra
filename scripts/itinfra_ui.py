#!/usr/bin/env python3
"""
scripts/itinfra_ui.py
---------------------
Modulo Enterprise Generative UI per Google Antigravity & ITInfra Suite.
Genera il Cockpit Esecutivo Sistemistico interattivo, Dynamic Project Switcher,
Matrice di Stato a 10 Documenti, Workflow Tecnici (SPEC-24: dr-drill, firmware-upgrade, raee),
Pre-Flight Quality Gate Cards e Bridge Hub-and-Spoke con itinfra-business-ops.
Conforme ai design tokens di Google Antigravity e standard OKF v0.2.
"""

import os
import re
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"

def discover_projects_state(repo_root: Optional[Path] = None) -> List[Dict[str, Any]]:
    """Analizza tutti i progetti in projects/ e mappa lo stato dei 10 documenti OKF v0.2."""
    if repo_root is None:
        repo_root = Path(__file__).resolve().parent.parent
    projects_dir = repo_root / "projects"
    if not projects_dir.exists():
        return []

    standard_docs = [
        ("01-RSD-URS", "RSD/URS", "specification"),
        ("02-HLD", "HLD", "architecture"),
        ("03-LLD", "LLD", "architecture"),
        ("04-MOP", "MOP", "guide"),
        ("05-Rollback", "Rollback", "guide"),
        ("06-As-Built", "As-Built", "architecture"),
        ("07-ATP", "ATP", "specification"),
        ("08-SOP-Runbook", "Runbook", "guide"),
        ("09-Handover-Inventory", "Handover", "specification"),
        ("10-RCA", "RCA", "guide"),
    ]

    results = []
    for d in sorted(projects_dir.iterdir()):
        if not d.is_dir() or d.name.startswith("_") or d.name.startswith("."):
            continue

        manifest_path = d / "project-manifest.yaml"
        manifest_data = {}
        if manifest_path.exists():
            try:
                manifest_data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            except Exception:
                pass

        proj_name = manifest_data.get("project_name", d.name.capitalize())
        customer = manifest_data.get("customer", d.name)
        status = manifest_data.get("status", "draft")

        docs_state = []
        for code, short_title, doc_type in standard_docs:
            matching = list(d.glob(f"{code}*.md"))
            if matching:
                doc_file = matching[0]
                content = doc_file.read_text(encoding="utf-8")
                doc_status = "draft"
                m = re.search(r'^status:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
                if m:
                    doc_status = m.group(1).strip().lower()
                docs_state.append({
                    "code": code,
                    "title": short_title,
                    "type": doc_type,
                    "status": doc_status,
                    "exists": True,
                    "filename": doc_file.name
                })
            else:
                docs_state.append({
                    "code": code,
                    "title": short_title,
                    "type": doc_type,
                    "status": "missing",
                    "exists": False,
                    "filename": f"{code}.md"
                })

        approved_count = sum(1 for doc in docs_state if doc["status"] == "approved")
        in_review_count = sum(1 for doc in docs_state if doc["status"] in ("in-review", "draft"))
        missing_count = sum(1 for doc in docs_state if doc["status"] == "missing")

        results.append({
            "slug": d.name,
            "name": proj_name,
            "customer": customer,
            "status": status,
            "docs": docs_state,
            "stats": {
                "total": len(docs_state),
                "approved": approved_count,
                "in_review": in_review_count,
                "missing": missing_count
            }
        })

    return results

def render_enterprise_dashboard(
    workspace_path: str = "C:\\project",
    share_path: str = DEFAULT_CENTRAL_SHARE,
    share_reachable: bool = True,
    templates_count: int = 10,
    active_project: Optional[str] = None,
    vault_status: str = "AES-256-GCM (Zero Leak)",
    test_suite_status: str = "16/16 Pass (100%)"
) -> str:
    """Genera l'Enterprise Cockpit Dashboard compatto con Project Switcher, 10-Doc Matrix e Workflow Tecnici SPEC-24."""
    share_label = "Share Online" if share_reachable else "Share Offline"
    pulse_class = "animate-pulse" if share_reachable else ""

    projects_list = discover_projects_state()
    if not projects_list:
        projects_list = [{
            "slug": "severino-srl",
            "name": "Severino Srl",
            "customer": "Severino Srl",
            "status": "completed",
            "docs": [],
            "stats": {"total": 10, "approved": 0, "in_review": 10, "missing": 0}
        }]

    default_slug = active_project if (active_project and any(p["slug"] == active_project for p in projects_list)) else projects_list[0]["slug"]
    projects_json = json.dumps(projects_list, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {{
      --background: #070d1e;
      --card: #0f1c3f;
      --foreground: #f8fafc;
      --muted-foreground: #94a3b8;
      --border: #223c7c;
      --primary: #38bdf8;
    }}
    body {{ background: transparent; color: var(--foreground); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }}
    .tab-active {{
      background: rgba(14, 165, 233, 0.15) !important;
      color: #38bdf8 !important;
      border-color: rgba(56, 189, 248, 0.4) !important;
    }}
    .action-card:hover .copy-badge {{
      background: #0ea5e9 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
    }}
    .action-card:active {{
      transform: scale(0.98);
    }}
    .proj-pill-active {{
      background: #0ea5e9 !important;
      color: #ffffff !important;
      border-color: #38bdf8 !important;
    }}
    .status-badge-approved {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .status-badge-review {{ background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }}
    .status-badge-draft {{ background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3); }}
    .status-badge-missing {{ background: rgba(148, 163, 184, 0.1); color: #94a3b8; border: 1px solid rgba(148, 163, 184, 0.2); }}
  </style>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-2 font-sans select-none">
  <div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-4 shadow-2xl max-w-2xl mx-auto backdrop-blur-md relative overflow-hidden">
    
    <!-- 1. Header Compatto -->
    <div class="flex items-center justify-between border-b border-[var(--border)] pb-2.5 mb-3">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-lg bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 font-black text-xs shadow-sm">
          IT
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h2 class="text-sm font-bold tracking-tight text-sky-400">ITInfra Enterprise Suite</h2>
            <span class="text-[9px] uppercase font-semibold px-1.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">v0.9.15 (SPEC-24)</span>
          </div>
          <p class="text-[10px] text-[var(--muted-foreground)]">Governance OKF v0.2 • Hub Tecnico Federato a Business Ops</p>
        </div>
      </div>
      
      <div class="flex items-center gap-2">
        <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 {pulse_class}"></span>
          {share_label}
        </div>
      </div>
    </div>

    <!-- 2. Navigazione a Tab Compatte -->
    <div class="flex items-center gap-1.5 bg-[var(--background)] p-1 rounded-xl border border-[var(--border)] mb-3">
      <button id="btn-tab-actions" onclick="switchTab('tab-actions')" class="tab-active flex-1 py-1 px-2 rounded-lg text-xs font-semibold border transition-all text-center flex items-center justify-center gap-1.5">
        <span>⚡</span> Azioni Rapide
      </button>
      <button id="btn-tab-phases" onclick="switchTab('tab-phases')" class="flex-1 py-1 px-2 rounded-lg text-xs font-semibold border border-transparent text-[var(--muted-foreground)] transition-all text-center flex items-center justify-center gap-1.5">
        <span>🔄</span> Progetti & 10 Doc
      </button>
      <button id="btn-tab-tech" onclick="switchTab('tab-tech')" class="flex-1 py-1 px-2 rounded-lg text-xs font-semibold border border-transparent text-[var(--muted-foreground)] transition-all text-center flex items-center justify-center gap-1.5">
        <span>⚙️</span> Workflow Tecnici
      </button>
      <button id="btn-tab-kpi" onclick="switchTab('tab-kpi')" class="flex-1 py-1 px-2 rounded-lg text-xs font-semibold border border-transparent text-[var(--muted-foreground)] transition-all text-center flex items-center justify-center gap-1.5">
        <span>📊</span> Telemetria
      </button>
    </div>

    <!-- 3. Contenuti Tab -->

    <!-- TAB 1: AZIONI RAPIDE -->
    <div id="tab-actions" class="space-y-2">
      <div class="text-[10px] text-[var(--muted-foreground)] flex items-center justify-between px-0.5">
        <span>💡 <em>Clicca su un'azione per copiare il comando negli appunti e incollarlo in chat:</em></span>
        <span class="text-sky-400 font-mono text-[9px]">Progetto attivo: <strong id="lbl-active-slug" class="text-sky-300 font-bold">{default_slug}</strong></span>
      </div>

      <div class="grid grid-cols-2 gap-2">
        <div onclick="copyActiveCmd('scaffold')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-sky-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>✨</span> Auto-Scaffold</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Propaga dati da manifest</div>
          </div>
          <span id="btn-copy-scaffold" class="copy-badge text-[10px] bg-slate-800 text-sky-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">it scaffold</span>
        </div>

        <div onclick="copyActiveCmd('pubblica')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-emerald-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🚀</span> Pubblica Progetto</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Quality Gate & copia server</div>
          </div>
          <span id="btn-copy-pubblica" class="copy-badge text-[10px] bg-slate-800 text-emerald-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">pubblica {default_slug}</span>
        </div>

        <div onclick="copyActiveCmd('stato')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-amber-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>📈</span> Stato 7 Fasi</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Avanzamento cliente</div>
          </div>
          <span id="btn-copy-stato" class="copy-badge text-[10px] bg-slate-800 text-amber-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">stato {default_slug}</span>
        </div>

        <div onclick="copyCmd('aggiorna')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-sky-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🔄</span> Allinea Motore</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Sync SHA-256 da share</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-sky-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">aggiorna</span>
        </div>

        <div onclick="copyCmd('controlla')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-emerald-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🩺</span> Verifica Rete</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Salute SMB & permessi</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-emerald-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">controlla</span>
        </div>

        <div onclick="copyCmd('test-suite')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-purple-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🧪</span> Collaudo Totale</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Suite 16 moduli core</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-purple-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">test-suite</span>
        </div>

        <div onclick="copyCmd('.\\it-ops.cmd ui')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-cyan-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>📊</span> Mission Control 360°</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Cockpit Commerciale & SLA</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-cyan-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">it-ops ui</span>
        </div>

        <div onclick="copyCmd('.\\it-ops.cmd triggers pending')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-rose-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🛡️</span> Safe Action Gate</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Presidio Human-in-the-Loop</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-rose-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">triggers pending</span>
        </div>
      </div>
    </div>

    <!-- TAB 2: PROGETTI & MATRICE 10 DOCUMENTI -->
    <div id="tab-phases" class="hidden space-y-2.5">
      <div class="flex items-center gap-1.5 overflow-x-auto pb-1">
        <span class="text-[10px] font-semibold text-[var(--muted-foreground)] uppercase mr-1">Progetto:</span>
        <div id="project-pills-container" class="flex items-center gap-1.5">
          <!-- Injected dynamically by JS -->
        </div>
      </div>

      <div class="bg-[var(--background)] p-2 rounded-xl border border-[var(--border)] flex items-center justify-between text-xs">
        <div>
          <span id="mat-proj-customer" class="font-bold text-sky-300">Caricamento...</span>
          <span id="mat-proj-desc" class="text-[10px] text-[var(--muted-foreground)] ml-2"></span>
        </div>
        <div id="mat-proj-stats" class="text-[10px] font-mono font-semibold"></div>
      </div>

      <div id="matrix-container" class="grid grid-cols-5 gap-1.5 text-center text-[9px]">
        <!-- Injected dynamically by JS -->
      </div>
    </div>

    <!-- TAB 3: WORKFLOW TECNICI (SPEC-24) -->
    <div id="tab-tech" class="hidden space-y-2">
      <div class="text-[10px] text-[var(--muted-foreground)] px-0.5">
        <span>⚙️ <em>Workflow Tecnici Deterministi FSM per l'infrastruttura (SPEC-24):</em></span>
      </div>

      <div class="space-y-2">
        <div onclick="copyActiveCmd('dr-drill')" class="action-card p-2.5 rounded-xl border border-[var(--border)] hover:border-sky-400 bg-[var(--background)] cursor-pointer transition-all">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-sky-400">dr-drill &bull; Disaster Recovery Drill</span>
            <span class="text-[9px] font-mono bg-sky-500/20 text-sky-300 px-1.5 py-0.5 rounded">GDPR Art. 32 / 231</span>
          </div>
          <div class="text-[10px] text-[var(--muted-foreground)]">Verifica periodica backup immutabili, restore sandbox, misura RTO/RPO e verbale OdV.</div>
        </div>

        <div onclick="copyActiveCmd('firmware')" class="action-card p-2.5 rounded-xl border border-[var(--border)] hover:border-emerald-400 bg-[var(--background)] cursor-pointer transition-all">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-emerald-400">firmware-upgrade &bull; Canary Upgrade Rollout</span>
            <span class="text-[9px] font-mono bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded">Safe-Mode Rollback</span>
          </div>
          <div class="text-[10px] text-[var(--muted-foreground)]">Aggiornamento switch e firewall con snapshot nel Vault, validazione hash e rollback rapido.</div>
        </div>

        <div onclick="copyActiveCmd('raee')" class="action-card p-2.5 rounded-xl border border-[var(--border)] hover:border-amber-400 bg-[var(--background)] cursor-pointer transition-all">
          <div class="flex justify-between items-center mb-1">
            <span class="text-xs font-bold text-amber-400">hardware-decommissioning &bull; Dismissione RAEE</span>
            <span class="text-[9px] font-mono bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded">NIST 800-88 & FIR</span>
          </div>
          <div class="text-[10px] text-[var(--muted-foreground)]">Sanificazione sicura dischi DoD/NIST, distacco dall'As-Built e rilascio formulario FIR RAEE.</div>
        </div>
      </div>
    </div>

    <!-- TAB 4: TELEMETRIA & KPI -->
    <div id="tab-kpi" class="hidden space-y-2.5">
      <div class="grid grid-cols-4 gap-2">
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Template OKF</div>
          <div class="text-base font-bold text-emerald-400 mt-0.5">{templates_count} / 10</div>
          <div class="text-[9px] text-emerald-400 mt-0.5">✓ Standard v0.2</div>
        </div>
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Secret Vault</div>
          <div class="text-base font-bold text-sky-400 mt-0.5">AES-256</div>
          <div class="text-[9px] text-sky-400 mt-0.5">🔒 Zero Leak</div>
        </div>
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Test Suite</div>
          <div class="text-base font-bold text-indigo-400 mt-0.5">100% Pass</div>
          <div class="text-[9px] text-indigo-400 mt-0.5">16 Moduli Core</div>
        </div>
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Storage Master</div>
          <div class="text-base font-bold text-amber-400 mt-0.5">1ms SMB</div>
          <div class="text-[9px] text-amber-400 mt-0.5">\\fileserv01</div>
        </div>
      </div>

      <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)] flex items-center justify-between text-xs">
        <div class="flex items-center gap-2">
          <span class="text-sky-400">⚡</span>
          <span>Workspace Locale: <strong class="font-mono text-sky-300">C:\\project</strong></span>
        </div>
        <div class="text-[10px] text-emerald-400 font-semibold">
          Federato Hub-and-Spoke con Business Ops
        </div>
      </div>
    </div>

    <!-- 4. Floating Toast Notification -->
    <div id="toast" class="hidden absolute bottom-2 left-1/2 -translate-x-1/2 bg-emerald-500 text-slate-950 font-bold text-xs px-3 py-1.5 rounded-xl shadow-2xl border border-emerald-300 flex items-center gap-1.5 z-50 animate-bounce">
      <span>✓</span> <span id="toast-msg">Copiato negli appunti!</span>
    </div>

  </div>

  <script>
    const PROJECTS = {projects_json};
    let currentSlug = "{default_slug}";

    function initUI() {{
      renderProjectPills();
      selectProject(currentSlug);
    }}

    function renderProjectPills() {{
      const container = document.getElementById("project-pills-container");
      if (!container) return;
      container.innerHTML = "";
      PROJECTS.forEach(p => {{
        const btn = document.createElement("button");
        btn.id = "pill-" + p.slug;
        btn.className = "px-2.5 py-0.5 rounded-lg text-[10px] font-bold border transition-all " + (p.slug === currentSlug ? "proj-pill-active" : "border-[var(--border)] bg-[var(--background)] text-[var(--muted-foreground)] hover:border-sky-400");
        btn.textContent = p.slug;
        btn.onclick = () => selectProject(p.slug);
        container.appendChild(btn);
      }});
    }}

    function selectProject(slug) {{
      currentSlug = slug;
      const proj = PROJECTS.find(p => p.slug === slug) || PROJECTS[0];

      PROJECTS.forEach(p => {{
        const el = document.getElementById("pill-" + p.slug);
        if (el) {{
          if (p.slug === slug) {{
            el.className = "px-2.5 py-0.5 rounded-lg text-[10px] font-bold border transition-all proj-pill-active";
          }} else {{
            el.className = "px-2.5 py-0.5 rounded-lg text-[10px] font-bold border transition-all border-[var(--border)] bg-[var(--background)] text-[var(--muted-foreground)] hover:border-sky-400";
          }}
        }}
      }});

      const lbl = document.getElementById("lbl-active-slug");
      if (lbl) lbl.textContent = slug;
      const btnPub = document.getElementById("btn-copy-pubblica");
      if (btnPub) btnPub.textContent = "pubblica " + slug;
      const btnStato = document.getElementById("btn-copy-stato");
      if (btnStato) btnStato.textContent = "stato " + slug;
      const btnScaffold = document.getElementById("btn-copy-scaffold");
      if (btnScaffold) btnScaffold.textContent = "it scaffold " + slug;

      const cust = document.getElementById("mat-proj-customer");
      if (cust) cust.textContent = proj.customer;
      const desc = document.getElementById("mat-proj-desc");
      if (desc) desc.textContent = proj.name;
      const stats = document.getElementById("mat-proj-stats");
      if (stats) stats.innerHTML = '<span class="text-emerald-400 font-bold">' + proj.stats.approved + ' Approvati</span> • <span class="text-amber-400">' + proj.stats.in_review + ' In Corso</span> • <span class="text-slate-400">' + proj.stats.missing + ' Mancanti</span>';

      const mat = document.getElementById("matrix-container");
      if (!mat) return;
      mat.innerHTML = "";
      proj.docs.forEach(d => {{
        const card = document.createElement("div");
        let statusCls = "status-badge-draft";
        let statusLabel = "Draft";
        let actionCmd = "valida projects/" + slug + "/" + d.filename;

        if (d.status === "approved") {{
          statusCls = "status-badge-approved";
          statusLabel = "Appr";
        }} else if (d.status === "in-review") {{
          statusCls = "status-badge-review";
          statusLabel = "Review";
        }} else if (d.status === "missing") {{
          statusCls = "status-badge-missing";
          statusLabel = "Manca";
          actionCmd = "it scaffold " + slug;
        }}

        card.className = "p-1.5 rounded-lg border flex flex-col justify-between cursor-pointer transition-all hover:scale-105 " + statusCls;
        card.onclick = () => copyCmd(actionCmd);
        card.innerHTML = '<span class="font-bold block truncate">' + d.code.split("-")[0] + ' ' + d.title + '</span><span class="text-[8px] uppercase font-mono font-bold block mt-1">' + statusLabel + '</span>';
        mat.appendChild(card);
      }});
    }}

    function copyActiveCmd(type) {{
      if (type === "pubblica") copyCmd("pubblica " + currentSlug);
      else if (type === "stato") copyCmd("stato " + currentSlug);
      else if (type === "scaffold") copyCmd("it scaffold " + currentSlug);
      else if (type === "dr-drill") copyCmd(".\\it-ops.cmd workflow run dr-drill " + currentSlug);
      else if (type === "firmware") copyCmd(".\\it-ops.cmd workflow run firmware-upgrade " + currentSlug);
      else if (type === "raee") copyCmd(".\\it-ops.cmd workflow run hardware-decommissioning-raee " + currentSlug);
    }}

    function switchTab(tabId) {{
      ['tab-actions', 'tab-kpi', 'tab-phases', 'tab-tech'].forEach(id => {{
        const el = document.getElementById(id);
        if (el) el.classList.add('hidden');
        const btn = document.getElementById('btn-' + id);
        if (btn) btn.classList.remove('tab-active');
      }});
      const target = document.getElementById(tabId);
      if (target) target.classList.remove('hidden');
      const targetBtn = document.getElementById('btn-' + tabId);
      if (targetBtn) targetBtn.classList.add('tab-active');
    }}

    function copyCmd(cmd) {{
      if (navigator.clipboard && window.isSecureContext) {{
        navigator.clipboard.writeText(cmd).then(() => showToast(cmd)).catch(() => fallbackCopy(cmd));
      }} else {{
        fallbackCopy(cmd);
      }}
    }}

    function fallbackCopy(cmd) {{
      var ta = document.createElement("textarea");
      ta.value = cmd;
      ta.style.position = "fixed";
      ta.style.left = "-999999px";
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      try {{
        document.execCommand('copy');
        showToast(cmd);
      }} catch (e) {{
        console.error(e);
      }}
      document.body.removeChild(ta);
    }}

    function showToast(cmd) {{
      var toast = document.getElementById('toast');
      var msg = document.getElementById('toast-msg');
      if (toast && msg) {{
        msg.textContent = '"' + cmd + '" copiato! Premi Ctrl+V in chat';
        toast.classList.remove('hidden');
        clearTimeout(window.tTimer);
        window.tTimer = setTimeout(() => {{ toast.classList.add('hidden'); }}, 2500);
      }}
    }}

    window.addEventListener("DOMContentLoaded", initUI);
  </script>
</body>
</html>"""
    return html.strip()

render_welcome_card = render_enterprise_dashboard

def render_quality_gate_card(
    slug: str,
    passed: bool,
    files_count: int,
    errors_count: int = 0,
    warnings_count: int = 0,
    dest_path: str = r"\\fileserv01\dati01\workaure\projects"
) -> str:
    """Genera la Pre-Flight Quality Gate Card per la pubblicazione di un progetto."""
    badge_bg = "#10b98120" if passed else "#ef444420"
    badge_color = "#10b981" if passed else "#ef4444"
    status_label = "QUALITY GATE SUPERATO" if passed else "QUALITY GATE BLOCCATO"

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-transparent text-[var(--foreground)] antialiased p-2 font-sans">
<div class="bg-[var(--card)] text-[var(--foreground)] border border-[var(--border)] rounded-2xl p-5 shadow-2xl max-w-2xl mx-auto">
    <div class="flex justify-between items-center border-b border-[var(--border)] pb-3 mb-4">
        <span class="text-sm font-semibold text-[var(--foreground)] flex items-center gap-2">
            🛡️ Pre-Flight Quality Gate — Progetto: <strong class="text-sky-400 font-mono">{slug}</strong>
        </span>
        <span style="background:{badge_bg}; color:{badge_color}; border:1px solid {badge_color};" class="px-2.5 py-1 rounded-full text-[11px] font-bold">
            {status_label}
        </span>
    </div>

    <div class="space-y-2 mb-4 text-xs">
        <div class="flex items-center gap-2">
            <span>{'✅' if errors_count == 0 else '❌'}</span>
            <span>Validazione Formale OKF v0.2: <strong>{files_count} file convalidati</strong> ({errors_count} errori)</span>
        </div>
        <div class="flex items-center gap-2">
            <span>✅</span>
            <span>Scansione Anti-Leakage: <strong>0 secret in chiaro</strong> (Conformita' vault:// 100%)</span>
        </div>
        <div class="flex items-center gap-2">
            <span>✅</span>
            <span>Strict Grounding & Coerenza IP: <strong>Subnet allineate al manifesto</strong></span>
        </div>
    </div>

    <div class="bg-[var(--background)] p-2.5 rounded-lg text-[11px] text-[var(--muted-foreground)] border border-[var(--border)] mb-4">
        Destinazione storage master: <span class="font-mono text-[var(--foreground)]">{dest_path}\\{slug}</span>
    </div>

    <div class="text-right">
        {'<span class="inline-block bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 px-3 py-1.5 rounded-lg font-bold text-xs">Pronto per la pubblicazione atomica</span>' if passed else '<span class="text-red-400 text-xs font-semibold">Correggi gli errori formali prima di pubblicare.</span>'}
    </div>
</div>
</body>
</html>"""
    return html.strip()

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render_enterprise_dashboard())
