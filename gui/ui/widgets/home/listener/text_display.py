from PyQt6.QtWidgets import QTextEdit, QWidget

from utils import UIConstants


class TextDisplay(QTextEdit):
    def __init__(
        self,
        max_display_lines: int = UIConstants.MAX_DISPLAY_LINES,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent=parent)
        self.setReadOnly(True)
        self.setFixedWidth(450)
        self._max_display_lines = max_display_lines

    def print_text(self, text: str) -> None:
        self._manage_display(text)

    def _manage_display(self, text: str) -> None:
        self.append(text)
        current_text = self.toPlainText()
        lines = current_text.splitlines()

        if len(lines) <= self._max_display_lines:
            return

        vertical_scrollbar = self.verticalScrollBar()
        if not vertical_scrollbar:
            return

        scroll_position = vertical_scrollbar.value()

        self.setPlainText("\n".join(lines[-self._max_display_lines :]))
        vertical_scrollbar.setValue(scroll_position)
