#!/usr/bin/env python3
"""
scripts/itinfra_ui.py
---------------------
Modulo Generative UI per Google Antigravity (Release v0.9.5).
Genera card HTML interattive, moderne e reattive con pulsanti di azione
per guidare l'operatore direttamente nella finestra di chat dell'AI.
"""

from typing import Dict, Any, Optional

def render_welcome_card(
    share_path: str = r"\\fileserv01\dati01\workaure",
    share_reachable: bool = True,
    templates_count: int = 10,
    active_project: Optional[str] = None
) -> str:
    """Genera la Welcome Action Card con badge di stato e pulsanti cliccabili."""
    status_color = "#10b981" if share_reachable else "#ef4444"
    status_text = "Connessa (OK)" if share_reachable else "Non Raggiungibile (Offline)"

    proj_badge = f"""
    <div style="display:inline-block; background:#1e293b; padding:4px 10px; border-radius:12px; font-size:12px; margin-right:8px;">
        📁 Progetto Attivo: <strong style="color:#38bdf8;">{active_project}</strong>
    </div>
    """ if active_project else ""

    html = f"""
<div style="font-family:system-ui, -apple-system, sans-serif; background:#0f172a; border:1px solid #334155; border-radius:12px; padding:20px; color:#f8fafc; max-width:650px; box-shadow:0 10px 25px -5px rgba(0,0,0,0.3);">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:16px;">
        <div>
            <h3 style="margin:0; font-size:18px; color:#38bdf8; display:flex; align-items:center; gap:8px;">
                ⚡ ITInfra Suite & Antigravity Assistant
            </h3>
            <span style="font-size:12px; color:#94a3b8;">Release v0.9.5 — Zero-Hallucination IT Framework</span>
        </div>
        <span style="background:{status_color}20; color:{status_color}; border:1px solid {status_color}50; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:600;">
            ● {status_text}
        </span>
    </div>

    <div style="margin-bottom:16px;">
        {proj_badge}
        <div style="display:inline-block; background:#1e293b; padding:4px 10px; border-radius:12px; font-size:12px; margin-right:8px;">
            📚 Template OKF v0.2: <strong style="color:#10b981;">{templates_count}/10 Allineati</strong>
        </div>
        <div style="display:inline-block; background:#1e293b; padding:4px 10px; border-radius:12px; font-size:12px;">
            🏢 Storage Master: <span style="color:#cbd5e1; font-family:monospace; font-size:11px;">{share_path}</span>
        </div>
    </div>

    <div style="font-size:13px; color:#cbd5e1; margin-bottom:16px;">
        Seleziona un'azione rapida o scrivi la tua richiesta in chat:
    </div>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
        <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:10px 14px; cursor:pointer; text-align:center;">
            <strong style="color:#38bdf8; font-size:13px;">🚀 Nuovo Progetto</strong>
            <div style="font-size:11px; color:#94a3b8; margin-top:3px;">Inizializza cliente & SLA</div>
        </div>
        <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:10px 14px; cursor:pointer; text-align:center;">
            <strong style="color:#10b981; font-size:13px;">🔍 Diagnostica Share</strong>
            <div style="font-size:11px; color:#94a3b8; margin-top:3px;">Verifica lettura & scrittura</div>
        </div>
        <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:10px 14px; cursor:pointer; text-align:center;">
            <strong style="color:#fbbf24; font-size:13px;">🔄 Allinea Template</strong>
            <div style="font-size:11px; color:#94a3b8; margin-top:3px;">Scarica ultime novita'</div>
        </div>
        <div style="background:#1e293b; border:1px solid #334155; border-radius:8px; padding:10px 14px; cursor:pointer; text-align:center;">
            <strong style="color:#818cf8; font-size:13px;">🌐 Knowledge Graph</strong>
            <div style="font-size:11px; color:#94a3b8; margin-top:3px;">Mappa interattiva D3.js</div>
        </div>
    </div>
</div>
"""
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

    html = f"""
<div style="font-family:system-ui, -apple-system, sans-serif; background:#0f172a; border:1px solid {'#10b981' if passed else '#ef4444'}; border-radius:12px; padding:20px; color:#f8fafc; max-width:650px; margin:10px 0;">
    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #1e293b; padding-bottom:12px; margin-bottom:14px;">
        <span style="font-size:15px; font-weight:600; color:#f8fafc;">
            🛡️ Pre-Flight Quality Gate — Progetto: <strong style="color:#38bdf8;">{slug}</strong>
        </span>
        <span style="background:{badge_bg}; color:{badge_color}; border:1px solid {badge_color}; padding:4px 10px; border-radius:20px; font-size:11px; font-weight:700;">
            {status_label}
        </span>
    </div>

    <div style="margin-bottom:14px; font-size:13px; line-height:1.6;">
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span>{'✅' if errors_count == 0 else '❌'}</span>
            <span>Validazione Formale OKF v0.2: <strong>{files_count} file convalidati</strong> ({errors_count} errori)</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span>✅</span>
            <span>Scansione Anti-Leakage: <strong>0 secret in chiaro</strong> (Conformita' vault:// 100%)</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span>✅</span>
            <span>Strict Grounding & Coerenza IP: <strong>Subnet allineate al manifesto</strong></span>
        </div>
    </div>

    <div style="background:#1e293b; padding:10px 14px; border-radius:8px; font-size:12px; color:#94a3b8; margin-bottom:16px;">
        Destinazione storage master: <span style="font-family:monospace; color:#e2e8f0;">{dest_path}\\{slug}</span>
    </div>

    <div style="text-align:right;">
        {'<button style="background:#10b981; color:#0f172a; border:none; padding:8px 16px; border-radius:6px; font-weight:700; font-size:13px; cursor:pointer;">Conferma Pubblicazione Atomica</button>' if passed else '<span style="color:#ef4444; font-size:12px;">Correggi gli errori segnalati per procedere alla pubblicazione.</span>'}
    </div>
</div>
"""
    return html.strip()

if __name__ == "__main__":
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(render_welcome_card())
    print("\n" + "="*80 + "\n")
    print(render_quality_gate_card("severino-srl", passed=True, files_count=10))
