from collections.abc import Callable

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from utils import SerialOutputs, UIConstants


class ByteInput(QWidget):
    """
    ### ByteInput Widget

    A widget that allows the user to input a byte value (0-255) and send it to a callback function.

    #### Parameters:
    - `label` (str): The label for the input field.
    - `command` (SerialOutputs): The command associated with the input value.
    - `callback` (Callable[[SerialOutputs, bytes], None]): The callback function to be called when the input value is submitted.

    #### Attributes:
    - `label` (QLabel): The label for the input field.
    - `input` (QLineEdit): The input field for the byte value.
    - `button` (QPushButton): The button to submit the input value.
    """

    def __init__(
        self,
        label: str,
        command: SerialOutputs,
        callback: Callable[[SerialOutputs, bytes], None],
    ):
        super().__init__()
        self._command = command
        self._on_send = callback

        self.setFixedHeight(UIConstants.ROW_HEIGHT)
        self._init_ui(label)

    def _init_ui(self, label: str) -> None:
        self._add_widgets(label)
        self._set_layout()

    def _add_widgets(self, label: str) -> None:
        self._add_label(label)
        self._add_input()
        self._add_button()

    def _add_label(self, label: str) -> None:
        self.label = QLabel(label)
        self.label.setFixedWidth(80)

    def _add_input(self) -> None:
        self.input = QLineEdit()
        self.input.setFixedWidth(60)
        self.input.setMaxLength(3)
        self.input.setPlaceholderText("0-255")
        self.input.setValidator(QIntValidator(0, 255))
        self.input.setToolTip("Enter a value between 0 and 255")
        self.input.textChanged.connect(self._on_text_changed)
        self.input.returnPressed.connect(self._on_input)

    def _add_button(self) -> None:
        self.button = QPushButton("Send")
        self.button.setFixedWidth(50)
        self.button.setToolTip("Send the value")
        self.button.clicked.connect(self._on_input)

    def _on_text_changed(self, text: str) -> None:
        if text.isdigit() and int(text) > 255:
            self.input.setText("255")

    def _on_input(self) -> None:
        value = self.input.text()

        if not value.isdigit():
            return

        value = int(value)
        self._on_send(self._command, value.to_bytes())

    def _set_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.input)
        layout.addWidget(self.button)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
