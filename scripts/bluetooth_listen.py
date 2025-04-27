import sys
from pathlib import Path

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import time

import serial

from utils import Files, SerialConfig, SerialInputs


def clear_files() -> None:
    with open(Files.BINARY_FILE, "wb"), open(Files.TEXT_FILE, "w"), open(
        Files.TIMESTAMP_FILE, "w"
    ):
        pass


def read_string_from_bluetooth(bluetooth: serial.Serial) -> None:
    with open(Files.TEXT_FILE, "a") as f:
        while True:
            if bluetooth.in_waiting <= 0:
                continue

            data = bluetooth.readline().decode("utf-8")
            print(f"Received: {data}")

            if data == SerialInputs.START_SIGNAL.value:
                print("Start signal received. Recording binary data...")
                return

            f.write(f"{data}\n")
            f.flush()


def check_buffer(buffer: bytes) -> bool:
    return not buffer == SerialInputs.STOP_SIGNAL.value[: len(buffer)]


def read_binary_from_bluetooth(bluetooth: serial.Serial) -> None:
    buffer = b""

    start_time = time.time()

    with open(Files.BINARY_FILE, "ab") as binary_file, open(
        Files.TIMESTAMP_FILE, "a"
    ) as timestamp_file:
        while True:
            if bluetooth.in_waiting <= 0:
                continue

            data = bluetooth.read(2)
            print(f"Received: {data}")

            buffer += data

            if buffer == SerialInputs.STOP_SIGNAL.value:
                print("Stop signal received. Stopping binary data recording...")
                return

            if not check_buffer(buffer):
                continue

            elapsed_time_ms = int((time.time() - start_time) * 1000)
            timestamp_file.write(f"{elapsed_time_ms}\n")
            timestamp_file.flush()

            binary_file.write(buffer)
            binary_file.flush()

            bits = " ".join(f"{byte:08b}" for byte in buffer)
            print(f"{elapsed_time_ms} ms: {buffer.hex()} - {bits}")
            buffer = b""


def main() -> None:
    clear_files()

    print(f"Connecting to {SerialConfig.PORT} at {SerialConfig.BAUD_RATE} baud...")
    bluetooth = serial.Serial(
        SerialConfig.PORT, SerialConfig.BAUD_RATE, timeout=SerialConfig.TIMEOUT
    )
    time.sleep(2)  # Wait for the connection to initialize

    print(f"Connected. Listening for data... Saving to {Files.BINARY_FILE}")
    try:
        while True:
            read_string_from_bluetooth(bluetooth)
            read_binary_from_bluetooth(bluetooth)

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        if "bluetooth" in locals() and bluetooth.is_open:
            bluetooth.close()
            print("Bluetooth connection closed.")


if __name__ == "__main__":
    main()
