from enum import Enum


class Files:
    """List of file names used in the program."""

    BINARY_FILE = "data/serial_data_log.bin"
    TIMESTAMP_FILE = "data/timestamps.txt"
    TEXT_FILE = "data/serial_data_log.txt"
    SENSOR_DATA = "data/sensors.csv"


class SerialConfig:
    """Serial port configuration."""

    PORT = "COM9"
    BAUD_RATE = 9600
    TIMEOUT = 1


class UIConstants:
    MAX_DISPLAY_LINES = 70
    ROW_HEIGHT = 40


class Booleans(Enum):
    """List of boolean values used in the program."""

    FALSE = 0
    TRUE = 1
