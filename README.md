# LeRobot Logsplitter

**[YouTube Expo](https://youtu.be/pou4PEhgJao)**

Extending the hardware and code for the huggingface LeRobot SO-101; adding a (desktop-sized) log splitter and training it to operate autonomously via the ACT policy.

## Hardware

**Splitter**
- 4" travel linear actuator
- H-Bridge motor driver

**Arduinos**
- **Leader side:** Reads switches for up/down control (during teleoperation only), sends actions (commanded splitter velocity) to host computer running lerobot

I'm using a dual-throw switch with both arduino inputs configured as INPUT_PULLUP, so the switch is either open, or connecting one of the input pins to ground:

           ┌──── Pin 2
          /  ↑ up:    Pin 2 → GND (reads LOW)
  GND ───·   ─ center: open (both pins float HIGH)
          \  ↓ down:  Pin 3 → GND (reads LOW)
           └──── Pin 3

- **Follower side:** Receives actions (velocity commands) from host and drives the splitter motor accordingly

Here's the overall signal flow from switch handle to actuator (

```
Leader Switch    Leader Arduino Sends    logsplitter.vel (in LeRobot)    Follower Arduino Effects    Actuator Goes
─────────────    ────────────────────    ────────────────────────────    ────────────────────────    ─────────────
    Up        →         -50           →              -50              →        motor_b HIGH       →     Reverse
   Middle     →           0           →                0              →        both LOW           →     Off
   Down       →          50           →               50              →        motor_a HIGH       →     Forward
```

The follower has a dead-band: incoming commands in the range {-40, 40} leave the motor off. It turns out that the trained ACT policy produces pretty crisp actions for the logsplitter velocity that transition quickly at appropriate times between discrete values (roughly) -50, 0, and 50, as intended, and this can be seen in the evaluation episiodes recorded during policy rollout: [Visualize dataset](https://huggingface.co/spaces/lerobot/visualize_dataset?path=primordial-spork/eval_logsplitter_act_single_log_merged_all)

## Code

Both LogsplitterFollower and LogsplitterLeader inherit from LeRobot's SOFollower and SOLeader respectively. Rather than re-implementing arm logic, each method calls super() to get the base class result, then merges in a small contribution from the accessory. For example, get_observation() returns 
```python
{**super().get_observation(), **self.accessory.get_observation()}
```
i.e., the full arm observation dict with one extra key (logsplitter.vel) appended. The same pattern applies to action_features, observation_features, connect(), and disconnect().

Arduino sketches are in [`arduino/`](arduino/). 

## Packages

This project is installed as two packages so that LeRobot can discover each by its name prefix during register_third_party_plugins():

| Package | Role |
|---|---|
| `lerobot_teleoperator_logsplitter_leader` | Teleoperation — merges SO-101 leader with toggle switch input |
| `lerobot_robot_logsplitter_follower` | Robot — merges SO-101 follower with actuator control |

### Install

(In the venv you use for LeRobot)

```bash
pip install -e ./lerobot_teleoperator_logsplitter_leader
pip install -e ./lerobot_robot_logsplitter_follower
```

### Usage

To manually instantiate (with your LeRobot venv activated)

```python
from lerobot_teleoperator_logsplitter_leader import LogsplitterLeader, LogsplitterLeaderConfig
from lerobot_robot_logsplitter_follower import LogsplitterFollower, LogsplitterFollowerConfig

leader = LogsplitterLeader(LogsplitterLeaderConfig(
	id="my_logsplitter_leader",
    port="/dev/ttyUSB0",
    logsplitter_switches_port="/dev/ttyUSB1",
))

robot = LogsplitterFollower(LogsplitterFollowerConfig(
	id="my_logsplitter_follower"
    port="/dev/ttyUSB2",
    logsplitter_motor_port="/dev/ttyUSB3",
))
```

**If this is working, you should be able to use any lerobot- command line script with this new robot (lerobot-teleoperate, etc)**

Of course, you'll want to add your cameras as well before doing anything too fun.

## I Learned:

- **LeRobot Library Structure and Hardware Integration**
- **The importance of feature scaling:** At first, I had the teleop-side arduino sending 0 & 1 based on the switch state.  This resulted in **extremely** slow progress during policy training (loss was decreasing slower than molasses). The realization that came was that the logsplitter.vel feature should have about the same range as the other robot joints, which are scaled from -100 to 100 in the LeRobot code. Changing logsplitter.vel to range from -50 to 50 immediately fixed my slow training convergence problem.
- **Test material:** I tried _many_ materials for viable "logs". Zucchini work best ;) (see video)
