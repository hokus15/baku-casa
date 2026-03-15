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


# Validation constants
VALID_TYPES = {"feature", "enabler"}
VALID_STATUSES = {"planned", "in_progress", "done"}
VALID_PHASES = {"MVP0", "MVP1", "MVP2", "MVP3", "MVP4", "MVP5"}
VALID_SCOPES = {"cross_cutting", "module"}
FEATURE_REQUIRED_HEADINGS = [
    "Objetivo",
    "Alcance",
    "Fuera de alcance",
    "Definiciones",
    "Entidades principales",
    "Datos principales",
    "Capacidades",
    "Reglas del dominio",
    "Casos borde",
    "Dependencias",
    "Shared specs aplicables",
    "Criterios de aceptación",
]
ENABLER_REQUIRED_HEADINGS = [
    "Objetivo",
    "Alcance",
    "Fuera de alcance",
    "Problema que resuelve",
    "Capacidad introducida",
    "Impacto en el sistema",
    "Dependencias",
    "Relación con ADR",
    "Criterios de aceptación",
]
FEATURE_ID_RE = re.compile(r"^F-\d{4}$")
ENABLER_ID_RE = re.compile(r"^EN-\d{4}$")
ROADMAP_MVP_RE = re.compile(r"^# MVP\s+(\d+)\b", re.IGNORECASE)
ROADMAP_ITEM_RE = re.compile(r"^##\s+(F-\d{4}|EN-\d{4})\b")
SPEC_FEATURE_FILE_RE = re.compile(r"^(F-\d{4})-.+\.md$")
SPEC_ENABLER_FILE_RE = re.compile(r"^(EN-\d{4})-.+\.md$")
ADR_FILE_RE = re.compile(r"^ADR-(\d{4})(?:-.*)?\.md$")
SHARED_FILE_RE = re.compile(r"^SHARED-(\d{4})-(?:.+)\.md$")
INDEX_LINK_RE = re.compile(r"\(([^)]+\.md)\)")
SECTION_ID_RE = re.compile(r"^#+\s+\[([a-z0-9_]+)\]\s+", re.MULTILINE)
SPEC_TITLE_RE = re.compile(r"^#\s+((?:F|EN)-\d{4}):\s+(.+?)\s*$", re.MULTILINE)
ADR_TITLE_RE = re.compile(r"^#\s+(ADR-\d{4}):\s+(.+?)\s*$", re.MULTILINE)
SHARED_TITLE_RE = re.compile(r"^#\s+(SHARED-\d{4}):\s+(.+?)\s*$", re.MULTILINE)
H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
ADR_REF_RE = re.compile(r"\bADR-\d{4}\b")
ITEM_REF_RE = re.compile(r"\b(?:F|EN)-\d{4}\b")
SHARED_SPEC_REF_RE = re.compile(r"docs/specs/shared/([^\s)]+)")
WORK_IN_PROGRESS_MARKER_RE = re.compile(r"\b(?:TBD|TODO)\b")
TRANSVERSAL_LANGUAGE_RE = re.compile(
    r"\b(?:capacidad transversal|base com[uú]n|features futuras)\b",
    re.IGNORECASE,
)
MODULE_LANGUAGE_RE = re.compile(
    r"\b(?:subsistema espec[íi]fico|m[oó]dulo espec[íi]fico|alcance acotado)\b",
    re.IGNORECASE,
)
DUPLICATE_SEPARATOR_RE = re.compile(r"(?ms)^---\s*$\n^\s*$\n^---\s*$")
SPEC_BOILERPLATE_MARKERS = (
    "### ADR aplicables",
    "### Baseline de observabilidad (EN-0200)",
)
SHARED_PAGINATION_REF = "SHARED-0002-pagination-contract.md"
SHARED_AUDIT_SOFT_DELETE_REF = "SHARED-0001-audit-and-soft-delete.md"
SHARED_API_RESPONSE_REF = "SHARED-0003-api-response-conventions.md"
SHARED_FINANCIAL_REF = "SHARED-0004-financial-entity-semantics.md"
SHARED_IDEMPOTENCY_REF = "SHARED-0005-idempotency-contract.md"
IDEMPOTENCY_MARKERS = (
    re.compile(r"\bidempotency_key\b", re.IGNORECASE),
    re.compile(r"\bautomation_key\b", re.IGNORECASE),
    re.compile(r"\bidempotenc(?:ia|y)\b", re.IGNORECASE),
    re.compile(r"\breintentos?\b", re.IGNORECASE),
    re.compile(r"\boperaci[oó]n l[oó]gica\b", re.IGNORECASE),
)
FINANCIAL_SEMANTICS_MARKERS = (
    re.compile(r"\beffect_sign\b", re.IGNORECASE),
    re.compile(
        r"\beffective_(?:amount|base|vat|withholding|gross|net|applied|outstanding|unallocated)(?:_[a-z]+)?\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bgross_(?:amount|total)\b", re.IGNORECASE),
    re.compile(r"\bnet_payable_(?:amount|total)\b", re.IGNORECASE),
)
PAGINATION_MARKERS = (
    re.compile(r"\bpaginaci[oó]n\b", re.IGNORECASE),
    re.compile(r"\bpage_size\b", re.IGNORECASE),
    re.compile(r"\bper_page\b", re.IGNORECASE),
    re.compile(r"\bpaged?\b", re.IGNORECASE),
    re.compile(r"\bcolecci[oó]n(?:es)?\b", re.IGNORECASE),
)
API_CONTRACT_MARKERS = (
    re.compile(r"\bHTTP\b", re.IGNORECASE),
    re.compile(r"\bendpoint(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bJSON\b", re.IGNORECASE),
    re.compile(r"\bREST(?:ful)?\b", re.IGNORECASE),
    re.compile(r"\bOpenAPI\b", re.IGNORECASE),
)
AUDIT_SOFT_DELETE_MARKERS = (
    re.compile(r"\bsoft[\s-]?delete\b", re.IGNORECASE),
    re.compile(r"\bdeleted_at\b", re.IGNORECASE),
    re.compile(r"\bdeleted_by\b", re.IGNORECASE),
    re.compile(r"\bcreated_at\b", re.IGNORECASE),
    re.compile(r"\bcreated_by\b", re.IGNORECASE),
    re.compile(r"\bupdated_at\b", re.IGNORECASE),
    re.compile(r"\bupdated_by\b", re.IGNORECASE),
    re.compile(r"\binclude_deleted\b", re.IGNORECASE),
)
API_RESPONSE_MARKERS = (
    re.compile(r"\bJSON\b", re.IGNORECASE),
    re.compile(r"\berror_code\b", re.IGNORECASE),
    re.compile(r"\bsnake_case\b", re.IGNORECASE),
    re.compile(r"\brespuesta(?:s)?\s+de\s+API\b", re.IGNORECASE),
    re.compile(r"\brespuesta(?:s)?\s+serializada(?:s)?\b", re.IGNORECASE),
    re.compile(r"\bserializad[ao]s?\b", re.IGNORECASE),
    re.compile(r"\bvalor\s+`?null`?\b", re.IGNORECASE),
    re.compile(r"\bcampos?\s+opcionales?\s+serializados?\b", re.IGNORECASE),
    re.compile(r"\brespuestas?\s+de\s+error\b", re.IGNORECASE),
    re.compile(r"\bmessage\b", re.IGNORECASE),
)
STACK_SPECIFIC_MARKERS = (
    re.compile(r"\bFastAPI\b", re.IGNORECASE),
    re.compile(r"\bSQLAlchemy\b", re.IGNORECASE),
    re.compile(r"\bSQLite\b", re.IGNORECASE),
    re.compile(r"\bDocker(?: Compose)?\b", re.IGNORECASE),
    re.compile(r"\bJWT\b", re.IGNORECASE),
    re.compile(r"\bPydantic\b", re.IGNORECASE),
    re.compile(r"\bAlembic\b", re.IGNORECASE),
    re.compile(r"\bOpenAPI\b", re.IGNORECASE),
    re.compile(r"\bMQTT\b", re.IGNORECASE),
    re.compile(r"\bCloudEvents\b", re.IGNORECASE),
)
CONVENTIONS_NORMATIVE_MARKERS = (
    re.compile(r"\breglas globales\b", re.IGNORECASE),
    re.compile(r"\binvariantes?\b", re.IGNORECASE),
    re.compile(r"\bdecisiones tecnol[oó]gicas concretas\b", re.IGNORECASE),
)
FORBIDDEN_SPEC_HEADINGS = {"Notas de implementación (opcional)"}


