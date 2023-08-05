from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Optional

from ._ipython_utils import run_from_ipython
from ._version import VERSION
from .query.session import HttpException

if TYPE_CHECKING:
    from ipykernel.comm import Comm
    from ipykernel.ipkernel import IPythonKernel

    from ._sessions import Sessions
    from .cube import Cube
    from .query._cellset import Cellset
    from .query._context import Context
    from .session import Session

# Keep in sync with tokenCommTargetName in widget.tsx
_TOKEN_COMM_TARGET_NAME = "atoti-token"  # nosec
# Keep in sync with widgetCommTargetName in widget.tsx
_WIDGET_COMM_TARGET_NAME = "atoti-widget"

# Same naming scheme as Plotly:
# https://github.com/plotly/plotly.py/blob/3ca829c73bd4841666c8b810f5e8457514eb3c99/packages/javascript/jupyterlab-plotly/src/javascript-renderer-extension.ts#L24-L28
_WIDGET_MIME_TYPE = f"application/vnd.atoti.v{VERSION.split('.')[0]}+json"

_WidgetState = Any  # pylint: disable=invalid-name


@dataclass(frozen=True)
class _WidgetQuery:
    mdx: str
    context: Context


def _get_query(state: _WidgetState) -> _WidgetQuery:
    value = state["value"]
    body = value["body"]
    query = body["query"] if value["containerKey"] == "chart" else body
    mdx = query["mdx"]
    context = query.get("contextValues", {})
    return _WidgetQuery(mdx, context)


def _execute_query(session: Session, state: _WidgetState) -> Cellset:
    query = _get_query(state)
    query_session = session._open_query_session()  # pylint: disable=protected-access
    cellset = query_session._query_mdx_to_cellset(  # pylint: disable=protected-access
        query.mdx, query.context
    )
    return cellset


def _register_comm_targets(
    kernel: IPythonKernel,  # type: ignore
    sessions: Sessions,
):
    """Register Jupyter comm targets with our extension.

    - _TOKEN_COMM_TARGET_NAME sends fresh admin tokens.
      It stays open until the session is stopped or the browser tab is closed.
    - _WIDGET_COMM_TARGET_NAME detects if our extension is enabled
      and sends session details to the extension.
      It only stays open during the widget loading process.
    """

    def _token_callback(comm: Comm, open_msg: Any):  # type: ignore
        session_name = open_msg["content"]["data"]["session"]
        session = sessions[session_name]
        comm.send(
            {"token": session._generate_token()}  # pylint: disable=protected-access
        )

    def _widget_callback(comm: Comm, open_msg: Any):  # type: ignore
        session_name = open_msg["content"]["data"]["session"]
        session = sessions[session_name]
        comm.send(
            {
                "session": {
                    "port": session.port,
                    "token": session._generate_token(),  # pylint: disable=protected-access
                    "url": session.url,
                },
            }
        )

    kernel.comm_manager.register_target(_TOKEN_COMM_TARGET_NAME, _token_callback)
    kernel.comm_manager.register_target(_WIDGET_COMM_TARGET_NAME, _widget_callback)


class WidgetManager:
    """Register Jupyter comm targets and keep track of the widget state coming from kernel requests."""

    _state: Optional[_WidgetState] = None
    _running_in_supported_kernel = False

    def __init__(self, sessions: Sessions):
        """Create the manager.

        Args:
            sessions: The session manager
        """
        if not run_from_ipython():
            return

        from IPython import get_ipython

        ipython = get_ipython()

        if not hasattr(ipython, "kernel") or not hasattr(
            ipython.kernel, "comm_manager"
        ):
            # When run from IPython or another less elaborated environment
            # than JupyterLab, these attributes might be missing.
            # In that case, there is no need to register anything.
            return

        self._running_in_supported_kernel = True

        kernel = ipython.kernel
        _register_comm_targets(kernel, sessions)
        self._wrap_execute_request_handler(kernel)

    def display_widget(self, cube: Cube, session: Session, name: Optional[str]):
        """Display the output that will lead the atoti JupyterLab extension to show a widget."""
        if not self._running_in_supported_kernel:
            print(
                "atoti widgets can only be shown in JupyterLab with the atoti JupyterLab extension enabled."
            )
            return

        from IPython.display import publish_display_data

        cellset = None
        error = None

        if self._state:
            try:
                cellset = _execute_query(session, self._state)
            except HttpException as err:
                error = err.args

        publish_display_data(
            {
                _WIDGET_MIME_TYPE: {
                    "cellSet": cellset,
                    "cube": cube.name,
                    "error": error,
                    "name": name,
                    "session": session.name,
                },
                "text/plain": f"""Open the notebook in JupyterLab with the atoti extension installed and enabled to {"see" if self._state else "start editing"} this widget.""",  # pylint: disable=line-too-long
            }
        )

    def _wrap_execute_request_handler(
        self, kernel: IPythonKernel  # type: ignore
    ):
        original_handler = kernel.shell_handlers["execute_request"]

        def execute_request(stream: Any, ident: Any, parent: Any) -> Any:
            self._state = parent["metadata"].get("atoti", {}).get("state")
            return original_handler(stream, ident, parent)

        kernel.shell_handlers["execute_request"] = execute_request
