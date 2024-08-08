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


# Define file path
ply_file_path = "ccascii2.ply"

# Extract vertices with colors
vertices_with_colors = extract_xyz_rgb_from_ply(ply_file_path)

# Print extracted vertices
for vertex in vertices_with_colors:
    print(vertex)

# Save extracted vertices to a new file (optional)
output_file_path = "extracted_vertices.xyz"
with open(output_file_path, "w") as f:
    for vertex in vertices_with_colors:
        f.write(
            f"{vertex[0]} {vertex[1]} {vertex[2]} {vertex[3]} {vertex[4]} {vertex[5]}\n"
        )

print(f"Extracted vertices saved to {output_file_path}")
