from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget

from robot import LineFollower

from .connector.connector import ControllerWidget
from .listener.listener import ListenerWidget
from .sender.sender import SenderWidget


class HomeWidget(QWidget):
    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()

        self._init_ui()

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self.sender_widget = SenderWidget()
        self.listener_widget = ListenerWidget()
        self.connector_widget = ControllerWidget()

    def _set_layout(self) -> None:
        main_layout = QVBoxLayout(self)

        display_layout = QHBoxLayout()
        display_layout.addWidget(self.sender_widget)
        display_layout.addWidget(self.listener_widget)

        main_layout.addLayout(display_layout)
        main_layout.addWidget(self.connector_widget)
