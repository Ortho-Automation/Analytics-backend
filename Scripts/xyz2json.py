import json
import math


def normalize(x, y, z):
    norm = math.sqrt(x**2 + y**2 + z**2)
    if norm == 0:
        return (0.0, 0.0, 0.0)
    return (x / norm, y / norm, z / norm)


def is_valid_value(value):
    return not (math.isinf(value) or math.isnan(value))


def rotate_90_degrees(x, y, z):
    # First transformation
    x, y, z = -y, x, z
    # Second transformation
    x, y, z = z, y, -x
    return x, y, z


def xyz_to_json(file_path, origincenter=None):
    json_data = []

    # Add the origin center entry at the beginning
    if origincenter is not None:
        json_data.append({"origincenter": origincenter})

    with open(file_path, "r") as file:
        for line in file:
            try:
                values = list(map(float, line.strip().split()))

                if len(values) not in [3, 6]:
                    print(
                        f"Skipping line with incorrect number of values: {line.strip()}"
                    )
                    continue

                x, y, z = values[:3]

                # Check if position values are valid
                if not all(is_valid_value(v) for v in [x, y, z]):
                    print(f"Skipping invalid position values: {line.strip()}")
                    continue

                # Rotate coordinates
                # x, y, z = rotate_90_degrees(x, y, z)

                normal_x, normal_y, normal_z = normalize(x, y, z)
                json_entry = {
                    "position": [x, y, z],
                    "normal": [normal_x, normal_y, normal_z],
                }

                if len(values) == 6:
                    r, g, b = values[3:6]
                    # Check if color values are valid
                    if all(is_valid_value(v) for v in [r, g, b]):
                        color = [int(r), int(g), int(b)]
                        json_entry["color"] = color
                    else:
                        print(f"Skipping invalid color values: {line.strip()}")
                        continue

                json_data.append(json_entry)

            except ValueError as e:
                print(
                    f"Skipping line due to parsing error: {line.strip()} - Error: {e}"
                )

    return json.dumps(json_data, indent=2)


# File path to your XYZ data file
file_path = "extracted_vertices.xyz"  # Adjust this path as needed
origincenter = [
    85.40098373553582,
    21.93062635270207,
]  # Adjust the origin center coordinates as needed
json_output = xyz_to_json(
    file_path, origincenter=origincenter
)  # Adjust the axis if needed

# Save the JSON output to a file
output_file_path = "open_pit_mine_3.json"
with open(output_file_path, "w") as json_file:
    json_file.write(json_output)

print(f"JSON data has been written to {output_file_path}")
