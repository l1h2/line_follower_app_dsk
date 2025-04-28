from enum import Enum

from .robot_configs import RunningModes, StopModes


class SerialInputs(Enum):
    """List of serial inputs used in the program."""

    START_SIGNAL = "START"
    STOP_SIGNAL = b"STOP"
    KP = "KP:"
    KI = "KI:"
    KD = "KD:"
    BASE_PWM = "BASE_PWM:"
    MAX_PWM = "MAX_PWM:"
    STATE = "STATE:"
    RUNNING_MODE = "R_MODE:"
    STOP_MODE = "S_MODE:"
    LAPS = "LAPS:"
    STOP_TIME = "S_TIME:"
    LOG_DATA = "L_DATA:"


class SerialOutputs(Enum):
    """List of serial outputs used in the program."""

    START = b"$"
    STOP = b"%"
    SET_KP = b"P"
    SET_KI = b"I"
    SET_KD = b"D"
    SET_BASE_PWM = b"B"
    SET_MAX_PWM = b"M"
    SET_RUNNING_MODE = b"R"
    SET_STOP_MODE = b"S"
    SET_LAPS = b"L"
    SET_STOP_TIME = b"T"
    SET_LOG_DATA = b"G"


class Messages:
    """List of messages that can be sent to the robot."""

    @staticmethod
    def COMMAND(command: SerialOutputs, value: bytes = b"\0") -> bytes:
        if len(value) != 1:
            raise ValueError("value must be a single byte.")

        return command.value + value

    START_SIGNAL = COMMAND(SerialOutputs.START)
    STOP_SIGNAL = COMMAND(SerialOutputs.STOP)

    @staticmethod
    def SET_KP(kp: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_KP, kp)

    @staticmethod
    def SET_KI(ki: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_KI, ki)

    @staticmethod
    def SET_KD(kd: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_KD, kd)

    @staticmethod
    def SET_BASE_PWM(base_pwm: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_BASE_PWM, base_pwm)

    @staticmethod
    def SET_MAX_PWM(max_pwm: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_MAX_PWM, max_pwm)

    @staticmethod
    def SET_LAPS(laps: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_LAPS, laps)

    @staticmethod
    def SET_STOP_TIME(stop_time: bytes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_STOP_TIME, stop_time)

    @staticmethod
    def SET_RUNNING_MODE(mode: RunningModes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_RUNNING_MODE, bytes([mode.value]))

    @staticmethod
    def SET_STOP_MODE(mode: StopModes) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_STOP_MODE, bytes([mode.value]))

    @staticmethod
    def SET_LOG_DATA(log_data: bool) -> bytes:
        return Messages.COMMAND(SerialOutputs.SET_LOG_DATA, log_data.to_bytes())
