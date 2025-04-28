from PyQt6.QtCore import QObject, pyqtSignal

from utils import RobotStates, RunningModes, SerialInputs, StopModes

from .api import BluetoothApi


class StateChanger(QObject):
    state_change = pyqtSignal()

    def __init__(self):
        super().__init__()

    def signal_state_change(self) -> None:
        self.state_change.emit()


class LineFollower:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LineFollower, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._state_changer = StateChanger()
            self._is_running = False

            self._kp = None
            self._ki = None
            self._kd = None
            self._base_pwm = None
            self._max_pwm = None
            self._state = None
            self._running_mode = None
            self._stop_mode = None
            self._laps = 0
            self._stop_time = 0

            self._bluetooth = BluetoothApi()
            self._initialized = True

            self._config_map = {
                SerialInputs.KP: self._update_kp,
                SerialInputs.KI: self._update_ki,
                SerialInputs.KD: self._update_kd,
                SerialInputs.BASE_PWM: self._update_base_pwm,
                SerialInputs.MAX_PWM: self._update_max_pwm,
                SerialInputs.STATE: self._update_state,
                SerialInputs.RUNNING_MODE: self._update_running_mode,
                SerialInputs.STOP_MODE: self._update_stop_mode,
                SerialInputs.LAPS: self._update_laps,
                SerialInputs.STOP_TIME: self._update_stop_time,
            }

    @property
    def state_changer(self) -> StateChanger:
        return self._state_changer

    @property
    def bluetooth(self) -> BluetoothApi:
        return self._bluetooth

    @property
    def kp(self) -> int | None:
        return self._kp

    @property
    def ki(self) -> int | None:
        return self._ki

    @property
    def kd(self) -> int | None:
        return self._kd

    @property
    def base_pwm(self) -> int | None:
        return self._base_pwm

    @property
    def max_pwm(self) -> int | None:
        return self._max_pwm

    @property
    def state(self) -> RobotStates | None:
        return self._state

    @property
    def running_mode(self) -> RunningModes | None:
        return self._running_mode

    @property
    def stop_mode(self) -> StopModes | None:
        return self._stop_mode

    @property
    def laps(self) -> int:
        return self._laps

    @property
    def stop_time(self) -> int:
        return self._stop_time

    def update_config(self, command: SerialInputs, value: int) -> None:
        if command not in self._config_map:
            return

        self._config_map[command](value)

    def _update_kp(self, kp: int) -> None:
        self._kp = kp

    def _update_ki(self, ki: int) -> None:
        self._ki = ki

    def _update_kd(self, kd: int) -> None:
        self._kd = kd

    def _update_base_pwm(self, base_pwm: int) -> None:
        self._base_pwm = base_pwm

    def _update_max_pwm(self, max_pwm: int) -> None:
        self._max_pwm = max_pwm

    def _update_state(self, state: int) -> None:
        self._state = RobotStates(state)
        self._state_changer.signal_state_change()

    def _update_running_mode(self, mode: int) -> None:
        self._running_mode = RunningModes(mode)

    def _update_stop_mode(self, mode: int) -> None:
        self._stop_mode = StopModes(mode)

    def _update_laps(self, laps: int) -> None:
        self._laps = laps

    def _update_stop_time(self, stop_time: int) -> None:
        self._stop_time = stop_time
