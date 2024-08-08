def read_mtl_file(file_path):
    mtl_data = {}
    current_mtl = None
    with open(file_path, "r") as mtl_file:
        for line in mtl_file:
            if line.startswith("newmtl"):
                current_mtl = line.split()[1]
            elif line.startswith("Kd") and current_mtl is not None:
                kd_values = list(map(float, line.split()[1:]))
                mtl_data[current_mtl] = kd_values
    return mtl_data


def read_obj_file(file_path):
    vertices = []
    with open(file_path, "r") as obj_file:
        for line in obj_file:
            if line.startswith("v "):
                vertices.append(list(map(float, line.split()[1:4])))
    return vertices


def create_xyz_file(obj_path, mtl_path, output_path):
    mtl_data = read_mtl_file(mtl_path)
    vertices = read_obj_file(obj_path)

    with open(output_path, "w") as xyz_file:
        for vertex in vertices:
            x, y, z = vertex
            kd_values = mtl_data.get(
                "mat0", [0.0, 0.0, 0.0]
            )  # Default to mat0 if not specified
            xyz_file.write(
                f"{x} {y} {z} {kd_values[0]*255} {kd_values[1]*255} {kd_values[2]*255}\n"
            )


# Paths to your files
obj_file_path = "test.obj"
mtl_file_path = "open_pit_mine.mtl"
output_xyz_path = "test_combined.xyz"

# Create the XYZ file
create_xyz_file(obj_file_path, mtl_file_path, output_xyz_path)
