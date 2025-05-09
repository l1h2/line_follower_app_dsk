import time

from PyQt6.QtCore import QThread, pyqtSignal

from robot import LineFollower
from utils import BIT_POSITIONS, Files, SerialInputs


class BluetoothListenerWorker(QThread):
    """
    ### BluetoothListenerWorker Class

    This class is responsible for listening to the Bluetooth device and processing the received data.
    It inherits from QThread to run in a separate thread.

    #### Signals:
    - `output (str)`: Signal emitted when new data is received from the Bluetooth device.

    #### Properties:
    - `listening (bool)`: Indicates if the listener is currently active.

    #### Methods:
    - `run()`: Starts the listener thread.
    - `stop()`: Stops the listener thread.
    """

    output = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._listening = False

    @property
    def listening(self) -> bool:
        """Check if the listener is currently active."""
        return self._listening

    def run(self) -> None:
        """
        Starts the listener thread.
        """
        self._listening = True

        while self._listening:
            self._listen_string()
            self._listen_binary()

    def stop(self) -> None:
        """
        Stops the listener thread.
        """
        self._listening = False

    def _listen_string(self) -> None:
        """Listen for string data from the Bluetooth device and write it to a text file."""
        with open(Files.TEXT_FILE, "a", encoding="latin-1") as f:
            while self._listening:
                data = self._line_follower.bluetooth.read_string()

                if not data:
                    continue

                if data == SerialInputs.START_SIGNAL.value:
                    return

                f.write(f"{data}\n")
                f.flush()
                self.output.emit(data)

    def _listen_binary(self) -> None:
        """Listen for binary data from the Bluetooth device and write it to a binary file."""
        buffer = b""
        start_time = time.time()

        # TODO: Offload file and binary processing operations to a faster C++ subprocess
        with open(Files.BINARY_FILE, "ab") as binary_file, open(
            Files.TIMESTAMP_FILE, "a"
        ) as timestamp_file:
            while self._listening:
                data = self._line_follower.bluetooth.read_binary()

                if not data:
                    continue

                buffer += data

                if buffer == SerialInputs.STOP_SIGNAL.value:
                    return

                if not self._check_buffer(buffer):
                    continue

                elapsed_time_ms = int((time.time() - start_time) * 1000)
                timestamp_file.write(f"{elapsed_time_ms}\n")
                timestamp_file.flush()

                binary_file.write(buffer)
                binary_file.flush()

                self._handle_binary(buffer, elapsed_time_ms)
                buffer = b""

    def _handle_binary(self, buffer: bytes, timestamp: int) -> None:
        """Handle the binary data received from the Bluetooth device."""
        try:
            word = (buffer[0] << 8) | buffer[1]
        except IndexError:
            return

        bits = [(word & (1 << i)) >> i for i in BIT_POSITIONS]
        formatted_bits = "   ".join(
            [
                f"{bits[0] if bits[0] == 1 else '  '}",
                "|",
                "  ".join(str(bit if bit == 1 else "  ") for bit in bits[1:10]),
                "|",
                f"{bits[10] if bits[10] == 1 else '  '}",
                f"||  {bits[11] if bits[11] == 1 else '  '}",
            ]
        )

        self.output.emit(f"{timestamp} ms:  {formatted_bits}")

    def _check_buffer(self, buffer: bytes) -> bool:
        """Check if the buffer is valid and not a stop signal."""
        return not buffer == SerialInputs.STOP_SIGNAL.value[: len(buffer)]
