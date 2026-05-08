from dataclasses import dataclass, field

from lerobot.robots.config import RobotConfig
from lerobot.robots.so_follower.config_so_follower import SOFollowerRobotConfig
from lerobot.cameras import CameraConfig

@RobotConfig.register_subclass("logsplitter_follower")
@dataclass
class LogsplitterFollowerConfig(RobotConfig):
    # Port to connect to the arm
    port: str

    # extra port for logsplitter
    logsplitter_motor_port: str

    disable_torque_on_disconnect: bool = True

    # `max_relative_target` limits the magnitude of the relative positional target vector for safety purposes.
    # Set this to a positive scalar to have the same value for all motors, or a dictionary that maps motor
    # names to the max_relative_target value for that motor.
    max_relative_target: float | dict[str, float] | None = None

    # cameras
    cameras: dict[str, CameraConfig] = field(default_factory=dict)

    # Set to `True` for backward compatibility with previous policies/dataset
    use_degrees: bool = False
