import logging
import serial
from lerobot.utils.decorators import check_if_already_connected, check_if_not_connected
import time

logger = logging.getLogger(__name__)

class LogsplitterSwitches():
    name = "logsplitter_switches"
    COM_TIMEOUT = 0.1
    COM_STARTUP_TIMEOUT = 2
    BAUD = 115200

    def __init__(self, port: str):
        self.port = port
        self._connected = False
        return
    
    def __repr__(self) -> str:
        return self.name

    @property
    def is_connected(self) -> bool:
        return self._connected
    
    @check_if_already_connected
    def connect(self) -> None:
        try:
            self.serial = serial.Serial(self.port, self.BAUD, timeout=self.COM_TIMEOUT)
            accessory_response = self.listen_com(startup=True)
            assert "READY" in accessory_response
        except (FileNotFoundError, OSError, serial.SerialException, AssertionError) as e:
            raise ConnectionError(
                f"Failed to connect to {self} on port: {self.port}"
            ) from e
        
        self._connected = True
        return
    
    # @check_if_not_connected
    # def calibrate(self) -> None:
    #     pass
    # def is_calibrated(self) -> bool:
    #     return True

    def send_com(self, message) -> None:
        self.serial.write(f"{message}\n".encode('utf-8'))
        return

    def listen_com(self, startup=False):
        if startup:
            start_time = time.perf_counter()
            while not self.serial.in_waiting:
                if time.perf_counter() - start_time > self.COM_STARTUP_TIMEOUT:
                    raise ConnectionError(f"Failed to connect to {self.name}")
                time.sleep(0.01)
        response = self.serial.readline().decode('utf-8').rstrip()
        if not response:
            raise ConnectionError(f"No response received from {self.name}")
        return response    
    
    @property
    def action_features(self):
        return { "logsplitter.vel": float }

    @check_if_not_connected
    def get_action(self):
        self.send_com("READ")
        response = self.listen_com()
        return { "logsplitter.vel": float(response) }

    @check_if_not_connected
    def disconnect(self):
        self.serial.close()
        self._connected = False
