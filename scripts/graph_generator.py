#!/usr/bin/env python3
"""
Modulo per la generazione di Knowledge Graph interattivi D3.js
a partire da documenti e template con standard OKF v0.2.
"""

import os
import re
import json
import html
from pathlib import Path
from typing import Dict, List, Any, Optional

try:
    import yaml
except ImportError:
    yaml = None

OKF_TYPE_COLORS = {
    "architecture": "#38bdf8",      # Ciano / Sky
    "specification": "#34d399",     # Smeraldo / Green
    "guide": "#fbbf24",             # Ambra / Arancione
    "concept": "#a855f7",           # Viola
    "tool_description": "#f43f5e",  # Rosa / Rosso
    "prompt_skill": "#ec4899",      # Fucsia
    "default": "#94a3b8"            # Grigio Slate
}

RELATION_COLORS = {
    "depends_on": "#ef4444",        # Rosso (Dipendenza forte)
    "extends": "#3b82f6",           # Blu
    "documents": "#10b981",         # Verde
    "implements": "#8b5cf6",        # Viola
    "references": "#94a3b8",        # Grigio chiaro
    "relates_to": "#06b6d4",        # Ciano
    "governs": "#f97316",           # Arancio
    "constrains": "#e11d48",        # Carminio
    "default": "#64748b"
}

def parse_md_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    content = content.lstrip("\ufeff")
    match = re.search(r"^---\r?\n(.*?)\r?\n---\r?\n", content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1)) if yaml else None
    except Exception:
        return None

def build_graph_data(folder_path: Path) -> Dict[str, Any]:
    nodes = []
    links = []
    node_ids = set()
    raw_nodes = []

    md_files = sorted(folder_path.glob("*.md"))
    for file_p in md_files:
        try:
            content = file_p.read_text(encoding="utf-8")
        except Exception:
            continue

        fm = parse_md_frontmatter(content)
        if not fm or not isinstance(fm, dict):
            continue

        doc_id = fm.get("id", file_p.stem)
        doc_type = fm.get("type", "concept")
        title = fm.get("title", file_p.stem)
        phase = fm.get("phase", 0)
        status = fm.get("status", "draft")
        author = fm.get("author", "N/A")
        entities = fm.get("entities", [])
        relations = fm.get("relations", [])
        depends_on = fm.get("depends_on", []) or []
        related_docs = fm.get("related_docs", []) or []
        tags = fm.get("tags", []) or []

        node_color = OKF_TYPE_COLORS.get(doc_type, OKF_TYPE_COLORS["default"])

        node_data = {
            "id": doc_id,
            "filename": file_p.name,
            "title": title,
            "type": doc_type,
            "phase": phase,
            "status": status,
            "author": author,
            "tags": tags,
            "entities": entities,
            "color": node_color,
            "val": 15,
            "relations_raw": relations,
            "depends_on_raw": depends_on,
            "related_docs_raw": related_docs
        }
        raw_nodes.append(node_data)
        node_ids.add(doc_id)

    for n in raw_nodes:
        nodes.append({
            "id": n["id"],
            "filename": n["filename"],
            "title": n["title"],
            "type": n["type"],
            "phase": n["phase"],
            "status": n["status"],
            "author": n["author"],
            "tags": n["tags"],
            "entities": n["entities"],
            "color": n["color"],
            "val": 15
        })

    link_signatures = set()

    for n in raw_nodes:
        src = n["id"]

        for rel in n["relations_raw"]:
            tgt = rel.get("targetId")
            rel_type = rel.get("relationType", "relates_to")
            desc = rel.get("description", "")
            weight = rel.get("weight", 1.0)
            
            actual_tgt = None
            if tgt in node_ids:
                actual_tgt = tgt
            else:
                for candidate in node_ids:
                    if tgt and (tgt in candidate or candidate in tgt):
                        actual_tgt = candidate
                        break

            if actual_tgt:
                sig = (src, actual_tgt, rel_type)
                if sig not in link_signatures:
                    link_signatures.add(sig)
                    links.append({
                        "source": src,
                        "target": actual_tgt,
                        "relationType": rel_type,
                        "description": desc,
                        "weight": weight,
                        "color": RELATION_COLORS.get(rel_type, RELATION_COLORS["default"])
                    })

        for dep in n["depends_on_raw"]:
            actual_dep = None
            if dep in node_ids:
                actual_dep = dep
            else:
                for candidate in node_ids:
                    if dep and (dep in candidate or candidate in dep):
                        actual_dep = candidate
                        break
            if actual_dep:
                sig = (src, actual_dep, "depends_on")
                if sig not in link_signatures:
                    link_signatures.add(sig)
                    links.append({
                        "source": src,
                        "target": actual_dep,
                        "relationType": "depends_on",
                        "description": "Dipendenza architetturale obbligatoria",
                        "weight": 1.0,
                        "color": RELATION_COLORS["depends_on"]
                    })

    degree_map = {n["id"]: 0 for n in nodes}
    for l in links:
        s_id = l["source"]
        t_id = l["target"]
        if s_id in degree_map:
            degree_map[s_id] += 1
        if t_id in degree_map:
            degree_map[t_id] += 1

    for n in nodes:
        deg = degree_map.get(n["id"], 0)
        n["degree"] = deg
        n["val"] = 14 + min(deg * 3, 26)

    return {"nodes": nodes, "links": links}

