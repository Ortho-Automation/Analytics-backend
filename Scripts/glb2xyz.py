import numpy as np
from pygltflib import GLTF2


def extract_data_from_gltf(file_path):
    gltf = GLTF2().load(file_path)

    def get_buffer_data(buffer, buffer_view, accessor, dtype, num_components):
        buffer_bytes = buffer[
            buffer_view.byteOffset : buffer_view.byteOffset + buffer_view.byteLength
        ]
        data = np.frombuffer(
            buffer_bytes,
            dtype=dtype,
            count=accessor.count
            * num_components,  # 3 components per vertex (e.g., x, y, z)
            offset=accessor.byteOffset,
        ).reshape((accessor.count, num_components))
        return data

    # Load the buffer data from the external binary file
    buffer_uri = gltf.buffers[0].uri
    with open(buffer_uri, "rb") as f:
        buffer = f.read()

    # Extract positions and colors
    positions_accessor_index = gltf.meshes[0].primitives[0].attributes.POSITION
    colors_accessor_index = gltf.meshes[0].primitives[0].attributes.COLOR_0

    positions_accessor = gltf.accessors[positions_accessor_index]
    colors_accessor = gltf.accessors[colors_accessor_index]

    positions_buffer_view = gltf.bufferViews[positions_accessor.bufferView]
    colors_buffer_view = gltf.bufferViews[colors_accessor.bufferView]

    positions = get_buffer_data(
        buffer, positions_buffer_view, positions_accessor, np.float32, 3
    )
    colors = get_buffer_data(
        buffer, colors_buffer_view, colors_accessor, np.uint8, 4
    )  # Assuming VEC4 for colors

    return positions, colors


def save_xyz_with_color(positions, colors, output_file):
    with open(output_file, "w") as file:
        for pos, color in zip(positions, colors):
            line = f"{pos[0]} {pos[1]} {pos[2]} {int(color[0])} {int(color[1])} {int(color[2])}\n"
            file.write(line)


# File path to your pruned GLTF file
file_path = "Open_Pit_Mine_pruned.gltf"
positions, colors = extract_data_from_gltf(file_path)

# Save the extracted data to an XYZ file with color
output_file = "open_pit_mine_with_color.xyz"
save_xyz_with_color(positions, colors, output_file)

print(f"XYZ data with color has been written to {output_file}")
