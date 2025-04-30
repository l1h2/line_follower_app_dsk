import atexit

import serial
from PyQt6.QtCore import QObject, pyqtSignal
from serial.tools import list_ports

from utils import SerialConfig


class BluetoothApi(QObject):
    connection_change = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._bluetooth: serial.Serial | None = None
        self._com_port = self._get_initial_port()

        atexit.register(self._safe_disconnect)

    @property
    def port(self) -> str:
        if self._com_port not in self.ports:
            self._com_port = self._get_initial_port()

        return self._com_port

    @property
    def ports(self) -> list[str]:
        return self.list_available_ports()

    @property
    def connected(self) -> bool:
        return self._bluetooth is not None and self._bluetooth.is_open

    @staticmethod
    def list_available_ports() -> list[str]:
        return [
            port.device
            for port in sorted(list_ports.comports(), key=lambda port: port.device)
        ]

    def set_com_port(self, com_port: str) -> bool:
        if com_port == self._com_port:
            return False

        if self.connected:
            print("Disconnect before changing port.")
            return False

        if com_port not in self.ports:
            print(f"Port {com_port} is not available.")
            return False

        self._com_port = com_port
        return True

    def connect_serial(self) -> bool:
        try:
            self._bluetooth = serial.Serial(
                self._com_port,
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

    def _get_initial_port(self) -> str:
        ports = self.ports
        if SerialConfig.PORT in ports:
            return SerialConfig.PORT
        return ports[0] if ports else ""

    def _safe_disconnect(self) -> None:
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None
