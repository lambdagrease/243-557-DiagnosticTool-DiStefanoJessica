from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from src.models.sensor import Sensor


class SensorWidget(QGroupBox):

    def __init__(self, sensor: Sensor) -> None:
        super().__init__("Sensor")

        self.sensor = sensor

        self.name_label = QLabel(
            self.sensor.name
        )

        self.value_label = QLabel("---")

        self.read_button = QPushButton(
            "Automatic Update"
        )

        self.read_button.setEnabled(False)

        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setStyleSheet(
            """
            font-size: 30px;
            font-family: Billa Mount;
            font-weight: bold;
            padding: 10px;
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.read_button)

        self.setLayout(layout)

    def update_value(
        self,
        value: float,
    ) -> None:
        """Actualise la valeur affichée."""
        self.value_label.setText(
            f"{value:.1f} {self.sensor.unit}"
    )