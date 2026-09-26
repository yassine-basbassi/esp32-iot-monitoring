import network
import time
import dht
import machine
import ujson
import random
from umqtt.simple import MQTTClient


# ============================================================
# CONFIGURATION
# ============================================================

WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

MQTT_SERVER = "test.mosquitto.org"
MQTT_PORT = 1883

MQTT_TOPIC = b"iot/esp32/001/sensors"

DEVICE_ID = "ESP32_001"


# ============================================================
# GPIO
# ============================================================

DHT_PIN = 15

LED_GREEN_PIN = 4
LED_RED_PIN = 16


# ============================================================
# SEUILS
# ============================================================

MAX_NORMAL_TEMPERATURE = 35.0
MIN_NORMAL_HUMIDITY = 20.0


# ============================================================
# OBJETS
# ============================================================

dht_sensor = dht.DHT22(
    machine.Pin(DHT_PIN)
)

led_green = machine.Pin(
    LED_GREEN_PIN,
    machine.Pin.OUT
)

led_red = machine.Pin(
    LED_RED_PIN,
    machine.Pin.OUT
)


# ============================================================
# WIFI
# ============================================================

def connect_wifi():

    print()
    print("Connexion au Wi-Fi...")

    wlan = network.WLAN(
        network.STA_IF
    )

    wlan.active(True)

    wlan.connect(
        WIFI_SSID,
        WIFI_PASSWORD
    )

    while not wlan.isconnected():

        print(".", end="")

        time.sleep(0.5)

    print()
    print("Wi-Fi connecte.")

    print(
        "Adresse IP :",
        wlan.ifconfig()[0]
    )


# ============================================================
# MQTT
# ============================================================

def connect_mqtt():

    print(
        "Connexion au broker MQTT..."
    )

    client = MQTTClient(
        DEVICE_ID,
        MQTT_SERVER,
        port=MQTT_PORT
    )

    client.connect()

    print(
        "MQTT connecte."
    )

    return client


# ============================================================
# LEDS
# ============================================================

def update_leds(
    temperature,
    humidity
):

    anomaly = False

    if temperature > MAX_NORMAL_TEMPERATURE:
        anomaly = True

    if humidity < MIN_NORMAL_HUMIDITY:
        anomaly = True


    if anomaly:

        led_green.value(0)
        led_red.value(1)

        print(
            "Etat : ANOMALIE"
        )

    else:

        led_green.value(1)
        led_red.value(0)

        print(
            "Etat : NORMAL"
        )


# ============================================================
# GENERATION DE DONNEES SIMULEES
# ============================================================

def generate_sensor_data():

    # Temperature entre 20 et 38 °C
    temperature = random.uniform(
        20.0,
        38.0
    )

    # Humidite entre 30 et 70 %
    humidity = random.uniform(
        30.0,
        70.0
    )

    return (
        round(temperature, 1),
        round(humidity, 1)
    )


# ============================================================
# MQTT
# ============================================================

def publish_data(
    mqtt_client,
    temperature,
    humidity
):

    data = {

        "device_id": DEVICE_ID,

        "temperature": temperature,

        "humidity": humidity
    }


    payload = ujson.dumps(
        data
    )


    print(
        "MQTT ->",
        payload
    )


    mqtt_client.publish(
        MQTT_TOPIC,
        payload
    )


    print(
        "Message MQTT publie."
    )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

print()
print(
    "======================================"
)

print(
    "       ESP32 IoT Monitoring"
)

print(
    "======================================"
)


led_green.value(0)
led_red.value(0)


# Wi-Fi

connect_wifi()


# MQTT

mqtt_client = connect_mqtt()


print()
print(
    "Systeme pret."
)


# ============================================================
# BOUCLE PRINCIPALE
# ============================================================

while True:

    try:

        # ----------------------------------------------------
        # Simulation des capteurs
        # ----------------------------------------------------

        temperature, humidity = (
            generate_sensor_data()
        )


        # ----------------------------------------------------
        # Affichage
        # ----------------------------------------------------

        print()
        print(
            "--------------------------------------"
        )


        print(
            "Temperature :",
            temperature,
            "C"
        )


        print(
            "Humidite    :",
            humidity,
            "%"
        )


        # ----------------------------------------------------
        # LEDs
        # ----------------------------------------------------

        update_leds(
            temperature,
            humidity
        )


        # ----------------------------------------------------
        # MQTT
        # ----------------------------------------------------

        publish_data(
            mqtt_client,
            temperature,
            humidity
        )


    except Exception as error:

        print(
            "Erreur :",
            error
        )


    time.sleep(5)