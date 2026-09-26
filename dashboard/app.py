import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = (
    BASE_DIR
    / "data"
    / "sensors.db"
)


# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ESP32 IoT Monitoring",
    page_icon="🌐",
    layout="wide"
)


# ============================================================
# TITRE
# ============================================================

st.title(
    "🌐 ESP32 IoT Monitoring"
)

st.write(
    "Plateforme de supervision des données "
    "IoT avec ESP32, MQTT, SQLite et Data Science."
)


# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================

@st.cache_data(ttl=5)
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

    if not dataframe.empty:

        dataframe["timestamp"] = pd.to_datetime(
            dataframe["timestamp"]
        )

    return dataframe


dataframe = load_data()


# ============================================================
# VÉRIFICATION
# ============================================================

if dataframe.empty:

    st.warning(
        "Aucune donnée disponible dans SQLite."
    )

    st.stop()


# ============================================================
# ANOMALIES
# ============================================================

dataframe["anomaly"] = (
    (dataframe["temperature"] > 35)
    |
    (dataframe["humidity"] < 20)
)


# ============================================================
# KPI
# ============================================================

total_measurements = len(
    dataframe
)

average_temperature = dataframe[
    "temperature"
].mean()

average_humidity = dataframe[
    "humidity"
].mean()

anomalies = dataframe[
    "anomaly"
].sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📊 Mesures",
        total_measurements
    )


with col2:

    st.metric(
        "🌡️ Température moyenne",
        f"{average_temperature:.1f} °C"
    )


with col3:

    st.metric(
        "💧 Humidité moyenne",
        f"{average_humidity:.1f} %"
    )


with col4:

    st.metric(
        "⚠️ Anomalies",
        anomalies
    )


# ============================================================
# SÉPARATEUR
# ============================================================

st.divider()


# ============================================================
# GRAPHIQUE TEMPÉRATURE
# ============================================================

st.subheader(
    "🌡️ Évolution de la température"
)


temperature_chart = px.line(
    dataframe,
    x="timestamp",
    y="temperature",
    markers=True,
    labels={
        "timestamp": "Temps",
        "temperature": "Température (°C)"
    }
)


temperature_chart.add_hline(
    y=35,
    line_dash="dash",
    annotation_text="Seuil anomalie"
)


st.plotly_chart(
    temperature_chart,
    use_container_width=True
)


# ============================================================
# GRAPHIQUE HUMIDITÉ
# ============================================================

st.subheader(
    "💧 Évolution de l'humidité"
)


humidity_chart = px.line(
    dataframe,
    x="timestamp",
    y="humidity",
    markers=True,
    labels={
        "timestamp": "Temps",
        "humidity": "Humidité (%)"
    }
)


humidity_chart.add_hline(
    y=20,
    line_dash="dash",
    annotation_text="Seuil anomalie"
)


st.plotly_chart(
    humidity_chart,
    use_container_width=True
)


# ============================================================
# DONNÉES
# ============================================================

st.subheader(
    "📋 Dernières mesures"
)


display_data = dataframe.sort_values(
    "timestamp",
    ascending=False
).head(20)


st.dataframe(
    display_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# INFORMATIONS SYSTÈME
# ============================================================

st.divider()

st.subheader(
    "ℹ️ Informations système"
)


info_col1, info_col2 = st.columns(2)


with info_col1:

    st.write(
        "**Device :**",
        dataframe["device_id"].iloc[-1]
    )

    st.write(
        "**Nombre total de mesures :**",
        len(dataframe)
    )


with info_col2:

    st.write(
        "**Dernière mesure :**",
        dataframe["timestamp"].max()
    )

    st.write(
        "**Anomalies détectées :**",
        int(anomalies)
    )


# ============================================================
# ACTUALISATION
# ============================================================

st.sidebar.title(
    "⚙️ Configuration"
)

st.sidebar.write(
    "ESP32 IoT Monitoring"
)

st.sidebar.write(
    "MQTT → SQLite → Streamlit"
)

if st.sidebar.button(
    "🔄 Actualiser les données"
):

    st.cache_data.clear()

    st.rerun()