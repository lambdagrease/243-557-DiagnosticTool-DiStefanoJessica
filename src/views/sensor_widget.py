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
            "Read Sensor"
        )

        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value_label.setStyleSheet(
            """
            font-size: 24px;
            font-weight: bold;
            """
        )

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.read_button)

        self.setLayout(layout)

        self.read_button.clicked.connect(
            self.read_sensor
        )

    def read_sensor(self) -> None:
        value = self.sensor.read()
        self.value_label.setText(
            f"{value:.1f} {self.sensor.unit}"
        )
