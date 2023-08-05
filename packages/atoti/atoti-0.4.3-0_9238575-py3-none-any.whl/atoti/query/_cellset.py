from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union, cast

import pandas as pd
from typing_extensions import TypedDict

from ._context import Context
from ._discovery import Discovery, dictionarize_cube_dimensions
from .query_result import QueryResult

if TYPE_CHECKING:
    from pandas.io.formats.style import Styler

    IndexDataType = Union[str, float, int, pd.Timestamp]

LevelName = str
MeasureName = str

CubeName = str
DimensionName = str
HierarchyName = str

MeasureValue = Optional[Union[float, int, str]]
MemberIdentifier = str
DataFrameCell = Union[MemberIdentifier, MeasureValue]
DataFrameRow = List[DataFrameCell]
DataFrameData = List[DataFrameRow]
LevelCoordinates = Tuple[HierarchyName, LevelName]

SUPPORTED_DATE_FORMATS = [
    "LocalDate[yyyy-MM-dd]",
    "localDate[yyyy/MM/dd]",
    "localDate[MM-dd-yyyy]",
    "localDate[MM/dd/yyyy]",
    "localDate[dd-MM-yyyy]",
    "localDate[dd/MM/yyyy]",
    "localDate[d-MMM-yyyy]",
    "zonedDateTime[EEE MMM dd HH:mm:ss zzz yyyy]",
]

LOCAL_DATE_REGEX = re.compile(r"[lL]ocalDate\[(.*)\]")

DATE_FORMAT_MAPPING = {
    "yyyy": "%Y",
    "MM": "%m",
    "MMM": "%m",
    "dd": "%d",
    r"^d": "%d",
    "HH": "%H",
    "mm": "%M",
    "ss": "%S",
}

MEASURES_HIERARCHY: CellsetHierarchy = {
    "dimension": "Measures",
    "hierarchy": "Measures",
}


class CellsetHierarchy(TypedDict):  # noqa: D101
    dimension: DimensionName
    hierarchy: HierarchyName


class CellsetMember(TypedDict):  # noqa: D101
    # The captionPath is ignored on purpose to not repr a DataFrame index
    # containing captions that would confuse users trying to select or filter
    # members in this index.
    namePath: List[MemberIdentifier]


class CellsetAxis(TypedDict):  # noqa: D101
    id: int
    hierarchies: List[CellsetHierarchy]
    positions: List[List[CellsetMember]]


class CellsetCellProperties(TypedDict):  # noqa: D101
    BACK_COLOR: Optional[Union[int, str]]
    FONT_FLAGS: Optional[int]
    FONT_NAME: Optional[str]
    FONT_SIZE: Optional[int]
    FORE_COLOR: Optional[Union[int, str]]


class CellsetCell(TypedDict):  # noqa: D101
    formattedValue: str
    ordinal: int
    properties: CellsetCellProperties
    value: MeasureValue


class CellsetDefaultMember(TypedDict):  # noqa: D101
    dimension: DimensionName
    hierarchy: HierarchyName
    path: List[MemberIdentifier]


class Cellset(TypedDict):  # noqa: D101
    axes: List[CellsetAxis]
    cells: List[CellsetCell]
    cube: CubeName
    defaultMembers: List[CellsetDefaultMember]


@dataclass(frozen=True)
class DataFrameContent:
    """Allow to generate a stylized rendering of the query result."""

    formatted_values: Union[DataFrameData, DataFrameRow]
    values: Union[DataFrameData, DataFrameRow]
    styles: Optional[Union[DataFrameData, DataFrameRow]] = None


def _extract_axes(
    axes: List[CellsetAxis],
) -> Tuple[Optional[CellsetAxis], Optional[CellsetAxis]]:
    non_slicing_axes = [axis for axis in axes if axis["id"] != -1]
    if len(non_slicing_axes) > 2:
        raise ValueError(
            "Cellsets with more than two non-slicing axes are not supported"
        )
    columns_axis = None
    rows_axis = None
    for axis in non_slicing_axes:
        if axis["id"] == 0:
            columns_axis = axis
        else:
            rows_axis = axis
    return (columns_axis, rows_axis)


