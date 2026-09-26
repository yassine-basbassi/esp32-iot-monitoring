import sqlite3
from pathlib import Path


# ============================================================
# CHEMIN DE LA BASE DE DONNÉES
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "sensors.db"


# ============================================================
# CRÉATION DE LA BASE
# ============================================================

def create_database():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensor_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_id TEXT NOT NULL,

            temperature REAL NOT NULL,

            humidity REAL NOT NULL,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# INSERTION D'UNE MESURE
# ============================================================

def insert_sensor_data(
    device_id,
    temperature,
    humidity
):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sensor_data
        (
            device_id,
            temperature,
            humidity
        )

        VALUES (?, ?, ?)
        """,
        (
            device_id,
            temperature,
            humidity
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# LECTURE DES DERNIÈRES DONNÉES
# ============================================================

def get_latest_data(limit=10):

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            device_id,
            temperature,
            humidity,
            timestamp

        FROM sensor_data

        ORDER BY id DESC

        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# TEST DIRECT
# ============================================================

if __name__ == "__main__":

    create_database()

    print(
        "Base de données créée :"
    )

    print(
        DATABASE_PATH
    )