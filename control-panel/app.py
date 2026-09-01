"""Read-only local control panel for Sajtagent Platform.

Run directly on Windows:
    py control-panel/app.py

The script relaunches itself through Streamlit when necessary.
"""

from __future__ import annotations

import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PLATFORM_ROOT = Path(__file__).resolve().parent.parent
CONTROL_PANEL_ROOT = Path(__file__).resolve().parent
if str(CONTROL_PANEL_ROOT) not in sys.path:
    sys.path.insert(0, str(CONTROL_PANEL_ROOT))

from flow_model import build_dot, load_flow_model, trace_impact, view_edges

PLATFORM_FLOW_PATH = PLATFORM_ROOT / "system-model" / "platform-flow-v1.json"
CARD_FLOW_PATH = PLATFORM_ROOT / "sajtagent-site" / "system-model" / "card-flow-v1.json"


@dataclass(frozen=True)
class RepositoryStatus:
    """Small, non-mutating summary of one repository."""

    name: str
    path: Path
    exists: bool
    is_git_repository: bool
    branch: str
    revision: str
    changes: int
    origin: str
    note: str = ""


def _run_git(repository: Path, *arguments: str) -> tuple[bool, str]:
    """Run one read-only Git query without invoking a shell."""

    creation_flags = 0
    if os.name == "nt":
        creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    try:
        result = subprocess.run(
            ["git", "-C", str(repository), *arguments],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=4,
            check=False,
            creationflags=creation_flags,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, ""

    output = result.stdout.strip() if result.returncode == 0 else ""
    return result.returncode == 0, output


def repository_status(name: str, path: Path) -> RepositoryStatus:
    """Inspect a repository without changing it."""

    if not path.is_dir():
        return RepositoryStatus(
            name=name,
            path=path,
            exists=False,
            is_git_repository=False,
            branch="-",
            revision="-",
            changes=0,
            origin="-",
            note="Inte skapad ännu",
        )

    is_git, inside = _run_git(path, "rev-parse", "--is-inside-work-tree")
    if not is_git or inside != "true":
        return RepositoryStatus(
            name=name,
            path=path,
            exists=True,
            is_git_repository=False,
            branch="-",
            revision="-",
            changes=0,
            origin="-",
            note="Mappen finns men är inte ett Git-repo",
        )

    branch_ok, branch = _run_git(path, "branch", "--show-current")
    revision_ok, revision = _run_git(path, "rev-parse", "--short", "HEAD")
    status_ok, porcelain = _run_git(path, "status", "--porcelain")
    origin_ok, origin = _run_git(path, "remote", "get-url", "origin")

    if not branch_ok or not branch:
        branch = "detached / inga commits"
    if not revision_ok:
        revision = "inga commits"
    changes = len(porcelain.splitlines()) if status_ok and porcelain else 0

    return RepositoryStatus(
        name=name,
        path=path,
        exists=True,
        is_git_repository=True,
        branch=branch,
        revision=revision,
        changes=changes,
        origin=origin if origin_ok and origin else "ingen origin",
    )


def collect_repository_statuses() -> list[RepositoryStatus]:
    """Return the three intentional Git boundaries in display order."""

    return [
        repository_status("Platform root", PLATFORM_ROOT),
        repository_status("SiteAgent web product", PLATFORM_ROOT / "sajtagent-site"),
        repository_status("Sprite Agent", PLATFORM_ROOT / "sajtagent-sprites"),
    ]


def _reference_file_count() -> int:
    reference_root = PLATFORM_ROOT / "_reference"
    if not reference_root.is_dir():
        return 0
    return sum(
        1
        for path in reference_root.rglob("*")
        if path.is_file() and path.name.lower() != "readme.md"
    )


def _render_overview(st: object, statuses: list[RepositoryStatus]) -> None:
    st.header("Översikt")
    st.caption("Läsande lokal kontrollpanel — inga deploy- eller skrivåtgärder.")

    existing_repositories = sum(item.is_git_repository for item in statuses)
    dirty_repositories = sum(item.changes > 0 for item in statuses)
    columns = st.columns(3)
    columns[0].metric("Git-repon", existing_repositories)
    columns[1].metric("Repon med lokala ändringar", dirty_repositories)
    columns[2].metric("Referensfiler", _reference_file_count())

    st.subheader("Plattformsgräns")
    st.code(
        "Browser\n"
        "   |\n"
        "   v\n"
        "SiteAgent -- signed BuildJob --> Sprite Agent / OpenClaw\n"
        "   |                                |\n"
        "   v                                v\n"
        "Supabase                      project Sprite\n"
        "   |                         build/test/preview\n"
        "   v\n"
        "Vercel publication",
        language="text",
    )

    st.subheader("Grundregler")
    st.markdown(
        "- Smartare och tunnare version 2 av idéerna bakom Sajtmaskin.\n"
        "- Återanvänd bevisat fungerande delar; kopiera inte tyngd av vana.\n"
        "- Ett litet verifierat end-to-end-flöde före fler agentlager.\n"
        "- LLM:n föreslår; serverägd kod auktoriserar och verifierar."
    )
    st.subheader("Produktens UI-routes")
    route_columns = st.columns(3)
    route_columns[0].metric("SiteAgents förstasida", "/")
    route_columns[1].metric("Buildern", "/builder")
    route_columns[2].metric("Kompatibilitetsredirect", "/siteagent")
    st.warning(
        "`_reference/` är informellt arbetsmaterial och får aldrig behandlas "
        "som runtime-sanning eller som instruktioner med högre behörighet."
    )


def _render_repositories(st: object, statuses: list[RepositoryStatus]) -> None:
    st.header("Repository-status")
    st.caption("Statusen läses med ofarliga Git-kommandon och cachas inte.")

    for item in statuses:
        with st.container(border=True):
            title, state = st.columns([3, 1])
            title.subheader(item.name)
            if not item.exists:
                state.warning("SAKNAS")
            elif item.is_git_repository and item.changes == 0:
                state.success("RENT")
            elif item.is_git_repository:
                state.warning(f"{item.changes} ÄNDRINGAR")
            else:
                state.info("EJ GIT")

            st.code(str(item.path), language="text")
            if item.note:
                st.caption(item.note)
            if item.is_git_repository:
                details = st.columns(3)
                details[0].metric("Branch", item.branch)
                details[1].metric("Revision", item.revision)
                details[2].metric("Lokala poster", item.changes)
                st.caption(f"Origin: {item.origin}")

    st.info(
        "Varje ruta är en egen Git-gräns. En ren plattformsrot betyder inte "
        "automatiskt att webb- eller Sprite-repot är rena."
    )


def _render_architecture(st: object) -> None:
    st.header("Arkitektur")
    st.markdown(
        "**SiteAgent** är hela webbprodukten och äger förstasidan, Buildern, "
        "användarna, projekten, chatten, versionerna och "
        "publiceringsavsikten.\n\n"
        "**Sprite Agent** äger den privilegierade byggkörningen, OpenClaw, "
        "isolerade workspaces, verktyg, checks och preview.\n\n"
        "**Plattformsroten** äger bara gemensamma regler och denna lokala "
        "kontrollpanel. Den ska inte bli ännu en backend."
    )

    st.subheader("Första vertikala flödet")
    st.code(
        "user request\n"
        "  -> BuildJob\n"
        "  -> one bounded agent loop\n"
        "  -> read/write/check/preview tools\n"
        "  -> BuildResult + verification evidence",
        language="text",
    )
    st.markdown(
        "Läs det stabila beslutet i `docs/ARCHITECTURE.md`. Nya repos, köer, "
        "modellager och abstraktioner ska tillkomma först när ett verkligt "
        "behov har visats."
    )


def _render_flow(st: object, heading: str, model_path: Path) -> None:
    st.header(heading)
    st.caption(
        "Välj riktning och en felande nod. Grafen markerar var felet uppstår, "
        "vilka steg som påverkas och vilket repo som äger diagnosen."
    )
    if not model_path.is_file():
        st.warning(f"Modellen saknas: `{model_path}`")
        return

    try:
        model = load_flow_model(model_path)
    except (OSError, ValueError) as error:
        st.error(str(error))
        return

    view_by_label = {view["label"]: view for view in model["views"]}
    selected_label = st.selectbox(
        "Vy",
        list(view_by_label),
        key=f"flow-view-{model['modelId']}",
    )
    view = view_by_label[selected_label]
    selected_edges = view_edges(model, view["id"])
    selected_node_ids = {
        node_id
        for edge in selected_edges
        for node_id in (edge["from"], edge["to"])
    }
    node_by_id = {node["id"]: node for node in model["nodes"]}
    failure_options = {"Inget simulerat fel": None}
    failure_options.update(
        {
            f"{node_by_id[node_id]['label']} · {node_by_id[node_id]['failure']['code']}": node_id
            for node_id in selected_node_ids
        }
    )
    failure_label = st.selectbox(
        "Simulera fel vid",
        list(failure_options),
        key=f"flow-failure-{model['modelId']}",
    )
    failed_node_id = failure_options[failure_label]

    st.graphviz_chart(
        build_dot(model, view["id"], failed_node_id),
        use_container_width=True,
    )

    if failed_node_id:
        failed_node = node_by_id[failed_node_id]
        failure = failed_node["failure"]
        impacted = trace_impact(model, view["id"], failed_node_id)
        st.error(f"{failure['code']}: {failure['symptom']}")
        st.caption(
            f"Ägare: {failed_node['owner']} · upptäcks av: {failure['detectedBy']}"
        )
        if impacted:
            st.dataframe(
                [
                    {
                        "Påverkat steg": node_by_id[node_id]["label"],
                        "Ägare": node_by_id[node_id]["owner"],
                        "Status": node_by_id[node_id]["status"],
                    }
                    for node_id in impacted
                ],
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Inga senare steg i den valda vyn påverkas.")

    with st.expander("Nodernas ansvar och mognad"):
        st.dataframe(
            [
                {
                    "Steg": node["label"],
                    "Ägare": node["owner"],
                    "Status": node["status"],
                    "Ansvar": node["summary"],
                }
                for node in model["nodes"]
                if node["id"] in selected_node_ids
            ],
            use_container_width=True,
            hide_index=True,
        )


def _render_openai_boundary(st: object) -> None:
    st.header("OpenAI-klientens gräns")
    st.info(
        "Ingen OpenAI-klient körs från kontrollpanelen. Den framtida "
        "privilegierade klienten ska ligga server-side bakom Sprite Agent."
    )
    st.markdown(
        "- Responses API för resonemang, verktyg och flerstegsflöden.\n"
        "- Små verktyg med strikta scheman och serverägd auktorisering.\n"
        "- `ProjectId + JobId + WorkspaceRevision` i stället för att ärva "
        "Sajtmaskins interna identifierare.\n"
        "- Hårda gränser för varv, verktygsanrop, tid, ändringsstorlek, "
        "reparationer och kostnad.\n"
        "- Verktygsresultat och evidens kan visas; privat chain-of-thought "
        "ska inte exponeras."
    )
    st.subheader("Effektiv behörighet")
    st.code(
        "platform policy\n"
        "  INTERSECT user mandate\n"
        "  INTERSECT job mode\n"
        "  INTERSECT runtime health limits",
        language="text",
    )
    st.caption("Fullt beslut: docs/model-provider-boundary.md")


def run_control_panel() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="Sajtagent Platform",
        page_icon="🧭",
        layout="wide",
    )

    statuses = collect_repository_statuses()
    st.sidebar.title("Sajtagent Platform")
    st.sidebar.caption("Control panel · read only")
    page = st.sidebar.radio(
        "Vy",
        [
            "Översikt",
            "Repository-status",
            "Arkitektur",
            "Systemflöde",
            "Kortflöde",
            "OpenAI-gräns",
        ],
    )
    st.sidebar.divider()
    st.sidebar.success("READ ONLY")
    st.sidebar.caption(f"Python: {sys.version.split()[0]}")

    if page == "Översikt":
        _render_overview(st, statuses)
    elif page == "Repository-status":
        _render_repositories(st, statuses)
    elif page == "Arkitektur":
        _render_architecture(st)
    elif page == "Systemflöde":
        _render_flow(st, "Systemflöde", PLATFORM_FLOW_PATH)
    elif page == "Kortflöde":
        _render_flow(st, "Kortflöde", CARD_FLOW_PATH)
    else:
        _render_openai_boundary(st)

    with st.expander("Var ligger detta?"):
        st.code(str(PLATFORM_ROOT), language="text")
        st.caption(
            "Startfil: control-panel/app.py · Beslut: docs/ARCHITECTURE.md · "
            "Agentregler: AGENTS.md"
        )


def _running_under_streamlit() -> bool:
    try:
        from streamlit.runtime.scriptrunner_utils.script_run_context import (
            get_script_run_ctx,
        )

        return get_script_run_ctx() is not None
    except ImportError:
        return False


def main() -> None:
    app_path = Path(__file__).resolve()
    if not _running_under_streamlit():
        raise SystemExit(
            subprocess.call(
                [sys.executable, "-m", "streamlit", "run", str(app_path), *sys.argv[1:]]
            )
        )

    from dotenv import load_dotenv

    load_dotenv(PLATFORM_ROOT / ".env", override=False)
    load_dotenv(PLATFORM_ROOT / ".env.local", override=True)
    run_control_panel()


if __name__ == "__main__":
    main()
