import sqlite3
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "data" / "sensors.db"

PLOTS_DIR = BASE_DIR / "analysis" / "plots"

PLOTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

def load_data():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    query = """
        SELECT
            id,
            device_id,
            temperature,
            humidity,
            timestamp
        FROM sensor_data
        ORDER BY timestamp
    """

    dataframe = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    return dataframe


# ============================================================
# ANALYSE
# ============================================================

def analyze_data(dataframe):

    if dataframe.empty:

        print("Aucune donnée disponible.")

        return

    dataframe["timestamp"] = pd.to_datetime(
        dataframe["timestamp"]
    )

    # --------------------------------------------------------
    # Statistiques température
    # --------------------------------------------------------

    temperature_array = np.array(
        dataframe["temperature"]
    )

    humidity_array = np.array(
        dataframe["humidity"]
    )

    print()
    print("======================================")
    print("        ANALYSE DES DONNÉES IoT")
    print("======================================")

    print()
    print("Nombre de mesures :")
    print(
        len(dataframe)
    )

    print()
    print("Appareils :")
    print(
        dataframe["device_id"].unique()
    )

    print()
    print("--------------------------------------")
    print("TEMPÉRATURE")
    print("--------------------------------------")

    print(
        "Minimum :",
        dataframe["temperature"].min(),
        "°C"
    )

    print(
        "Maximum :",
        dataframe["temperature"].max(),
        "°C"
    )

    print(
        "Moyenne :",
        round(
            dataframe["temperature"].mean(),
            2
        ),
        "°C"
    )

    print(
        "Écart-type :",
        round(
            np.std(temperature_array),
            2
        )
    )

    print()
    print("--------------------------------------")
    print("HUMIDITÉ")
    print("--------------------------------------")

    print(
        "Minimum :",
        dataframe["humidity"].min(),
        "%"
    )

    print(
        "Maximum :",
        dataframe["humidity"].max(),
        "%"
    )

    print(
        "Moyenne :",
        round(
            dataframe["humidity"].mean(),
            2
        ),
        "%"
    )

    print(
        "Écart-type :",
        round(
            np.std(humidity_array),
            2
        )
    )

    # --------------------------------------------------------
    # Détection des anomalies
    # --------------------------------------------------------

    dataframe["anomaly"] = (
        (dataframe["temperature"] > 35)
        |
        (dataframe["humidity"] < 20)
    )

    anomaly_count = int(
        dataframe["anomaly"].sum()
    )

    print()
    print("--------------------------------------")
    print("ANOMALIES")
    print("--------------------------------------")

    print(
        "Nombre d'anomalies :",
        anomaly_count
    )

    print(
        "Pourcentage :",
        round(
            anomaly_count
            / len(dataframe)
            * 100,
            2
        ),
        "%"
    )

    # --------------------------------------------------------
    # Dernières mesures
    # --------------------------------------------------------

    print()
    print("--------------------------------------")
    print("DERNIÈRES MESURES")
    print("--------------------------------------")

    print(
        dataframe.tail(10).to_string(
            index=False
        )
    )

    return dataframe


# ============================================================
# GRAPHIQUE TEMPÉRATURE
# ============================================================

def create_temperature_plot(dataframe):

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        dataframe["timestamp"],
        dataframe["temperature"],
        marker="o"
    )

    plt.axhline(
        y=35,
        linestyle="--",
        label="Seuil anomalie"
    )

    plt.title(
        "Évolution de la température"
    )

    plt.xlabel(
        "Temps"
    )

    plt.ylabel(
        "Température (°C)"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    output = (
        PLOTS_DIR
        / "temperature.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()

    print()
    print(
        "Graphique température :",
        output
    )


# ============================================================
# GRAPHIQUE HUMIDITÉ
# ============================================================

def create_humidity_plot(dataframe):

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        dataframe["timestamp"],
        dataframe["humidity"],
        marker="o"
    )

    plt.axhline(
        y=20,
        linestyle="--",
        label="Seuil anomalie"
    )

    plt.title(
        "Évolution de l'humidité"
    )

    plt.xlabel(
        "Temps"
    )

    plt.ylabel(
        "Humidité (%)"
    )

    plt.xticks(
        rotation=45
    )

    plt.legend()

    plt.tight_layout()

    output = (
        PLOTS_DIR
        / "humidity.png"
    )

    plt.savefig(
        output,
        dpi=150
    )

    plt.close()

    print()
    print(
        "Graphique humidité :",
        output
    )


# ============================================================
# GRAPHIQUE TEMPÉRATURE + HUMIDITÉ
# ============================================================

def create_combined_plot(dataframe):

    figure, axis1 = plt.subplots(
        figsize=(10, 5)
    )

    axis1.plot(
        dataframe["timestamp"],
        dataframe["temperature"],
        marker="o",
        label="Température"
    )

    axis1.set_xlabel(
        "Temps"
    )

    axis1.set_ylabel(
        "Température (°C)"
    )

    axis2 = axis1.twinx()

    axis2.plot(
        dataframe["timestamp"],
        dataframe["humidity"],
        marker="s",
        label="Humidité"
    )

    axis2.set_ylabel(
        "Humidité (%)"
    )

    figure.suptitle(
        "Monitoring IoT ESP32"
    )

    figure.tight_layout()

    output = (
        PLOTS_DIR
        / "monitoring.png"
    )

    figure.savefig(
        output,
        dpi=150
    )

    plt.close(
        figure
    )

    print()
    print(
        "Graphique monitoring :",
        output
    )


# ============================================================
# PROGRAMME PRINCIPAL
# ============================================================

if __name__ == "__main__":

    dataframe = load_data()

    dataframe = analyze_data(
        dataframe
    )

    if dataframe is not None:

        create_temperature_plot(
            dataframe
        )

        create_humidity_plot(
            dataframe
        )

        create_combined_plot(
            dataframe
        )

        print()
        print(
            "======================================"
        )

        print(
            "Analyse terminée."
        )

        print(
            "Les graphiques sont dans :"
        )

        print(
            PLOTS_DIR
        )