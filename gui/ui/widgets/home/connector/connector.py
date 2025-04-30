from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from robot import LineFollower
from utils import Messages, RobotStates, Styles


class ControllerWidget(QWidget):

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._current_port = self._line_follower.bluetooth.port
        self._update_port = True

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
        self._add_ports_refresh_button()
        self._add_port_selector()
        self._add_connect_button()

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

    def _add_ports_refresh_button(self) -> None:
        self.refresh_button = QPushButton("⟳")
        self.refresh_button.setFixedWidth(20)
        self.refresh_button.setToolTip("Refresh COM ports")
        self.refresh_button.clicked.connect(lambda: self._update_ports(True))

    def _add_port_selector(self) -> None:
        self.ports = QComboBox()
        self.ports.setFixedWidth(80)
        self.ports.addItems(self._line_follower.bluetooth.ports)
        self.ports.setCurrentText(self._current_port)
        self.ports.setToolTip("Select a COM port")
        self.ports.currentTextChanged.connect(self._on_port_change)

    def _on_port_change(self, port: str | None) -> None:
        if not port or not self._update_port or port == self._current_port:
            return

        self._update_ports(False)

        if self._line_follower.bluetooth.set_com_port(port):
            self._current_port = port

        self.ports.setCurrentText(self._current_port)

    def _update_ports(self, change_text: bool = True) -> None:
        self._update_port = False

        self.ports.clear()
        self.ports.addItems(self._line_follower.bluetooth.ports)

        if not change_text:
            self._update_port = True
            return

        if self._current_port not in self._line_follower.bluetooth.ports:
            self._current_port = self._line_follower.bluetooth.port

        self.ports.setCurrentText(self._current_port)
        self._update_port = True

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

        self._update_ports()

    def _update_connection_button(self) -> None:
        if self._line_follower.bluetooth.connected:
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet(Styles.STOP_BUTTONS)
            self.ports.setEnabled(False)
        else:
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet(Styles.START_BUTTONS)
            self._disable_start_button()
            self.ports.setEnabled(True)

    def _set_layout(self) -> None:
        ports_options_layout = QHBoxLayout()
        ports_options_layout.addWidget(self.refresh_button)
        ports_options_layout.addWidget(self.ports)
        ports_options_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        connector_layout = QVBoxLayout()
        connector_layout.addWidget(self.connect_button)
        connector_layout.addLayout(ports_options_layout)

        controller_layout = QVBoxLayout()
        controller_layout.addWidget(self.start_button)
        controller_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(controller_layout)
        main_layout.addSpacing(300)
        main_layout.addLayout(connector_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
