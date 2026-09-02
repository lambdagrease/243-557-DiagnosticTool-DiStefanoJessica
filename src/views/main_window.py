from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)

from src.models.sensor import Sensor
from src.models.actuator import Actuator


class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")
        self.resize(360, 220)
        self.sensor = Sensor(
            "Distance",
            "cm",
            35.0,
        )
        self.actuator = Actuator(
            "LED de diagnostic"
        )

        self.title_label = QLabel("Logiciel de diagnostic - Jessica Di Stefano")
        self.sensor_name_label = QLabel(
            f"Capteur : {self.sensor.name}"
        )
        self.sensor_value_label = QLabel("Valeur : ---")

        self.actuator_name_label = QLabel(
            f"LED : {self.actuator.name}"
        )

        self.actuator_state_label = QLabel("State : OFF")

        self.read_button = QPushButton("Lire le capteur")
        self.actuator_button = QPushButton("Changer l'état de LED")

        capteur_group = QGroupBox("Capteur")
        capteur_layout = QVBoxLayout()
        capteur_layout.addWidget(self.sensor_name_label)
        capteur_layout.addWidget(self.sensor_value_label)
        capteur_layout.addWidget(self.read_button)
        capteur_group.setLayout(capteur_layout)

        led_group = QGroupBox("LED")
        led_layout = QVBoxLayout()
        led_layout.addWidget(self.actuator_name_label)
        led_layout.addWidget(self.actuator_state_label)
        led_layout.addWidget(self.actuator_button)
        led_group.setLayout(led_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(capteur_group)
        layout.addWidget(led_group)

        self.setLayout(layout)

        self.read_button.clicked.connect(self.read_sensor)
        self.actuator_button.clicked.connect(self.change_actuator_state)

    def read_sensor(self) -> None:
        value = self.sensor.read()
        """Simule la lecture d'un capteur de température."""
        self.sensor_value_label.setText(
            f"Valeur : {value} {self.sensor.unit}"
        )

    def change_actuator_state(self) -> None:
        self.actuator.state_invert()

        if self.actuator.state:
            self.actuator_state_label.setText("State: Actif")
        else:
            self.actuator_state_label.setText("State : Inactif")