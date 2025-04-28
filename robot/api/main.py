import atexit

import serial
from PyQt6.QtCore import QObject, pyqtSignal

from utils import SerialConfig


class BluetoothApi(QObject):
    connection_change = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._bluetooth: serial.Serial | None = None
        atexit.register(self._safe_disconnect)

    @property
    def connected(self) -> bool:
        return self._bluetooth is not None and self._bluetooth.is_open

    def connect_serial(self) -> bool:
        try:
            self._bluetooth = serial.Serial(
                SerialConfig.PORT,
                SerialConfig.BAUD_RATE,
                timeout=SerialConfig.TIMEOUT,
            )
            self.connection_change.emit()
        except serial.SerialException as e:
            print(f"Failed to connect to Bluetooth device: {e}")
            self._bluetooth = None

        return self.connected

    def disconnect_serial(self) -> None:
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None

        self.connection_change.emit()

    def read_string(self) -> str | None:
        if not self.connected:
            return None

        try:
            if self._bluetooth.in_waiting <= 0:  # type: ignore[union-attr]
                return None

            data = self._bluetooth.read_until(b"\r\n")  # type: ignore[union-attr]
            return data[:-2].decode("latin-1")
        except serial.SerialException as e:
            print(f"Failed to read data from Bluetooth device: {e}")
            self.disconnect_serial()
            return None

    def read_binary(self) -> bytes | None:
        if not self.connected:
            return None

        try:
            if self._bluetooth.in_waiting <= 0:  # type: ignore[union-attr]
                return None

            data = self._bluetooth.read(2)  # type: ignore[union-attr]
            return data
        except serial.SerialException as e:
            print(f"Failed to read data from Bluetooth device: {e}")
            self.disconnect_serial()
            return None

    def write_data(self, data: bytes) -> None:
        if not self.connected:
            return

        try:
            self._bluetooth.write(data)  # type: ignore[union-attr]
            print(f"Sent: {data}")
        except serial.SerialException as e:
            print(f"Failed to write data to Bluetooth device: {e}")
            self.disconnect_serial()

    def _safe_disconnect(self) -> None:
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None
