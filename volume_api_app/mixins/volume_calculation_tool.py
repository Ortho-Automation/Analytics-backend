import rasterio
import numpy as np
from rasterio.mask import mask
from shapely.geometry import Polygon


class VolumeCalculationToolStandalone:
    def __init__(self):
        pass

    def calculate_volume_above_approx_base_level(
        self, dem_path, polygons, pixel_size_x, pixel_size_y
    ):
        volumes = []
        pixel_area = pixel_size_x * pixel_size_y

        with rasterio.open(dem_path) as src:
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
