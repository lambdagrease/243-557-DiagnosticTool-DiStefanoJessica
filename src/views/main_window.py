from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QTextEdit,
)

from src.hardware.simulation_hardware import (
    SimulationHardware,
)
from src.models.actuator import Actuator
from src.models.sensor import Sensor
from src.views.actuator_widget import ActuatorWidget
from src.views.sensor_widget import SensorWidget
from src.mqtt_topics import MqttTopics
from src.network.mqtt_client import MqttClient


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

        self.connection_label = QLabel(
            "MQTT : déconnecté"
        )

        self.log_view = QTextEdit()

        self.log_view.setReadOnly(True)

        self.log_view.setPlaceholderText(
            "Journal des communications MQTT"
        )


        self.connection_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: darkred;
            color: white;
            """
        )

        self.hardware = SimulationHardware()

        # OBJECT CREATION
  
        self.distance_sensor = Sensor(      # DISTANCE SENSOR
            "Distance",
            "cm",
            self.hardware,
        )

        self.temperature_sensor = Sensor(
            "Temperature",
            "°C",
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
        self.distance_widget.setStyleSheet(
            """
            font-size: 30px;
            """
        ) 

        self.temperature_widget = SensorWidget(
            self.temperature_sensor
        )
        self.temperature_widget.setStyleSheet(
            """
            font-size: 30px;
            """
        ) 

        self.actuator_widget = ActuatorWidget(
            self.diagnostic_actuator
        )
        self.actuator_widget.setStyleSheet(
            """
            font-size: 30px;
            """
        )

        self.mqtt_client = MqttClient()

        self.mqtt_client.connected.connect(
            self.on_mqtt_connected
        )

        self.mqtt_client.disconnected.connect(
            self.on_mqtt_disconnected
        )

        self.mqtt_client.connection_failed.connect(
            self.on_mqtt_connection_failed
        )

        self.mqtt_client.message_received.connect(
            self.on_mqtt_message
        )

        self.actuator_widget.command_requested.connect(
            self.send_led_command
        )

        # BOX LAYOUT

        layouth = QHBoxLayout()
        layouth.addWidget(self.actuator_widget)
        layouth.addWidget(self.distance_widget)
        layouth.addWidget(self.temperature_widget)
        layouth.setSpacing(20)
        layoutv = QVBoxLayout()
        layoutv.addWidget(self.title_label)
        layoutv.addWidget(self.connection_label)
        layoutv.addLayout(layouth)
        layoutv.addWidget(self.log_view)
        layoutv.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layoutv)

        self.mqtt_client.connect_to_broker()

    
    def add_log(
        self,
        message: str,
    ) -> None:
        """Ajoute un message au journal."""
        self.log_view.append(message)

    def on_mqtt_connected(self) -> None:
        """Traite la connexion au broker."""

        self.connection_label.setText(
            "MQTT : connecté"
        )

        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: green;
            color: white;
            """
        )

        self.add_log(
            "Connexion au broker MQTT établie."
        )

        self.mqtt_client.subscribe(
            MqttTopics.sensor("distance")
        )

        self.mqtt_client.subscribe(
            MqttTopics.sensor("temperature")
        )

        self.mqtt_client.subscribe(
            MqttTopics.actuator("led")
        )

        self.mqtt_client.subscribe(
            MqttTopics.status()
        )

    def on_mqtt_disconnected(self) -> None:
        """Traite la déconnexion du broker."""

        self.connection_label.setText(
            "MQTT : déconnecté"
        )

        self.connection_label.setStyleSheet(
            """
            font-weight: bold;
            padding: 8px;
            background-color: darkred;
            color: white;
            """
        )

        self.add_log(
            "Connexion MQTT fermée."
        )

    def on_mqtt_connection_failed(
        self,
        reason: str,
    ) -> None:
        """Traite un échec de connexion."""

        self.add_log(
            f"Échec de connexion MQTT : {reason}"
        )

    def send_led_command(
        self,
        requested_state: bool,
    ) -> None:
        """Envoie une commande au Raspberry Pi."""

        payload = (
            "ON"
            if requested_state
            else "OFF"
        )

        self.mqtt_client.publish(
            MqttTopics.command("led"),
            payload,
        )

        self.add_log(
            f"Commande DEL envoyée : {payload}"
        )

    def on_mqtt_message(
        self,
        topic: str,
        payload: str,
    ) -> None:
        if topic == MqttTopics.sensor(
            "distance"
        ):
            value = float(payload)
            self.distance_widget.update_value(
                value
            )
            self.add_log(
                f"Distance reçue : {value:.1f} cm"
            )
        elif topic == MqttTopics.sensor(
            "temperature"
        ):
            value = float(payload)
            self.temperature_widget.update_value(
                value
            )
            self.add_log(
                f"Température reçue : {value:.1f} °C"
            )
        elif topic == MqttTopics.actuator(
            "led"
        ):
            is_active = payload == "ON"
            self.actuator_widget.set_state(
                is_active
            )
            self.add_log(
                f"État DEL reçu : {payload}"
            )
        elif topic == MqttTopics.status():
            self.add_log(
                f"État du service Raspberry : "
                f"{payload}"
            )

    def closeEvent(self, event) -> None:
        """Ferme proprement la connexion MQTT."""
        self.mqtt_client.disconnect_from_broker()
        event.accept()