# Data model
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
    titles: dict[str, str]
    invalid_files: list[Path]
    duplicate_ids: list[tuple[str, Path, Path]]


@dataclass
class ManifestItem:
    id: str
    spec: str
    primary_scope: str
    affected_scopes: list[str]
    adr_refs: list[str]
    constitution_sections: list[str]
    context_sections: list[str]


@dataclass
class ParsedManifest:
    items: dict[str, ManifestItem]


@dataclass
class AdrReference:
    adr_id: str
    adr_title: str
    reason: str


@dataclass
class ParsedAdrMap:
    items: dict[str, list[AdrReference]]


ADR_REASON_VALUES = {
    "monorepo_architecture",
    "architecture",
    "persistence",
    "api_contract",
    "authentication",
    "integration_contracts",
    "delivery",
    "governance_ci",
    "observability_errors",
    "event_delivery",
    "money_percentages",
    "time_policy",
    "configuration",
    "idempotency",
}

CONSTITUTION_SECTION_TO_ADR_REASONS: dict[str, set[str]] = {
    "api_contracts": {"api_contract"},
    "api_versioning": {"api_contract", "integration_contracts"},
    "observability": {"observability_errors"},
    "monetary_policy": {"money_percentages"},
    "percentage_representation": {"money_percentages"},
    "time_policy": {"time_policy"},
    "idempotency": {"idempotency"},
}


@dataclass
class SliceDefinition:
    constitution_sections: list[str]
    context_sections: list[str]


@dataclass
class ParsedContextSlices:
    slices: dict[str, SliceDefinition]
    assignments: dict[str, list[str]]


@dataclass
class ParsedSections:
    constitution: set[str]
    context: set[str]


class LintError(Exception):
    """Raised for fatal loading/parsing errors."""


# Entry points
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
        manifest = load_item_manifest(planning_dir / "item-manifest.yaml")
        adr_map = load_adr_map(planning_dir / "adr-map.yaml")
        context_slices = load_context_slices(planning_dir / "context-slices.yaml")
        system_sections = load_system_sections(system_dir)
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
    messages.extend(validate_specs_format(specs, graph, adrs, docs_root))
    messages.extend(validate_index_files(specs_dir, specs))
    messages.extend(validate_index_order(specs_dir))
    messages.extend(validate_index_link_format(specs_dir))
    messages.extend(validate_shared_files(specs_dir / "shared"))

    messages.extend(validate_adrs(adrs, strict=args.strict))
    messages.extend(validate_adr_files(adrs))
    messages.extend(validate_adr_index(decisions_dir, adrs))
    messages.extend(validate_item_manifest(manifest, graph, specs, adrs, adr_map, system_sections))
    messages.extend(validate_adr_map(adr_map, graph, adrs, manifest))
    messages.extend(validate_spec_semantic_alignment(specs, adr_map, graph))
    messages.extend(
        validate_context_slices(
            context_slices,
            graph,
            system_sections,
            manifest,
        )
    )
    messages.extend(validate_system_files(system_dir))

    return print_report(messages)


# Repository structure validation
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
        docs_root / "specs" / "shared",
        docs_root / "sdd",
        docs_root / "sdd" / "templates",
        docs_root / "meta",
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
        docs_root / "planning" / "item-manifest.yaml",
        docs_root / "planning" / "adr-map.yaml",
        docs_root / "planning" / "context-slices.yaml",
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

        if path.name == "constitution.md":
            messages.extend(validate_constitution_content(path, content))
        elif path.name == "conventions.md":
            messages.extend(validate_conventions_content(path, content))

    return messages


def validate_constitution_content(path: Path, content: str) -> list[LintMessage]:
    messages: list[LintMessage] = []

    found_markers = sorted(
        {
            match.group(0)
            for pattern in STACK_SPECIFIC_MARKERS
            for match in pattern.finditer(content)
        }
    )
    if found_markers:
        messages.append(
            error(
                "SYS-003",
                f"{path} must remain stack-agnostic and should not mention concrete technologies: {', '.join(found_markers)}",
            )
        )

    return messages


