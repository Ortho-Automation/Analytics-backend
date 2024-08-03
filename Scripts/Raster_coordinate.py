import rasterio
import os

# Path to the reprojected orthophoto
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(script_dir)
ortho_path = os.path.join(data_dir, "Data", "sample_orthov1.tiff")
dem_path = os.path.join(data_dir, "Data", "sample_demv1.tiff")
output_path = os.path.join(data_dir, "Data", "sample_orthov1_reprojected.tiff")

# Open the reprojected orthophoto
with rasterio.open(output_path) as src:
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
