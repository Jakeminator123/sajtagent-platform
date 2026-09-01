"""Pure helpers for validating and rendering Sajtagent flow models."""

from __future__ import annotations

import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any


def load_flow_model(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        model = json.load(handle)
    errors = validate_flow_model(model)
    if errors:
        raise ValueError("Invalid flow model:\n- " + "\n- ".join(errors))
    return model


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        seen.add(value)
    return duplicates


def validate_flow_model(model: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if model.get("schemaVersion") != 1:
        errors.append("schemaVersion must be 1")

    nodes = model.get("nodes")
    edges = model.get("edges")
    views = model.get("views")
    if not isinstance(nodes, list) or not nodes:
        return errors + ["nodes must be a non-empty list"]
    if not isinstance(edges, list) or not edges:
        return errors + ["edges must be a non-empty list"]
    if not isinstance(views, list) or not views:
        return errors + ["views must be a non-empty list"]

    node_ids = [item.get("id") for item in nodes if isinstance(item, dict)]
    edge_ids = [item.get("id") for item in edges if isinstance(item, dict)]
    view_ids = [item.get("id") for item in views if isinstance(item, dict)]
    for label, values in (("node", node_ids), ("edge", edge_ids), ("view", view_ids)):
        if any(not isinstance(value, str) or not value for value in values):
            errors.append(f"every {label} must have a non-empty string id")
        for duplicate in sorted(_duplicates([value for value in values if isinstance(value, str)])):
            errors.append(f"duplicate {label} id: {duplicate}")

    known_nodes = set(node_ids)
    known_edges = set(edge_ids)
    known_owners = set(model.get("owners", []))
    known_statuses = set(model.get("statuses", []))
    known_channels = set(model.get("channels", {}).keys())
    known_layers = {item.get("id") for item in model.get("layers", [])}
    failure_codes: list[str] = []

    for node in nodes:
        node_id = node.get("id", "<missing>")
        for field in ("label", "kind", "owner", "status", "summary"):
            if not isinstance(node.get(field), str) or not node[field].strip():
                errors.append(f"node {node_id} is missing {field}")
        if node.get("owner") not in known_owners:
            errors.append(f"node {node_id} has unknown owner {node.get('owner')}")
        if node.get("status") not in known_statuses:
            errors.append(f"node {node_id} has unknown status {node.get('status')}")
        if node.get("layer") not in known_layers:
            errors.append(f"node {node_id} has unknown layer {node.get('layer')}")
        failure = node.get("failure")
        if not isinstance(failure, dict):
            errors.append(f"node {node_id} has no failure contract")
            continue
        for field in ("code", "symptom", "detectedBy"):
            if not isinstance(failure.get(field), str) or not failure[field].strip():
                errors.append(f"node {node_id} failure is missing {field}")
        if isinstance(failure.get("code"), str):
            failure_codes.append(failure["code"])

    for duplicate in sorted(_duplicates(failure_codes)):
        errors.append(f"duplicate failure code: {duplicate}")

    edge_by_id = {edge.get("id"): edge for edge in edges}
    for edge in edges:
        edge_id = edge.get("id", "<missing>")
        if edge.get("from") not in known_nodes:
            errors.append(f"edge {edge_id} has unknown from node {edge.get('from')}")
        if edge.get("to") not in known_nodes:
            errors.append(f"edge {edge_id} has unknown to node {edge.get('to')}")
        if edge.get("channel") not in known_channels:
            errors.append(f"edge {edge_id} has unknown channel {edge.get('channel')}")
        if not isinstance(edge.get("contract"), str) or not edge["contract"].strip():
            errors.append(f"edge {edge_id} has no contract")

    for view in views:
        view_id = view.get("id", "<missing>")
        if view.get("orientation") not in {"TB", "BT", "LR", "RL"}:
            errors.append(f"view {view_id} has invalid orientation")
        selected = view.get("edgeIds")
        if not isinstance(selected, list) or not selected:
            errors.append(f"view {view_id} must select at least one edge")
            continue
        invalid_edges = [edge_id for edge_id in selected if edge_id not in known_edges]
        for edge_id in invalid_edges:
            errors.append(f"view {view_id} references unknown edge {edge_id}")
        if not invalid_edges and _has_cycle([edge_by_id[edge_id] for edge_id in selected]):
            errors.append(f"view {view_id} must be acyclic")

    return errors


def _has_cycle(edges: list[dict[str, Any]]) -> bool:
    adjacency: dict[str, list[str]] = defaultdict(list)
    nodes: set[str] = set()
    for edge in edges:
        adjacency[edge["from"]].append(edge["to"])
        nodes.update((edge["from"], edge["to"]))

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(target) for target in adjacency[node]):
            return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in nodes)


def view_edges(model: dict[str, Any], view_id: str) -> list[dict[str, Any]]:
    edge_by_id = {edge["id"]: edge for edge in model["edges"]}
    view = next(item for item in model["views"] if item["id"] == view_id)
    return [edge_by_id[edge_id] for edge_id in view["edgeIds"]]


def trace_impact(model: dict[str, Any], view_id: str, failed_node_id: str) -> list[str]:
    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in view_edges(model, view_id):
        adjacency[edge["from"]].append(edge["to"])

    queue = deque(adjacency[failed_node_id])
    impacted: list[str] = []
    seen = {failed_node_id}
    while queue:
        node_id = queue.popleft()
        if node_id in seen:
            continue
        seen.add(node_id)
        impacted.append(node_id)
        queue.extend(adjacency[node_id])
    return impacted


def _dot_id(value: str) -> str:
    return "n_" + re.sub(r"[^a-zA-Z0-9_]", "_", value)


def _dot_text(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


def build_dot(model: dict[str, Any], view_id: str, failed_node_id: str | None = None) -> str:
    view = next(item for item in model["views"] if item["id"] == view_id)
    edges = view_edges(model, view_id)
    selected_node_ids = {node_id for edge in edges for node_id in (edge["from"], edge["to"])}
    impacted = set(trace_impact(model, view_id, failed_node_id)) if failed_node_id else set()

    lines = [
        "digraph flow {",
        f'  rankdir="{view["orientation"]}";',
        '  graph [bgcolor="transparent", pad="0.25", nodesep="0.35", ranksep="0.55"];',
        '  node [shape="box", style="rounded,filled", fontname="Arial", fontsize="10", color="#6b7280", fillcolor="#f3f4f6", fontcolor="#111827"];',
        '  edge [fontname="Arial", fontsize="9", color="#64748b", fontcolor="#475569"];',
    ]
    for node in model["nodes"]:
        if node["id"] not in selected_node_ids:
            continue
        fill = "#f3f4f6"
        color = "#6b7280"
        penwidth = "1"
        if node["id"] == failed_node_id:
            fill, color, penwidth = "#fee2e2", "#dc2626", "2"
        elif node["id"] in impacted:
            fill, color = "#fef3c7", "#d97706"
        label = _dot_text(f'{node["label"]}\n{node["owner"]} · {node["status"]}')
        lines.append(
            f'  {_dot_id(node["id"])} [label="{label}", fillcolor="{fill}", color="{color}", penwidth="{penwidth}"];'
        )
    for edge in edges:
        label = _dot_text(f'{edge["contract"]} · {edge["channel"]}')
        lines.append(f'  {_dot_id(edge["from"])} -> {_dot_id(edge["to"])} [label="{label}"];')
    lines.append("}")
    return "\n".join(lines)
