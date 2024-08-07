import rasterio
import os
from pyproj import Transformer

# Path to the reprojected orthophoto
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(script_dir)
ortho_path = os.path.join(data_dir, "Data", "ORTHO_TIFF.tif")
dem_path = os.path.join(data_dir, "Data", "sample_demv1.tiff")
output_path = os.path.join(data_dir, "Data", "sample_orthov1_reprojected.tiff")

# Open the reprojected orthophoto
with rasterio.open(ortho_path) as src:
    # Extract the transform and bounds
    transform = src.transform
    bounds = src.bounds

    # Print the bounds and other geospatial information
    print(f"Transform: {transform}")
    print(f"Bounds: {bounds}")
    print(f"CRS: {src.crs}")

    # Optionally, extract the four corners of the image
    top_left = (bounds.left, bounds.top)
    top_right = (bounds.right, bounds.top)
    bottom_left = (bounds.left, bounds.bottom)
    bottom_right = (bounds.right, bounds.bottom)

    print(f"Top left: {top_left}")
    print(f"Top right: {top_right}")
    print(f"Bottom left: {bottom_left}")
    print(f"Bottom right: {bottom_right}")

    # Calculate the center coordinate
    center_x = (bounds.left + bounds.right) / 2
    center_y = (bounds.top + bounds.bottom) / 2
    center_coordinate = (center_x, center_y)

    print(f"Center coordinate: {center_coordinate}")

    # Transform the coordinates to latitude and longitude
    transformer = Transformer.from_crs(src.crs, "EPSG:4326", always_xy=True)

    top_left_latlon = transformer.transform(*top_left)
    top_right_latlon = transformer.transform(*top_right)
    bottom_left_latlon = transformer.transform(*bottom_left)
    bottom_right_latlon = transformer.transform(*bottom_right)
    center_coordinate_latlon = transformer.transform(*center_coordinate)

    print(f"Top left (lat, lon): {top_left_latlon}")
    print(f"Top right (lat, lon): {top_right_latlon}")
    print(f"Bottom left (lat, lon): {bottom_left_latlon}")
    print(f"Bottom right (lat, lon): {bottom_right_latlon}")
    print(f"Center coordinate (lat, lon): {center_coordinate_latlon}")
