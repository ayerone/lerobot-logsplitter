from dataclasses import dataclass
from lerobot.teleoperators.config import TeleoperatorConfig

@TeleoperatorConfig.register_subclass("logsplitter_leader")
@dataclass
class LogsplitterLeaderConfig(TeleoperatorConfig):
    # Port to connect to the arm
    port: str

    # extra port for teleop inputs to control logsplitter
    logsplitter_switches_port: str

    # Whether to use degrees for angles
    use_degrees: bool = False
