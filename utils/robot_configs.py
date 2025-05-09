from enum import Enum

# Bit arrangement for sensor data when receiving binary data from the robot
BIT_POSITIONS = (0, 8, 9, 10, 11, 1, 12, 13, 14, 15, 3, 2)


class RobotStates(Enum):
    """List of robot states used in the program."""

    INIT = 0
    IDLE = 1
    RUNNING = 2
    STOPPED = 3
    ERROR = 4


class RunningModes(Enum):
    """List of running modes used by the robot."""

    INIT = 0
    BASE_PID = 1
    SENSOR_TEST = 2


class StopModes(Enum):
    """List of stop modes used by the robot."""

    NONE = 0
    TIME = 1
    LAPS = 2
