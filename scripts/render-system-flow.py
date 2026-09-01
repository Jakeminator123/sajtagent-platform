"""Render deterministic Markdown and SVG projections from the canonical flow model."""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict, deque
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "system-model" / "platform-flow-v1.json"
OUTPUT_PATH = ROOT / "docs" / "system-flow.md"
SVG_OUTPUT_PATH = ROOT / "docs" / "assets" / "system-flow.svg"
sys.path.insert(0, str(ROOT / "control-panel"))

from flow_model import load_flow_model, view_edges  # noqa: E402

CHANNEL_COLORS = {
    "intent": "#2563eb",
    "execution": "#7c3aed",
    "evidence": "#059669",
    "projection": "#d97706",
}
STATUS_STYLES = {
    "planned": ("#f3e8ff", "#7e22ce"),
    "prototype": ("#fef3c7", "#b45309"),
    "contracted": ("#dbeafe", "#1d4ed8"),
    "implemented": ("#dcfce7", "#15803d"),
    "verified": ("#d1fae5", "#047857"),
}


def mermaid_id(value: str) -> str:
    return "n_" + re.sub(r"[^a-zA-Z0-9_]", "_", value)


def render_mermaid(model: dict, view: dict) -> list[str]:
    nodes = {node["id"]: node for node in model["nodes"]}
    lines = [f"flowchart {view['orientation']}"]
    emitted: set[str] = set()
    for edge in view_edges(model, view["id"]):
        for node_id in (edge["from"], edge["to"]):
            if node_id not in emitted:
                node = nodes[node_id]
                label = f"{node['label']}<br/>{node['owner']} · {node['status']}"
                lines.append(f'    {mermaid_id(node_id)}["{label}"]')
                emitted.add(node_id)
        lines.append(
            f'    {mermaid_id(edge["from"])} -->|"{edge["contract"]}"| {mermaid_id(edge["to"])}'
        )
    return lines


def topological_levels(edges: list[dict]) -> dict[str, int]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = defaultdict(int)
    nodes: set[str] = set()
    for edge in edges:
        source, target = edge["from"], edge["to"]
        adjacency[source].append(target)
        indegree[target] += 1
        nodes.update((source, target))
    queue = deque(sorted(node for node in nodes if indegree[node] == 0))
    levels = {node: 0 for node in queue}
    visited = 0
    while queue:
        source = queue.popleft()
        visited += 1
        for target in sorted(adjacency[source]):
            levels[target] = max(levels.get(target, 0), levels[source] + 1)
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(nodes):
        raise ValueError("SVG projection requires an acyclic view")
    return levels


def short_label(value: str, limit: int = 38) -> str:
    return value if len(value) <= limit else value[: limit - 1].rstrip() + "…"


