import json
from typing import Any, Mapping, Optional, Union
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from .._docs_utils import doc
from .._repr_utils import convert_repr_json_to_html, repr_json_session
from ._cellset import Cellset, cellset_to_query_result
from ._context import Context
from ._discovery import Discovery
from ._discovery_utils import create_cubes_from_discovery
from .auth import Auth
from .cubes import QueryCubes
from .query_result import QueryResult

SUPPORTED_VERSIONS = ["5", "5.Z1", "4"]

_QUERY_MDX_ARGS = """Args:
            mdx: The MDX ``SELECT`` query to execute.
                Requirements to guarantee that the DataFrame is well shaped:

                * No more than two axes.
                * No grand or sub totals.
                * Nothing else but measures on the ``COLUMNS`` axis.
            timeout: The query timeout in seconds.
"""

_QUERY_MDX_DOC = f"""Execute an MDX query and return its result as a pandas DataFrame.

        {_QUERY_MDX_ARGS}
"""


class HttpException(Exception):
    """Exception representing and HTTP error."""

    def __init__(self, parent: HTTPError):
        """Init."""
        error_data = json.loads(parent.read())["error"]
        message = error_data["errorChain"][0]["message"]
        stacktrace = error_data["stackTrace"]
        super().__init__(message, stacktrace)


class QuerySession:
    """Used to query an existing session."""

    def __init__(self, url: str, auth: Auth, name: str):
        """Init.

        Args:
            url: The server base URL.
            auth: The authentication to use.
            name: The name to give to the session.
        """
        self._url = url
        self._name = name
        self._auth = auth
        self._version = self._fetch_version()
        self._discovery = self._fetch_discovery()
        self._cubes = create_cubes_from_discovery(self._discovery, self)

    @property
    def cubes(self) -> QueryCubes:
        """Cubes of the session."""
        return self._cubes

    @property
    def name(self) -> str:
        """Name of the session."""
        return self._name

    @property
    def url(self) -> str:
        """URL of the session."""
        return self._url

    def _execute_json_request(self, url: str, body: Optional[Any] = None) -> Any:
        headers = {"Content-Type": "application/json"}
        headers.update(self._auth(url) or {})
        data = json.dumps(body).encode("utf8") if body else None
        # The user can send any URL, wrapping it in a request object makes it a bit safer
        request = Request(url, data=data, headers=headers)
        try:
            response = urlopen(request)  # nosec
            return json.load(response)
        except HTTPError as error:
            raise HttpException(error) from error

    def _fetch_version(self) -> str:
        url = f"{self._url}/versions/rest"
        response = self._execute_json_request(url)
        exposed_versions = [
            version["id"] for version in response["apis"]["pivot"]["versions"]
        ]
        try:
            return next(
                version for version in SUPPORTED_VERSIONS if version in exposed_versions
            )
        except Exception:
            raise RuntimeError(
                f"Exposed versions: {exposed_versions}"
                f" don't match supported ones: {SUPPORTED_VERSIONS}"
            ) from None

    def _fetch_discovery(self) -> Discovery:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/discovery"
        response = self._execute_json_request(url)
        return response["data"]

    def _query_mdx_to_cellset(self, mdx: str, context: Context) -> Cellset:
        url = f"{self._url}/pivot/rest/v{self._version}/cube/query/mdx"
        body: Mapping[str, Union[str, Context]] = {"context": context, "mdx": mdx}
        response = self._execute_json_request(url, body)
        return response["data"]

    @doc(_QUERY_MDX_DOC)
    def query_mdx(self, mdx: str, *, timeout: int = 30, **kwargs: Any,) -> QueryResult:
        # We use kwargs to hide uncommon features from the public API.
        context: Context = kwargs.get("context", {})
        if timeout is not None:
            context = {**context, "queriesTimeLimit": timeout}
        cellset = self._query_mdx_to_cellset(mdx, context)
        query_result = cellset_to_query_result(
            cellset,
            self._discovery,
            context=context,
            get_level_data_types=kwargs.get("get_level_data_types"),
            mdx=mdx,
        )
        return query_result

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self):
        return repr_json_session(self)
