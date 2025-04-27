from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from utils import Messages, RunningModes, StopModes

from .byte_input import ByteInput
from .mode_select import ModeSelect


class SenderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self.kp_input = ByteInput("KP:", self._on_kp_input)
        self.ki_input = ByteInput("KI:", self._on_ki_input)
        self.kd_input = ByteInput("KD:", self._on_kd_input)
        self.base_pwm_input = ByteInput("Base PWM:", self._on_base_pwm_input)
        self.max_pwm_input = ByteInput("Max PWM:", self._on_max_pwm_input)
        self.laps_input = ByteInput("Laps:", self._on_laps_input)
        self.stop_time_input = ByteInput("Stop Time:", self._on_stop_time_input)

        self.running_mode_input = ModeSelect(
            "Running Mode:", RunningModes, self._on_running_mode_input
        )
        self.stop_mode_input = ModeSelect(
            "Stop Mode:", StopModes, self._on_stop_mode_input
        )

    def _on_kp_input(self, value: bytes) -> None:
        print(Messages.SET_KP(value))

    def _on_ki_input(self, value: bytes) -> None:
        print(Messages.SET_KI(value))

    def _on_kd_input(self, value: bytes) -> None:
        print(Messages.SET_KD(value))

    def _on_base_pwm_input(self, value: bytes) -> None:
        print(Messages.SET_BASE_PWM(value))

    def _on_max_pwm_input(self, value: bytes) -> None:
        print(Messages.SET_MAX_PWM(value))

    def _on_laps_input(self, value: bytes) -> None:
        print(Messages.SET_LAPS(value))

    def _on_stop_time_input(self, value: bytes) -> None:
        print(Messages.SET_STOP_TIME(value))

    def _on_running_mode_input(self, mode: RunningModes) -> None:
        print(Messages.SET_RUNNING_MODE(mode))

    def _on_stop_mode_input(self, mode: StopModes) -> None:
        print(Messages.SET_STOP_MODE(mode))

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
