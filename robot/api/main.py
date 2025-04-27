import atexit

import serial

from utils import SerialConfig


class BluetoothApi:
    def __init__(self):
        self._bluetooth: serial.Serial | None = None
        atexit.register(self.disconnect)

    def connect(self) -> None:
        try:
            self._bluetooth = serial.Serial(
                SerialConfig.PORT,
                SerialConfig.BAUD_RATE,
                timeout=SerialConfig.TIMEOUT,
            )
        except serial.SerialException as e:
            print(f"Failed to connect to Bluetooth device: {e}")
            self._bluetooth = None
            return

    def disconnect(self) -> None:
        if self._bluetooth and self._bluetooth.is_open:
            self._bluetooth.close()
        self._bluetooth = None

    def read_string(self) -> str | None:
        if not self._bluetooth:
            return None

        if self._bluetooth.in_waiting <= 0:
            return None

        data = self._bluetooth.readline().decode("utf-8")
        return data

    def read_binary(self) -> bytes | None:
        if not self._bluetooth:
            return None

        if self._bluetooth.in_waiting <= 0:
            return None

        data = self._bluetooth.read(2)
        return data

    def write_data(self):
        # Write data to the Bluetooth device
        pass
