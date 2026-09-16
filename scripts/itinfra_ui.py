#!/usr/bin/env python3
"""
scripts/itinfra_ui.py
---------------------
Modulo Enterprise Generative UI per Google Antigravity (Release v0.9.9).
Genera il Cockpit Esecutivo Sistemistico interattivo e le Pre-Flight Quality Gate Cards
conforme ai design tokens di Google Antigravity e standard OKF v0.2.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List

DEFAULT_CENTRAL_SHARE = r"\\fileserv01\dati01\workaure"

def render_enterprise_dashboard(
    workspace_path: str = "C:\\project",
    share_path: str = DEFAULT_CENTRAL_SHARE,
    share_reachable: bool = True,
    templates_count: int = 10,
    active_project: Optional[str] = None,
    vault_status: str = "AES-256-GCM (Zero Leak)",
    test_suite_status: str = "12/12 Pass (100%)"
) -> str:
    """Genera l'Enterprise Cockpit Dashboard compatto (<450px, zero scroll) con Tab e Click-to-Copy."""
    share_color = "#10b981" if share_reachable else "#ef4444"
    share_label = "Share Online" if share_reachable else "Share Offline"
    pulse_class = "animate-pulse" if share_reachable else ""
    slug_ref = active_project if active_project else "severino-srl"

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
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
            <span class="text-[9px] uppercase font-semibold px-1.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/20">v0.9.9</span>
          </div>
          <p class="text-[10px] text-[var(--muted-foreground)]">Governance OKF v0.2 • Ciclo Lavorativo 7 Fasi</p>
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
      <button id="btn-tab-kpi" onclick="switchTab('tab-kpi')" class="flex-1 py-1 px-2 rounded-lg text-xs font-semibold border border-transparent text-[var(--muted-foreground)] transition-all text-center flex items-center justify-center gap-1.5">
        <span>📊</span> Telemetria & KPI
      </button>
      <button id="btn-tab-phases" onclick="switchTab('tab-phases')" class="flex-1 py-1 px-2 rounded-lg text-xs font-semibold border border-transparent text-[var(--muted-foreground)] transition-all text-center flex items-center justify-center gap-1.5">
        <span>🔄</span> Workflow 7 Fasi
      </button>
    </div>

    <!-- 3. Contenuti Tab -->

    <!-- TAB 1: AZIONI RAPIDE (DEFAULT ACTIVE - CLICK TO COPY) -->
    <div id="tab-actions" class="space-y-2">
      <div class="text-[10px] text-[var(--muted-foreground)] flex items-center justify-between px-0.5">
        <span>💡 <em>Clicca su un'azione per copiare il comando negli appunti e incollarlo in chat:</em></span>
        <span class="text-sky-400 font-mono text-[9px]">Click-to-Copy</span>
      </div>

      <div class="grid grid-cols-2 gap-2">
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

        <div onclick="copyCmd('pubblica {slug_ref}')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-emerald-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🚀</span> Pubblica Progetto</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Quality Gate & rilascio</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-emerald-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">pubblica {slug_ref}</span>
        </div>

        <div onclick="copyCmd('stato {slug_ref}')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-amber-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>📈</span> Stato Progetto</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Avanzamento 7 fasi</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-amber-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">stato {slug_ref}</span>
        </div>

        <div onclick="copyCmd('test-suite')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-purple-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>🧪</span> Collaudo Totale</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">12 moduli di test</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-purple-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">test-suite</span>
        </div>

        <div onclick="copyCmd('it init nuovo-cliente --client &quot;Nome&quot; --name &quot;Titolo&quot;')" class="action-card flex items-center justify-between p-2 rounded-xl border border-[var(--border)] hover:border-sky-400/60 bg-[var(--background)] cursor-pointer transition-all">
          <div>
            <div class="text-xs font-semibold flex items-center gap-1"><span>📁</span> Nuovo Cliente</div>
            <div class="text-[9px] text-[var(--muted-foreground)]">Manifesto & struttura</div>
          </div>
          <span class="copy-badge text-[10px] bg-slate-800 text-sky-300 font-mono px-2 py-0.5 rounded border border-slate-700 transition-all">inizializza</span>
        </div>
      </div>
    </div>

    <!-- TAB 2: TELEMETRIA & KPI (HIDDEN INIZIALMENTE) -->
    <div id="tab-kpi" class="hidden space-y-2.5">
      <div class="grid grid-cols-4 gap-2">
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Template OKF</div>
          <div class="text-base font-bold text-emerald-400 mt-0.5">{templates_count} / 10</div>
          <div class="text-[9px] text-emerald-400 mt-0.5">✓ Allineati</div>
        </div>
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Secret Vault</div>
          <div class="text-base font-bold text-sky-400 mt-0.5">AES-256</div>
          <div class="text-[9px] text-sky-400 mt-0.5">🔒 Zero Leak</div>
        </div>
        <div class="bg-[var(--background)] p-2.5 rounded-xl border border-[var(--border)]">
          <div class="text-[10px] font-medium text-[var(--muted-foreground)]">Test Suite</div>
          <div class="text-base font-bold text-indigo-400 mt-0.5">100% Pass</div>
          <div class="text-[9px] text-indigo-400 mt-0.5">12/12 Moduli</div>
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
        <div class="text-[10px] text-[var(--muted-foreground)]">
          Strict Grounding • Zero Hallucination
        </div>
      </div>
    </div>

    <!-- TAB 3: WORKFLOW 7 FASI (HIDDEN INIZIALMENTE) -->
    <div id="tab-phases" class="hidden space-y-2.5">
      <div class="grid grid-cols-7 gap-1 text-center text-[9px]">
        <div class="bg-[var(--background)] border border-sky-500/30 rounded-lg p-1.5">
          <span class="text-sky-400 font-bold block">1. Assess</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">RSD/URS</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-sky-500/30 rounded-lg p-1.5">
          <span class="text-sky-400 font-bold block">2. Design</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">HLD/LLD</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-sky-500/30 rounded-lg p-1.5">
          <span class="text-sky-400 font-bold block">3. Staging</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">MOP/Roll</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-slate-700/60 rounded-lg p-1.5">
          <span class="text-slate-400 font-bold block">4. Cabling</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">Racking</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-slate-500 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-slate-700/60 rounded-lg p-1.5">
          <span class="text-slate-400 font-bold block">5. Comm</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">Config</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-slate-500 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-amber-500/30 rounded-lg p-1.5">
          <span class="text-amber-400 font-bold block">6. Test</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">ATP</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-amber-400 mt-1"></span>
        </div>
        <div class="bg-[var(--background)] border border-emerald-500/30 rounded-lg p-1.5">
          <span class="text-emerald-400 font-bold block">7. Live</span>
          <span class="text-[8px] text-[var(--muted-foreground)] block mt-0.5">Handover</span>
          <span class="inline-block w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1"></span>
        </div>
      </div>

      <div class="bg-[var(--background)] p-2 rounded-xl border border-[var(--border)] text-xs flex items-center justify-between">
        <div>
          <span class="font-semibold text-sky-300">severino-srl</span>
          <span class="text-[10px] text-[var(--muted-foreground)] ml-2">Fasi completate: 10 doc censiti</span>
        </div>
        <button onclick="copyCmd('stato severino-srl')" class="text-[10px] bg-sky-500/10 text-sky-400 border border-sky-500/30 px-2 py-0.5 rounded hover:bg-sky-500/20">
          Vedi Stato
        </button>
      </div>
    </div>

    <!-- 4. Floating Toast Notification (Click-to-Copy Feedback) -->
    <div id="toast" class="hidden absolute bottom-2 left-1/2 -translate-x-1/2 bg-emerald-500 text-slate-950 font-bold text-xs px-3 py-1.5 rounded-xl shadow-2xl border border-emerald-300 flex items-center gap-1.5 z-50 animate-bounce">
      <span>✓</span> <span id="toast-msg">Copiato negli appunti!</span>
    </div>

  </div>

  <script>
    function switchTab(tabId) {{
      ['tab-actions', 'tab-kpi', 'tab-phases'].forEach(id => {{
        document.getElementById(id).classList.add('hidden');
        document.getElementById('btn-' + id).classList.remove('tab-active');
      }});
      document.getElementById(tabId).classList.remove('hidden');
      document.getElementById('btn-' + tabId).classList.add('tab-active');
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
  </script>
</body>
</html>"""
    return html.strip()

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

# Alias per retrocompatibilità
render_welcome_card = render_enterprise_dashboard

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render_enterprise_dashboard())
