from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QGroupBox,
)

# IMPORTS

from src.models.sensor import Sensor
from src.models.actuator import Actuator
from src.controllers.system_controller import SystemController
from src.controllers.system_controller import SystemState
from src.hardware.simulation_hardware import SimulationHardware
from src.views.sensor_widget import SensorWidget

# MAIN WINDOW

class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("243-557 — DiagnosticTool")

        self.resize(360, 220)

        self.hardware = SimulationHardware()

        self.sensor = Sensor(
            "Distance",
            "cm",
            self.hardware,
        )

        self.actuator = Actuator(
            "Diagnostics LED",
            self.hardware,
        )

        self.controller = SystemController(
            self.sensor,
            self.actuator,
        )

        self.title_label = QLabel("Logiciel de diagnostic - Jessica Di Stefano")
        self.sensor_name_label = QLabel(
            f"Capteur : {self.sensor.name}"
        )

        self.sensor_value_label = QLabel("Value : ---")

        self.actuator_name_label = QLabel(
            f"LED : {self.actuator.name}"
        )

        self.system_state_label = QLabel("System State : STOPPED")
        self.actuator_state_label = QLabel("State : OFF")

        self.read_button = QPushButton("Read Sensor")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.reset_button = QPushButton("Reset")

    # QAPPLICATION WINDOW LAYOUTS

        capteur_group = QGroupBox("Sensor")
        capteur_layout = QVBoxLayout()
        capteur_layout.addWidget(self.sensor_name_label)
        capteur_layout.addWidget(self.sensor_value_label)
        capteur_layout.addWidget(self.read_button)
        capteur_group.setLayout(capteur_layout)

        led_group = QGroupBox("LED")
        led_layout = QVBoxLayout()
        led_layout.addWidget(self.actuator_name_label)
        led_layout.addWidget(self.actuator_state_label)
        led_layout.addWidget(self.system_state_label)
        led_layout.addWidget(self.start_button)
        led_layout.addWidget(self.stop_button)
        led_layout.addWidget(self.reset_button)
        led_group.setLayout(led_layout)

        layout = QVBoxLayout()
        layout.addWidget(self.title_label)
        layout.addWidget(capteur_group)
        layout.addWidget(led_group)

        self.setLayout(layout)

    # BUTTON CLICK UPDATES

        self.read_button.clicked.connect(self.read_sensor)
        self.start_button.clicked.connect(self.start_system)
        self.stop_button.clicked.connect(self.stop_system)
        self.reset_button.clicked.connect(self.reset_system)

    # READ SENSOR 

    def read_sensor(self) -> None:
        value = self.sensor.read()
        self.sensor_value_label.setText(
            f"Value : {value} {self.sensor.unit}"
        )
        self.controller.alarm_system(value)
        self.update_actuator_state_label()
        self.update_system_state_label()

    # UPDATE SYSTEM STATE LABEL METHODS

    def update_actuator_state_label(self) -> None:
        if self.actuator.state:
            self.actuator_state_label.setText(
                "State : ON")
        else:
                self.actuator_state_label.setText(
                "State : OFF")  

    def update_system_state_label(self) -> None:
        self.system_state_label.setText(
            f"System State : {self.controller.get_state().value}"
        )


    # UPDATE SYSTEM STATE VIEW METHODS

    def start_system(self) -> None:
        self.controller.start_system()
        self.update_system_state_label()    

    def stop_system(self) -> None:
        self.controller.stop_system()
        self.update_system_state_label()

    def reset_system(self) -> None:
        self.controller.reset_system()
        self.update_system_state_label()
        self.update_actuator_state_label() 

