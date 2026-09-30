from PyQt6.QtCore import(
    Qt,
    pyqtSignal,
)
from PyQt6.QtWidgets import (
    QGroupBox,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from src.models.actuator import Actuator


class ActuatorWidget(QGroupBox):
    """Composant graphique représentant un actionneur."""

    command_requested = pyqtSignal(bool)

    def __init__(
        self,
        actuator: Actuator,
    ) -> None:
        super().__init__("Actionneur")

        self.actuator = actuator

        self.name_label = QLabel(
            self.actuator.name
        )

        self.state_label = QLabel()

        self.toggle_button = QPushButton()

        self.name_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.state_label)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

        self.toggle_button.clicked.connect(
            self.toggle_actuator
        )

        self.update_display()

    def toggle_actuator(self) -> None:
        requested_state = not self.actuator.state
        self.command_requested.emit(
            requested_state
        )

    def set_state(
        self,
        is_active: bool,
    ) -> None:
        """Applique l'état confirmé par le système."""
        self.actuator.state = is_active
        self.update_display()

    def update_display(self) -> None:
        if self.actuator.state:
            self.state_label.setText("On")
            self.toggle_button.setText("Deactivate")
            self.state_label.setStyleSheet(
                """
                font-size: 24px;
                font-family: Billa Mount;
                font-weight: bold;
                padding: 10px;
                color: green;
                """
            )

        else:
            self.state_label.setText("Off")
            self.toggle_button.setText("Activate")
            self.state_label.setStyleSheet(
                """
                font-size: 24px;
                font-family: Billa Mount;
                font-weight: bold;
                padding: 10px;
                color: red;
                """
            )
