from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Sequence

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..sampling import SamplingMode
    from ..store import Store


class ParquetDataSource(DataSource):
    """Parquet data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "PARQUET")

    def create_store_from_parquet(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Sequence[str]],
        in_all_scenarios: bool,
        partitioning: Optional[str],
        sampling: SamplingMode,
        watch: bool,
    ):
        """Create a java store from a parquet file.

        Args:
            path: The path of the file or directory.
            store_name: The name to give to the store
            keys (optional): The key columns for the store
            in_all_scenarios: Whether to load the parquet in all existing scenarios.
                True by default.
            partitioning: The partitioning description.
            sampling: The sampling mode
            watch: Watch the provided path for changes and dynamically load them into the datastore.
                This should not be set to True if the provided path is not a directory.

        """
        self.create_store_from_source(
            store_name,
            keys,
            partitioning,
            None,
            sampling,
            in_all_scenarios,
            watch,
            {"filePath": to_absolute_path(path)},
        )

    def load_parquet_into_store(
        self,
        path: PathLike,
        store: Store,
        scenario_name: ScenarioName,
        in_all_scenarios: bool = False,
        truncate: bool = False,
        watch: bool = False,
    ):
        """Load a Parquet into an existing store.

        Args:
            path: The path of the file or directory.
            store: The store to load the parquet into
            scenario_name: The name of the scenario to load the data into
            in_all_scenarios: load the data into all of the store's scenarios
            truncate: Whether the store should be emptied before loading the new content.
            watch: Watch the provided path for changes and dynamically load them into the datastore.
                This should not be set to True if the provided path is not a directory.

        """
        self.load_data_into_store(
            store.name,
            scenario_name,
            in_all_scenarios,
            watch,
            truncate,
            {"filePath": to_absolute_path(path)},
        )
