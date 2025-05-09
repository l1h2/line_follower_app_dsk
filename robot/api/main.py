import atexit

import serial
from PyQt6.QtCore import QObject, pyqtSignal
from serial.tools import list_ports

from utils import SerialConfig


class BluetoothApi(QObject):
    """
    ### BluetoothApi Class

    Handles Bluetooth communication with the robot. Inherits from QObject to use signals and slots.

    #### Signals:
    - `connection_change`: Signal emitted when the Bluetooth connection changes.

    #### Properties:
    - `port (str)`: Current COM port for the Bluetooth connection.
    - `ports (list[str])`: List of available COM ports.
    - `connected (bool)`: Indicates if the Bluetooth connection is open.

    #### Methods:
    - `list_available_ports() -> list[str]`: Lists all available COM ports.
    - `set_com_port(com_port: str) -> bool`: Sets the COM port for the Bluetooth connection.
    - `connect_serial() -> bool`: Connects to the Bluetooth device using the specified COM port.
    - `disconnect_serial() -> None`: Disconnects from the Bluetooth device.
    - `read_string() -> str | None`: Reads a string from the Bluetooth device.
    - `read_binary() -> bytes | None`: Reads binary data from the Bluetooth device.
    - `write_data(data: bytes) -> None`: Writes binary data to the Bluetooth device.
    """

    connection_change = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._bluetooth: serial.Serial | None = None
        self._com_port = self._get_initial_port()

        atexit.register(self._safe_disconnect)

    @property
    def port(self) -> str:
        """Get the current COM port."""
        if self._com_port not in self.ports:
            self._com_port = self._get_initial_port()

        return self._com_port

    @property
    def ports(self) -> list[str]:
        """Get the list of available COM ports."""
        return self.list_available_ports()

    @property
    def connected(self) -> bool:
        """Check if the Bluetooth connection is open."""
        return self._bluetooth is not None and self._bluetooth.is_open

    @staticmethod
    def list_available_ports() -> list[str]:
        """
        List all available COM ports.

        Returns:
            list[str]: List of available COM ports.
        """
        return [
            port.device
            for port in sorted(list_ports.comports(), key=lambda port: port.device)
        ]

    def set_com_port(self, com_port: str) -> bool:
        """
        Set the COM port for the Bluetooth connection.

        Args:
            com_port (str): The COM port to set.

        Returns:
            bool: True if the COM port was changed successfully, False otherwise.
        """
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
        """
        Connect to the Bluetooth device using the specified COM port.

        Returns:
            bool: True if the connection was successful, False otherwise.
        """
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
        """
        Disconnect from the Bluetooth device.
        """
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None

        self.connection_change.emit()

    def read_string(self) -> str | None:
        """
        Read a string from the Bluetooth device.

        Returns:
            str | None: The read string, or None if no data is available.
        """
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
        """
        Read binary data from the Bluetooth device.

        Returns:
            bytes | None: The read binary data, or None if no data is available.
        """
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
        """
        Write binary data to the Bluetooth device.

        Args:
            data (bytes): The binary data to write.
        """
        if not self.connected:
            return

        try:
            self._bluetooth.write(data)  # type: ignore[union-attr]
            print(f"Sent: {data}")
        except serial.SerialException as e:
            print(f"Failed to write data to Bluetooth device: {e}")
            self.disconnect_serial()

    def _get_initial_port(self) -> str:
        """Get the initial COM port for the Bluetooth connection."""
        ports = self.ports
        if SerialConfig.PORT in ports:
            return SerialConfig.PORT
        return ports[0] if ports else ""

    def _safe_disconnect(self) -> None:
        """Safely disconnect from the Bluetooth device when the program exits."""
        if self.connected:
            self._bluetooth.close()  # type: ignore[union-attr]
        self._bluetooth = None
