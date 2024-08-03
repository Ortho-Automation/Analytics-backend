import os
import rasterio
import numpy as np
import geopandas as gpd
from rasterio.mask import mask
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon as mplPolygon
from rasterio.plot import show  # Import show function explicitly


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
                print(exterior_coords)
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


# Orthophoto path for visualization
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(script_dir)
ortho_path = os.path.join(data_dir, "Data", "sample_orthov1.tiff")
dem_path = os.path.join(data_dir, "Data", "sample_demv1.tiff")

# List to store polygons
polygons = []

# For interactive drawing
current_polygon = []
current_polygon_line = None
ax = None  # Initialize axis globally


def draw_polygon(event):
    global current_polygon, current_polygon_line, ax

    if event.inaxes != ax:
        return

    if event.button == 1:  # Left mouse button (add point)
        current_polygon.append((event.xdata, event.ydata))
        if len(current_polygon) > 1:
            if current_polygon_line:
                current_polygon_line.remove()
            current_polygon_line = Line2D(
                [x for x, y in current_polygon],
                [y for x, y in current_polygon],
                marker="o",
            )
            ax.add_line(current_polygon_line)
        fig.canvas.draw()

    elif event.button == 3:  # Right mouse button (close polygon)
        if len(current_polygon) > 2:
            # Close polygon
            current_polygon.append(
                current_polygon[0]
            )  # Connect last point to first point
            poly = mplPolygon(current_polygon, closed=True, edgecolor="r", fill=False)
            ax.add_patch(poly)
            polygon = Polygon(current_polygon)
            polygons.append(polygon)

            # Clear drawn polygon
            current_polygon.clear()
            if current_polygon_line:
                current_polygon_line.remove()
                current_polygon_line = None

            # Calculate volume for the polygon
            volumes = calculate_and_display_volume(
                dem_path, polygons, pixel_size_x, pixel_size_y
            )

            # Save polygons to shapefile
            # poly_gdf = gpd.GeoDataFrame(geometry=polygons, crs=ortho_crs)
            # poly_gdf.to_file(
            #     f"{data_dir}/Data/Shapefiles/polygons.shp", driver="ESRI Shapefile"
            # )
            # print(f"Polygon saved: {polygon}")


def calculate_and_display_volume(dem_path, polygons, pixel_size_x, pixel_size_y):
    tool = VolumeCalculationToolStandalone()
    volumes = tool.calculate_volume_above_approx_base_level(
        dem_path, polygons, pixel_size_x, pixel_size_y
    )

    # Clear previous annotations
    for ann in ax.texts:
        ann.remove()

    # Display polygon ID and volume in plot
    for i, (polygon, volume) in enumerate(zip(polygons, volumes)):
        x, y = polygon.exterior.xy
        centroid_x, centroid_y = polygon.centroid.xy
        ax.annotate(
            f"ID: {i+1}\nVolume: {volume:.2f} m³",
            xy=(centroid_x[0], centroid_y[0]),
            xytext=(centroid_x[0], centroid_y[0]),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="black", lw=1),
            fontsize=8,
            ha="center",
            va="center",
        )

    fig.canvas.draw()

    return volumes


# Connect draw_polygon function to mouse click events
fig, ax = plt.subplots()
fig.canvas.mpl_connect("button_press_event", draw_polygon)

# Load the orthophoto
with rasterio.open(ortho_path) as src:
    ortho = src.read([1, 2, 3])
    ortho_transform = src.transform
    ortho_crs = src.crs

# Plot the orthophoto as a multiband image
show(ortho, transform=ortho_transform, ax=ax, title="Multiband Ortho Image")

# Example pixel size in x and y direction (meters)
pixel_size_x = 0.07085796904697951037
pixel_size_y = 0.07085530815116512782

plt.show()
