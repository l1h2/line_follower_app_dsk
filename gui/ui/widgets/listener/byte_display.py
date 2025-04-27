from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QWidget

from utils import UIConstants


class ByteDisplay(QWidget):
    def __init__(
        self,
        label: str = "Current value:",
        align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignLeft,
    ) -> None:
        super().__init__()
        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label, align)

    def set_value(self, value: str) -> None:
        self.value.setText(value)

    def _init_ui(self, label: str, align: Qt.AlignmentFlag) -> None:
        self._add_widgets(label)
        self._set_layout(align)

    def _add_widgets(self, label: str) -> None:
        self._add_label(label)
        self._add_value()

    def _add_label(self, label: str) -> None:
        self.label = QLabel(label)
        self.label.setFixedWidth(80)

    def _add_value(self) -> None:
        self.value = QLineEdit()
        self.value.setText("-")
        self.value.setFixedWidth(100)
        self.value.setToolTip("Current value in the robot")
        self.value.setReadOnly(True)

    def _set_layout(self, align: Qt.AlignmentFlag) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.value)
        layout.setAlignment(align)
