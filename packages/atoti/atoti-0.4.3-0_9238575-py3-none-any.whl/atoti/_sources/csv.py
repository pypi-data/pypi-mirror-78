from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Mapping, Optional, Sequence, Union

from .._path_utils import PathLike, to_absolute_path
from .._type_utils import ScenarioName
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..sampling import SamplingMode
    from ..simulation import Simulation
    from ..store import Store
    from ..types import AtotiType


def create_csv_params(
    path: PathLike,
    sep: Optional[str],
    encoding: str,
    process_quotes: Optional[bool],
    array_sep: Optional[str],
    pattern: Optional[str],
) -> Dict[str, Any]:
    """Create the CSV spefic parameters."""
    return {
        "path": to_absolute_path(path),
        "separator": sep,
        "encoding": encoding,
        "processQuotes": process_quotes,
        "arraySeparator": array_sep,
        "pattern": pattern,
    }


class CsvDataSource(DataSource):
    """CSV data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "CSV")

    def create_store_from_csv(
        self,
        path: PathLike,
        store_name: str,
        keys: Optional[Sequence[str]],
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        partitioning: Optional[str],
        types: Optional[Mapping[str, AtotiType]],
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
        sampling: SamplingMode,
    ):
        """Create a Java store from a CSV file or directory.

        Args:
            path: The path of the file or directory.
            store_name: The name to give to the store.
            keys (optional): The key columns for the store.
            in_all_scenarios: Whether to load the CSV in all existing scenarios. True by default.
            sep: Delimiter to use. If sep is None, the separator will automatically be detected.
            encoding: Encoding to use for UTF when reading.
            process_quotes: Whether double quotes should be processed.
            partitioning: The partitioning description.
            types: Type for some of the columns.
            watch: Whether or not the source file or directory should be watched for changes. If
                this option is set to true, whenever you change the source, the changes will be
                reflected in the store.
            array_sep: Delimiter to use for arrays. Setting it to a non-None value will parse all
                the columns containing this separator as arrays.
            pattern: glob pattern used to specify which files to load if the provided path is a
                directory. If none is passed we match all csv files by default.
            sampling: The sampling mode.

        """
        source_params = create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.create_store_from_source(
            store_name,
            keys,
            partitioning,
            types,
            sampling,
            in_all_scenarios,
            watch,
            source_params,
        )

    def load_csv_into_store(
        self,
        path: PathLike,
        store: Union[Store, Simulation],
        scenario_name: ScenarioName,
        in_all_scenarios: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: bool,
        truncate: bool,
        watch: bool,
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a csv into an existing store.

        Args:
            path: The path of the file or directory.
            store: The store to load the CSV into
            scenario_name: The name of the scenario to load the data into
            in_all_scenarios: load the data into all of the store's scenarios
            sep: Delimiter to use. If sep is None, the separator will automatically be detected.
            encoding: Encoding to use for UTF when reading.
            process_quotes: Whether double quotes should be processed to follow the official
              CSV specification.
            truncate: Whether the store should be emptied before loading the content of the CSV
            watch: Whether or not the source file or directory should be watched for changes. If
                this option is set to true, whenever you change the source, the changes will be
                reflected in the store.
            array_sep: Delimiter to use for arrays. Setting it to a non-None value will parse all
                the columns containing this separator as arrays.
            pattern: Glob pattern used to specify which files to load if the provided path is a
                directory. If no pattern is provided, we match all csv files by default.

        """
        source_params = create_csv_params(
            path, sep, encoding, process_quotes, array_sep, pattern
        )
        self.load_data_into_store(
            store.name, scenario_name, in_all_scenarios, watch, truncate, source_params,
        )


class MultiScenarioCsvDataSource(DataSource):
    """Multi scenarios CSV data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "MULTI_SCENARIO_CSV")

    def load_scenarios_from_csv(
        self,
        scenario_directory_path: PathLike,
        store_name: str,
        base_scenario_directory: str,
        truncate: bool,
        watch: bool,
        sep: Optional[str],
        encoding: str,
        process_quotes: Optional[bool],
        array_sep: Optional[str],
        pattern: Optional[str],
    ):
        """Load a directory of CSV files into a store while automatically generating scenarios.

        Args:
            scenario_directory_path: The path to the folder containing all the scenarios.
            store_name: The name of the store
            base_scenario_directory: The name of a folder whose data we will load into the base
                scenario instead of a new scenario with the original name of the folder
            truncate: Whether or not the content of the store should be truncated on each branch
            watch: Whether or not we should watch the source directory for changes, or simply
                or simply perform the initial load
            sep: Seperator to use, if None is set it will automatically be detected
            encoding: Encoding to use for UTF when reading, defaults to 'utf-8'
            process_quotes: Whether double quotes should be processed to follow the official CSV
                specification
            array_sep: Delimiter to use for arrays
            pattern: glob pattern used to specify which files to load if the provided path is a
                directory.

        """
        source_params = create_csv_params(
            scenario_directory_path, sep, encoding, process_quotes, array_sep, pattern
        )
        source_params["baseFolderName"] = base_scenario_directory
        self.load_data_into_store(
            store_name, None, False, watch, truncate, source_params,
        )
