from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QTextEdit, QVBoxLayout, QWidget

from gui.workers import BluetoothListenerWorker
from robot import LineFollower
from utils import RobotStates, RunningModes, SerialInputs, StopModes, UIConstants

from .byte_display import ByteDisplay


class ListenerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._max_display_lines = UIConstants.MAX_DISPLAY_LINES
        self._line_follower = LineFollower()
        self._worker = BluetoothListenerWorker()

        self._init_ui()
        self._start_worker()

        self._update_map = {
            SerialInputs.KP: self.kp_display.set_value,
            SerialInputs.KI: self.ki_display.set_value,
            SerialInputs.KD: self.kd_display.set_value,
            SerialInputs.BASE_PWM: self.base_pwm_display.set_value,
            SerialInputs.MAX_PWM: self.max_pwm_display.set_value,
            SerialInputs.LAPS: self.laps_display.set_value,
            SerialInputs.STOP_TIME: self.stop_time_display.set_value,
            SerialInputs.STATE: self.state_display.set_value,
            SerialInputs.RUNNING_MODE: self.running_mode_display.set_value,
            SerialInputs.STOP_MODE: self.stop_mode_display.set_value,
        }

    def print_text(self, text: str) -> None:
        self._manage_display(text)

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self.kp_display = ByteDisplay()
        self.ki_display = ByteDisplay()
        self.kd_display = ByteDisplay()
        self.base_pwm_display = ByteDisplay()
        self.max_pwm_display = ByteDisplay()
        self.laps_display = ByteDisplay()
        self.stop_time_display = ByteDisplay()
        self.running_mode_display = ByteDisplay()
        self.stop_mode_display = ByteDisplay()

        self.state_display = ByteDisplay("STATE:", Qt.AlignmentFlag.AlignCenter)
        self._add_text_display()

    def _add_text_display(self) -> None:
        self._output_display = QTextEdit(self)
        self._output_display.setReadOnly(True)
        self._output_display.setFixedWidth(400)

    def _set_layout(self) -> None:
        values_layout = QVBoxLayout()
        values_layout.addWidget(self.kp_display)
        values_layout.addWidget(self.ki_display)
        values_layout.addWidget(self.kd_display)
        values_layout.addWidget(self.base_pwm_display)
        values_layout.addWidget(self.max_pwm_display)
        values_layout.addWidget(self.laps_display)
        values_layout.addWidget(self.stop_time_display)
        values_layout.addWidget(self.running_mode_display)
        values_layout.addWidget(self.stop_mode_display)
        values_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        text_display_layout = QVBoxLayout()
        text_display_layout.addWidget(self.state_display)
        text_display_layout.addWidget(self._output_display)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(values_layout)
        main_layout.addLayout(text_display_layout)

    def _start_worker(self) -> None:
        self._worker.output.connect(self._handle_output)
        self._worker.start()

    def _handle_output(self, data: str) -> None:
        self._manage_display(data)
        self._handle_command(data)

    def _manage_display(self, text: str) -> None:
        self._output_display.append(text)
        current_text = self._output_display.toPlainText()
        lines = current_text.splitlines()

        if len(lines) <= self._max_display_lines:
            return

        vertical_scrollbar = self._output_display.verticalScrollBar()
        if not vertical_scrollbar:
            return

        scroll_position = vertical_scrollbar.value()

        self._output_display.setPlainText("\n".join(lines[-self._max_display_lines :]))
        vertical_scrollbar.setValue(scroll_position)

    def _handle_command(self, msg: str) -> None:
        for command in self._update_map.keys():
            if not isinstance(command.value, str):
                continue

            if not msg.startswith(command.value):
                continue

            int_value = int(ord(msg[-1]))
            str_value = str(int_value)

            if command == SerialInputs.RUNNING_MODE:
                str_value = RunningModes(int_value).name
            elif command == SerialInputs.STOP_MODE:
                str_value = StopModes(int_value).name
            elif command == SerialInputs.STATE:
                str_value = RobotStates(int_value).name

            self._update_map[command](str_value)
            self._line_follower.update_config(command, int_value)
            break