def render_svg(model: dict) -> str:
    width, height = 1840, 1190
    panel_width, panel_height = 860, 1010
    panel_y = 105
    node_width, node_height = 200, 68
    level_gap = 120
    node_by_id = {node["id"]: node for node in model["nodes"]}
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Sajtagent systemflöde</title>',
        '<desc id="desc">Kommandon går nedåt genom produktcontroller och runtime. Verifierbara kvitton och resultat går nedifrån och upp till användaren.</desc>',
        '<rect width="1840" height="1190" fill="#ffffff"/>',
        '<text x="40" y="42" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#111827">Sajtagent systemflöde</text>',
        '<text x="40" y="70" font-family="Arial, sans-serif" font-size="14" fill="#4b5563">Genererad från system-model/platform-flow-v1.json · modellen är testfacit</text>',
        '<defs>',
    ]
    for channel, color in CHANNEL_COLORS.items():
        lines.extend(
            [
                f'<marker id="arrow-{channel}" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">',
                f'<path d="M0,0 L0,6 L9,3 z" fill="{color}"/>',
                '</marker>',
            ]
        )
    lines.append('</defs>')

    for panel_index, view in enumerate(model["views"][:2]):
        panel_x = 40 + panel_index * 920
        edges = view_edges(model, view["id"])
        levels = topological_levels(edges)
        grouped: dict[int, list[str]] = defaultdict(list)
        for node_id, level in levels.items():
            grouped[level].append(node_id)
        positions: dict[str, tuple[float, float]] = {}
        for level, node_ids in grouped.items():
            ordered_ids = sorted(node_ids)
            for index, node_id in enumerate(ordered_ids):
                x = panel_x + (index + 1) * panel_width / (len(ordered_ids) + 1)
                if view["orientation"] == "BT":
                    y = panel_y + panel_height - 80 - level * level_gap
                else:
                    y = panel_y + 100 + level * level_gap
                positions[node_id] = (x, y)

        lines.extend(
            [
                f'<rect x="{panel_x}" y="{panel_y}" width="{panel_width}" height="{panel_height}" rx="18" fill="#f8fafc" stroke="#d1d5db"/>',
                f'<text x="{panel_x + 24}" y="{panel_y + 38}" font-family="Arial, sans-serif" font-size="19" font-weight="700" fill="#111827">{escape(view["label"])}</text>',
            ]
        )
        for edge in edges:
            source_x, source_y = positions[edge["from"]]
            target_x, target_y = positions[edge["to"]]
            direction = 1 if target_y > source_y else -1
            start_y = source_y + direction * node_height / 2
            end_y = target_y - direction * node_height / 2
            control_y = (start_y + end_y) / 2
            channel = edge["channel"]
            color = CHANNEL_COLORS[channel]
            label = short_label(edge["contract"])
            if view["orientation"] == "BT":
                label_x = source_x * 0.75 + target_x * 0.25
            else:
                label_x = source_x * 0.25 + target_x * 0.75
            label_y = (start_y + end_y) / 2 - 7
            label_width = max(64, len(label) * 6.2 + 14)
            lines.extend(
                [
                    f'<path d="M {source_x:.1f} {start_y:.1f} C {source_x:.1f} {control_y:.1f}, {target_x:.1f} {control_y:.1f}, {target_x:.1f} {end_y:.1f}" fill="none" stroke="{color}" stroke-width="2" marker-end="url(#arrow-{channel})"/>',
                    f'<rect x="{label_x - label_width / 2:.1f}" y="{label_y - 13:.1f}" width="{label_width:.1f}" height="19" rx="4" fill="#ffffff" opacity="0.94"/>',
                    f'<text x="{label_x:.1f}" y="{label_y:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#374151">{escape(label)}</text>',
                ]
            )
        for node_id, (x, y) in positions.items():
            node = node_by_id[node_id]
            fill, border = STATUS_STYLES[node["status"]]
            lines.extend(
                [
                    f'<rect x="{x - node_width / 2:.1f}" y="{y - node_height / 2:.1f}" width="{node_width}" height="{node_height}" rx="10" fill="{fill}" stroke="{border}" stroke-width="1.5"/>',
                    f'<text x="{x:.1f}" y="{y - 5:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="13" font-weight="700" fill="#111827">{escape(short_label(node["label"], 29))}</text>',
                    f'<text x="{x:.1f}" y="{y + 17:.1f}" text-anchor="middle" font-family="Arial, sans-serif" font-size="11" fill="#4b5563">{escape(node["owner"])} · {escape(node["status"])}</text>',
                ]
            )

    legend_y = 1155
    legend_x = 42
    for channel, color in CHANNEL_COLORS.items():
        label = model["channels"][channel].split(".", 1)[0]
        lines.extend(
            [
                f'<line x1="{legend_x}" y1="{legend_y}" x2="{legend_x + 30}" y2="{legend_y}" stroke="{color}" stroke-width="3"/>',
                f'<text x="{legend_x + 40}" y="{legend_y + 4}" font-family="Arial, sans-serif" font-size="12" fill="#374151">{escape(channel)} — {escape(label)}</text>',
            ]
        )
        legend_x += 440
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def render_markdown(model: dict) -> str:
    lines = [
        "# Sajtagent systemflöde",
        "",
        "<!-- Generated by scripts/render-system-flow.py from system-model/platform-flow-v1.json. -->",
        "",
        "Den maskinläsbara modellen är auktoritativ. Diagrammen visar samma flöde i två riktningar: kommandon nedåt och verifierbara bevis nedifrån och upp.",
        "",
        "![Sajtagent systemflöde](assets/system-flow.svg)",
        "",
    ]
    for view in model["views"][:2]:
        lines.extend([f"## {view['label']}", "", "```mermaid", *render_mermaid(model, view), "```", ""])

    lines.extend(
        [
            "## Felkarta",
            "",
            "Välj en felande nod i kontrollpanelens vy **Systemflöde** för att se alla påverkade steg och vilket repo som äger diagnosen.",
            "",
            "| Kod | Nod | Upptäcks av | Synligt symptom |",
            "| --- | --- | --- | --- |",
        ]
    )
    for node in model["nodes"]:
        failure = node["failure"]
        lines.append(
            f"| `{failure['code']}` | {node['label']} | `{failure['detectedBy']}` | {failure['symptom']} |"
        )
    lines.extend(
        [
            "",
            "## Så ändras modellen",
            "",
            "1. Ändra `system-model/platform-flow-v1.json`.",
            "2. Kör `python scripts/render-system-flow.py`.",
            "3. Kör `python scripts/validate-system-flow.py` och testerna.",
            "4. En PR eller push får inte passera om modellen är ogiltig eller den genererade dokumentationen har driftat.",
            "",
            "Kortens detaljer ägs av `sajtagent-site/system-model/card-flow-v1.json` och visas som en separat dynamisk vy i den lokala kontrollpanelen.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    model = load_flow_model(MODEL_PATH)
    expected = render_markdown(model)
    expected_svg = render_svg(model)
    if args.check:
        actual = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else ""
        if actual != expected:
            raise SystemExit("docs/system-flow.md is stale; run python scripts/render-system-flow.py")
        actual_svg = SVG_OUTPUT_PATH.read_text(encoding="utf-8") if SVG_OUTPUT_PATH.exists() else ""
        if actual_svg != expected_svg:
            raise SystemExit("docs/assets/system-flow.svg is stale; run python scripts/render-system-flow.py")
        print("OK: generated system-flow Markdown and SVG match the canonical model")
        return
    SVG_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(expected, encoding="utf-8", newline="\n")
    SVG_OUTPUT_PATH.write_text(expected_svg, encoding="utf-8", newline="\n")
    print(f"Wrote {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Wrote {SVG_OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
