from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from robot import LineFollower

from .widgets import HomeWidget


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
        self.resize(1000, 500)

    def _set_main_widget(self) -> None:
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)

    def _add_widgets(self) -> None:
        self.home_widget = HomeWidget()

    def _set_layout(self) -> None:
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.addWidget(self.home_widget)
