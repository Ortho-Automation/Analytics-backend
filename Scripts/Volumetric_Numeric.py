import os
import rasterio
import numpy as np
import geopandas as gpd
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
                    volumes.append(0.0)  # No valid elevation data found

        return volumes


def input_polygon_coordinates():
    polygons = []
    while True:
        input_coords = input(
            "Enter polygon coordinates as a list of tuples (at least 3 points) or 'done' to finish: "
        )
        if input_coords.lower() == "done":
            break
        try:
            coords = eval(input_coords)
            if len(coords) >= 3:
                polygon = Polygon(coords)
                polygons.append(polygon)
                print(f"Polygon ready: {polygon}")
            else:
                print("A polygon must have at least 3 points.")
        except Exception as e:
            print(f"Invalid input. Error: {e}")
    return polygons


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.dirname(script_dir)
    dem_path = os.path.join(data_dir, "Data", "sample_demv1.tiff")

    # Example pixel size in x and y direction (meters)
    pixel_size_x = 0.07085796904697951037
    pixel_size_y = 0.07085530815116512782

    polygons = input_polygon_coordinates()

    if polygons:
        tool = VolumeCalculationToolStandalone()
        volumes = tool.calculate_volume_above_approx_base_level(
            dem_path, polygons, pixel_size_x, pixel_size_y
        )

        for i, volume in enumerate(volumes):
            print(f"Polygon ID: {i+1}, Volume above base level: {volume:.2f} m³")
    else:
        print("No polygons entered.")


if __name__ == "__main__":
    main()
