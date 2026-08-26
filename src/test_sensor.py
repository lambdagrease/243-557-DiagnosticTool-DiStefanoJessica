from sensor import Sensor


temperature_sensor = Sensor(
    "Température",
    "°C",
    22.5,
)

character_sensor = Sensor(
    "Minecraft Steve",
    "HP",
    20.0,
)

print(temperature_sensor.name)
print(temperature_sensor.read())
print(temperature_sensor.unit)

print(character_sensor.name)
print(character_sensor.read())
print(character_sensor.unit)