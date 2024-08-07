import rasterio
import numpy as np
from rasterio.mask import mask
from shapely.geometry import Polygon
from shapely.ops import transform
from functools import partial
import pyproj


class VolumeCalculationToolStandalone:
    def __init__(self):
        pass

    def transform_polygon(self, polygon, src_crs, dst_crs):
        project = partial(
            pyproj.transform, pyproj.Proj(init=src_crs), pyproj.Proj(init=dst_crs)
        )
        return transform(project, polygon)

    def calculate_volume_above_approx_base_level(
        self, dem_path, polygons, pixel_size_x, pixel_size_y
    ):
        volumes = []
        pixel_area = pixel_size_x * pixel_size_y

        with rasterio.open(dem_path) as src:
            raster_crs = src.crs.to_string()
            if raster_crs != "EPSG:4326":
                for i in range(len(polygons)):
                    polygons[i] = self.transform_polygon(
                        polygons[i], "EPSG:4326", raster_crs
                    )

            for polygon in polygons:
                try:
                    # Extract vertices and find average elevation
                    exterior_coords = list(polygon.exterior.coords)

                    # Calculate average elevation of polygon vertices
                    elevations = []
                    for x, y in exterior_coords:
                        try:
                            value = next(
                                src.sample([(x, y)], indexes=1)
                            )  # Get the next value from the generator
                            if not np.isnan(value):
                                elevations.append(value)
                        except StopIteration:
                            pass

                    if elevations:
                        avg_base_level = np.mean(elevations)

                        # Calculate volume above the approximate base level
                        dem_masked, _ = mask(
                            src, [polygon], crop=True, filled=True, nodata=np.nan
                        )
                        dem_masked = dem_masked[0]

                        # Set values below avg_base_level to NaN
                        dem_masked[dem_masked <= avg_base_level] = np.nan

                        # Calculate volume above the approximate base level
                        volume_above_base_level = np.nansum(
                            (dem_masked - avg_base_level) * pixel_area
                        )

                        volumes.append(volume_above_base_level)
                    else:
                        volumes.append(None)  # No valid elevation data found
                except Exception as e:
                    # Handle any exceptions during processing
                    print(f"Error processing polygon: {polygon}, error: {e}")
                    volumes.append(None)

        return volumes
