"""
Common raster handling methods shared between blocks
"""
from pathlib import Path

import numpy as np
import rasterio as rio
from rio_cogeo.cogeo import cog_translate
from rio_cogeo.profiles import cog_profiles

from blockutils.logging import get_logger

logger = get_logger(__name__)


def is_empty(path_to_image: Path, nodataval=0) -> bool:
    """
    Tests if a created geotiff image only consists of nodata or NaN values
    Converts NaN to nodata values as a side effect
    Args:
        path_to_image: Path object pointing to geotiff image
        nodataval: no data value, default is 0

    Returns: True if image is empty, False otherwise
    """
    with rio.open(str(path_to_image)) as img_file:
        data = img_file.read()
        np.nan_to_num(data, nan=nodataval, copy=False)
        return not np.any(data - nodataval)


def to_cog(path_to_image: Path, profile: str = "deflate", **options) -> bool:
    """
    Converts a GeoTIFF into a Cloud-optimized GeoTIFF
    :param path_to_image: path to GeoTIFF
    :param profile: compression profile
    :param options: additional kwargs
    :return: True if all went well
    """
    logger.info("Now converting to COG")
    tmp_file_path = Path(str(path_to_image) + ".tmp")
    path_to_image.rename(tmp_file_path)

    # Format creation option (see gdalwarp `-co` option)
    output_profile = cog_profiles.get(profile)
    output_profile.update(dict(BIGTIFF="IF_SAFER"))

    # Dataset Open option (see gdalwarp `-oo` option)
    config = dict(
        GDAL_NUM_THREADS="ALL_CPUS",
        GDAL_TIFF_INTERNAL_MASK=True,
        GDAL_TIFF_OVR_BLOCKSIZE="128",
    )

    cog_translate(
        str(tmp_file_path),
        str(path_to_image),
        output_profile,
        config=config,
        in_memory=False,
        quiet=False,
        **options,
    )
    tmp_file_path.unlink()
    return True
