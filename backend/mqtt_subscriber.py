import json
import paho.mqtt.client as mqtt

from config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_TOPIC
)

from database import (
    create_database,
    insert_sensor_data
)


# ============================================================
# INITIALISATION DATABASE
# ============================================================

create_database()

print(
    "Base de données SQLite prête."
)


# ============================================================
# CONNEXION MQTT
# ============================================================

def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties=None
):

    print()
    print(
        "======================================"
    )

    print(
        "       MQTT Python Subscriber"
    )

    print(
        "======================================"
    )


    if reason_code == 0:

        print(
            "Connexion MQTT réussie."
        )

        client.subscribe(
            MQTT_TOPIC
        )

        print(
            f"Abonnement au topic : {MQTT_TOPIC}"
        )

    else:

        print(
            f"Échec MQTT. Code : {reason_code}"
        )


# ============================================================
# RÉCEPTION DES MESSAGES
# ============================================================

def on_message(
    client,
    userdata,
    message
):

    print()
    print(
        "--------------------------------------"
    )

    print(
        "Topic :",
        message.topic
    )


    try:

        # ----------------------------------------------------
        # Décodage du message
        # ----------------------------------------------------

        payload = (
            message
            .payload
            .decode("utf-8")
        )


        # ----------------------------------------------------
        # JSON
        # ----------------------------------------------------

        data = json.loads(
            payload
        )


        # ----------------------------------------------------
        # Extraction
        # ----------------------------------------------------

        device_id = data["device_id"]

        temperature = data["temperature"]

        humidity = data["humidity"]


        # ----------------------------------------------------
        # Affichage
        # ----------------------------------------------------

        print(
            "Device ID    :",
            device_id
        )

        print(
            "Temperature  :",
            temperature,
            "°C"
        )

        print(
            "Humidite     :",
            humidity,
            "%"
        )


        # ----------------------------------------------------
        # SQLite
        # ----------------------------------------------------

        insert_sensor_data(
            device_id,
            temperature,
            humidity
        )


        print(
            "✓ Données enregistrées dans SQLite."
        )


    except json.JSONDecodeError:

        print(
            "Erreur : JSON invalide."
        )


    except KeyError as error:

        print(
            f"Champ manquant : {error}"
        )


    except Exception as error:

        print(
            f"Erreur : {error}"
        )


# ============================================================
# CLIENT MQTT
# ============================================================

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)


client.on_connect = on_connect

client.on_message = on_message


# ============================================================
# CONNEXION
# ============================================================

print(
    "Connexion au broker MQTT..."
)


client.connect(
    MQTT_BROKER,
    MQTT_PORT,
    60
)


# ============================================================
# BOUCLE
# ============================================================

print(
    "En attente des données ESP32..."
)

print(
    "Appuyez sur CTRL+C pour arrêter."
)


client.loop_forever()