# ESP32 IoT Monitoring

Plateforme de monitoring IoT basée sur ESP32, MQTT, Python, SQLite et Data Science.

Le projet permet de collecter des données de température et d'humidité, de les transmettre via MQTT, de les stocker dans SQLite, de les analyser avec Pandas/NumPy et de les visualiser dans un dashboard Streamlit.

---

## Architecture

```text
DHT22 / Simulation
        │
        ▼
      ESP32
        │
        │ Wi-Fi
        ▼
      MQTT
        │
        ▼
Python MQTT Subscriber
        │
        ▼
     SQLite
        │
        ├───────────────┐
        ▼               ▼
 Pandas / NumPy     Streamlit
        │               │
        ▼               ▼
   Data Analysis    Dashboard
```

---

## Fonctionnalités

* Lecture et acquisition de données de température et d'humidité
* Simulation du système ESP32 avec Wokwi
* Connexion Wi-Fi
* Communication MQTT
* Réception et traitement des données avec Python
* Stockage des données dans SQLite
* Analyse statistique avec Pandas et NumPy
* Détection de règles d'anomalies
* Visualisation des données avec Matplotlib
* Dashboard interactif avec Streamlit et Plotly
* Tests automatisés avec Pytest

---

## Technologies utilisées

### IoT & Systèmes embarqués

* ESP32
* DHT22
* Wokwi
* Wi-Fi
* MQTT

### Backend & Base de données

* Python
* Paho MQTT
* SQLite

### Data Science

* Pandas
* NumPy
* Matplotlib

### Dashboard & Visualisation

* Streamlit
* Plotly

### Tests

* Pytest

### Version Control

* Git
* GitHub

---

## Structure du projet

```text
01-esp32-iot-monitoring/
│
├── firmware/
│   ├── diagram.json
│   ├── wokwi.toml
│   └── main.py
│
├── backend/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   └── mqtt_subscriber.py
│
├── data/
│   └── .gitkeep
│
├── analysis/
│   ├── data_analysis.py
│   └── plots/
│
├── dashboard/
│   └── app.py
│
├── docs/
│   └── screenshots/
│
├── tests/
│   └── test_database.py
│
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Installation

### 1. Cloner le repository

```bash
git clone https://github.com/yassine-basbassi/01-esp32-iot-monitoring.git
```

### 2. Entrer dans le projet

```bash
cd 01-esp32-iot-monitoring
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## Lancer le système IoT

Le firmware ESP32 est simulé avec Wokwi.

Le système utilise :

```text
ESP32 → Wi-Fi → MQTT → Python → SQLite
```

Topic MQTT :

```text
iot/esp32/001/sensors
```

### Backend MQTT

Lancer le subscriber Python :

```bash
python backend/mqtt_subscriber.py
```

Le programme se connecte au broker MQTT et attend les données provenant de l'ESP32.

---

## Analyse des données

Lancer :

```bash
python analysis/data_analysis.py
```

Le programme calcule notamment :

* Minimum
* Maximum
* Moyenne
* Écart-type
* Nombre d'anomalies

Les graphiques sont générés dans :

```text
analysis/plots/
```

---

## Dashboard

Lancer Streamlit :

```bash
streamlit run dashboard/app.py
```

Puis ouvrir :

```text
http://localhost:8501
```

Le dashboard affiche :

* Nombre de mesures
* Température moyenne
* Humidité moyenne
* Nombre d'anomalies
* Évolution de la température
* Évolution de l'humidité
* Dernières mesures

---

## Tests

Exécuter :

```bash
pytest
```

Les tests vérifient notamment :

* Création de la base SQLite
* Insertion des données
* Récupération des données

---

## Détection d'anomalies

Une mesure est actuellement considérée comme anormale lorsque :

```text
Température > 35 °C
```

ou :

```text
Humidité < 20 %
```

Cette logique constitue une première étape avant l'intégration future de méthodes de Machine Learning.

---

## Évolutions prévues

Le projet peut évoluer vers une architecture AIoT plus avancée :

* PostgreSQL
* FastAPI
* Docker
* Grafana
* Cloud IoT
* Machine Learning
* Isolation Forest
* Random Forest
* XGBoost
* Prédiction de température
* Détection automatique d'anomalies
* Gestion de plusieurs ESP32

---

## Objectif

Ce projet a été développé comme projet portfolio dans le domaine :

**IoT + Data Science + AIoT**

Il démontre l'intégration entre systèmes embarqués, communication IoT, backend Python, bases de données, analyse de données et visualisation.

---

## Auteur

**Yassine Basbassi**

GitHub :

https://github.com/yassine-basbassi