def _extract_measure_names(
    default_members: List[CellsetDefaultMember],
    columns_axis: Optional[CellsetAxis] = None,
    rows_axis: Optional[CellsetAxis] = None,
) -> List[str]:
    if not columns_axis:
        if not rows_axis:
            # When there are no axes at all, we get only one cell:
            # the aggregated value of the default measure at the top.
            return [
                next(
                    member["path"][0]
                    for member in default_members
                    if member["dimension"] == "Measures"
                )
            ]
        return []
    if len(columns_axis["hierarchies"]) > 0 and columns_axis["hierarchies"] != [
        MEASURES_HIERARCHY
    ]:
        raise ValueError(
            "Cellsets with something else than measures on the COLUMNS axis are not supported"
        )
    return [position[0]["namePath"][0] for position in columns_axis["positions"]]


def _extract_level_count_per_hierarchy(rows_axis: CellsetAxis) -> List[int]:
    level_count_per_hierarchy = []
    for (position_index, position) in enumerate(rows_axis["positions"]):
        for (hierachy_index, member) in enumerate(position):
            identifier_count = len(member["namePath"])
            if position_index == 0:
                level_count_per_hierarchy.insert(hierachy_index, identifier_count)
            elif identifier_count != level_count_per_hierarchy[hierachy_index]:
                raise ValueError("Cellsets with grand or sub totals are not supported")
    return level_count_per_hierarchy


def _extract_level_coords(
    cube_name: CubeName, rows_axis: Optional[CellsetAxis], discovery: Discovery
) -> List[LevelCoordinates]:
    if not rows_axis:
        return []
    dimensions = dictionarize_cube_dimensions(
        next(
            cube
            for catalog in discovery["catalogs"]
            for cube in catalog["cubes"]
            if cube["name"] == cube_name
        )
    )
    level_count_per_hierarchy = _extract_level_count_per_hierarchy(rows_axis)
    return [
        (hierarchy["hierarchy"], level["name"])
        for (hierarchy_index, hierarchy) in enumerate(rows_axis["hierarchies"])
        for (level_index, level) in enumerate(
            dimensions[hierarchy["dimension"]][hierarchy["hierarchy"]]["levels"]
        )
        if level_index < level_count_per_hierarchy[hierarchy_index]
        and level["type"] != "ALL"
    ]


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-fore-color-and-back-color-contents. pylint: disable=line-too-long
# Improved over from https://github.com/activeviam/activeui/blob/ba42f1891cd6908de618fdbbab34580a6fe3ee58/packages/activeui-sdk/src/widgets/tabular/cell/MdxCellStyle.tsx#L29-L48. pylint: disable=line-too-long
def _cell_color_to_css_value(color: Union[int, str]) -> str:
    if isinstance(color, str):
        return "transparent" if color == '"transparent"' else color
    rest, red = divmod(color, 256)
    rest, green = divmod(rest, 256)
    rest, blue = divmod(rest, 256)
    return f"rgb({red}, {green}, {blue})"


# See https://docs.microsoft.com/en-us/analysis-services/multidimensional-models/mdx/mdx-cell-properties-using-cell-properties.
def _cell_font_flags_to_styles(font_flags: int) -> List[str]:
    styles = []
    text_decorations = []

    if font_flags & 1 == 1:
        styles.append("font-weight: bold")
    if font_flags & 2 == 2:
        styles.append("font-style: italic")
    if font_flags & 4 == 4:
        text_decorations.append("underline")
    if font_flags & 8 == 8:
        text_decorations.append("line-through")

    if text_decorations:
        styles.append(f"""text-decoration: {" ".join(text_decorations)}""")

    return styles


def _cell_properties_to_style(properties: CellsetCellProperties) -> str:
    styles = []

    back_color = properties.get("BACK_COLOR")
    if back_color is not None:
        styles.append(f"background-color: {_cell_color_to_css_value(back_color)}")

    font_flags = properties.get("FONT_FLAGS")
    if font_flags is not None:
        styles.extend(_cell_font_flags_to_styles(font_flags))

    font_name = properties.get("FONT_NAME")
    if font_name is not None:
        styles.append(f"font-family: {font_name}")

    font_size = properties.get("FONT_SIZE")
    if font_size is not None:
        styles.append(f"font-size: {font_size}px")

    fore_color = properties.get("FORE_COLOR")
    if fore_color is not None:
        styles.append(f"color: {_cell_color_to_css_value(fore_color)}")

    return "; ".join(styles)


