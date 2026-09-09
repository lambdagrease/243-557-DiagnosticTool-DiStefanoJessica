from src.hardware.simulation_hardware import SimulationHardware

class Actuator:
    def __init__(
        self,
        name: str,
        hardware: SimulationHardware,
    ) -> None:
        self.name = name
        self.hardware = hardware
        self.state = False

    def state_on(self) -> None:
        self.state = True
        self.hardware.set_actuator(
            self.name,
            is_active = True
        )

    def state_off(self) -> None:
        self.state = False
        self.hardware.set_actuator(
            self.name,
            is_active = False
        )

    def state_invert(self) -> None:
        self.state = not self.state