def validate_conventions_content(path: Path, content: str) -> list[LintMessage]:
    messages: list[LintMessage] = []

    found_stack_markers = sorted(
        {
            match.group(0)
            for pattern in STACK_SPECIFIC_MARKERS
            for match in pattern.finditer(content)
        }
    )
    if found_stack_markers:
        messages.append(
            warn(
                "SYS-004",
                f"{path} should avoid concrete technology names unless strictly needed for naming or style guidance: {', '.join(found_stack_markers)}",
            )
        )

    if "no define reglas invariantes del sistema" not in content.lower():
        messages.append(
            warn(
                "SYS-005",
                f"{path} should explicitly state that it does not define system invariants",
            )
        )

    found_normative_markers = sorted(
        {
            match.group(0)
            for pattern in CONVENTIONS_NORMATIVE_MARKERS
            for match in pattern.finditer(content)
        }
    )
    if not found_normative_markers:
        return messages

    return messages


# Index validation
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


# Parsing and loading
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
    titles: dict[str, str] = {}
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
                titles[adr_id] = extract_adr_title(path)

    return ParsedAdrs(
        ids=ids,
        titles=titles,
        invalid_files=invalid_files,
        duplicate_ids=duplicate_ids,
    )


def load_item_manifest(path: Path) -> ParsedManifest:
    if not path.exists():
        raise LintError(f"Missing file: {path}")

    raw = load_yaml_file(path)
    items_raw = raw.get("items")
    if not isinstance(items_raw, dict):
        raise LintError(f"{path} must contain top-level key 'items' as a mapping")

    items: dict[str, ManifestItem] = {}
    for item_id, entry in items_raw.items():
        if not isinstance(item_id, str):
            raise LintError(f"{path}: item manifest IDs must be strings")
        if not isinstance(entry, dict):
            raise LintError(f"{path}: item {item_id} must be a mapping")

        spec = require_str(path, item_id, entry, "spec")
        primary_scope = require_str(path, item_id, entry, "primary_scope")
        affected_scopes = require_list_of_str(path, item_id, entry, "affected_scopes")
        adr_refs = optional_list_of_str(path, item_id, entry, "adr_refs")
        constitution_sections = require_list_of_str(
            path, item_id, entry, "constitution_sections"
        )
        context_sections = require_list_of_str(path, item_id, entry, "context_sections")

        items[item_id] = ManifestItem(
            id=item_id,
            spec=spec,
            primary_scope=primary_scope,
            affected_scopes=affected_scopes,
            adr_refs=adr_refs,
            constitution_sections=constitution_sections,
            context_sections=context_sections,
        )

    return ParsedManifest(items=items)


def load_adr_map(path: Path) -> ParsedAdrMap:
    if not path.exists():
        raise LintError(f"Missing file: {path}")

    raw = load_yaml_file(path)
    items_raw = raw.get("items")
    if not isinstance(items_raw, dict):
        raise LintError(f"{path} must contain top-level key 'items' as a mapping")

    items: dict[str, list[AdrReference]] = {}
    for item_id, entry in items_raw.items():
        if not isinstance(item_id, str):
            raise LintError(f"{path}: ADR map IDs must be strings")
        if not isinstance(entry, dict):
            raise LintError(f"{path}: item {item_id} must be a mapping")

        adrs_raw = entry.get("adrs", [])
        if not isinstance(adrs_raw, list):
            raise LintError(f"{path}: item {item_id} field 'adrs' must be a list")

        refs: list[AdrReference] = []
        for index, adr_entry in enumerate(adrs_raw):
            if not isinstance(adr_entry, dict):
                raise LintError(
                    f"{path}: item {item_id} ADR entry at index {index} must be a mapping"
                )
            adr_id = require_str(path, item_id, adr_entry, "adr_id")
            adr_title = require_str(path, item_id, adr_entry, "adr_title")
            reason = require_str(path, item_id, adr_entry, "reason")
            refs.append(AdrReference(adr_id=adr_id, adr_title=adr_title, reason=reason))

        items[item_id] = refs

    return ParsedAdrMap(items=items)


def load_context_slices(path: Path) -> ParsedContextSlices:
    if not path.exists():
        raise LintError(f"Missing file: {path}")

    raw = load_yaml_file(path)
    slices_raw = raw.get("slices")
    assignments_raw = raw.get("assignments")
    if not isinstance(slices_raw, dict):
        raise LintError(f"{path} must contain top-level key 'slices' as a mapping")
    if not isinstance(assignments_raw, dict):
        raise LintError(f"{path} must contain top-level key 'assignments' as a mapping")

    slices: dict[str, SliceDefinition] = {}
    for slice_name, entry in slices_raw.items():
        if not isinstance(slice_name, str):
            raise LintError(f"{path}: slice names must be strings")
        if not isinstance(entry, dict):
            raise LintError(f"{path}: slice {slice_name} must be a mapping")

        constitution_sections = require_list_of_str(
            path, slice_name, entry, "constitution_sections"
        )
        context_sections = require_list_of_str(path, slice_name, entry, "context_sections")
        slices[slice_name] = SliceDefinition(
            constitution_sections=constitution_sections,
            context_sections=context_sections,
        )

    assignments: dict[str, list[str]] = {}
    for item_id, entry in assignments_raw.items():
        if not isinstance(item_id, str):
            raise LintError(f"{path}: assignment IDs must be strings")
        if not isinstance(entry, dict):
            raise LintError(f"{path}: assignment for {item_id} must be a mapping")
        assignments[item_id] = require_list_of_str(path, item_id, entry, "slices")

    return ParsedContextSlices(slices=slices, assignments=assignments)


