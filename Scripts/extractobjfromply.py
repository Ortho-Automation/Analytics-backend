def extract_xyz_rgb_from_ply(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    header_ended = False
    vertices = []

    for line in lines:
        if header_ended:
            parts = line.strip().split()
            if len(parts) == 6:
                x, y, z, r, g, b = parts
                vertices.append((float(x), float(y), float(z), int(r), int(g), int(b)))
        elif line.strip() == "end_header":
            header_ended = True

    return vertices


def create_obj_with_colors(ply_vertices, obj_file_path, output_obj_file_path):
    with open(obj_file_path, "r") as f:
        obj_lines = f.readlines()

    vertex_index = 0
    with open(output_obj_file_path, "w") as f:
        for line in obj_lines:
            if line.startswith("v "):
                parts = line.strip().split()
                x, y, z = parts[1], parts[2], parts[3]
                if vertex_index < len(ply_vertices):
                    r, g, b = (
                        ply_vertices[vertex_index][3],
                        ply_vertices[vertex_index][4],
                        ply_vertices[vertex_index][5],
                    )
                    # Normalize the RGB values to the range 0 to 1
                    r_normalized = r / 255.0
                    g_normalized = g / 255.0
                    b_normalized = b / 255.0
                    f.write(
                        f"v {x} {y} {z} {r_normalized:.6f} {g_normalized:.6f} {b_normalized:.6f}\n"
                    )
                    vertex_index += 1
                else:
                    f.write(line)
            else:
                f.write(line)


# Define file paths
ply_file_path = "ccascii2.ply"
obj_file_path = "Open_Pit_Mine_Rotated.obj"
output_obj_file_path = "open_pit_mine_with_rotated_with_color.obj"

# Extract vertices with colors from PLY file
ply_vertices = extract_xyz_rgb_from_ply(ply_file_path)
print(f"Extracted {len(ply_vertices)} vertices from PLY file.")

# Modify the OBJ file with the extracted color information
create_obj_with_colors(ply_vertices, obj_file_path, output_obj_file_path)

print(f"Modified OBJ file with colors has been saved to {output_obj_file_path}")
