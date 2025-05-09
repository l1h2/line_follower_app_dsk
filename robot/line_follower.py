from PyQt6.QtCore import QObject, pyqtSignal

from utils import RobotStates, RunningModes, SerialInputs, StopModes

from .api import BluetoothApi


class StateChanger(QObject):
    """
    ### StateChanger Class

    Handles state changes and emit signals. Inherits from QObject to use signals and slots.

    #### Signals:
    - `state_change`: Signal emitted when the state changes.
    """

    state_change = pyqtSignal()

    def __init__(self):
        super().__init__()

    def signal_state_change(self) -> None:
        self.state_change.emit()


class LineFollower:
    """
    ### LineFollower Class

    Singleton class that manages the state of the line follower robot. It handles configuration updates and
    communicates with the robot via Bluetooth. Should be updated with the latest configuration values.

    #### Attributes:
    - `BATTERY_CELLS (int)`: Number of battery cells.
    - `CELL_MAX_VOLTAGE (float)`: Maximum voltage of a single battery cell.

    #### Properties:
    - `is_running (bool)`: Indicates if the robot is currently running.
    - `state_changer (StateChanger)`: Instance of StateChanger for handling state changes.
    - `bluetooth (BluetoothApi)`: Instance of BluetoothApi for Bluetooth communication.
    - `battery (float | None)`: Current battery voltage.
    - `kp (int | None)`: Proportional gain for PID controller.
    - `ki (int | None)`: Integral gain for PID controller.
    - `kd (int | None)`: Derivative gain for PID controller.
    - `kff (int | None)`: Feedforward gain for PID controller.
    - `kb (int | None)`: Brake gain for PID controller.
    - `base_pwm (int | None)`: Base PWM value for motor control.
    - `max_pwm (int | None)`: Maximum PWM value for motor control.
    - `state (RobotStates | None)`: Current state of the robot.
    - `running_mode (RunningModes | None)`: Current running mode of the robot.
    - `stop_mode (StopModes | None)`: Current stop mode of the robot.
    - `laps (int)`: Number of laps completed.
    - `stop_time (int)`: Time to stop the robot.
    - `log_data (bool)`: Indicates if data logging is enabled.

    #### Methods:
    - `get_battery_voltage(byte: int) -> float`: Converts a byte value to battery voltage.
    - `update_config(command: SerialInputs, value: int) -> None`: Updates the configuration of the robot based on the command received.
    """

    _instance = None

    BATTERY_CELLS = 2
    CELL_MAX_VOLTAGE = 5.0

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LineFollower, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._state_changer = StateChanger()
            self._is_running = False

            self._battery = None
            self._kp = None
            self._ki = None
            self._kd = None
            self._kff = None
            self._kb = None
            self._base_pwm = None
            self._max_pwm = None
            self._state = None
            self._running_mode = None
            self._stop_mode = None
            self._laps = 0
            self._stop_time = 0
            self._log_data = False

            self._bluetooth = BluetoothApi()
            self._initialized = True

            self._config_map = {
                SerialInputs.BATTERY: self._update_battery,
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
    def is_running(self) -> bool:
        """Indicates if the robot is currently running."""
        return self._is_running

    @property
    def state_changer(self) -> StateChanger:
        """Instance of StateChanger for handling state changes."""
        return self._state_changer

    @property
    def bluetooth(self) -> BluetoothApi:
        """Instance of BluetoothApi for Bluetooth communication."""
        return self._bluetooth

    @property
    def battery(self) -> int | None:
        """Current battery voltage."""
        return self._battery

    @property
    def kp(self) -> int | None:
        """Proportional gain for PID controller."""
        return self._kp

    @property
    def ki(self) -> int | None:
        """Integral gain for PID controller."""
        return self._ki

    @property
    def kd(self) -> int | None:
        """Derivative gain for PID controller."""
        return self._kd

    @property
    def kff(self) -> int | None:
        """Feedforward gain for PID controller."""
        return self._kff

    @property
    def kb(self) -> int | None:
        """Brake gain for PID controller."""
        return self._kb

    @property
    def base_pwm(self) -> int | None:
        """Base PWM value for motor control."""
        return self._base_pwm

    @property
    def max_pwm(self) -> int | None:
        """Maximum PWM value for motor control."""
        return self._max_pwm

    @property
    def state(self) -> RobotStates | None:
        """Current state of the robot."""
        return self._state

    @property
    def running_mode(self) -> RunningModes | None:
        """Current running mode of the robot."""
        return self._running_mode

    @property
    def stop_mode(self) -> StopModes | None:
        """Current stop mode of the robot."""
        return self._stop_mode

    @property
    def laps(self) -> int:
        """Number of laps completed."""
        return self._laps

    @property
    def stop_time(self) -> int:
        """Time to stop the robot."""
        return self._stop_time

    @property
    def log_data(self) -> bool:
        """Indicates if data logging is enabled."""
        return self._log_data

    @staticmethod
    def get_battery_voltage(byte: int) -> float:
        """
        Converts a byte value to battery voltage.

        Args:
            byte (int): The byte value representing the battery voltage.

        Returns:
            float: The calculated battery voltage.
        """
        if byte == 0:
            return 0.0

        voltage = (
            (byte / 255) * LineFollower.CELL_MAX_VOLTAGE * LineFollower.BATTERY_CELLS
        )
        return round(voltage, 2)

    def update_config(self, command: SerialInputs, value: int) -> None:
        """
        Updates the configuration of the robot based on the command received.

        Args:
            command (SerialInputs): The command to be executed.
            value (int): The value associated with the command.
        """
        if command not in self._config_map:
            return

        self._config_map[command](value)

    def _update_battery(self, battery: int) -> None:
        """Updates the battery voltage."""
        self._battery = battery

    def _update_kp(self, kp: int) -> None:
        """Updates the proportional gain for PID controller."""
        self._kp = kp

    def _update_ki(self, ki: int) -> None:
        """Updates the integral gain for PID controller."""
        self._ki = ki

    def _update_kd(self, kd: int) -> None:
        """Updates the derivative gain for PID controller."""
        self._kd = kd

    def _update_base_pwm(self, base_pwm: int) -> None:
        """Updates the base PWM value for motor control."""
        self._base_pwm = base_pwm

    def _update_max_pwm(self, max_pwm: int) -> None:
        """Updates the maximum PWM value for motor control."""
        self._max_pwm = max_pwm

    def _update_state(self, state: int) -> None:
        """Updates the state of the robot."""
        self._state = RobotStates(state)
        self._is_running = state == RobotStates.RUNNING
        self._state_changer.signal_state_change()

    def _update_running_mode(self, mode: int) -> None:
        """Updates the running mode of the robot."""
        self._running_mode = RunningModes(mode)

    def _update_stop_mode(self, mode: int) -> None:
        """Updates the stop mode of the robot."""
        self._stop_mode = StopModes(mode)

    def _update_laps(self, laps: int) -> None:
        """Updates the number of laps completed."""
        self._laps = laps

    def _update_stop_time(self, stop_time: int) -> None:
        """Updates the time to stop the robot."""
        self._stop_time = stop_time

    def _set_log_data(self, log_data: int) -> None:
        """Sets the log data flag."""
        self._log_data = log_data == 1
