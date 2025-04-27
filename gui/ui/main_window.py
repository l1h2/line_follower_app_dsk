from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget

from robot import LineFollower

from .widgets import ListenerWidget, SenderWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._init_ui()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        super().closeEvent(a0)

    def _init_ui(self) -> None:
        self._set_window()
        self._set_main_widget()
        self._add_widgets()
        self._set_layout()

    def _set_window(self) -> None:
        self.setWindowTitle("Line Follower App")
        self.resize(600, 500)

    def _set_main_widget(self) -> None:
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

    def _add_widgets(self) -> None:
        self.sender_widget = SenderWidget()
        self.listener_widget = ListenerWidget()
        self._add_connect_button()

    def _add_connect_button(self) -> None:
        self.button = QPushButton("Connect")
        self.button.setFixedWidth(200)
        self.button.setFixedHeight(80)
        self.button.setToolTip("Connect bluetooth")
        self.button.clicked.connect(self._line_follower.bluetooth.connect)

    def _set_layout(self) -> None:
        main_layout = QVBoxLayout(self.main_widget)

        display_layout = QHBoxLayout()
        display_layout.addWidget(self.sender_widget)
        display_layout.addWidget(self.listener_widget)

        main_layout.addLayout(display_layout)
        main_layout.addWidget(self.button)
