from .config_logsplitter_leader import LogsplitterLeaderConfig
from .logsplitter_switches import LogsplitterSwitches

import logging
logger = logging.getLogger(__name__)

from lerobot.teleoperators.so_leader import SOLeader

from lerobot.utils.decorators import check_if_already_connected, check_if_not_connected

class LogsplitterLeader(SOLeader):
    name = "logsplitter_leader"
    
    def __init__(self, config: LogsplitterLeaderConfig):
        super().__init__(config)

        self.accessory = LogsplitterSwitches(
            port=self.config.logsplitter_switches_port
        )
        return
    
    @property
    def action_features(self) -> dict[str, type]:
        return { 
            **super().action_features, 
            **self.accessory.action_features()
        }
    
    def connect(self, calibrate: bool = True) -> None:
        super().connect(calibrate=calibrate)
        self.accessory.connect()
        logger.info(f"{self.name} Connected")
        return
     
    def get_action(self) -> dict[str: float]:
        return {
            **super().get_action(),
            **self.accessory.get_action()
        }
    
    # @property
    # def is_connected(self) -> bool:
    #     return super().is_connected and self.accessory.is_connected
    
    def disconnect(self) -> None:
        super().disconnect();
        self.accessory.disconnect();
        return
