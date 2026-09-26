import sys
from pathlib import Path

# Ajouter la racine du projet au PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)


from backend.database import (
    create_database,
    insert_sensor_data,
    get_latest_data,
)


def test_create_database():

    create_database()

    rows = get_latest_data(1)

    assert isinstance(rows, list)


def test_insert_sensor_data():

    create_database()

    insert_sensor_data(
        "TEST_DEVICE",
        25.5,
        50.0
    )

    rows = get_latest_data(1)

    assert len(rows) >= 1

    latest = rows[0]

    assert latest[1] == "TEST_DEVICE"
    assert latest[2] == 25.5
    assert latest[3] == 50.0