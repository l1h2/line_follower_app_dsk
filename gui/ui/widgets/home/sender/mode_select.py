from collections.abc import Callable
from enum import Enum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QLabel, QPushButton, QWidget

from utils import SerialOutputs, UIConstants


class ModeSelect(QWidget):

    def __init__(
        self,
        label: str,
        command: SerialOutputs,
        enum_class: type[Enum],
        callback: Callable[[SerialOutputs, bytes], None],
    ):
        super().__init__()
        self._command = command
        self._on_send = callback
        self._enum_class = enum_class

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label)

    def _init_ui(self, label: str) -> None:
        self._add_widgets(label)
        self._set_layout()

    def _add_widgets(self, label: str) -> None:
        self._add_label(label)
        self._add_options()
        self._add_button()

    def _add_label(self, label: str) -> None:
        self.label = QLabel(label)
        self.label.setFixedWidth(90)

    def _add_options(self) -> None:
        self.options = QComboBox()
        self.options.setFixedWidth(100)
        self.options.addItems([e.name for e in self._enum_class])
        self.options.setToolTip("Select a mode")

    def _add_button(self) -> None:
        self.button = QPushButton("Send")
        self.button.setFixedWidth(50)
        self.button.setToolTip("Send the value")
        self.button.clicked.connect(self._on_input)

    def _on_input(self) -> None:
        value = self.options.currentText()

        if not value:
            return

        mode: int = self._enum_class[value].value
        self._on_send(self._command, mode.to_bytes())

    def _set_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.options)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
