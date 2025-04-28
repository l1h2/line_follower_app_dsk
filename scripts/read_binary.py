import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))


import csv

from utils import BIT_POSITIONS, Files


def read_binary_file(data_path: str, timestamps_path: str, output_path: str) -> None:
    try:
        with open(data_path, "rb") as binary_file, open(
            timestamps_path, "r"
        ) as timestamps_file, open(output_path, "w", newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            header = ["index", "timestamp"] + [f"IR{i}" for i in range(1, 13)]
            csv_writer.writerow(header)

            byte_pair_index = 0

            while True:
                data = binary_file.read(2)
                if not data:
                    break

                if len(data) < 2:
                    raise ValueError("Incomplete byte pair read.")

                timestamp = timestamps_file.readline().strip()
                if not timestamp:
                    raise ValueError("No more timestamps available.")

                word = (data[0] << 8) | data[1]
                bits = ((word & (1 << i)) >> i for i in BIT_POSITIONS)

                csv_writer.writerow((byte_pair_index, timestamp, *bits))
                byte_pair_index += 1

        print(f"Bit values written to {output} successfully.")

    except FileNotFoundError:
        print(f"File not found: {data_path} or {timestamps_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    data = Files.BINARY_FILE
    timestamps = Files.TIMESTAMP_FILE
    output = Files.SENSOR_DATA
    read_binary_file(data, timestamps, output)