def generate_graph_html(graph_data: Dict[str, Any], title: str = "ITInfra Knowledge Graph OKF v0.2") -> str:
    graph_json = json.dumps(graph_data, ensure_ascii=False)

    html_code = f"""<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <!-- D3.js v7 da CDN -->
    <script src="https://cdn.jsdelivr.net/npm/d3@7"></script>
    <style>
        :root {{
            --bg-primary: #0b0f19;
            --bg-secondary: #111827;
            --bg-card: #1f2937;
            --border-color: #374151;
            --text-primary: #f9fafb;
            --text-secondary: #9ca3af;
            --accent-cyan: #06b6d4;
            --accent-blue: #3b82f6;
            --font-main: 'Segoe UI', system-ui, -apple-system, sans-serif;
            --font-mono: 'Cascadia Code', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-main);
            overflow: hidden;
            display: flex;
            height: 100vh;
            width: 100vw;
        }}

        #top-bar {{
            position: absolute;
            top: 1rem;
            left: 1rem;
            right: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 20;
            pointer-events: none;
        }}

        .interactive-panel {{
            pointer-events: auto;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.75rem 1.25rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
            display: flex;
            gap: 1rem;
            align-items: center;
        }}

        h1 {{
            font-size: 1.15rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--text-primary);
        }}

        .badge-okf {{
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            color: #fff;
            padding: 0.2rem 0.6rem;
            border-radius: 999px;
            font-size: 0.75rem;
            font-weight: 700;
        }}

        .search-input {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            width: 180px;
            outline: none;
            transition: all 0.2s;
        }}
        .search-input:focus {{
            border-color: var(--accent-cyan);
            width: 220px;
        }}

        .filter-select {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            outline: none;
            cursor: pointer;
        }}

        .btn-action {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-action:hover {{
            background: #374151;
        }}

        #graph-container {{
            flex: 1;
            height: 100%;
            width: 100%;
            cursor: grab;
        }}
        #graph-container:active {{
            cursor: grabbing;
        }}

        .node {{
            cursor: pointer;
            transition: transform 0.2s;
        }}
        .node circle {{
            stroke-width: 2.5px;
            stroke: #ffffff33;
            transition: all 0.3s;
        }}
        .node:hover circle {{
            stroke: #ffffff;
            stroke-width: 3.5px;
            filter: drop-shadow(0 0 10px currentColor);
        }}

        .node text {{
            font-size: 11px;
            font-weight: 500;
            fill: #e2e8f0;
            pointer-events: none;
            text-shadow: 0 2px 4px rgba(0,0,0,0.8);
        }}

        .link {{
            stroke-opacity: 0.65;
            transition: stroke-opacity 0.2s, stroke-width 0.2s;
        }}
        .link.highlighted {{
            stroke-opacity: 1 !important;
            stroke-width: 3px !important;
        }}
        .node.dimmed, .link.dimmed {{
            opacity: 0.15;
        }}

        #sidebar {{
            position: absolute;
            top: 5.5rem;
            right: 1.5rem;
            bottom: 1.5rem;
            width: 380px;
            background: rgba(17, 24, 39, 0.95);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            box-shadow: -10px 10px 30px rgba(0,0,0,0.6);
            display: flex;
            flex-direction: column;
            transform: translateX(450px);
            transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
            z-index: 30;
            padding: 1.5rem;
            overflow-y: auto;
        }}
        #sidebar.open {{
            transform: translateX(0);
        }}

        .close-btn {{
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 1.5rem;
            cursor: pointer;
        }}
        .close-btn:hover {{
            color: var(--text-primary);
        }}

        .sidebar-type {{
            text-transform: uppercase;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }}

        .sidebar-title {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }}

        .sidebar-id {{
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--accent-cyan);
            word-break: break-all;
            background: #0f172a;
            padding: 0.3rem 0.5rem;
            border-radius: 4px;
            border: 1px solid var(--border-color);
            margin-bottom: 1rem;
        }}

        .sidebar-section {{
            margin-top: 1.25rem;
            border-top: 1px solid var(--border-color);
            padding-top: 1rem;
        }}

        .sidebar-section h4 {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            letter-spacing: 0.05em;
        }}

        .entity-chip {{
            display: inline-block;
            background: #1e293b;
            border: 1px solid #334155;
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
            margin: 0.2rem;
        }}
        .entity-chip strong {{
            color: var(--accent-cyan);
        }}

        .relation-item {{
            background: #0f172a;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.6rem;
            margin-bottom: 0.5rem;
            font-size: 0.8rem;
        }}
        .relation-type {{
            font-weight: 700;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            display: inline-block;
            font-size: 0.7rem;
            margin-bottom: 0.3rem;
        }}

        #legend {{
            position: absolute;
            bottom: 1.5rem;
            left: 1.5rem;
            background: rgba(17, 24, 39, 0.85);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 0.85rem 1.25rem;
            z-index: 10;
            font-size: 0.75rem;
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        .legend-line {{
            width: 16px;
            height: 3px;
            border-radius: 2px;
        }}
    </style>
</head>
<body>

<div id="top-bar">
    <div class="interactive-panel">
        <h1>
            <span>🕸️</span> {html.escape(title)}
            <span class="badge-okf">OKF v0.2 Graph</span>
        </h1>
    </div>

    <div class="interactive-panel">
        <input type="text" id="search-box" class="search-input" placeholder="🔍 Cerca nodo o entità...">
        <select id="type-filter" class="filter-select">
            <option value="ALL">Tutti i Tipi</option>
            <option value="architecture">Architecture (HLD, LLD, As-Built)</option>
            <option value="specification">Specification (RSD, ATP, Handover)</option>
            <option value="guide">Guide (MOP, Rollback, SOP, RCA)</option>
            <option value="concept">Concept & Index</option>
        </select>
        <button class="btn-action" onclick="resetZoom()">Centra Vista</button>
    </div>
</div>

<div id="graph-container"></div>

<!-- Sidebar Informativa -->
<div id="sidebar">
    <button class="close-btn" onclick="closeSidebar()">&times;</button>
    <div id="sidebar-content"></div>
</div>

<!-- Legenda Ontologica -->
<div id="legend">
    <div style="font-weight: 700; margin-bottom: 0.2rem; color: #cbd5e1;">Tipi Documentali OKF</div>
    <div class="legend-item"><div class="legend-color" style="background: #38bdf8;"></div> Architecture (HLD, LLD, As-Built)</div>
    <div class="legend-item"><div class="legend-color" style="background: #34d399;"></div> Specification (RSD, ATP, Handover)</div>
    <div class="legend-item"><div class="legend-color" style="background: #fbbf24;"></div> Guide (MOP, Rollback, SOP, RCA)</div>
    <div style="font-weight: 700; margin-top: 0.5rem; margin-bottom: 0.2rem; color: #cbd5e1;">Archi Semantici</div>
    <div class="legend-item"><div class="legend-line" style="background: #ef4444;"></div> depends_on (Forte)</div>
    <div class="legend-item"><div class="legend-line" style="background: #3b82f6;"></div> extends (Estensione)</div>
    <div class="legend-item"><div class="legend-line" style="background: #10b981;"></div> documents (Attestazione)</div>
    <div class="legend-item"><div class="legend-line" style="background: #94a3b8;"></div> references / relates_to</div>
</div>

<script>
    const graphData = {graph_json};

    const container = document.getElementById('graph-container');
    const width = window.innerWidth;
    const height = window.innerHeight;

    const svg = d3.select("#graph-container")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr("viewBox", [0, 0, width, height]);

    const g = svg.append("g");

    const zoom = d3.zoom()
        .scaleExtent([0.15, 4])
        .on("zoom", (event) => {{
            g.attr("transform", event.transform);
        }});

    svg.call(zoom);

    function resetZoom() {{
        svg.transition().duration(750).call(
            zoom.transform,
            d3.zoomIdentity.translate(width / 2, height / 2).scale(0.85).translate(-width / 2, -height / 2)
        );
    }}

    const defs = svg.append("defs");
    const relationColors = {json.dumps(RELATION_COLORS)};

    Object.entries(relationColors).forEach(([rel, col]) => {{
        defs.append("marker")
            .attr("id", "arrow-" + rel)
            .attr("viewBox", "0 -5 10 10")
            .attr("refX", 22)
            .attr("refY", 0)
            .attr("markerWidth", 6)
            .attr("markerHeight", 6)
            .attr("orient", "auto")
            .append("path")
            .attr("d", "M0,-5L10,0L0,5")
            .attr("fill", col);
    }});

    const simulation = d3.forceSimulation(graphData.nodes)
        .force("link", d3.forceLink(graphData.links).id(d => d.id).distance(140))
        .force("charge", d3.forceManyBody().strength(-550))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collision", d3.forceCollide().radius(d => d.val + 25));

    const link = g.append("g")
        .selectAll("line")
        .data(graphData.links)
        .join("line")
        .attr("class", "link")
        .attr("stroke", d => d.color || "#64748b")
        .attr("stroke-width", d => Math.max(1.5, (d.weight || 1) * 2))
        .attr("marker-end", d => `url(#arrow-${{d.relationType || 'default'}}`);

    const node = g.append("g")
        .selectAll("g")
        .data(graphData.nodes)
        .join("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    node.append("circle")
        .attr("r", d => d.val)
        .attr("fill", d => d.color);

    node.append("text")
        .attr("dx", d => d.val + 8)
        .attr("dy", "0.35em")
        .text(d => d.filename.replace(".md", ""));

    simulation.on("tick", () => {{
        link
            .attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        node
            .attr("transform", d => `translate(${{d.x}},${{d.y}})`);
    }});

    function dragstarted(event, d) {{
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    }}
    function dragged(event, d) {{
        d.fx = event.x;
        d.fy = event.y;
    }}
    function dragended(event, d) {{
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
    }}

    let selectedNode = null;

    node.on("mouseover", (event, d) => {{
        if (selectedNode) return;
        const neighborIds = new Set();
        neighborIds.add(d.id);

        link.each(function(l) {{
            if (l.source.id === d.id || l.target.id === d.id) {{
                neighborIds.add(l.source.id);
                neighborIds.add(l.target.id);
                d3.select(this).classed("highlighted", true);
            }} else {{
                d3.select(this).classed("dimmed", true);
            }}
        }});

        node.classed("dimmed", n => !neighborIds.has(n.id));
    }});

    node.on("mouseout", () => {{
        if (selectedNode) return;
        link.classed("highlighted", false).classed("dimmed", false);
        node.classed("dimmed", false);
    }});

    node.on("click", (event, d) => {{
        event.stopPropagation();
        selectedNode = d;
        showSidebar(d);

        const neighborIds = new Set([d.id]);
        link.each(function(l) {{
            if (l.source.id === d.id || l.target.id === d.id) {{
                neighborIds.add(l.source.id);
                neighborIds.add(l.target.id);
                d3.select(this).classed("highlighted", true).classed("dimmed", false);
            }} else {{
                d3.select(this).classed("highlighted", false).classed("dimmed", true);
            }}
        }});
        node.classed("dimmed", n => !neighborIds.has(n.id));
    }});

    svg.on("click", () => {{
        selectedNode = null;
        closeSidebar();
        link.classed("highlighted", false).classed("dimmed", false);
        node.classed("dimmed", false);
    }});

    function showSidebar(d) {{
        const sidebar = document.getElementById("sidebar");
        const content = document.getElementById("sidebar-content");

        const outgoing = graphData.links.filter(l => l.source.id === d.id || l.source === d.id);
        const incoming = graphData.links.filter(l => l.target.id === d.id || l.target === d.id);

        let entitiesHtml = (d.entities && d.entities.length > 0)
            ? d.entities.map(e => `<span class="entity-chip"><strong>${{escapeHtml(e.name)}}</strong> (${{e.type}})</span>`).join(" ")
            : '<span style="color:#64748b; font-size:0.8rem;">Nessuna entità registrata</span>';

        let outgoingHtml = outgoing.length > 0 ? outgoing.map(l => {{
            const targetName = l.target.filename || l.target.id || l.target;
            return `<div class="relation-item">
                <span class="relation-type" style="background:${{l.color || '#3b82f6'}}22; color:${{l.color || '#3b82f6'}}">${{l.relationType}}</span>
                &rarr; <strong>${{escapeHtml(targetName)}}</strong>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:2px;">${{escapeHtml(l.description || '')}}</div>
            </div>`;
        }}).join("") : '<div style="color:#64748b; font-size:0.8rem;">Nessuna relazione in uscita</div>';

        let incomingHtml = incoming.length > 0 ? incoming.map(l => {{
            const sourceName = l.source.filename || l.source.id || l.source;
            return `<div class="relation-item">
                <strong>${{escapeHtml(sourceName)}}</strong>
                &rarr; <span class="relation-type" style="background:${{l.color || '#3b82f6'}}22; color:${{l.color || '#3b82f6'}}">${{l.relationType}}</span>
                <div style="color:#94a3b8; font-size:0.75rem; margin-top:2px;">${{escapeHtml(l.description || '')}}</div>
            </div>`;
        }}).join("") : '<div style="color:#64748b; font-size:0.8rem;">Nessuna relazione in entrata</div>';

        content.innerHTML = `
            <span class="sidebar-type" style="background:${{d.color}}22; color:${{d.color}}">${{d.type}} — Fase ${{d.phase}}</span>
            <div class="sidebar-title">${{escapeHtml(d.title)}}</div>
            <div class="sidebar-id">${{escapeHtml(d.id)}}</div>
            <div style="font-size:0.85rem; color:#94a3b8; margin-bottom:1rem;">
                Autore: <strong>${{escapeHtml(d.author)}}</strong> | Stato: <strong>${{escapeHtml(d.status)}}</strong>
            </div>

            <div class="sidebar-section">
                <h4>Entità Ontologiche (${{d.entities ? d.entities.length : 0}})</h4>
                ${{entitiesHtml}}
            </div>

            <div class="sidebar-section">
                <h4>Relazioni in Uscita (${{outgoing.length}})</h4>
                ${{outgoingHtml}}
            </div>

            <div class="sidebar-section">
                <h4>Relazioni in Entrata (${{incoming.length}})</h4>
                ${{incomingHtml}}
            </div>
        `;

        sidebar.classList.add("open");
    }}

    function closeSidebar() {{
        document.getElementById("sidebar").classList.remove("open");
    }}

    function escapeHtml(str) {{
        if (!str) return '';
        return String(str).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }}

    document.getElementById("search-box").addEventListener("input", (e) => {{
        const term = e.target.value.toLowerCase().trim();
        if (!term) {{
            node.classed("dimmed", false);
            link.classed("dimmed", false);
            return;
        }}

        const matchedIds = new Set();
        graphData.nodes.forEach(n => {{
            const inTitle = n.title.toLowerCase().includes(term);
            const inId = n.id.toLowerCase().includes(term);
            const inFilename = n.filename.toLowerCase().includes(term);
            const inEntities = n.entities && n.entities.some(ent => ent.name.toLowerCase().includes(term));
            if (inTitle || inId || inFilename || inEntities) {{
                matchedIds.add(n.id);
            }}
        }});

        node.classed("dimmed", n => !matchedIds.has(n.id));
        link.classed("dimmed", l => !matchedIds.has(l.source.id) || !matchedIds.has(l.target.id));
    }});

    document.getElementById("type-filter").addEventListener("change", (e) => {{
        const selectedType = e.target.value;
        if (selectedType === "ALL") {{
            node.classed("dimmed", false);
            link.classed("dimmed", false);
            return;
        }}
        const matchedIds = new Set(graphData.nodes.filter(n => n.type === selectedType).map(n => n.id));
        node.classed("dimmed", n => !matchedIds.has(n.id));
        link.classed("dimmed", l => !matchedIds.has(l.source.id) || !matchedIds.has(l.target.id));
    }});

    resetZoom();
</script>

</body>
</html>
"""
    return html_code
