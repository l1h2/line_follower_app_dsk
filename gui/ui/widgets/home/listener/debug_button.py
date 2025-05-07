from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from utils import Styles


class DebugButton(QWidget):
    debug_state_changed = pyqtSignal(bool)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(50)
        self.setContentsMargins(0, 0, 20, 0)
        self._init_ui()

    def _init_ui(self) -> None:
        self._add_widgets()
        self._set_layout()

    def _add_widgets(self) -> None:
        self._add_debug_button()

    def _add_debug_button(self) -> None:
        self._debug_button = QPushButton("Debug")
        self._debug_button.setCheckable(True)
        self._debug_button.setChecked(False)
        self._debug_button.setToolTip("Enable debug prints")
        self._debug_button.setStyleSheet(Styles.CHECK_BUTTONS)
        self._debug_button.setFixedSize(70, 30)
        self._debug_button.clicked.connect(
            lambda: self.debug_state_changed.emit(self._debug_button.isChecked())
        )

    def _set_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.addWidget(self._debug_button)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
