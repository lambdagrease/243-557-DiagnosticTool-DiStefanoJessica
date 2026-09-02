class Actuator:
    def __init__(
        self,
        name: str,
    ) -> None:
        self.name = name
        self.state = False

    def state_on(self) -> None:
        self.state = True

    def state_off(self) -> None:
        self.state = False

    def state_invert(self) -> None:
        self.state = not self.state