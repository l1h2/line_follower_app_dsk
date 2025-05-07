from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QStackedLayout, QVBoxLayout, QWidget

from gui.workers import BluetoothListenerWorker
from robot import LineFollower
from utils import RobotStates, RunningModes, SerialInputs, StopModes

from .byte_display import ByteDisplay
from .debug_button import DebugButton
from .text_display import TextDisplay


class ListenerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._debug_prints = False

        self._line_follower = LineFollower()
        self._worker = BluetoothListenerWorker()

        self._init_ui()
        self._start_worker()

        self._update_map = {
            SerialInputs.BATTERY: self.battery_display.set_value,
            SerialInputs.KP: self.kp_display.set_value,
            SerialInputs.KI: self.ki_display.set_value,
            SerialInputs.KD: self.kd_display.set_value,
            SerialInputs.KFF: self.kff_display.set_value,
            SerialInputs.KB: self.kb_display.set_value,
            SerialInputs.BASE_PWM: self.base_pwm_display.set_value,
            SerialInputs.LAPS: self.laps_display.set_value,
            SerialInputs.STOP_TIME: self.stop_time_display.set_value,
            SerialInputs.STATE: self.state_display.set_value,
            SerialInputs.RUNNING_MODE: self.running_mode_display.set_value,
            SerialInputs.STOP_MODE: self.stop_mode_display.set_value,
            SerialInputs.LOG_DATA: self.log_data_display.set_value,
        }

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self.kp_display = ByteDisplay()
        self.ki_display = ByteDisplay()
        self.kd_display = ByteDisplay()
        self.kff_display = ByteDisplay()
        self.kb_display = ByteDisplay()
        self.base_pwm_display = ByteDisplay()
        self.laps_display = ByteDisplay()
        self.stop_time_display = ByteDisplay()
        self.running_mode_display = ByteDisplay()
        self.stop_mode_display = ByteDisplay()
        self.log_data_display = ByteDisplay()

        self.state_display = ByteDisplay("STATE:", Qt.AlignmentFlag.AlignCenter)
        self.battery_display = ByteDisplay("BATTERY:", Qt.AlignmentFlag.AlignCenter)

        self.output_display = TextDisplay(parent=self)
        self.debug_button = DebugButton(self)
        self.debug_button.debug_state_changed.connect(self._update_debug_state)

    def _update_debug_state(self, state: bool) -> None:
        self._debug_prints = state

    def _set_layout(self) -> None:
        values_layout = QVBoxLayout()
        values_layout.addWidget(self.kp_display)
        values_layout.addWidget(self.ki_display)
        values_layout.addWidget(self.kd_display)
        values_layout.addWidget(self.kff_display)
        values_layout.addWidget(self.kb_display)
        values_layout.addWidget(self.base_pwm_display)
        values_layout.addWidget(self.laps_display)
        values_layout.addWidget(self.stop_time_display)
        values_layout.addWidget(self.running_mode_display)
        values_layout.addWidget(self.stop_mode_display)
        values_layout.addWidget(self.log_data_display)
        values_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        state_layout = QHBoxLayout()
        state_layout.addWidget(self.state_display)
        state_layout.addWidget(self.battery_display)

        text_output_layout = QStackedLayout()
        text_output_layout.addWidget(self.debug_button)
        text_output_layout.addWidget(self.output_display)
        text_output_layout.setStackingMode(QStackedLayout.StackingMode.StackAll)

        text_display_layout = QVBoxLayout()
        text_display_layout.addLayout(state_layout)
        text_display_layout.addLayout(text_output_layout)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(values_layout)
        main_layout.addLayout(text_display_layout)

    def _start_worker(self) -> None:
        self._worker.output.connect(self._handle_output)
        self._worker.start()

    def _handle_output(self, data: str) -> None:
        if not self._handle_command(data) or self._debug_prints:
            self.output_display.print_text(data)

    def _handle_command(self, msg: str) -> bool:
        for command in self._update_map.keys():
            if not isinstance(command.value, str):
                continue

            if not msg.startswith(command.value):
                continue

            int_value = int(ord(msg[-1]))
            str_value = str(int_value)

            if command == SerialInputs.BATTERY:
                str_value = str(LineFollower.get_battery_voltage(int_value)) + " V"
            elif command == SerialInputs.STATE:
                str_value = RobotStates(int_value).name
            elif command == SerialInputs.RUNNING_MODE:
                str_value = RunningModes(int_value).name
            elif command == SerialInputs.STOP_MODE:
                str_value = StopModes(int_value).name
            elif command == SerialInputs.LOG_DATA:
                str_value = "OFF" if int_value == 0 else "ON"
            elif command == SerialInputs.KD:
                if int_value == 255:
                    int_value = 1000
                    str_value = "1000"

            self._update_map[command](str_value)
            self._line_follower.update_config(command, int_value)
            return True

        return False
