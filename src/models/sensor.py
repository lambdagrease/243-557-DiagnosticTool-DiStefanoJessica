from src.hardware.simulation_hardware import SimulationHardware

class Sensor:
    def __init__(
        self,
        name: str,
        unit: str,
        hardware: SimulationHardware,   # "voici l'objet qui sait obtenir la valeur"
    ) -> None:
        self.name = name
        self.unit = unit
        self.hardware = hardware

    def read(self) -> float:
        return self.hardware.read_sensor(self.name) # retour de la valeur
        