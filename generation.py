import csv
import numpy as np
from datetime import datetime, timedelta

# =====================================================
# PHYSICS-INFORMED SYNTHETIC DATASET GENERATOR
# Для статті з контролю якості обліку природного газу
# =====================================================

np.random.seed(42)


def generate_physics_informed_data(days=14):
    """
    Генерує фізично осмислений synthetic dataset.

    Сценарії:
    1. Нормальна робота
    2. Drift сенсора
    3. Leakage
    4. Spike anomaly
    5. Desynchronization
    """

    rows = []

    start = datetime(2026, 5, 1)
    total_minutes = days * 24 * 60

    models = [
        "IsolationForest",
        "DBSCAN",
        "Autoencoder",
        "Kalman",
        "DoubleControl"
    ]

    for i in range(total_minutes):

        timestamp = start + timedelta(minutes=i)

        # =========================================
        # 1. БАЗОВИЙ ДОБОВИЙ ПРОФІЛЬ СПОЖИВАННЯ
        # =========================================

        hour = timestamp.hour

        base_flow = (
            240
            + 25 * np.sin(2 * np.pi * hour / 24)
            + np.random.normal(0, 2)
        )

        pressure = 412 - 0.03 * base_flow + np.random.normal(0, 0.8)
        temp = 15 + 8 * np.sin(2 * np.pi * hour / 24)

        anomaly = 0
        anomaly_type = "normal"

        # =========================================
        # 2. DRIFT
        # =========================================
        if 3000 <= i <= 4000:
            base_flow += 0.02 * (i - 3000)
            anomaly = 1
            anomaly_type = "drift"

        # =========================================
        # 3. LEAKAGE
        # =========================================
        if 7000 <= i <= 7300:
            base_flow -= 18
            anomaly = 1
            anomaly_type = "leakage"

        # =========================================
        # 4. SPIKES
        # =========================================
        if np.random.rand() < 0.002:
            base_flow += np.random.uniform(25, 50)
            anomaly = 1
            anomaly_type = "spike"

        # =========================================
        # 5. DESYNC
        # =========================================
        if 11000 <= i <= 11300:
            pressure += 8
            anomaly = 1
            anomaly_type = "desync"

        flow = round(base_flow, 2)

        volume = 10452 + i * flow / 60
        std_volume = volume * 0.94

        # =========================================
        # БАЛАНСОВА НЕВ'ЯЗКА
        # =========================================

        if anomaly_type == "normal":
            balance_error = np.random.normal(0, 0.15)
        elif anomaly_type == "drift":
            balance_error = np.random.normal(1.2, 0.4)
        elif anomaly_type == "leakage":
            balance_error = np.random.normal(4.5, 0.7)
        elif anomaly_type == "spike":
            balance_error = np.random.normal(3.2, 0.8)
        else:
            balance_error = np.random.normal(2.4, 0.5)

        # =========================================
        # ІМІТАЦІЯ РОБОТИ МОДЕЛЕЙ
        # =========================================

        for model in models:

            if model == "DoubleControl":
                score = min(1, max(0, abs(balance_error)/5 + np.random.normal(0,0.05)))

            elif model == "Kalman":
                score = min(1, max(0, abs(balance_error)/6 + np.random.normal(0,0.08)))

            elif model == "IsolationForest":
                score = min(1, max(0, abs(balance_error)/7 + np.random.normal(0,0.12)))

            elif model == "Autoencoder":
                score = min(1, max(0, abs(balance_error)/8 + np.random.normal(0,0.15)))

            else:
                score = min(1, max(0, abs(balance_error)/9 + np.random.normal(0,0.18)))

            pred = 1 if score > 0.5 else 0

            rows.append([
                timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                "S1",
                round(pressure, 2),
                round(temp, 2),
                flow,
                round(volume, 2),
                round(std_volume, 2),
                round(balance_error, 3),
                anomaly,
                model,
                anomaly,
                round(score, 3),
                pred
            ])

    return rows


def save_csv(rows, filename):

    headers = [
        "timestamp",
        "node_id",
        "pressure_kpa",
        "temp_c",
        "flow_m3h",
        "volume_m3",
        "std_volume_m3",
        "balance_error",
        "anomaly_label",
        "model",
        "y_true",
        "score",
        "pred"
    ]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


if __name__ == "__main__":
    data = generate_physics_informed_data(days=14)
    save_csv(data, "metrological_data.csv")
    print("Dataset generated.")