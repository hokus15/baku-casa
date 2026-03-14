#!/usr/bin/env python3
"""
SDD documentation linter for Baku.Casa.

Validates consistency between:
- docs/system/
- docs/planning/dependency-graph.yaml
- docs/planning/roadmap.md
- docs/decisions/ADR-INDEX.md
- docs/decisions/adr/
- docs/specs/features/
- docs/specs/enablers/

Usage:
    python tools/lint_sdd.py
    python tools/lint_sdd.py --strict
    python tools/lint_sdd.py --docs-root docs

Exit codes:
    0 -> no errors
    1 -> errors found
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path

import yaml


VALID_TYPES = {"feature", "enabler"}
VALID_STATUSES = {"planned", "in_progress", "done"}
VALID_PHASES = {"MVP0", "MVP1", "MVP2", "MVP3", "MVP4", "MVP5"}
VALID_SCOPES = {"cross_cutting", "module"}

FEATURE_ID_RE = re.compile(r"^F-\d{4}$")
ENABLER_ID_RE = re.compile(r"^EN-\d{4}$")
ROADMAP_MVP_RE = re.compile(r"^# MVP\s+(\d+)\b", re.IGNORECASE)
ROADMAP_ITEM_RE = re.compile(r"^##\s+(F-\d{4}|EN-\d{4})\b")
SPEC_FEATURE_FILE_RE = re.compile(r"^(F-\d{4})-.+\.md$")
SPEC_ENABLER_FILE_RE = re.compile(r"^(EN-\d{4})-.+\.md$")
ADR_FILE_RE = re.compile(r"^ADR-(\d{4})(?:-.*)?\.md$")
INDEX_LINK_RE = re.compile(r"\(([^)]+\.md)\)")


@dataclass(frozen=True)
class LintMessage:
    level: str  # ERROR | WARN
    code: str
    message: str


@dataclass
class GraphItem:
    id: str
    type: str
    status: str
    phase: str
    depends_on: list[str]
    scope: str | None = None
    affects_future_features: bool | None = None
    applies_to: list[str] | None = None


@dataclass
class RoadmapEntry:
    id: str
    phase: str
    line_no: int


@dataclass
class ParsedRoadmap:
    entries: dict[str, RoadmapEntry]
    duplicate_ids: list[tuple[str, int]]


@dataclass
class ParsedSpecs:
    feature_specs: dict[str, Path]
    enabler_specs: dict[str, Path]
    invalid_files: list[Path]
    duplicate_ids: list[tuple[str, Path, Path]]


@dataclass
class ParsedAdrs:
    ids: dict[str, Path]
    invalid_files: list[Path]
    duplicate_ids: list[tuple[str, Path, Path]]


class LintError(Exception):
    """Raised for fatal loading/parsing errors."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint SDD documentation.")
    parser.add_argument(
        "--docs-root",
        default="docs",
        help="Path to docs root directory. Default: docs",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat some warnings as errors.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    docs_root = Path(args.docs_root)

    planning_dir = docs_root / "planning"
    specs_dir = docs_root / "specs"
    decisions_dir = docs_root / "decisions"
    adr_dir = decisions_dir / "adr"
    system_dir = docs_root / "system"

    messages: list[LintMessage] = []

    try:
        graph = load_dependency_graph(planning_dir / "dependency-graph.yaml")
        roadmap = load_roadmap(planning_dir / "roadmap.md")
        specs = load_specs(specs_dir)
        adrs = load_adrs(adr_dir)
    except LintError as exc:
        print("SDD lint failed.\n")
        print(f"[ERROR] LOAD-000 {exc}")
        return 1

    messages.extend(validate_required_structure(docs_root))
    messages.extend(validate_graph_schema(graph))
    messages.extend(validate_graph_ids(graph))
    messages.extend(validate_graph_dependencies(graph))
    messages.extend(validate_graph_dag(graph))
    messages.extend(validate_graph_states(graph))

    messages.extend(validate_roadmap(roadmap))
    messages.extend(validate_roadmap_vs_graph(roadmap, graph))

    messages.extend(validate_specs(specs))
    messages.extend(validate_specs_vs_graph(specs, graph, strict=args.strict))
    messages.extend(validate_index_files(specs_dir, specs))
    messages.extend(validate_index_order(specs_dir))
    messages.extend(validate_index_link_format(specs_dir))

    messages.extend(validate_adrs(adrs, strict=args.strict))
    messages.extend(validate_adr_index(decisions_dir, adrs))
    messages.extend(validate_system_files(system_dir))

    return print_report(messages)


def validate_required_structure(docs_root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []

    required_dirs = [
        docs_root / "system",
        docs_root / "planning",
        docs_root / "decisions",
        docs_root / "decisions" / "adr",
        docs_root / "specs",
        docs_root / "specs" / "features",
        docs_root / "specs" / "enablers",
    ]

    for path in required_dirs:
        if not path.exists():
            messages.append(error("STRUCT-001", f"Missing required directory: {path}"))
        elif not path.is_dir():
            messages.append(
                error(
                    "STRUCT-002", f"Expected directory but found non-directory: {path}"
                )
            )

    required_files = [
        docs_root / "planning" / "dependency-graph.yaml",
        docs_root / "planning" / "roadmap.md",
        docs_root / "decisions" / "ADR-INDEX.md",
        docs_root / "system" / "constitution.md",
        docs_root / "system" / "context.md",
        docs_root / "system" / "glossary.md",
        docs_root / "system" / "conventions.md",
    ]

    for path in required_files:
        if not path.exists():
            messages.append(error("STRUCT-003", f"Missing required file: {path}"))
        elif not path.is_file():
            messages.append(
                error("STRUCT-004", f"Expected file but found non-file: {path}")
            )

    return messages


def validate_system_files(system_dir: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []

    required_files = [
        system_dir / "constitution.md",
        system_dir / "context.md",
        system_dir / "glossary.md",
        system_dir / "conventions.md",
    ]

    for path in required_files:
        if not path.exists():
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            messages.append(error("SYS-001", f"Failed reading {path}: {exc}"))
            continue

        if not content.strip():
            messages.append(error("SYS-002", f"System file is empty: {path}"))

    return messages


def validate_adr_index(decisions_dir: Path, adrs: ParsedAdrs) -> list[LintMessage]:
    messages: list[LintMessage] = []

    index_file = decisions_dir / "ADR-INDEX.md"
    if not index_file.exists():
        return messages

    try:
        content = index_file.read_text(encoding="utf-8")
    except Exception as exc:
        return [error("ADR-003", f"Failed reading {index_file}: {exc}")]

    if not content.strip():
        messages.append(error("ADR-004", f"ADR index file is empty: {index_file}"))
        return messages

    links = set(INDEX_LINK_RE.findall(content))
    adr_files = {f"adr/{path.name}" for path in adrs.ids.values()}

    for missing in sorted(adr_files - links):
        messages.append(
            error(
                "ADR-005",
                f"{index_file} missing entry for ADR file {missing}",
            )
        )

    for orphan in sorted(links - adr_files):
        messages.append(
            error(
                "ADR-006",
                f"{index_file} references non-existent ADR file {orphan}",
            )
        )

    for link in sorted(links):
        if not link.startswith("adr/"):
            messages.append(
                error(
                    "ADR-007",
                    f"{index_file} must use relative links under adr/: {link}",
                )
            )

    ordered_ids: list[str] = []
    for link in INDEX_LINK_RE.findall(content):
        name = Path(link).name
        match = ADR_FILE_RE.match(name)
        if match:
            ordered_ids.append(match.group(1))

    if ordered_ids != sorted(ordered_ids):
        messages.append(
            error(
                "ADR-008",
                f"{index_file} entries must be sorted by ADR ID",
            )
        )

    return messages


def validate_index_files(specs_root: Path, specs: ParsedSpecs) -> list[LintMessage]:
    messages: list[LintMessage] = []

    checks = [
        ("features", specs.feature_specs),
        ("enablers", specs.enabler_specs),
    ]

    for folder_name, spec_map in checks:
        folder = specs_root / folder_name
        index_file = folder / "INDEX.md"

        if not index_file.exists():
            messages.append(
                error(
                    "INDEX-001",
                    f"Missing {index_file}. Each spec folder must contain an INDEX.md",
                )
            )
            continue

        try:
            content = index_file.read_text(encoding="utf-8")
        except Exception as exc:
            messages.append(
                error(
                    "INDEX-002",
                    f"Failed reading {index_file}: {exc}",
                )
            )
            continue

        links = set(INDEX_LINK_RE.findall(content))
        spec_files = {path.name for path in spec_map.values()}

        for missing in sorted(spec_files - links):
            messages.append(
                error(
                    "INDEX-003",
                    f"{index_file} missing entry for spec file {missing}",
                )
            )

        for orphan in sorted(links - spec_files):
            messages.append(
                error(
                    "INDEX-004",
                    f"{index_file} references non-existent spec file {orphan}",
                )
            )

    return messages


def load_dependency_graph(path: Path) -> dict[str, GraphItem]:
    if not path.exists():
        raise LintError(f"Missing file: {path}")

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise LintError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise LintError(f"{path} must contain a top-level mapping")

    items_raw = raw.get("items")
    if not isinstance(items_raw, list):
        raise LintError(f"{path} must contain top-level key 'items' as a list")

    items: dict[str, GraphItem] = {}
    duplicate_ids: list[str] = []

    for index, entry in enumerate(items_raw):
        if not isinstance(entry, dict):
            raise LintError(f"{path}: items[{index}] must be a mapping")

        item_id = entry.get("id")
        if not isinstance(item_id, str):
            raise LintError(f"{path}: items[{index}] missing string field 'id'")

        if item_id in items:
            duplicate_ids.append(item_id)

        depends_on = entry.get("depends_on", [])
        if depends_on is None:
            depends_on = []
        if not isinstance(depends_on, list) or not all(
            isinstance(v, str) for v in depends_on
        ):
            raise LintError(
                f"{path}: item {item_id} field 'depends_on' must be a list[str]"
            )

        applies_to = entry.get("applies_to")
        if applies_to is not None:
            if not isinstance(applies_to, list) or not all(
                isinstance(v, str) for v in applies_to
            ):
                raise LintError(
                    f"{path}: item {item_id} field 'applies_to' must be a list[str]"
                )

        items[item_id] = GraphItem(
            id=item_id,
            type=entry.get("type"),
            status=entry.get("status"),
            phase=entry.get("phase"),
            depends_on=depends_on,
            scope=entry.get("scope"),
            affects_future_features=entry.get("affects_future_features"),
            applies_to=applies_to,
        )

    if duplicate_ids:
        dupes = ", ".join(sorted(set(duplicate_ids)))
        raise LintError(f"Duplicate IDs in {path}: {dupes}")

    return items


def load_roadmap(path: Path) -> ParsedRoadmap:
    if not path.exists():
        raise LintError(f"Missing file: {path}")

    current_phase: str | None = None
    entries: dict[str, RoadmapEntry] = {}
    duplicate_ids: list[tuple[str, int]] = []

    for line_no, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        phase_match = ROADMAP_MVP_RE.match(line.strip())
        if phase_match:
            current_phase = f"MVP{phase_match.group(1)}"
            continue

        item_match = ROADMAP_ITEM_RE.match(line.strip())
        if item_match:
            item_id = item_match.group(1)
            if current_phase is None:
                raise LintError(
                    f"{path}:{line_no} item {item_id} appears before any MVP section header"
                )
            if item_id in entries:
                duplicate_ids.append((item_id, line_no))
            else:
                entries[item_id] = RoadmapEntry(
                    id=item_id,
                    phase=current_phase,
                    line_no=line_no,
                )

    return ParsedRoadmap(entries=entries, duplicate_ids=duplicate_ids)


def load_specs(specs_root: Path) -> ParsedSpecs:
    features_dir = specs_root / "features"
    enablers_dir = specs_root / "enablers"

    feature_specs: dict[str, Path] = {}
    enabler_specs: dict[str, Path] = {}
    invalid_files: list[Path] = []
    duplicate_ids: list[tuple[str, Path, Path]] = []

    if features_dir.exists():
        for path in sorted(features_dir.glob("*.md")):
            if path.name == "INDEX.md":
                continue

            match = SPEC_FEATURE_FILE_RE.match(path.name)
            if not match:
                invalid_files.append(path)
                continue

            item_id = match.group(1)
            if item_id in feature_specs:
                duplicate_ids.append((item_id, feature_specs[item_id], path))
            else:
                feature_specs[item_id] = path

    if enablers_dir.exists():
        for path in sorted(enablers_dir.glob("*.md")):
            if path.name == "INDEX.md":
                continue

            match = SPEC_ENABLER_FILE_RE.match(path.name)
            if not match:
                invalid_files.append(path)
                continue

            item_id = match.group(1)
            if item_id in enabler_specs:
                duplicate_ids.append((item_id, enabler_specs[item_id], path))
            else:
                enabler_specs[item_id] = path

    return ParsedSpecs(
        feature_specs=feature_specs,
        enabler_specs=enabler_specs,
        invalid_files=invalid_files,
        duplicate_ids=duplicate_ids,
    )


def load_adrs(adr_root: Path) -> ParsedAdrs:
    ids: dict[str, Path] = {}
    invalid_files: list[Path] = []
    duplicate_ids: list[tuple[str, Path, Path]] = []

    if adr_root.exists():
        for path in sorted(adr_root.glob("*.md")):
            match = ADR_FILE_RE.match(path.name)
            if not match:
                invalid_files.append(path)
                continue

            adr_id = match.group(1)
            if adr_id in ids:
                duplicate_ids.append((adr_id, ids[adr_id], path))
            else:
                ids[adr_id] = path

    return ParsedAdrs(ids=ids, invalid_files=invalid_files, duplicate_ids=duplicate_ids)


def validate_index_order(specs_root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for folder_name in ("features", "enablers"):
        index_file = specs_root / folder_name / "INDEX.md"
        if not index_file.exists():
            continue

        content = index_file.read_text(encoding="utf-8")
        links = INDEX_LINK_RE.findall(content)

        ids: list[str] = []
        for link in links:
            name = Path(link).name
            match = re.match(r"^(F-\d{4}|EN-\d{4})-", name)
            if match:
                ids.append(match.group(1))

        if ids != sorted(ids):
            messages.append(
                error(
                    "INDEX-005",
                    f"{index_file} entries must be sorted by ID",
                )
            )

    return messages


def validate_index_link_format(specs_root: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for folder_name in ("features", "enablers"):
        index_file = specs_root / folder_name / "INDEX.md"
        if not index_file.exists():
            continue

        content = index_file.read_text(encoding="utf-8")
        links = INDEX_LINK_RE.findall(content)

        for link in links:
            path = Path(link)
            if path.name != link:
                messages.append(
                    error(
                        "INDEX-006",
                        f"{index_file} must use relative file links without subdirectories: {link}",
                    )
                )

    return messages


def validate_graph_schema(graph: dict[str, GraphItem]) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item in graph.values():
        if item.type not in VALID_TYPES:
            messages.append(
                error("DAG-001", f"Item {item.id} has invalid type: {item.type!r}")
            )

        if item.status not in VALID_STATUSES:
            messages.append(
                error("DAG-002", f"Item {item.id} has invalid status: {item.status!r}")
            )

        if item.phase not in VALID_PHASES:
            messages.append(
                error("DAG-003", f"Item {item.id} has invalid phase: {item.phase!r}")
            )

        if item.type == "enabler":
            if item.scope is None:
                messages.append(
                    error(
                        "DAG-004",
                        f"Enabler {item.id} is missing required field 'scope'",
                    )
                )
            elif item.scope not in VALID_SCOPES:
                messages.append(
                    error(
                        "DAG-005",
                        f"Enabler {item.id} has invalid scope: {item.scope!r}",
                    )
                )

            if not isinstance(item.affects_future_features, bool):
                messages.append(
                    error(
                        "DAG-006",
                        f"Enabler {item.id} must define boolean field 'affects_future_features'",
                    )
                )

            if item.applies_to is None:
                messages.append(
                    error(
                        "DAG-007",
                        f"Enabler {item.id} is missing required field 'applies_to'",
                    )
                )
            elif len(item.applies_to) == 0:
                messages.append(
                    warn("DAG-008", f"Enabler {item.id} has empty 'applies_to' list")
                )
        else:
            if item.scope is not None:
                messages.append(
                    warn("DAG-009", f"Feature {item.id} should not define 'scope'")
                )
            if item.affects_future_features is not None:
                messages.append(
                    warn(
                        "DAG-010",
                        f"Feature {item.id} should not define 'affects_future_features'",
                    )
                )
            if item.applies_to is not None:
                messages.append(
                    warn("DAG-011", f"Feature {item.id} should not define 'applies_to'")
                )

    return messages


def validate_graph_ids(graph: dict[str, GraphItem]) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item in graph.values():
        if item.type == "feature":
            if not FEATURE_ID_RE.match(item.id):
                messages.append(
                    error(
                        "DAG-012",
                        f"Feature {item.id} does not match pattern ^F-\\d{{4}}$",
                    )
                )
        elif item.type == "enabler":
            if not ENABLER_ID_RE.match(item.id):
                messages.append(
                    error(
                        "DAG-013",
                        f"Enabler {item.id} does not match pattern ^EN-\\d{{4}}$",
                    )
                )

        if item.id.startswith("F-") and item.type != "feature":
            messages.append(
                error(
                    "DAG-014",
                    f"Item {item.id} prefix implies feature but type is {item.type}",
                )
            )
        if item.id.startswith("EN-") and item.type != "enabler":
            messages.append(
                error(
                    "DAG-015",
                    f"Item {item.id} prefix implies enabler but type is {item.type}",
                )
            )

    return messages


def validate_graph_dependencies(graph: dict[str, GraphItem]) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item in graph.values():
        for dep in item.depends_on:
            if dep not in graph:
                messages.append(
                    error(
                        "DAG-016",
                        f"Item {item.id} depends on unknown item {dep}",
                    )
                )
                continue

            dep_phase = graph[dep].phase
            if phase_rank(dep_phase) > phase_rank(item.phase):
                messages.append(
                    error(
                        "DAG-017",
                        f"Item {item.id} in phase {item.phase} depends on future-phase item {dep} in phase {dep_phase}",
                    )
                )

    return messages


def validate_graph_dag(graph: dict[str, GraphItem]) -> list[LintMessage]:
    indegree: dict[str, int] = {item_id: 0 for item_id in graph}
    adjacency: dict[str, list[str]] = defaultdict(list)

    for item in graph.values():
        for dep in item.depends_on:
            if dep in graph:
                adjacency[dep].append(item.id)
                indegree[item.id] += 1

    queue = deque(
        sorted(item_id for item_id, degree in indegree.items() if degree == 0)
    )
    visited: list[str] = []

    while queue:
        node = queue.popleft()
        visited.append(node)
        for nxt in adjacency[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(visited) == len(graph):
        return []

    cyclic_nodes = sorted(item_id for item_id, degree in indegree.items() if degree > 0)
    return [
        error(
            "DAG-018",
            "Cycle detected or unresolved cyclic dependency among items: "
            + ", ".join(cyclic_nodes),
        )
    ]


def validate_graph_states(graph: dict[str, GraphItem]) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item in graph.values():
        for dep in item.depends_on:
            if dep not in graph:
                continue

            dep_status = graph[dep].status
            if item.status == "done" and dep_status != "done":
                messages.append(
                    error(
                        "STATE-001",
                        f"Item {item.id} is done but depends on {dep} with status {dep_status}",
                    )
                )
            if item.status == "in_progress" and dep_status == "planned":
                messages.append(
                    error(
                        "STATE-002",
                        f"Item {item.id} is in_progress but depends on planned item {dep}",
                    )
                )

        if item.type == "enabler" and item.affects_future_features is True:
            if not item.applies_to:
                messages.append(
                    warn(
                        "STATE-003",
                        f"Enabler {item.id} propagates to future features but 'applies_to' is empty",
                    )
                )

    return messages


def validate_roadmap(roadmap: ParsedRoadmap) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item_id, line_no in roadmap.duplicate_ids:
        messages.append(
            error("ROADMAP-001", f"Duplicate roadmap item {item_id} at line {line_no}")
        )

    return messages


def validate_roadmap_vs_graph(
    roadmap: ParsedRoadmap,
    graph: dict[str, GraphItem],
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    roadmap_ids = set(roadmap.entries)
    graph_ids = set(graph)

    for item_id in sorted(roadmap_ids - graph_ids):
        entry = roadmap.entries[item_id]
        messages.append(
            error(
                "ROADMAP-002",
                f"Roadmap item {item_id} at line {entry.line_no} does not exist in dependency graph",
            )
        )

    for item_id in sorted(graph_ids - roadmap_ids):
        messages.append(
            error(
                "ROADMAP-003",
                f"Dependency graph item {item_id} does not appear in roadmap.md",
            )
        )

    for item_id in sorted(roadmap_ids & graph_ids):
        roadmap_phase = roadmap.entries[item_id].phase
        graph_phase = graph[item_id].phase
        if roadmap_phase != graph_phase:
            messages.append(
                error(
                    "ROADMAP-004",
                    f"Item {item_id} has phase {roadmap_phase} in roadmap.md but {graph_phase} in dependency graph",
                )
            )

    return messages


def validate_specs(specs: ParsedSpecs) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for path in specs.invalid_files:
        messages.append(
            error(
                "SPEC-001",
                f"Invalid spec filename: {path}. Expected F-0001-name.md or EN-0200-name.md",
            )
        )

    for item_id, first, second in specs.duplicate_ids:
        messages.append(
            error(
                "SPEC-002",
                f"Duplicate spec ID {item_id}: {first} and {second}",
            )
        )

    return messages


def validate_specs_vs_graph(
    specs: ParsedSpecs,
    graph: dict[str, GraphItem],
    *,
    strict: bool,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    feature_ids = set(specs.feature_specs)
    enabler_ids = set(specs.enabler_specs)
    spec_ids = feature_ids | enabler_ids

    for item_id in sorted(feature_ids):
        graph_item = graph.get(item_id)
        if graph_item is None:
            messages.append(
                error(
                    "SPEC-003",
                    f"Feature spec exists for unknown item {item_id}: {specs.feature_specs[item_id]}",
                )
            )
        elif graph_item.type != "feature":
            messages.append(
                error(
                    "SPEC-004",
                    f"Spec {specs.feature_specs[item_id]} is under features/ but graph type for {item_id} is {graph_item.type}",
                )
            )

    for item_id in sorted(enabler_ids):
        graph_item = graph.get(item_id)
        if graph_item is None:
            messages.append(
                error(
                    "SPEC-005",
                    f"Enabler spec exists for unknown item {item_id}: {specs.enabler_specs[item_id]}",
                )
            )
        elif graph_item.type != "enabler":
            messages.append(
                error(
                    "SPEC-006",
                    f"Spec {specs.enabler_specs[item_id]} is under enablers/ but graph type for {item_id} is {graph_item.type}",
                )
            )

    for item_id, item in sorted(graph.items()):
        if item_id in spec_ids:
            continue

        if item.type == "feature":
            msg = (
                f"Feature {item_id} exists in dependency graph with status "
                f"{item.status} but has no spec file in docs/specs/features/"
            )
            if strict or item.status in {"done", "in_progress"}:
                messages.append(error("SPEC-007", msg))
            else:
                messages.append(warn("SPEC-007", msg))

        elif item.type == "enabler":
            msg = (
                f"Enabler {item_id} exists in dependency graph with status "
                f"{item.status} but has no spec file in docs/specs/enablers/"
            )
            if strict or item.status in {"done", "in_progress"}:
                messages.append(error("SPEC-008", msg))
            else:
                messages.append(warn("SPEC-008", msg))

    return messages


def validate_adrs(adrs: ParsedAdrs, *, strict: bool) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for path in adrs.invalid_files:
        msg = f"Invalid ADR filename: {path}. Expected ADR-0001-name.md"
        if strict:
            messages.append(error("ADR-001", msg))
        else:
            messages.append(warn("ADR-001", msg))

    for adr_id, first, second in adrs.duplicate_ids:
        messages.append(
            error(
                "ADR-002",
                f"Duplicate ADR ID {adr_id}: {first} and {second}",
            )
        )

    return messages


def phase_rank(phase: str) -> int:
    return int(phase.replace("MVP", ""))


def error(code: str, message: str) -> LintMessage:
    return LintMessage(level="ERROR", code=code, message=message)


def warn(code: str, message: str) -> LintMessage:
    return LintMessage(level="WARN", code=code, message=message)


def print_report(messages: list[LintMessage]) -> int:
    errors = [m for m in messages if m.level == "ERROR"]
    warnings = [m for m in messages if m.level == "WARN"]

    if not messages:
        print("SDD lint passed.")
        return 0

    print("SDD lint report.\n")

    for msg in messages:
        print(f"[{msg.level:<5}] {msg.code} {msg.message}")

    print()
    print(f"Errors:   {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
