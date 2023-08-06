"""
Common methods shared between blocks, especially useful for directory handling
and block parameter/query input.
"""
import json
import os
from typing import Callable
from contextlib import ContextDecorator
import pathlib
from enum import Enum
import shutil
import base64

import rasterio as rio
from rasterio import warp
from shapely.geometry import box, mapping

from geojson import FeatureCollection, Feature

from .stac import STACQuery
from .logging import get_logger

logger = get_logger(__name__)


def ensure_data_directories_exist():
    """Creates required directories for any block input and output (`/tmp/input`,
     `tmp/output`, `/tmp/quicklooks`).
    """
    pathlib.Path("/tmp/input/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/output/").mkdir(parents=True, exist_ok=True)
    pathlib.Path("/tmp/quicklooks/").mkdir(parents=True, exist_ok=True)


def setup_test_directories(test_dir: pathlib.Path):
    """Creates given test directory and empty input/output/quicklook subfolders.

    Arguments:
        test_dir: A directory to store temporary files (usually `/tmp` or
            `/tmp/e2e_test`)

    """
    test_dir.mkdir(parents=True, exist_ok=True)

    cleanup_test_directories(test_dir)


def cleanup_test_directories(test_dir: pathlib.Path):
    """Deletes given test directory.

    Arguments:
        test_dir: A directory to store temporary files (usually `/tmp` or \
            `/tmp/e2e_test`)
    """
    if test_dir.exists():
        for folder in ["input", "output", "quicklooks"]:
            try:
                shutil.rmtree(test_dir / folder)
                pathlib.Path(test_dir / folder).mkdir(parents=True, exist_ok=True)
            # Deleting subfolder sometimes does not work in temp, then remove all subfiles.
            except (PermissionError, OSError):
                pathlib.Path(test_dir / folder).mkdir(parents=True, exist_ok=True)
                files_to_delete = pathlib.Path(test_dir / folder).rglob("*.*")
                for file_path in files_to_delete:
                    file_path.unlink()


class TestDirectoryContext(ContextDecorator):
    """Yields the test directory making sure folders exist and cleans up when
    context is closed.
    """

    def __init__(self, test_dir: pathlib.Path):
        """
        Example:
            ```python
            with TestDirectoryContext(pathlib.Path("/tmp")) as test_dir:
                block.process(dir=pathlib.Path("/tmp"))
            ```

        Arguments:
            test_dir: A directory to store temporary files (usually `/tmp`
                or `/tmp/e2e_test`)
        """
        self.test_dir = test_dir

    def __enter__(self) -> pathlib.Path:
        """Context entry point.

        Returns:
            Temporary test directory.
        """
        setup_test_directories(self.test_dir)
        return self.test_dir

    def __exit__(self, *exc):
        """Context exit point. Deletes temporary directory.
        """
        cleanup_test_directories(self.test_dir)
        return False


def load_query(validator: Callable = lambda x: True) -> STACQuery:
    """Get the query for the current task directly from the task parameters
    in `UP42_TASK_PARAMETERS` environment variable.

    Example:
        ```python
        def val(data: dict) -> bool:
            # Ensure bbox is defined.
            return "bbox" in data

        query = load_query(val)
        ```

    Arguments:
        validator: Callable that returns if the loaded query is valid.

    Returns:
        A `STACQuery` object initialized with the parameters if valid.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Raw task parameters from UP42_TASK_PARAMETERS are: %s", data)
    query_data = json.loads(data)
    return STACQuery.from_dict(query_data, validator)


def load_params() -> dict:
    """Get the parameters for the current task directly from the task
    parameters parameters in `UP42_TASK_PARAMETERS` environment variable.

    Returns:
        Dictionary of task parameters.
    """
    data: str = os.environ.get("UP42_TASK_PARAMETERS", "{}")
    logger.debug("Fetching parameters for this block: %s", data)
    if data == "":
        data = "{}"
    return json.loads(data)


def load_metadata() -> FeatureCollection:
    """Get the geojson metadata input.

    Returns:
        Object defining input features for block.
    """
    ensure_data_directories_exist()
    if os.path.exists("/tmp/input/data.json"):
        with open("/tmp/input/data.json") as fp:
            data = json.loads(fp.read())

        features = []
        for feature in data["features"]:
            features.append(Feature(**feature))

        return FeatureCollection(features)
    else:
        return FeatureCollection([])


def save_metadata(result: FeatureCollection):
    """Save the geojson metadata output.

    Arguments:
        result: Output feature collection.
    """
    ensure_data_directories_exist()
    with open("/tmp/output/data.json", "w") as fp:
        fp.write(json.dumps(result))


def update_extents(feat_coll: FeatureCollection) -> FeatureCollection:
    """
    Updates all geometry extents to reflect actual images
    Args:
        feature_coll: geojson Feature Collection

    Returns: A FeatureCollection where image extents reflect actual images
    """
    for feature in feat_coll.features:
        with rio.open(
            os.path.join("/tmp/output", feature.properties["up42.data_path"])
        ) as img_file:
            img_bounds = img_file.bounds
        bounds_trans = warp.transform_bounds(
            img_file.crs, {"init": "epsg:4326"}, *img_bounds
        )

        geom = box(*bounds_trans)
        feature["geometry"] = mapping(geom)
        feature["bbox"] = geom.bounds

    return feat_coll


class BlockModes(Enum):
    """
    Types of block modes: DRY_RUN or DEFAULT.

    Important:
        Find out more about job modes/block modes in our
        [documentation](https://docs.up42.com/reference/block-envvars.html#up42-job-mode).
    """

    DRY_RUN = "DRY_RUN"
    DEFAULT = "DEFAULT"


def get_block_mode() -> str:
    """Gets the task mode from environment variables. If no task mode is set,
    DEFAULT mode will be returned.

    Important:
        Find out more about job modes/block modes in our
        [documentation](https://docs.up42.com/reference/block-envvars.html#up42-job-mode).

    Returns:
        Block mode.
    """
    value = os.environ.get("UP42_JOB_MODE", BlockModes.DEFAULT.value)
    if value not in [mode.value for mode in BlockModes]:
        value = "DEFAULT"
    return value


def get_block_info() -> dict:
    """Gets the Block Info variable as a dictionary.

    Returns:
        Block info as a dict.
    """
    value_str = str(os.environ.get("UP42_BLOCK_INFO"))
    value_dict = json.loads(value_str)

    return value_dict


def encode_str_base64(string: str) -> str:
    """
    A function that encodes strings in base64. The primary use case is passing complex environment variables into
    docker containers. In cases where these env variables are complex json objects including a number of different
    special characters the process of getting them unharmed into a docker container sometimes fails. Encoding them
    in base64 is a save method to solve this problem.

    Args:
        A, potentially complex, non-encoded string
    Returns:
        A base64-encoded string
    """
    return base64.b64encode(string.encode("ascii")).decode("ascii")


def decode_str_base64(string: str) -> str:
    """
    Inverter function for encode_str_base64

    Args:
        A base64-encoded string
    Returns:
        A decoded string
    """

    str_encoded_byte = bytes(string, "utf-8")
    str_decoded_byte = base64.b64decode(str_encoded_byte)
    return str_decoded_byte.decode("utf-8")