def _create_empty_dataframe_data(
    measure_names: List[MeasureName], rows_axis: Optional[CellsetAxis]
) -> DataFrameData:
    return cast(
        DataFrameData,
        [
            [None] * len(measure_names)
            for _ in range(len(rows_axis["positions"]) if rows_axis else 1)
        ],
    )


def _extract_dataframe_content(
    cells: List[CellsetCell],
    has_some_style: bool,
    measure_names: List[MeasureName],
    rows_axis: Optional[CellsetAxis],
) -> DataFrameContent:
    formatted_values = _create_empty_dataframe_data(measure_names, rows_axis)
    values = _create_empty_dataframe_data(measure_names, rows_axis)
    styles = (
        _create_empty_dataframe_data(measure_names, rows_axis)
        if has_some_style
        else None
    )

    if measure_names:
        measure_count = len(measure_names)
        for cell in cells:
            (row_index, column_offset) = divmod(cell["ordinal"], measure_count)
            formatted_values[row_index][column_offset] = cell["formattedValue"]
            values[row_index][column_offset] = cell["value"]
            if has_some_style:
                cast(DataFrameData, styles)[row_index][
                    column_offset
                ] = _cell_properties_to_style(cell["properties"])

    return DataFrameContent(formatted_values, values, styles)


def _format_to_pandas_type(value_type: str, values: List[Any]) -> List[IndexDataType]:
    """Format values to a specific pandas data type.

    Formatted value can be a date, int, float or object.
    """
    if value_type in ["int", "float"]:
        return pd.to_numeric(values)
    if value_type in SUPPORTED_DATE_FORMATS:
        try:
            if value_type.lower().startswith("localdate["):
                date_format = LOCAL_DATE_REGEX.match(value_type).groups()[0]  # type: ignore
                for regex, value in DATE_FORMAT_MAPPING.items():
                    date_format = re.sub(regex, value, date_format)
                return pd.to_datetime(values, format=date_format)
            if value_type.startswith("zonedDateTime["):
                return pd.to_datetime(values)
        except ValueError as err:
            logging.getLogger("atoti.query").warning(
                "Failed to convert type %s to a pandas date, using string instead. %s",
                value_type,
                err,
            )
    return values


def _extract_multi_index_data(
    rows_axis: CellsetAxis, level_data_types: List[str],
) -> List[List[IndexDataType]]:
    """Convert an MDX cellsetAxis to a list of list of Index data.

    Each level correspond to an index column.
    Generate a list of list containing index data column to be
    able to use pd.MultiIndex.from_arrays.

    Args:
        rows_axis: CellsetAxis
        level_data_types: list of level data types

    Returns:
        List of list, each sublist correspond to an index column containing formated index data.
        example: [
            [Continent1, Continent1, Continent2],
            [Continent1.city1, Continent1.city, Continent2.city1]
        ]

    """
    index_data: List[List[str]] = [[] for _ in level_data_types]
    for position in rows_axis["positions"]:
        index_data = _add_row_to_index_data(index_data, position)
    return [
        _format_to_pandas_type(level_data_type, index_data[index])
        for index, level_data_type in enumerate(level_data_types)
    ]


def _add_row_to_index_data(
    df_index_columns: List[List[str]], position: List[CellsetMember]
) -> List[List[str]]:
    """Add a value to each sub array of index data.

    It is equivalent to add a row in the index

    Args:
        df_index_columns: dataframe index data array
        position: list of cellset members
                    Position is a list of CellsetMember from the higher level to the deeper one.
                    For instance [Continent, Country, City, ...]
                    position = [CellsetMember(name_path=['AllMember', 'Level']), ...]

    Returns:
        List of list, each sublist correspond to an index column

    """
    # List of values for a row sorted by columns order of the index [value_col_1, value_col_2, ...]
    row_values = []
    for cellset_member in position:
        name_path = cellset_member["namePath"]
        if name_path[0] == "AllMember":
            name_path.pop(0)
        row_values += name_path
    # Fill df_index_columns column after column
    for i, column in enumerate(df_index_columns):
        column.append(row_values[i])
    return df_index_columns


