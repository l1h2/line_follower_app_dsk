from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from robot import LineFollower
from utils import RobotStates, Styles
from utils.messages import Messages


class ConnectorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._line_follower.bluetooth.connection_change.connect(
            self._update_connection_button
        )
        self._line_follower.state_changer.state_change.connect(
            self._update_start_button
        )

        self._init_ui()

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self._add_start_button()
        self._add_connect_button()

    def _add_connect_button(self) -> None:
        self.connect_button = QPushButton()
        self.connect_button.setFixedWidth(200)
        self.connect_button.setFixedHeight(80)
        self.connect_button.setToolTip("Connect bluetooth")
        self.connect_button.clicked.connect(self._toggle_connection)
        self._update_connection_button()

    def _toggle_connection(self) -> None:
        if self._line_follower.bluetooth.connected:
            self._line_follower.bluetooth.disconnect_serial()
        else:
            self._line_follower.bluetooth.connect_serial()

    def _update_connection_button(self) -> None:
        if self._line_follower.bluetooth.connected:
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(Styles.STOP_BUTTONS)
        else:
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(Styles.START_BUTTONS)
            self._disable_start_button()

    def _add_start_button(self) -> None:
        self.start_button = QPushButton()
        self.start_button.setFixedWidth(200)
        self.start_button.setFixedHeight(80)
        self.start_button.setToolTip("Start RUNNING mode")
        self.start_button.setStyleSheet(Styles.START_BUTTONS)
        self.start_button.clicked.connect(self._toggle_start)
        self._update_start_button()

    def _toggle_start(self) -> None:
        if self._line_follower.state == RobotStates.IDLE:
            self._line_follower.bluetooth.write_data(Messages.START_SIGNAL)
        elif self._line_follower.state == RobotStates.RUNNING:
            self._line_follower.bluetooth.write_data(Messages.STOP_SIGNAL)

    def _update_start_button(self) -> None:
        if self._line_follower.state == RobotStates.RUNNING:
            self.start_button.setText("Stop")
            self.start_button.setStyleSheet(Styles.STOP_BUTTONS)
            self.start_button.setEnabled(True)
        elif self._line_follower.state == RobotStates.IDLE:
            self.start_button.setText("Start")
            self.start_button.setStyleSheet(Styles.START_BUTTONS)
            self.start_button.setEnabled(True)
        else:
            self._disable_start_button()

    def _disable_start_button(self) -> None:
        self.start_button.setText("Not Available")
        self.start_button.setStyleSheet(Styles.DISABLED_BUTTONS)
        self.start_button.setEnabled(False)

    def _set_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self.start_button)
        main_layout.addSpacing(300)
        main_layout.addWidget(self.connect_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
