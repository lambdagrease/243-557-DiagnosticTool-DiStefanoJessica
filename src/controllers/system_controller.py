from enum import Enum

from src.models.sensor import Sensor
from src.models.actuator import Actuator

class SystemState(Enum):
    STOPPED = "STOPPED"
    RUNNING = "RUNNING"
    ALARM = "ALARM"

class SystemController:
    def __init__(
        self,
        sensor: Sensor,
        actuator: Actuator,
    ) -> None:
        self.sensor = sensor
        self.actuator = actuator
        self.state = SystemState.STOPPED

    def start_system(self) -> None:
        if self.state == SystemState.STOPPED:
            self.state = SystemState.RUNNING

    def stop_system(self) -> None:
        if self.state == SystemState.RUNNING:
            self.state = SystemState.STOPPED

    def alarm_system(self) -> None:
        if self.state == SystemState.RUNNING:
            self.state = SystemState.ALARM

    def reset_system(self) -> None:
        if self.state == SystemState.ALARM:
            self.state = SystemState.STOPPED

    def get_state(self) -> SystemState:
        return self.state