def _create_dataframe_multi_index(
    level_coords: List[Tuple[MemberIdentifier, MemberIdentifier]],
    level_data_types: List[str],
    rows_axis: Optional[CellsetAxis],
) -> Optional[pd.Index]:
    """Convert an MDX cellsetAxis to a pandas DataFrameIndex.

    Use level description type to convert index in the good pandas format.
    Index data is an array of arrays containing index values.

    Args:
        level_coords: level coordinates ((hierarchy, level)) of the indexes
        rows_axis: optional cellset_axis
                [
                    id = int,
                    Hierarchies = [
                        CellsetHierarchy(dimension='Hierarchies', hierarchy='Name'),
                        ...],
                    positions =  [...],
                ]
        level_data_types: list of types matching the list of level names

    Returns:
        a pandas MultiIndex

    """
    number_of_levels = len(level_coords)
    index_data = [[] for _ in range(number_of_levels)]
    if rows_axis:
        index_data = _extract_multi_index_data(rows_axis, level_data_types)
    return pd.MultiIndex.from_arrays(
        index_data, names=[level_coord[1] for level_coord in level_coords]
    )


def _extract_dataframe_index(
    level_coords: List[LevelCoordinates],
    level_data_types: List[str],
    rows_axis: Optional[CellsetAxis],
) -> Optional[pd.Index]:
    """Convert an MDX cellsetAxis to a pandas DataFrameIndex.

    Args:
        level_coords: list of coordinates of the indexes
        rows_axis: optional cellset_axis
        level_data_types: list of types matching the list of level names

    Returns:
        a pandas Index or MultiIndex

    """
    number_of_levels = len(level_coords)
    if number_of_levels > 1:
        return _create_dataframe_multi_index(level_coords, level_data_types, rows_axis)
    if number_of_levels == 1:
        index_data: List[str] = (
            [
                identifier
                for position in rows_axis["positions"]
                for member in position
                for identifier in member["namePath"]
                if identifier != "AllMember"
            ]
            if rows_axis
            else []
        )
        return pd.Index(
            _format_to_pandas_type(level_data_types[0], index_data),
            name=level_coords[0][1],
        )
    return None


def cellset_to_query_result(
    cellset: Cellset,
    discovery: Discovery,
    *,
    context: Optional[Context] = None,
    get_level_data_types: Optional[
        Callable[[str, List[LevelCoordinates]], List[str]]
    ] = None,
    mdx: Optional[str] = None,
) -> QueryResult:
    """Convert an MDX cellset to a pandas DataFrame.

    Requirements to guarantee that the DataFrame is well shaped:
      - no more than two axes
      - no grand or sub totals
      - nothing else but measures on the COLUMNS axis

    Args:
        cellset: the MDX cellset
        discovery: the discovery of the corresponding server
        context: the context values of the corresponding query
        get_level_data_types: return the list of types matching the list of level names
        mdx: the mdx of the corresponding query
    """
    (columns_axis, rows_axis) = _extract_axes(cellset["axes"])
    measure_names = _extract_measure_names(
        cellset["defaultMembers"], columns_axis, rows_axis
    )

    columns = None
    formatted_values = None
    index = None
    styles = None
    values = None

    cells = cellset["cells"]
    has_some_style = next((True for cell in cells if cell["properties"]), False)

    if not cells or (not columns_axis and not rows_axis):
        columns = measure_names
        formatted_values = []
        styles = []
        values = []

        if cells:
            cell = cells[0]
            formatted_values.append(cell["formattedValue"])
            styles.append(
                _cell_properties_to_style(cell["properties"]) if has_some_style else ""
            )
            values.append(cell["value"])

    else:
        level_coords = _extract_level_coords(cellset["cube"], rows_axis, discovery)
        level_data_types = (
            get_level_data_types(cellset["cube"], level_coords)
            if get_level_data_types
            else ["object"] * len(level_coords)
        )

        columns = measure_names
        index = _extract_dataframe_index(level_coords, level_data_types, rows_axis)
        dataframe_content = _extract_dataframe_content(
            cells, has_some_style, measure_names, rows_axis
        )

        formatted_values = dataframe_content.formatted_values
        styles = dataframe_content.styles
        values = dataframe_content.values

    formatted_values_dataframe = pd.DataFrame(formatted_values, index, columns)

    def _get_styler() -> Styler:
        styler = formatted_values_dataframe.style

        if has_some_style:
            styler = styler.apply(
                lambda _: pd.DataFrame(styles, index, columns), axis=None
            )

        return styler

    return QueryResult(
        values,
        index,
        columns,
        context=context,
        cube=cellset["cube"],
        formatted_values=formatted_values_dataframe,
        get_styler=_get_styler,
        mdx=mdx,
    )