def load_system_sections(system_dir: Path) -> ParsedSections:
    constitution_path = system_dir / "constitution.md"
    context_path = system_dir / "context.md"
    try:
        constitution = extract_section_ids(constitution_path.read_text(encoding="utf-8"))
        context = extract_section_ids(context_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LintError(f"Failed reading system section files: {exc}") from exc

    return ParsedSections(constitution=constitution, context=context)


def load_yaml_file(path: Path) -> dict:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise LintError(f"Invalid YAML in {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise LintError(f"{path} must contain a top-level mapping")

    return raw


def require_str(path: Path, item_id: str, entry: dict, field: str) -> str:
    value = entry.get(field)
    if not isinstance(value, str) or not value.strip():
        raise LintError(f"{path}: item {item_id} missing non-empty string field '{field}'")
    return value


def require_list_of_str(path: Path, item_id: str, entry: dict, field: str) -> list[str]:
    value = entry.get(field)
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise LintError(f"{path}: item {item_id} field '{field}' must be a list[str]")
    return value


def optional_list_of_str(path: Path, item_id: str, entry: dict, field: str) -> list[str]:
    value = entry.get(field, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(v, str) and v.strip() for v in value):
        raise LintError(f"{path}: item {item_id} field '{field}' must be a list[str]")
    return value


def extract_adr_title(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = ADR_TITLE_RE.search(content)
    if not match:
        raise LintError(f"{path} must start with '# ADR-xxxx: Title'")
    return match.group(2).strip()


def extract_shared_title(path: Path) -> str:
    content = path.read_text(encoding="utf-8")
    match = SHARED_TITLE_RE.search(content)
    if not match:
        raise LintError(f"{path} must start with '# SHARED-xxxx: Title'")
    return match.group(2).strip()


def extract_section_ids(content: str) -> set[str]:
    return set(SECTION_ID_RE.findall(content))


# Specs index validation
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


# Dependency graph validation
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


# Roadmap validation
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


# Specs and ADR inventory validation
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
                    f"Spec {specs.feature_specs[item_id]} is under features/ "
                    f"but graph type for {item_id} is {graph_item.type}",
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
                    f"Spec {specs.enabler_specs[item_id]} is under enablers/ "
                    f"but graph type for {item_id} is {graph_item.type}",
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


# ADR and planning metadata validation
def validate_adr_files(adrs: ParsedAdrs) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for adr_id, path in sorted(adrs.ids.items()):
        content = read_text_for_validation(path, messages, "ADR-009")
        if content is None:
            continue

        messages.extend(validate_adr_title(path, adr_id, content))
        messages.extend(validate_adr_required_sections(path, content))
        messages.extend(validate_markdown_duplicate_separators(path, content, "ADR-013"))
        messages.extend(validate_required_h2_section_bodies(path, content, ("Status", "Context", "Decision"), "ADR-014"))

    return messages


def validate_shared_files(shared_dir: Path) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for path in sorted(shared_dir.glob("*.md")):
        if path.name == "README.md":
            continue

        match = SHARED_FILE_RE.match(path.name)
        if not match:
            messages.append(
                error(
                    "SHARED-001",
                    f"Invalid shared spec filename: {path}. Expected SHARED-0001-name.md",
                )
            )
            continue

        content = read_text_for_validation(path, messages, "SHARED-002")
        if content is None:
            continue

        title_match = SHARED_TITLE_RE.search(content)
        if not title_match:
            messages.append(
                error("SHARED-003", f"{path} must start with '# SHARED-xxxx: Title'")
            )
            continue

        expected_title_id = f"SHARED-{match.group(1)}"
        if title_match.group(1) != expected_title_id:
            messages.append(
                error(
                    "SHARED-004",
                    f"{path} title ID {title_match.group(1)} does not match filename {expected_title_id}",
                )
            )

    return messages


def validate_item_manifest(
    manifest: ParsedManifest,
    graph: dict[str, GraphItem],
    specs: ParsedSpecs,
    adrs: ParsedAdrs,
    adr_map: ParsedAdrMap,
    system_sections: ParsedSections,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    spec_paths = build_spec_path_map(specs)
    messages.extend(
        validate_mapping_coverage(
            found_ids=set(manifest.items),
            expected_ids=set(graph),
            missing_code="MANIFEST-002",
            missing_template="Dependency graph item {item_id} is missing in item-manifest.yaml",
            unknown_code="MANIFEST-001",
            unknown_template="item-manifest.yaml references unknown item {item_id}",
        )
    )

    for item_id, entry in sorted(manifest.items.items()):
        if item_id not in graph:
            continue

        messages.extend(validate_manifest_spec_path(item_id, entry, graph[item_id], spec_paths))
        messages.extend(validate_manifest_scope(item_id, entry))
        messages.extend(validate_manifest_duplicates(item_id, entry))
        messages.extend(validate_manifest_adr_refs(item_id, entry, adrs, adr_map))
        messages.extend(validate_manifest_sections(item_id, entry, system_sections))

    return messages


def validate_adr_map(
    adr_map: ParsedAdrMap,
    graph: dict[str, GraphItem],
    adrs: ParsedAdrs,
    manifest: ParsedManifest,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    messages.extend(
        validate_mapping_coverage(
            found_ids=set(adr_map.items),
            expected_ids=set(graph),
            missing_code="ADRMAP-002",
            missing_template="Dependency graph item {item_id} is missing in adr-map.yaml",
            unknown_code="ADRMAP-001",
            unknown_template="adr-map.yaml references unknown item {item_id}",
        )
    )

    for item_id, refs in sorted(adr_map.items.items()):
        if item_id not in graph:
            continue

        messages.extend(validate_adr_map_refs(item_id, refs, adrs))
        messages.extend(validate_adr_map_vs_manifest(item_id, refs, manifest))
        messages.extend(validate_adr_map_manifest_alignment(item_id, refs, manifest))
        messages.extend(validate_adr_map_reason_uniqueness(item_id, refs))
        messages.extend(validate_adr_map_expected_reasons(item_id, refs, manifest))

    return messages


def validate_context_slices(
    context_slices: ParsedContextSlices,
    graph: dict[str, GraphItem],
    system_sections: ParsedSections,
    manifest: ParsedManifest,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    messages.extend(
        validate_mapping_coverage(
            found_ids=set(context_slices.assignments),
            expected_ids=set(graph),
            missing_code="SLICE-002",
            missing_template="Dependency graph item {item_id} is missing in context-slices.yaml",
            unknown_code="SLICE-001",
            unknown_template="context-slices.yaml assigns slices to unknown item {item_id}",
        )
    )

    for slice_name, definition in sorted(context_slices.slices.items()):
        messages.extend(validate_slice_definition(slice_name, definition, system_sections))

    for item_id, slice_names in sorted(context_slices.assignments.items()):
        messages.extend(validate_item_slice_refs(item_id, slice_names, context_slices))
        messages.extend(validate_item_slice_coverage(item_id, slice_names, context_slices, manifest))

    return messages


# Spec format validation
def validate_specs_format(
    specs: ParsedSpecs,
    graph: dict[str, GraphItem],
    adrs: ParsedAdrs,
    docs_root: Path,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item_id, path in iter_spec_items(specs):
        graph_item = graph.get(item_id)
        if graph_item is None:
            continue

        content = read_text_for_validation(path, messages, "SPECFMT-001")
        if content is None:
            continue

        messages.extend(validate_spec_title(path, item_id, content))
        messages.extend(validate_spec_template_markers(path, content))
        messages.extend(validate_spec_headings(path, graph_item.type, content))
        messages.extend(validate_spec_required_section_bodies(path, graph_item.type, content))
        messages.extend(validate_spec_dependencies_note(path, content))
        messages.extend(validate_spec_shared_refs(path, content, docs_root))
        messages.extend(validate_spec_adr_refs(path, content, adrs))
        messages.extend(validate_spec_item_refs(path, item_id, content, graph))
        messages.extend(validate_spec_delivery_markers(path, graph_item, content))
        messages.extend(validate_enabler_scope_semantics(path, graph_item, content))
        messages.extend(validate_markdown_duplicate_separators(path, content, "SPECFMT-015"))
        messages.extend(validate_spec_redundant_boilerplate(path, content))

    return messages


def validate_spec_semantic_alignment(
    specs: ParsedSpecs,
    adr_map: ParsedAdrMap,
    graph: dict[str, GraphItem],
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    for item_id, path in iter_spec_items(specs):
        graph_item = graph.get(item_id)
        if graph_item is None:
            continue

        content = read_text_for_validation(path, messages, "SPECFMT-001")
        if content is None:
            continue

        shared_refs = set(SHARED_SPEC_REF_RE.findall(content))
        item_reasons = {ref.reason for ref in adr_map.items.get(item_id, [])}

        messages.extend(
            validate_spec_shared_semantics(path, graph_item.type, shared_refs, content)
        )
        messages.extend(
            validate_spec_shared_duplication(path, graph_item.type, shared_refs, content)
        )
        messages.extend(
            validate_spec_adr_reason_semantics(
                path,
                item_id,
                graph_item.type,
                item_reasons,
                shared_refs,
                content,
            )
        )

    return messages


# Shared validation helpers
def read_text_for_validation(
    path: Path, messages: list[LintMessage], code: str
) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        messages.append(error(code, f"Failed reading {path}: {exc}"))
        return None


def validate_adr_title(path: Path, adr_id: str, content: str) -> list[LintMessage]:
    match = ADR_TITLE_RE.search(content)
    if not match:
        return [error("ADR-010", f"{path} must start with '# ADR-xxxx: Title'")]

    expected_title_id = f"ADR-{adr_id}"
    if match.group(1) == expected_title_id:
        return []

    return [
        error(
            "ADR-011",
            f"{path} title ID {match.group(1)} does not match filename {expected_title_id}",
        )
    ]


def validate_adr_required_sections(path: Path, content: str) -> list[LintMessage]:
    messages: list[LintMessage] = []
    headings = H2_RE.findall(content)
    for required_heading in ("Status", "Context", "Decision"):
        if required_heading not in headings:
            messages.append(
                error(
                    "ADR-012",
                    f"{path} is missing required section '## {required_heading}'",
                )
            )
    return messages


def extract_h2_sections(content: str) -> list[tuple[str, str]]:
    matches = list(H2_RE.finditer(content))
    sections: list[tuple[str, str]] = []

    for idx, match in enumerate(matches):
        heading = match.group(1).strip()
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(content)
        body = content[body_start:body_end]
        sections.append((heading, body))

    return sections


def normalize_section_body(body: str) -> str:
    lines = []
    for raw_line in body.splitlines():
        stripped = raw_line.strip()
        if stripped == "---":
            continue
        lines.append(raw_line)
    return "\n".join(lines).strip()


def validate_required_h2_section_bodies(
    path: Path,
    content: str,
    required_headings: tuple[str, ...],
    code: str,
) -> list[LintMessage]:
    section_map = {heading: body for heading, body in extract_h2_sections(content)}
    messages: list[LintMessage] = []

    for heading in required_headings:
        body = section_map.get(heading)
        if body is None:
            continue
        if normalize_section_body(body):
            continue
        messages.append(error(code, f"{path} section '## {heading}' must not be empty"))

    return messages


def build_spec_path_map(specs: ParsedSpecs) -> dict[str, Path]:
    return {
        **{item_id: path for item_id, path in specs.feature_specs.items()},
        **{item_id: path for item_id, path in specs.enabler_specs.items()},
    }


def validate_mapping_coverage(
    *,
    found_ids: set[str],
    expected_ids: set[str],
    missing_code: str,
    missing_template: str,
    unknown_code: str,
    unknown_template: str,
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for item_id in sorted(found_ids - expected_ids):
        messages.append(error(unknown_code, unknown_template.format(item_id=item_id)))
    for item_id in sorted(expected_ids - found_ids):
        messages.append(error(missing_code, missing_template.format(item_id=item_id)))
    return messages


def find_duplicates(values: list[str]) -> list[str]:
    return sorted({value for value in values if values.count(value) > 1})


def is_ordered_subsequence(expected: list[str], sequence: list[str]) -> bool:
    if not expected:
        return True

    idx = 0
    for value in sequence:
        if value == expected[idx]:
            idx += 1
            if idx == len(expected):
                return True

    return False


def validate_manifest_spec_path(
    item_id: str,
    entry: ManifestItem,
    graph_item: GraphItem,
    spec_paths: dict[str, Path],
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    spec_path = Path(entry.spec)
    if not spec_path.exists():
        messages.append(
            error(
                "MANIFEST-003",
                f"Manifest item {item_id} references missing spec path {entry.spec}",
            )
        )

    expected_path = spec_paths.get(item_id)
    if expected_path is not None and spec_path.as_posix() != expected_path.as_posix():
        messages.append(
            error(
                "MANIFEST-004",
                f"Manifest item {item_id} points to {entry.spec} but spec file is {expected_path.as_posix()}",
            )
        )

    expected_folder = "features" if graph_item.type == "feature" else "enablers"
    if expected_folder not in spec_path.parts:
        messages.append(
            error(
                "MANIFEST-005",
                f"Manifest item {item_id} spec path must live under docs/specs/{expected_folder}/",
            )
        )

    return messages


def validate_manifest_scope(item_id: str, entry: ManifestItem) -> list[LintMessage]:
    if entry.primary_scope in entry.affected_scopes:
        return []
    return [
        error(
            "MANIFEST-006",
            f"Manifest item {item_id} primary_scope '{entry.primary_scope}' must be included in affected_scopes",
        )
    ]


def validate_manifest_duplicates(item_id: str, entry: ManifestItem) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for field_name, values in (
        ("affected_scopes", entry.affected_scopes),
        ("adr_refs", entry.adr_refs),
        ("constitution_sections", entry.constitution_sections),
        ("context_sections", entry.context_sections),
    ):
        duplicates = find_duplicates(values)
        if duplicates:
            messages.append(
                error(
                    "MANIFEST-007",
                    f"Manifest item {item_id} field '{field_name}' contains duplicates: {', '.join(duplicates)}",
                )
            )
    return messages


def validate_manifest_adr_refs(
    item_id: str, entry: ManifestItem, adrs: ParsedAdrs, adr_map: ParsedAdrMap
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for adr_id in entry.adr_refs:
        if adr_id.replace("ADR-", "") not in adrs.ids:
            messages.append(
                error(
                    "MANIFEST-008",
                    f"Manifest item {item_id} references unknown ADR {adr_id}",
                )
            )
    if not entry.adr_refs and adr_map.items.get(item_id):
        messages.append(
            warn(
                "MANIFEST-011",
                f"Manifest item {item_id} should declare adr_refs as an ordered shortlist aligned with adr-map.yaml",
            )
        )
    return messages


def validate_manifest_sections(
    item_id: str, entry: ManifestItem, system_sections: ParsedSections
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    messages.extend(
        validate_manifest_section_list(
            item_id,
            "constitution",
            entry.constitution_sections,
            system_sections.constitution,
            "MANIFEST-009",
        )
    )
    messages.extend(
        validate_manifest_section_list(
            item_id,
            "context",
            entry.context_sections,
            system_sections.context,
            "MANIFEST-010",
        )
    )
    return messages


def validate_manifest_section_list(
    item_id: str,
    section_kind: str,
    values: list[str],
    valid_sections: set[str],
    code: str,
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for section_id in values:
        if section_id not in valid_sections:
            messages.append(
                error(
                    code,
                    f"Manifest item {item_id} references unknown {section_kind} section {section_id}",
                )
            )
    return messages


def validate_adr_map_refs(
    item_id: str, refs: list[AdrReference], adrs: ParsedAdrs
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    seen: set[str] = set()

    for ref in refs:
        adr_key = ref.adr_id.replace("ADR-", "")
        if ref.adr_id in seen:
            messages.append(
                error(
                    "ADRMAP-003",
                    f"adr-map.yaml item {item_id} contains duplicate ADR {ref.adr_id}",
                )
            )
        seen.add(ref.adr_id)

        if adr_key not in adrs.ids:
            messages.append(
                error(
                    "ADRMAP-004",
                    f"adr-map.yaml item {item_id} references unknown ADR {ref.adr_id}",
                )
            )
            continue

        expected_title = adrs.titles.get(adr_key)
        if expected_title is not None and ref.adr_title != expected_title:
            messages.append(
                error(
                    "ADRMAP-005",
                    f"adr-map.yaml item {item_id} ADR {ref.adr_id} title '{ref.adr_title}' must match '{expected_title}'",
                )
            )

        if ref.reason not in ADR_REASON_VALUES:
            messages.append(
                error(
                    "ADRMAP-008",
                    f"adr-map.yaml item {item_id} ADR {ref.adr_id} uses unknown reason '{ref.reason}'",
                )
            )

    return messages


def validate_adr_map_vs_manifest(
    item_id: str, refs: list[AdrReference], manifest: ParsedManifest
) -> list[LintMessage]:
    manifest_item = manifest.items.get(item_id)
    if manifest_item is None:
        return []

    mapped_adr_ids = {ref.adr_id for ref in refs}
    missing_manifest_refs = sorted(set(manifest_item.adr_refs) - mapped_adr_ids)
    if not missing_manifest_refs:
        return []

    return [
        error(
            "ADRMAP-006",
            f"Manifest item {item_id} references ADRs not present in adr-map.yaml: {', '.join(missing_manifest_refs)}",
        )
    ]


def validate_adr_map_manifest_alignment(
    item_id: str, refs: list[AdrReference], manifest: ParsedManifest
) -> list[LintMessage]:
    manifest_item = manifest.items.get(item_id)
    if manifest_item is None or not manifest_item.adr_refs:
        return []

    mapped_adr_ids = [ref.adr_id for ref in refs]
    manifest_adr_ids = manifest_item.adr_refs
    if is_ordered_subsequence(manifest_adr_ids, mapped_adr_ids):
        return []

    return [
        warn(
            "ADRMAP-007",
            f"Manifest item {item_id} adr_refs should remain an ordered shortlist aligned with adr-map.yaml",
        )
    ]


def validate_adr_map_reason_uniqueness(
    item_id: str, refs: list[AdrReference]
) -> list[LintMessage]:
    duplicates = find_duplicates([ref.reason for ref in refs])
    if not duplicates:
        return []

    return [
        warn(
            "ADRMAP-012",
            f"adr-map.yaml item {item_id} repeats ADR reasons that should normally be unique per item: {', '.join(duplicates)}",
        )
    ]


def validate_adr_map_expected_reasons(
    item_id: str, refs: list[AdrReference], manifest: ParsedManifest
) -> list[LintMessage]:
    manifest_item = manifest.items.get(item_id)
    if manifest_item is None:
        return []

    expected_reasons: set[str] = set()
    for section_id in manifest_item.constitution_sections:
        expected_reasons.update(CONSTITUTION_SECTION_TO_ADR_REASONS.get(section_id, set()))

    if not expected_reasons:
        return []

    present_reasons = {ref.reason for ref in refs}
    missing_reasons = sorted(expected_reasons - present_reasons)
    if not missing_reasons:
        return []

    return [
        warn(
            "ADRMAP-013",
            f"Manifest item {item_id} references constitution sections that imply ADR coverage missing in adr-map.yaml: {', '.join(missing_reasons)}",
        )
    ]


def validate_slice_definition(
    slice_name: str,
    definition: SliceDefinition,
    system_sections: ParsedSections,
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    messages.extend(
        validate_slice_section_list(
            slice_name,
            "constitution_sections",
            definition.constitution_sections,
            system_sections.constitution,
            "SLICE-003",
        )
    )
    messages.extend(
        validate_slice_section_list(
            slice_name,
            "context_sections",
            definition.context_sections,
            system_sections.context,
            "SLICE-004",
        )
    )
    return messages


def validate_slice_section_list(
    slice_name: str,
    field_name: str,
    values: list[str],
    valid_sections: set[str],
    code: str,
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    duplicates = find_duplicates(values)
    if duplicates:
        messages.append(
            error(
                code,
                f"Slice {slice_name} field '{field_name}' contains duplicates: {', '.join(duplicates)}",
            )
        )
    for section_id in values:
        if section_id not in valid_sections:
            messages.append(
                error(
                    code,
                    f"Slice {slice_name} references unknown section {section_id} in '{field_name}'",
                )
            )
    return messages


def validate_item_slice_refs(
    item_id: str,
    slice_names: list[str],
    context_slices: ParsedContextSlices,
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    seen: set[str] = set()
    for slice_name in slice_names:
        if slice_name in seen:
            messages.append(
                error(
                    "SLICE-005",
                    f"context-slices.yaml item {item_id} contains duplicate slice {slice_name}",
                )
            )
        seen.add(slice_name)
        if slice_name not in context_slices.slices:
            messages.append(
                error(
                    "SLICE-006",
                    f"context-slices.yaml item {item_id} references unknown slice {slice_name}",
                )
            )
    return messages


def validate_item_slice_coverage(
    item_id: str,
    slice_names: list[str],
    context_slices: ParsedContextSlices,
    manifest: ParsedManifest,
) -> list[LintMessage]:
    manifest_item = manifest.items.get(item_id)
    if manifest_item is None:
        return []

    constitution_union, context_union = collect_assigned_sections(slice_names, context_slices)
    messages: list[LintMessage] = []
    messages.extend(
        validate_section_coverage(
            item_id,
            "constitution",
            manifest_item.constitution_sections,
            constitution_union,
            "SLICE-007",
        )
    )
    messages.extend(
        validate_section_coverage(
            item_id,
            "context",
            manifest_item.context_sections,
            context_union,
            "SLICE-008",
        )
    )
    return messages


def collect_assigned_sections(
    slice_names: list[str], context_slices: ParsedContextSlices
) -> tuple[set[str], set[str]]:
    constitution_union: set[str] = set()
    context_union: set[str] = set()
    for slice_name in slice_names:
        definition = context_slices.slices.get(slice_name)
        if definition is None:
            continue
        constitution_union.update(definition.constitution_sections)
        context_union.update(definition.context_sections)
    return constitution_union, context_union


def validate_section_coverage(
    item_id: str,
    section_kind: str,
    required_sections: list[str],
    covered_sections: set[str],
    code: str,
) -> list[LintMessage]:
    missing_sections = sorted(set(required_sections) - covered_sections)
    if not missing_sections:
        return []

    return [
        error(
            code,
            f"Manifest item {item_id} {section_kind} sections are not covered by assigned slices: {', '.join(missing_sections)}",
        )
    ]


def iter_spec_items(specs: ParsedSpecs) -> list[tuple[str, Path]]:
    return [
        *sorted(specs.feature_specs.items()),
        *sorted(specs.enabler_specs.items()),
    ]


def validate_spec_title(path: Path, item_id: str, content: str) -> list[LintMessage]:
    title_match = SPEC_TITLE_RE.search(content)
    if not title_match:
        return [error("SPECFMT-002", f"{path} must start with '# {item_id}: Title'")]
    if title_match.group(1) == item_id:
        return []
    return [
        error(
            "SPECFMT-003",
            f"{path} title ID {title_match.group(1)} does not match filename item ID {item_id}",
        )
    ]


def validate_spec_template_markers(path: Path, content: str) -> list[LintMessage]:
    messages: list[LintMessage] = []
    if PLACEHOLDER_RE.search(content):
        messages.append(error("SPECFMT-004", f"{path} still contains template placeholders"))
    if "<<INSTRUCTION>>" in content or "<<END_INSTRUCTION>>" in content:
        messages.append(
            error("SPECFMT-005", f"{path} still contains template instruction markers")
        )
    return messages


def validate_spec_headings(path: Path, item_type: str, content: str) -> list[LintMessage]:
    required_headings = (
        FEATURE_REQUIRED_HEADINGS if item_type == "feature" else ENABLER_REQUIRED_HEADINGS
    )
    normalized_headings = [heading.strip() for heading in H2_RE.findall(content)]
    messages: list[LintMessage] = []

    if normalized_headings[: len(required_headings)] != required_headings:
        messages.append(
            error(
                "SPECFMT-006",
                f"{path} must contain the required sections in template order",
            )
        )

    extra_headings = normalized_headings[len(required_headings) :]
    forbidden = [heading for heading in extra_headings if heading in FORBIDDEN_SPEC_HEADINGS]
    if forbidden:
        messages.append(
            error(
                "SPECFMT-007",
                f"{path} contains forbidden legacy sections: {', '.join(forbidden)}",
            )
        )

    allowed_extra_headings = [heading for heading in extra_headings if heading not in FORBIDDEN_SPEC_HEADINGS]
    if allowed_extra_headings:
        messages.append(
            warn(
                "SPECFMT-021",
                f"{path} contains additional sections outside the standard template: {', '.join(allowed_extra_headings)}",
            )
        )

    return messages


def validate_spec_required_section_bodies(
    path: Path, item_type: str, content: str
) -> list[LintMessage]:
    required_headings = (
        FEATURE_REQUIRED_HEADINGS if item_type == "feature" else ENABLER_REQUIRED_HEADINGS
    )
    return validate_required_h2_section_bodies(
        path,
        content,
        tuple(required_headings),
        "SPECFMT-016",
    )


def validate_spec_dependencies_note(path: Path, content: str) -> list[LintMessage]:
    if (
        "docs/planning/dependency-graph.yaml" in content
        and "NO define dependencias" in content
    ):
        return []
    return [
        error(
            "SPECFMT-008",
            f"{path} must state that structural dependencies live in docs/planning/dependency-graph.yaml",
        )
    ]


def validate_spec_shared_refs(
    path: Path, content: str, docs_root: Path
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for shared_ref in SHARED_SPEC_REF_RE.findall(content):
        shared_path = docs_root / "specs" / "shared" / shared_ref
        if not shared_path.exists():
            messages.append(
                error(
                    "SPECFMT-009",
                    f"{path} references missing shared spec docs/specs/shared/{shared_ref}",
                )
            )
    return messages


def validate_spec_adr_refs(
    path: Path, content: str, adrs: ParsedAdrs
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for adr_ref in sorted(set(ADR_REF_RE.findall(content))):
        if adr_ref.replace("ADR-", "") not in adrs.ids:
            messages.append(error("SPECFMT-010", f"{path} references unknown ADR {adr_ref}"))
    return messages


def validate_spec_item_refs(
    path: Path, item_id: str, content: str, graph: dict[str, GraphItem]
) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for item_ref in sorted(set(ITEM_REF_RE.findall(content)) - {item_id}):
        if item_ref not in graph:
            messages.append(error("SPECFMT-011", f"{path} references unknown item {item_ref}"))
    return messages


def validate_markdown_duplicate_separators(
    path: Path, content: str, code: str
) -> list[LintMessage]:
    if DUPLICATE_SEPARATOR_RE.search(content):
        return [error(code, f"{path} contains adjacent markdown separators ('---') with no content between them")]
    return []


def validate_spec_redundant_boilerplate(path: Path, content: str) -> list[LintMessage]:
    messages: list[LintMessage] = []
    for marker in SPEC_BOILERPLATE_MARKERS:
        if marker not in content:
            continue
        messages.append(
            warn(
                "SPECFMT-017",
                f"{path} contains redundant implementation boilerplate ('{marker}'); resolve ADRs from adr-map.yaml and transversal rules from their source of truth",
            )
        )
    return messages


def has_any_marker(content: str, patterns: tuple[re.Pattern[str], ...]) -> bool:
    return any(pattern.search(content) for pattern in patterns)


def validate_spec_shared_semantics(
    path: Path, item_type: str, shared_refs: set[str], content: str
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    if item_type != "feature":
        return messages

    if (
        has_any_marker(content, IDEMPOTENCY_MARKERS)
        and SHARED_IDEMPOTENCY_REF not in shared_refs
    ):
        messages.append(
            warn(
                "SPECFMT-018",
                f"{path} uses idempotency semantics and should reference docs/specs/shared/{SHARED_IDEMPOTENCY_REF}",
            )
        )

    if (
        has_any_marker(content, FINANCIAL_SEMANTICS_MARKERS)
        and SHARED_FINANCIAL_REF not in shared_refs
    ):
        messages.append(
            warn(
                "SPECFMT-019",
                f"{path} uses shared financial semantics and should reference docs/specs/shared/{SHARED_FINANCIAL_REF}",
            )
        )

    if (
        has_any_marker(content, PAGINATION_MARKERS)
        and SHARED_PAGINATION_REF not in shared_refs
    ):
        messages.append(
            warn(
                "SPECFMT-020",
                f"{path} describes pagination or collection listing semantics and should reference docs/specs/shared/{SHARED_PAGINATION_REF}",
            )
        )

    return messages


def validate_spec_shared_duplication(
    path: Path, item_type: str, shared_refs: set[str], content: str
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    if item_type != "feature":
        return messages

    if (
        has_any_marker(content, AUDIT_SOFT_DELETE_MARKERS)
        and SHARED_AUDIT_SOFT_DELETE_REF not in shared_refs
    ):
        messages.append(
            warn(
                "SPECFMT-022",
                f"{path} describes audit or soft delete semantics and should reference docs/specs/shared/{SHARED_AUDIT_SOFT_DELETE_REF}",
            )
        )

    if (
        has_any_marker(content, API_RESPONSE_MARKERS)
        and SHARED_API_RESPONSE_REF not in shared_refs
    ):
        messages.append(
            warn(
                "SPECFMT-023",
                f"{path} describes shared API response conventions and should reference docs/specs/shared/{SHARED_API_RESPONSE_REF}",
            )
        )

    return messages


def validate_spec_adr_reason_semantics(
    path: Path,
    item_id: str,
    item_type: str,
    item_reasons: set[str],
    shared_refs: set[str],
    content: str,
) -> list[LintMessage]:
    messages: list[LintMessage] = []

    if (
        item_type == "feature"
        and has_any_marker(content, API_CONTRACT_MARKERS)
        and "api_contract" not in item_reasons
    ):
        messages.append(
            warn(
                "ADRMAP-009",
                f"{path} describes API or HTTP contract concerns but {item_id} has no ADR reason 'api_contract' in docs/planning/adr-map.yaml",
            )
        )

    if (
        item_type == "feature"
        and (
            SHARED_IDEMPOTENCY_REF in shared_refs
            or has_any_marker(content, IDEMPOTENCY_MARKERS)
        )
        and "idempotency" not in item_reasons
    ):
        messages.append(
            warn(
                "ADRMAP-010",
                f"{path} describes idempotency semantics but {item_id} has no ADR reason 'idempotency' in docs/planning/adr-map.yaml",
            )
        )

    if (
        item_type == "feature"
        and (
            SHARED_FINANCIAL_REF in shared_refs
            or has_any_marker(content, FINANCIAL_SEMANTICS_MARKERS)
        )
        and "money_percentages" not in item_reasons
    ):
        messages.append(
            warn(
                "ADRMAP-011",
                f"{path} describes shared money or percentage semantics but {item_id} has no ADR reason 'money_percentages' in docs/planning/adr-map.yaml",
            )
        )

    return messages


def validate_spec_delivery_markers(
    path: Path, graph_item: GraphItem, content: str
) -> list[LintMessage]:
    if graph_item.status != "done":
        return []

    markers = sorted(set(WORK_IN_PROGRESS_MARKER_RE.findall(content)))
    if not markers:
        return []

    return [
        error(
            "SPECFMT-012",
            f"{path} contains work-in-progress markers ({', '.join(markers)}) but {graph_item.id} is marked done in dependency-graph.yaml",
        )
    ]


def validate_enabler_scope_semantics(
    path: Path, graph_item: GraphItem, content: str
) -> list[LintMessage]:
    if graph_item.type != "enabler" or graph_item.scope is None:
        return []

    messages: list[LintMessage] = []
    if graph_item.scope == "module" and TRANSVERSAL_LANGUAGE_RE.search(content):
        messages.append(
            error(
                "SPECFMT-013",
                f"{path} describes {graph_item.id} with transversal language but dependency-graph.yaml marks its scope as module",
            )
        )

    if graph_item.scope == "cross_cutting" and MODULE_LANGUAGE_RE.search(content):
        messages.append(
            warn(
                "SPECFMT-014",
                f"{path} describes {graph_item.id} with module-scoped language but dependency-graph.yaml marks its scope as cross_cutting",
            )
        )

    return messages


# Generic utilities
def phase_rank(phase: str) -> int:
    return int(phase.replace("MVP", ""))


def error(code: str, message: str) -> LintMessage:
    return LintMessage(level="ERROR", code=code, message=message)


def warn(code: str, message: str) -> LintMessage:
    return LintMessage(level="WARN", code=code, message=message)


# Reporting
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
