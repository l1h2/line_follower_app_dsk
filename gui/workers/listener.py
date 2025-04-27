import time

from PyQt6.QtCore import QThread, pyqtSignal

from robot import LineFollower
from utils import SerialInputs


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
        while self._listening:
            data = self._line_follower.bluetooth.read_string()

            if not data:
                continue

            if data == SerialInputs.START_SIGNAL.value:
                return

            self.output.emit(data[:-1])

    def _listen_binary(self) -> None:
        buffer = b""
        start_time = time.time()

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
            self._handle_binary(buffer, elapsed_time_ms)
            buffer = b""

    def _handle_binary(self, buffer: bytes, timestamp: int) -> None:
        bits = " ".join(f"{byte:08b}" for byte in buffer)
        self.output.emit(f"{timestamp} ms: {buffer.hex()} - {bits}")

    def _check_buffer(self, buffer: bytes) -> bool:
        return not buffer == SerialInputs.STOP_SIGNAL.value[: len(buffer)]
