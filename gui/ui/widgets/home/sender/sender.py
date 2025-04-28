from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from robot import LineFollower
from utils import Messages, RunningModes, SerialOutputs, StopModes

from .byte_input import ByteInput
from .mode_select import ModeSelect


class SenderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()

        self._init_ui()

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self.kp_input = ByteInput("KP:", SerialOutputs.SET_KP, self._on_send)
        self.ki_input = ByteInput("KI:", SerialOutputs.SET_KI, self._on_send)
        self.kd_input = ByteInput("KD:", SerialOutputs.SET_KD, self._on_send)
        self.base_pwm_input = ByteInput(
            "Base PWM:", SerialOutputs.SET_BASE_PWM, self._on_send
        )
        self.max_pwm_input = ByteInput(
            "Max PWM:", SerialOutputs.SET_MAX_PWM, self._on_send
        )
        self.laps_input = ByteInput("Laps:", SerialOutputs.SET_LAPS, self._on_send)
        self.stop_time_input = ByteInput(
            "Stop Time:", SerialOutputs.SET_STOP_TIME, self._on_send
        )

        self.running_mode_input = ModeSelect(
            "Running Mode:",
            SerialOutputs.SET_RUNNING_MODE,
            RunningModes,
            self._on_send,
        )
        self.stop_mode_input = ModeSelect(
            "Stop Mode:",
            SerialOutputs.SET_STOP_MODE,
            StopModes,
            self._on_send,
        )

    def _on_send(self, command: SerialOutputs, value: bytes) -> None:
        msg = Messages.COMMAND(command, value)
        self._line_follower.bluetooth.write_data(msg)

    def _set_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.kp_input)
        main_layout.addWidget(self.ki_input)
        main_layout.addWidget(self.kd_input)
        main_layout.addWidget(self.base_pwm_input)
        main_layout.addWidget(self.max_pwm_input)
        main_layout.addWidget(self.laps_input)
        main_layout.addWidget(self.stop_time_input)
        main_layout.addWidget(self.running_mode_input)
        main_layout.addWidget(self.stop_mode_input)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
