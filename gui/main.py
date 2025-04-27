from PyQt6.QtWidgets import QApplication

from .ui import MainWindow


def start_gui() -> None:
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
