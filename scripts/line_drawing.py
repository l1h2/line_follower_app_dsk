import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Add the project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils import Files

TOTAL_CENTRAL_SENSORS = 9
AVG_ERROR = (TOTAL_CENTRAL_SENSORS - 1) / 2

# TODO: Calibrate values on actual track and adjust for different speeds
DELTA_DISTANCE = 1
SENSOR_ANGLE = np.pi / TOTAL_CENTRAL_SENSORS / 40

MARKER_OFFSET = 40


def get_dataframe() -> pd.DataFrame:
    return pd.read_csv(Files.SENSOR_DATA, index_col=0)


def get_line_path(
    data: pd.DataFrame,
) -> tuple[
    list[float], list[float], list[tuple[float, float]], list[tuple[float, float]]
]:
    x_positions: list[float] = [0]
    y_positions: list[float] = [0]

    left_markers: list[tuple[float, float]] = []
    right_markers: list[tuple[float, float]] = []

    last_error = 0
    cumulative_angle = 0

    for _, row in data.iterrows():  # type: ignore
        central_sensors = pd.concat([row[2:7], row[8:12]])  # type: ignore
        active_sensors = [
            i for i, value in enumerate(central_sensors, start=0) if value == 1
        ]

        error = (
            -(sum(active_sensors) / len(active_sensors) - AVG_ERROR)
            if active_sensors
            else last_error
        )
        last_error = error

        angle = error * SENSOR_ANGLE
        cumulative_angle += angle

        dx = DELTA_DISTANCE * np.cos(cumulative_angle)
        dy = DELTA_DISTANCE * np.sin(cumulative_angle)

        x_positions.append(x_positions[-1] + dx)
        y_positions.append(y_positions[-1] + dy)

        # Check for markers
        if row.iloc[1] == 1:
            left_markers.append(
                get_marker_coordinates(
                    x_positions[-1], y_positions[-1], cumulative_angle, left=True
                )
            )
        if row.iloc[12] == 1:
            right_markers.append(
                get_marker_coordinates(
                    x_positions[-1], y_positions[-1], cumulative_angle, left=False
                )
            )

    return x_positions, y_positions, left_markers, right_markers


def get_marker_coordinates(
    X: float, Y: float, angle: float, left: bool = True
) -> tuple[float, float]:
    offset = MARKER_OFFSET if left else -MARKER_OFFSET

    x_offset = -offset * np.sin(angle)
    y_offset = offset * np.cos(angle)

    return X + x_offset, Y + y_offset


def plot_line_path(
    x_positions: list[float],
    y_positions: list[float],
    left_markers: list[tuple[float, float]],
    right_markers: list[tuple[float, float]],
):
    plt.figure(figsize=(10, 6))
    plt.plot(x_positions, y_positions, marker="o", linestyle="-", label="Robot Path")

    # Plot left markers
    if left_markers:
        left_x, left_y = zip(*left_markers)
        plt.scatter(left_x, left_y, color="red", label="Left Markers", zorder=5)

    # Plot right markers
    if right_markers:
        right_x, right_y = zip(*right_markers)
        plt.scatter(right_x, right_y, color="blue", label="Right Markers", zorder=5)

    plt.axis("equal")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("2D Line Path with Markers")
    plt.grid()
    plt.legend()
    plt.show()


if __name__ == "__main__":
    df = get_dataframe()
    x_positions, y_positions, left_markers, right_markers = get_line_path(df)

    plot_line_path(x_positions, y_positions, left_markers, right_markers)
