from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from src.hardware.simulation_hardware import (
    SimulationHardware,
)
from src.models.actuator import Actuator
from src.models.sensor import Sensor
from src.views.actuator_widget import ActuatorWidget
from src.views.sensor_widget import SensorWidget


class MainWindow(QWidget):
    """Fenêtre principale du logiciel de diagnostic."""

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle(
            "243-557 — DiagnosticTool"
        )

        self.resize(800, 450)

        self.title_label = QLabel(
            "Diagnostic Program"
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title_label.setStyleSheet(
            """
            font-size: 80px;
            font-weight: bold;
            """
        )

        self.hardware = SimulationHardware()

        # OBJECT CREATION
  
        self.distance_sensor = Sensor(      # DISTANCE SENSOR
            "Distance",
            "cm",
            self.hardware,
        )

        self.diagnostic_actuator = Actuator(        # LED ACTUATOR
            "Diagnostic LED",
            self.hardware,
        )

        # WIDGET CREATION

        self.distance_widget = SensorWidget(
            self.distance_sensor
        )

        self.actuator_widget = ActuatorWidget(
            self.diagnostic_actuator
        )

        # BOX LAYOUT

        layouth = QHBoxLayout()
        layouth.addWidget(self.actuator_widget)
        layouth.addWidget(self.distance_widget)
        layouth.setSpacing(20)
        # À compléter :
        # 1. Créer un QHBoxLayout.
        # 2. Ajouter les deux composants.
        # 3. Définir un espacement visible.
        layoutv = QVBoxLayout()
        layoutv.addWidget(self.title_label)
        layoutv.addLayout(layouth)
        layoutv.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layoutv)
        # À compléter :
        # 1. Créer un QVBoxLayout.
        # 2. Ajouter le titre.
        # 3. Ajouter le layout horizontal.
        # 4. Définir les marges.
        # 5. Associer le layout principal
        #    à MainWindow.
