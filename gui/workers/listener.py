import time

from PyQt6.QtCore import QThread, pyqtSignal

from robot import LineFollower
from utils import BIT_POSITIONS, Files, SerialInputs


class BluetoothListenerWorker(QThread):
    output = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._line_follower = LineFollower()
        self._listening = False

    @property
    def listening(self) -> bool:
        return self._listening

    def run(self) -> None:
        self._listening = True

        while self._listening:
            self._listen_string()
            self._listen_binary()

    def stop(self) -> None:
        self._listening = False

    def _listen_string(self) -> None:
        with open(Files.TEXT_FILE, "a") as f:
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
        buffer = b""
        start_time = time.time()

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
        word = (buffer[0] << 8) | buffer[1]
        bits = [(word & (1 << i)) >> i for i in BIT_POSITIONS]
        formatted_bits = "  |  ".join(
            [
                f"{bits[0] if bits[0] == 1 else ' '}",
                "  ".join(str(bit if bit == 1 else " ") for bit in bits[1:6]),
                "  ".join(str(bit if bit == 1 else " ") for bit in bits[7:11]),
                f"{bits[11] if bits[11] == 1 else ' '}",
                f"||  {bits[6] if bits[6] == 1 else ' '}",
            ]
        )

        self.output.emit(f"{timestamp} ms:  {formatted_bits}")

    def _check_buffer(self, buffer: bytes) -> bool:
        return not buffer == SerialInputs.STOP_SIGNAL.value[: len(buffer)]
