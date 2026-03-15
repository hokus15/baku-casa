"""
Resolve minimum SDD context for a roadmap item and phase.

Usage examples:
    python tools/resolve_sdd_context.py --item F-0012 --phase plan
    python tools/resolve_sdd_context.py --item F-0014 --phase implement --format json
    python tools/resolve_sdd_context.py --item F-0014 --phase specify --profile minimal
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PLANNING = DOCS / "planning"
SYSTEM = DOCS / "system"

SECTION_ID_RE = re.compile(r"^#+\s+\[([a-z0-9_]+)\]\s+", re.MULTILINE)
SHARED_SPEC_REF_RE = re.compile(r"docs/specs/shared/([^\s)]+)")

PHASE_REASON_PRIORITY: dict[str, list[str]] = {
    "specify": [
        "architecture",
        "api_contract",
        "integration_contracts",
        "money_percentages",
        "time_policy",
        "idempotency",
        "event_delivery",
        "authentication",
        "observability_errors",
        "configuration",
        "persistence",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
    "clarify": [
        "architecture",
        "api_contract",
        "integration_contracts",
        "money_percentages",
        "time_policy",
        "idempotency",
        "event_delivery",
        "authentication",
        "observability_errors",
        "configuration",
        "persistence",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
    "plan": [
        "architecture",
        "persistence",
        "api_contract",
        "configuration",
        "observability_errors",
        "authentication",
        "integration_contracts",
        "event_delivery",
        "idempotency",
        "money_percentages",
        "time_policy",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
    "tasks": [
        "architecture",
        "persistence",
        "api_contract",
        "configuration",
        "observability_errors",
        "authentication",
        "integration_contracts",
        "event_delivery",
        "idempotency",
        "money_percentages",
        "time_policy",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
    "analyze": [
        "persistence",
        "configuration",
        "observability_errors",
        "api_contract",
        "integration_contracts",
        "idempotency",
        "event_delivery",
        "architecture",
        "authentication",
        "money_percentages",
        "time_policy",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
    "implement": [
        "architecture",
        "persistence",
        "api_contract",
        "configuration",
        "observability_errors",
        "authentication",
        "event_delivery",
        "idempotency",
        "integration_contracts",
        "money_percentages",
        "time_policy",
        "delivery",
        "governance_ci",
        "monorepo_architecture",
    ],
}

REASON_BASELINE_LABELS: dict[str, str] = {
    "architecture": "Arquitectura base aplicable",
    "api_contract": "Contrato e interfaz HTTP aplicable",
    "integration_contracts": "Disciplina de versionado e integracion aplicable",
    "money_percentages": "Politica de representacion monetaria aplicable",
    "time_policy": "Politica temporal aplicable",
    "idempotency": "Proteccion de idempotencia aplicable",
    "event_delivery": "Mecanismo de eventos aplicable",
    "authentication": "Estrategia de autenticacion aplicable",
    "observability_errors": "Baseline de errores y observabilidad aplicable",
    "configuration": "Sistema de configuracion aplicable",
    "persistence": "Baseline de persistencia aplicable",
    "delivery": "Modelo de entrega aplicable",
    "governance_ci": "Gobernanza y CI aplicables",
    "monorepo_architecture": "Baseline estructural del repositorio aplicable",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve minimum SDD context.")
    parser.add_argument("--item", required=True, help="Roadmap item ID, e.g. F-0012")
    parser.add_argument(
        "--phase",
        required=True,
        choices=sorted(PHASE_REASON_PRIORITY),
        help="SDD phase",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format",
    )
    parser.add_argument(
        "--profile",
        choices=("minimal", "default", "deep"),
        default="default",
        help="Context depth profile",
    )
    return parser.parse_args()


def load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_dependency_graph() -> dict[str, dict[str, Any]]:
    raw = load_yaml(PLANNING / "dependency-graph.yaml")
    return {entry["id"]: entry for entry in raw["items"]}


def load_manifest() -> dict[str, dict[str, Any]]:
    raw = load_yaml(PLANNING / "item-manifest.yaml")
    return raw["items"]


def load_adr_map() -> dict[str, list[dict[str, str]]]:
    raw = load_yaml(PLANNING / "adr-map.yaml")
    return {item_id: entry.get("adrs", []) for item_id, entry in raw["items"].items()}


def load_context_slices() -> tuple[dict[str, dict[str, list[str]]], dict[str, list[str]]]:
    raw = load_yaml(PLANNING / "context-slices.yaml")
    slices = raw["slices"]
    assignments = {
        item_id: entry.get("slices", []) for item_id, entry in raw["assignments"].items()
    }
    return slices, assignments


def extract_available_section_ids(path: Path) -> set[str]:
    return set(SECTION_ID_RE.findall(path.read_text(encoding="utf-8")))


def extract_shared_refs(spec_path: Path) -> list[str]:
    content = spec_path.read_text(encoding="utf-8")
    refs = []
    seen = set()
    for ref in SHARED_SPEC_REF_RE.findall(content):
        ref = ref.rstrip("`.,:;")
        if ref not in seen:
            refs.append(ref)
            seen.add(ref)
    return refs


def collect_dependency_shared_refs(
    dependency_ids: list[str], manifest: dict[str, dict[str, Any]]
) -> list[str]:
    refs: list[str] = []
    seen: set[str] = set()

    for item_id in dependency_ids:
        spec = manifest.get(item_id, {}).get("spec")
        if not spec:
            continue
        spec_path = ROOT / spec
        for ref in extract_shared_refs(spec_path):
            if ref in seen:
                continue
            refs.append(ref)
            seen.add(ref)

    return refs


def dependency_closure(item_id: str, graph: dict[str, dict[str, Any]]) -> list[str]:
    ordered: list[str] = []
    seen: set[str] = set()

    def visit(current: str) -> None:
        if current in seen:
            return
        seen.add(current)
        for dep in graph[current].get("depends_on", []):
            visit(dep)
        ordered.append(current)

    visit(item_id)
    return [dep for dep in ordered if dep != item_id]


def direct_dependencies(item_id: str, graph: dict[str, dict[str, Any]]) -> list[str]:
    return list(graph[item_id].get("depends_on", []))


def prioritize_adrs(
    refs: list[dict[str, str]], phase: str, shortlist: list[str]
) -> list[dict[str, Any]]:
    reason_order = {reason: index for index, reason in enumerate(PHASE_REASON_PRIORITY[phase])}
    shortlist_order = {adr_id: index for index, adr_id in enumerate(shortlist)}

    prioritized = []
    for ref in refs:
        prioritized.append(
            {
                **ref,
                "priority_rank": reason_order.get(ref["reason"], len(reason_order)),
                "shortlist": ref["adr_id"] in shortlist_order,
                "shortlist_rank": shortlist_order.get(ref["adr_id"], 999),
            }
        )

    prioritized.sort(
        key=lambda entry: (
            entry["priority_rank"],
            0 if entry["shortlist"] else 1,
            entry["shortlist_rank"],
            entry["adr_id"],
        )
    )
    return prioritized


def build_context(item_id: str, phase: str) -> dict[str, Any]:
    graph = load_dependency_graph()
    manifest = load_manifest()
    adr_map = load_adr_map()
    slices, assignments = load_context_slices()

    if item_id not in graph:
        raise SystemExit(f"Unknown item: {item_id}")
    if item_id not in manifest:
        raise SystemExit(f"Item missing in item-manifest.yaml: {item_id}")

    item_manifest = manifest[item_id]
    spec_path = ROOT / item_manifest["spec"]
    shared_specs = extract_shared_refs(spec_path)
    deps = dependency_closure(item_id, graph)
    direct_deps = direct_dependencies(item_id, graph)
    direct_dep_set = set(direct_deps)
    transitive_deps = [dep for dep in deps if dep not in direct_dep_set]
    direct_dependency_shared_specs = collect_dependency_shared_refs(direct_deps, manifest)
    transitive_dependency_shared_specs = collect_dependency_shared_refs(transitive_deps, manifest)
    inherited_shared_specs = [
        ref for ref in dedupe(direct_dependency_shared_specs + transitive_dependency_shared_specs)
        if ref not in set(shared_specs)
    ]

    slice_names = assignments.get(item_id, [])
    slice_constitution: list[str] = []
    slice_context: list[str] = []
    for slice_name in slice_names:
        definition = slices[slice_name]
        slice_constitution.extend(definition.get("constitution_sections", []))
        slice_context.extend(definition.get("context_sections", []))

    constitution_sections = dedupe(
        item_manifest.get("constitution_sections", []) + slice_constitution
    )
    context_sections = dedupe(item_manifest.get("context_sections", []) + slice_context)
    manifest_constitution_sections = item_manifest.get("constitution_sections", [])
    manifest_context_sections = item_manifest.get("context_sections", [])
    slice_added_constitution_sections = [
        section
        for section in constitution_sections
        if section not in set(manifest_constitution_sections)
    ]
    slice_added_context_sections = [
        section for section in context_sections if section not in set(manifest_context_sections)
    ]

    constitution_available = extract_available_section_ids(SYSTEM / "constitution.md")
    context_available = extract_available_section_ids(SYSTEM / "context.md")

    adr_refs = prioritize_adrs(
        adr_map.get(item_id, []), phase=phase, shortlist=item_manifest.get("adr_refs", [])
    )
    technical_baseline = summarize_technical_baseline(adr_refs)
    core_technical_baseline, supporting_technical_baseline, core_adrs, supporting_adrs = (
        split_baseline_by_shortlist(adr_refs, technical_baseline)
    )

    return {
        "item_id": item_id,
        "phase": phase,
        "item_type": graph[item_id]["type"],
        "spec": rel(spec_path),
        "planning_artifacts": [
            "docs/planning/item-manifest.yaml",
            "docs/planning/context-slices.yaml",
            "docs/planning/adr-map.yaml",
            "docs/planning/dependency-graph.yaml",
        ],
        "direct_dependencies": [
            {
                "id": dep,
                "spec": manifest.get(dep, {}).get("spec"),
            }
            for dep in direct_deps
        ],
        "transitive_dependencies": [
            {
                "id": dep,
                "spec": manifest.get(dep, {}).get("spec"),
            }
            for dep in transitive_deps
        ],
        "dependencies": [
            {
                "id": dep,
                "spec": manifest.get(dep, {}).get("spec"),
            }
            for dep in deps
        ],
        "shared_specs": [f"docs/specs/shared/{name}" for name in shared_specs],
        "direct_dependency_shared_specs": [
            f"docs/specs/shared/{name}" for name in direct_dependency_shared_specs
        ],
        "transitive_dependency_shared_specs": [
            f"docs/specs/shared/{name}" for name in transitive_dependency_shared_specs
        ],
        "inherited_shared_specs": [
            f"docs/specs/shared/{name}" for name in inherited_shared_specs
        ],
        "slice_names": slice_names,
        "manifest_constitution_sections": [
            section
            for section in manifest_constitution_sections
            if section in constitution_available
        ],
        "manifest_context_sections": [
            section for section in manifest_context_sections if section in context_available
        ],
        "slice_added_constitution_sections": [
            section
            for section in slice_added_constitution_sections
            if section in constitution_available
        ],
        "slice_added_context_sections": [
            section for section in slice_added_context_sections if section in context_available
        ],
        "core_constitution_sections": [
            section
            for section in manifest_constitution_sections
            if section in constitution_available
        ],
        "supporting_constitution_sections": [
            section
            for section in slice_added_constitution_sections
            if section in constitution_available
        ],
        "constitution_sections": [
            section for section in constitution_sections if section in constitution_available
        ],
        "core_context_sections": [
            section for section in manifest_context_sections if section in context_available
        ],
        "supporting_context_sections": [
            section for section in slice_added_context_sections if section in context_available
        ],
        "context_sections": [
            section for section in context_sections if section in context_available
        ],
        "adrs": [
            {
                "adr_id": ref["adr_id"],
                "adr_title": ref["adr_title"],
                "reason": ref["reason"],
                "shortlist": ref["shortlist"],
                "path": adr_path(ref["adr_id"]),
            }
            for ref in adr_refs
        ],
        "technical_baseline": technical_baseline,
        "core_adrs": [
            {
                "adr_id": ref["adr_id"],
                "adr_title": ref["adr_title"],
                "reason": ref["reason"],
                "shortlist": ref["shortlist"],
                "path": adr_path(ref["adr_id"]),
            }
            for ref in core_adrs
        ],
        "supporting_adrs": [
            {
                "adr_id": ref["adr_id"],
                "adr_title": ref["adr_title"],
                "reason": ref["reason"],
                "shortlist": ref["shortlist"],
                "path": adr_path(ref["adr_id"]),
            }
            for ref in supporting_adrs
        ],
        "core_technical_baseline": core_technical_baseline,
        "supporting_technical_baseline": supporting_technical_baseline,
    }


def adr_path(adr_id: str) -> str:
    suffix = adr_id.replace("ADR-", "")
    matches = sorted((DOCS / "decisions" / "adr").glob(f"ADR-{suffix}-*.md"))
    if not matches:
        return f"docs/decisions/adr/{adr_id}-<missing>.md"
    return rel(matches[0])


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered


def summarize_technical_baseline(adrs: list[dict[str, Any]]) -> list[dict[str, str]]:
    baseline: list[dict[str, str]] = []
    covered_reasons: set[str] = set()

    for ref in adrs:
        reason = ref["reason"]
        if reason in covered_reasons:
            continue
        covered_reasons.add(reason)
        baseline.append(
            {
                "reason": reason,
                "label": REASON_BASELINE_LABELS.get(reason, reason),
                "adr_id": ref["adr_id"],
                "adr_title": ref["adr_title"],
                "path": adr_path(ref["adr_id"]),
                "shortlist": "true" if ref["shortlist"] else "false",
            }
        )

    return baseline


def split_baseline_by_shortlist(
    adrs: list[dict[str, Any]], baseline: list[dict[str, str]]
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, Any]], list[dict[str, Any]]]:
    shortlist_reasons = {ref["reason"] for ref in adrs if ref["shortlist"]}
    if not shortlist_reasons:
        return baseline, [], adrs, []

    core_baseline = [entry for entry in baseline if entry["reason"] in shortlist_reasons]
    supporting_baseline = [entry for entry in baseline if entry["reason"] not in shortlist_reasons]
    core_adrs = [ref for ref in adrs if ref["shortlist"]]
    supporting_adrs = [ref for ref in adrs if not ref["shortlist"]]
    return core_baseline, supporting_baseline, core_adrs, supporting_adrs


def apply_profile(context: dict[str, Any], profile: str) -> dict[str, Any]:
    profiled = dict(context)
    profiled["profile"] = profile

    if profile == "deep":
        return profiled

    if profile == "minimal":
        keep_keys = {
            "item_id",
            "phase",
            "item_type",
            "profile",
            "spec",
            "planning_artifacts",
            "direct_dependencies",
            "shared_specs",
            "core_constitution_sections",
            "core_context_sections",
            "core_technical_baseline",
            "core_adrs",
        }
        return {key: profiled[key] for key in keep_keys}

    drop_keys = {
        "dependencies",
        "transitive_dependencies",
        "transitive_dependency_shared_specs",
        "technical_baseline",
        "adrs",
        "manifest_constitution_sections",
        "manifest_context_sections",
        "slice_added_constitution_sections",
        "slice_added_context_sections",
    }
    for key in drop_keys:
        profiled.pop(key, None)
    return profiled


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def render_text(context: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"Item: {context['item_id']} ({context['item_type']})")
    lines.append(f"Phase: {context['phase']}")
    lines.append(f"Profile: {context['profile']}")
    lines.append("")
    lines.append("Primary spec:")
    lines.append(f"- {context['spec']}")
    lines.append("")
    lines.append("Planning artifacts:")
    for artifact in context["planning_artifacts"]:
        lines.append(f"- {artifact}")

    if context["direct_dependencies"]:
        lines.append("")
        lines.append("Direct dependencies:")
        for dep in context["direct_dependencies"]:
            if dep["spec"]:
                lines.append(f"- {dep['id']} -> {dep['spec']}")
            else:
                lines.append(f"- {dep['id']}")

    if context.get("transitive_dependencies"):
        lines.append("")
        lines.append("Transitive baseline dependencies:")
        for dep in context["transitive_dependencies"]:
            if dep["spec"]:
                lines.append(f"- {dep['id']} -> {dep['spec']}")
            else:
                lines.append(f"- {dep['id']}")

    if context.get("dependencies"):
        lines.append("")
        lines.append("Full dependency closure:")
        for dep in context["dependencies"]:
            if dep["spec"]:
                lines.append(f"- {dep['id']} -> {dep['spec']}")
            else:
                lines.append(f"- {dep['id']}")

    if context.get("shared_specs"):
        lines.append("")
        lines.append("Direct shared specs:")
        for spec in context["shared_specs"]:
            lines.append(f"- {spec}")

    if context.get("direct_dependency_shared_specs"):
        lines.append("")
        lines.append("Direct dependency shared specs:")
        for spec in context["direct_dependency_shared_specs"]:
            lines.append(f"- {spec}")

    if context.get("transitive_dependency_shared_specs"):
        lines.append("")
        lines.append("Transitive dependency shared specs:")
        for spec in context["transitive_dependency_shared_specs"]:
            lines.append(f"- {spec}")

    if context.get("inherited_shared_specs"):
        lines.append("")
        lines.append("Inherited shared specs:")
        for spec in context["inherited_shared_specs"]:
            lines.append(f"- {spec}")

    if context.get("slice_names"):
        lines.append("")
        lines.append("Context slices:")
        for slice_name in context["slice_names"]:
            lines.append(f"- {slice_name}")

    if context.get("core_constitution_sections") is not None:
        lines.append("")
        lines.append("Core constitution sections:")
        for section in context["core_constitution_sections"]:
            lines.append(f"- {section}")

    if context.get("supporting_constitution_sections"):
        lines.append("")
        lines.append("Supporting constitution sections:")
        for section in context["supporting_constitution_sections"]:
            lines.append(f"- {section}")

    if context.get("constitution_sections") is not None:
        lines.append("")
        lines.append("Resolved constitution sections:")
        for section in context["constitution_sections"]:
            lines.append(f"- {section}")

    if context.get("core_context_sections") is not None:
        lines.append("")
        lines.append("Core context sections:")
        for section in context["core_context_sections"]:
            lines.append(f"- {section}")

    if context.get("supporting_context_sections"):
        lines.append("")
        lines.append("Supporting context sections:")
        for section in context["supporting_context_sections"]:
            lines.append(f"- {section}")

    if context.get("context_sections") is not None:
        lines.append("")
        lines.append("Resolved context sections:")
        for section in context["context_sections"]:
            lines.append(f"- {section}")

    if context.get("core_technical_baseline"):
        lines.append("")
        lines.append("Core technical baseline:")
        for entry in context["core_technical_baseline"]:
            shortlist = " shortlist" if entry["shortlist"] == "true" else ""
            lines.append(
                f"- {entry['label']} [{entry['reason']}{shortlist}] -> "
                f"{entry['adr_id']} :: {entry['adr_title']} ({entry['path']})"
            )

    if context.get("supporting_technical_baseline"):
        lines.append("")
        lines.append("Supporting technical baseline:")
        for entry in context["supporting_technical_baseline"]:
            shortlist = " shortlist" if entry["shortlist"] == "true" else ""
            lines.append(
                f"- {entry['label']} [{entry['reason']}{shortlist}] -> "
                f"{entry['adr_id']} :: {entry['adr_title']} ({entry['path']})"
            )

    if context.get("core_adrs") is not None:
        lines.append("")
        lines.append("Core ADRs:")
        for ref in context["core_adrs"]:
            shortlist = " shortlist" if ref["shortlist"] else ""
            lines.append(
                f"- {ref['adr_id']} [{ref['reason']}{shortlist}] -> {ref['path']} :: {ref['adr_title']}"
            )

    if context.get("supporting_adrs"):
        lines.append("")
        lines.append("Supporting ADRs:")
        for ref in context["supporting_adrs"]:
            shortlist = " shortlist" if ref["shortlist"] else ""
            lines.append(
                f"- {ref['adr_id']} [{ref['reason']}{shortlist}] -> {ref['path']} :: {ref['adr_title']}"
            )

    if context.get("adrs") is not None:
        lines.append("")
        lines.append("Prioritized ADRs:")
        for ref in context["adrs"]:
            shortlist = " shortlist" if ref["shortlist"] else ""
            lines.append(
                f"- {ref['adr_id']} [{ref['reason']}{shortlist}] -> {ref['path']} :: {ref['adr_title']}"
            )

    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    context = apply_profile(build_context(args.item, args.phase), args.profile)
    if args.format == "json":
        print(json.dumps(context, ensure_ascii=False, indent=2))
    else:
        print(render_text(context))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
