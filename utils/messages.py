from enum import Enum

from .robot_configs import RunningModes, StopModes


class SerialInputs(Enum):
    """List of serial inputs used in the program."""

    START_SIGNAL = "START\n"
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


class Messages:
    """List of messages that can be sent to the robot."""

    START = SerialOutputs.START
    STOP = SerialOutputs.STOP

    @staticmethod
    def SET_KP(kp: bytes) -> bytes:
        if len(kp) != 1:
            raise ValueError("kp must be a single byte.")

        return SerialOutputs.SET_KP.value + kp

    @staticmethod
    def SET_KI(ki: bytes) -> bytes:
        if len(ki) != 1:
            raise ValueError("ki must be a single byte.")

        return SerialOutputs.SET_KI.value + ki

    @staticmethod
    def SET_KD(kd: bytes) -> bytes:
        if len(kd) != 1:
            raise ValueError("kd must be a single byte.")

        return SerialOutputs.SET_KD.value + kd

    @staticmethod
    def SET_BASE_PWM(base_pwm: bytes) -> bytes:
        if len(base_pwm) != 1:
            raise ValueError("base_pwm must be a single byte.")

        return SerialOutputs.SET_BASE_PWM.value + base_pwm

    @staticmethod
    def SET_MAX_PWM(max_pwm: bytes) -> bytes:
        if len(max_pwm) != 1:
            raise ValueError("max_pwm must be a single byte.")

        return SerialOutputs.SET_MAX_PWM.value + max_pwm

    @staticmethod
    def SET_LAPS(laps: bytes) -> bytes:
        if len(laps) != 1:
            raise ValueError("laps must be a single byte.")

        return SerialOutputs.SET_LAPS.value + laps

    @staticmethod
    def SET_STOP_TIME(stop_time: bytes) -> bytes:
        if len(stop_time) != 1:
            raise ValueError("stop_time must be a single byte.")

        return SerialOutputs.SET_STOP_TIME.value + stop_time

    @staticmethod
    def SET_RUNNING_MODE(mode: RunningModes) -> bytes:
        return SerialOutputs.SET_RUNNING_MODE.value + bytes([mode.value])

    @staticmethod
    def SET_STOP_MODE(mode: StopModes) -> bytes:
        return SerialOutputs.SET_STOP_MODE.value + bytes([mode.value])
