# from lerobot.robots.robot import Robot
from lerobot.robots.so_follower import SOFollower
from lerobot.processor import RobotObservation
from lerobot.processor import RobotAction
# from lerobot.utils.decorators import check_if_already_connected, check_if_not_connected

from .config_logsplitter_follower import LogsplitterFollowerConfig
from .logsplitter_motor import LogsplitterMotor

import logging
logger = logging.getLogger(__name__)

class LogsplitterFollower(SOFollower):
    config_class = LogsplitterFollowerConfig
    name = "logsplitter_follower"

    def __init__(self, config: LogsplitterFollowerConfig):
        super().__init__(config)
        self.accessory = LogsplitterMotor(
            port=self.config.logsplitter_motor_port
        )
    
    @property
    def observation_features(self) -> dict[str, type | tuple]:
        return {
            **super().observation_features,
            **self.accessory.observation_features
        }
    
    @property
    def action_features(self) -> dict[str, type]:
        return {
            **super().action_features,
            **self.accessory.action_features
        }

    @property
    def is_connected(self) -> bool:
        return super().is_connected and self.accessory.is_connected
    
    def connect(self, calibrate: bool = True) -> None:
        super().connect(calibrate=calibrate)

        logger.info(f"connecting to {self.accessory}")
        self.accessory.connect()
        return
    
    def get_observation(self) -> RobotObservation:
        return {
            **super().get_observation(),
            **self.accessory.get_observation()
        }
    
    def send_action(self, action: RobotAction) -> RobotAction:
        super().send_action(action)
        self.accessory.send_action(action)
        return
    
    def disconnect(self) -> None:
        super().disconnect()
        self.accessory.disconnect()
        logger.info(f"{self} disconnected.")
        return
