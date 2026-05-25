# ============================================================
# PHYSICS-INFORMED ANOMALY BENCHMARK
# ============================================================
#
# РОЗШИРЕНИЙ КОД ДЛЯ:
#
# 1. Завантаження реальних даних витратоміра
# 2. Реконструкції односекундного сигналу
# 3. Ін'єкції фізично правдоподібних аномалій
# 4. Порівняння ML/physics-informed моделей
# 5. Формування таблиці результатів
# 6. Побудови ROC-графіків
# 7. Збереження результатів у папку data
#
# ============================================================
#
# ВАЖЛИВО:
#
# Код спеціально переписаний так,
# щоб уникнути помилок:
#
# ValueError:
# x and y must have same first dimension
#
# IndexError:
# index 300 is out of bounds
#
# ============================================================

# ============================================================
# ІМПОРТ БІБЛІОТЕК
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.interpolate import CubicSpline

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve
)

from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

from sklearn.neural_network import MLPRegressor

# ============================================================
# СТВОРЕННЯ ПАПОК
# ============================================================

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/plots", exist_ok=True)
os.makedirs("data/results", exist_ok=True)

# ============================================================
# ЗАВАНТАЖЕННЯ РЕАЛЬНИХ ДАНИХ
# ============================================================

print("\n======================================")
print("ЗАВАНТАЖЕННЯ РЕАЛЬНИХ ДАНИХ")
print("======================================")

# Завантаження CSV
df = pd.read_csv("data/raw/rec_date.csv")

# Видалення порожніх рядків
df = df.dropna()

# ============================================================
# ПЕРЕВІРКА НАЯВНОСТІ КОЛОНОК
# ============================================================

required_columns = ["time", "black"]

for col in required_columns:

    if col not in df.columns:

        raise Exception(
            f"У CSV відсутня колонка: {col}"
        )

# ============================================================
# ОТРИМАННЯ ДАНИХ
# ============================================================

time_real = df["time"].values.astype(float)

signal_real = df["black"].values.astype(float)

# ============================================================
# ВИРІВНЮВАННЯ РОЗМІРІВ МАСИВІВ
# ============================================================
#
# Саме тут була твоя помилка:
#
# x and y must have same first dimension
#
# Причина:
# time = 109
# black = 108
#
# Тому примусово вирівнюємо розміри.
#
# ============================================================

min_len = min(len(time_real), len(signal_real))

time_real = time_real[:min_len]

signal_real = signal_real[:min_len]

print(f"Кількість точок після вирівнювання: {min_len}")

# ============================================================
# СОРТУВАННЯ
# ============================================================

sort_idx = np.argsort(time_real)

time_real = time_real[sort_idx]

signal_real = signal_real[sort_idx]

# ============================================================
# РЕКОНСТРУКЦІЯ 1-СЕКУНДНОГО СИГНАЛУ
# ============================================================

print("\n======================================")
print("РЕКОНСТРУКЦІЯ СИГНАЛУ")
print("======================================")

# ============================================================
# НОВА ОДНОСЕКУНДНА ШКАЛА ЧАСУ
# ============================================================

time_dense = np.arange(
    int(time_real.min()),
    int(time_real.max()) + 1,
    1
)

# ============================================================
# CUBIC SPLINE
# ============================================================

spline = CubicSpline(
    time_real,
    signal_real
)

signal_spline = spline(time_dense)

# ============================================================
# PID-INSPIRED RECONSTRUCTION
# ============================================================

Kp = 0.15
Kd = 0.04

signal_reconstructed = np.zeros_like(signal_spline)

signal_reconstructed[0] = signal_spline[0]

prev_error = 0

for i in range(1, len(signal_spline)):

    target = signal_spline[i]

    current = signal_reconstructed[i - 1]

    error = target - current

    derivative = error - prev_error

    update = Kp * error + Kd * derivative

    signal_reconstructed[i] = current + update

    # ========================================================
    # ФІЗИЧНЕ ОБМЕЖЕННЯ
    # ========================================================

    max_delta = 0.8

    delta = (
        signal_reconstructed[i]
        -
        signal_reconstructed[i - 1]
    )

    if abs(delta) > max_delta:

        signal_reconstructed[i] = (
            signal_reconstructed[i - 1]
            +
            np.sign(delta) * max_delta
        )

    prev_error = error

# ============================================================
# ДОДАТКОВЕ ЗГЛАДЖУВАННЯ
# ============================================================

signal_reconstructed = (
    pd.Series(signal_reconstructed)
    .rolling(window=5, center=True)
    .mean()
    .bfill()
    .ffill()
    .values
)

# ============================================================
# ПЕРЕВІРКА ДОВЖИНИ
# ============================================================

print("Кількість reconstructed точок:",
      len(signal_reconstructed))

print("Кількість time_dense:",
      len(time_dense))

# ============================================================
# ІН'ЄКЦІЯ АНОМАЛІЙ
# ============================================================

print("\n======================================")
print("ІН'ЄКЦІЯ АНОМАЛІЙ")
print("======================================")

signal_anomaly = signal_reconstructed.copy()

# ============================================================
# TRUE LABELS
# ============================================================

y_true = np.zeros(len(signal_anomaly))

# ============================================================
# БЕЗПЕЧНІ МЕЖІ
# ============================================================

N = len(signal_anomaly)

# ============================================================
# DRIFT INJECTION
# ============================================================

drift_start = int(N * 0.30)

drift_end = int(N * 0.55)

for i in range(drift_start, drift_end):

    signal_anomaly[i] += (
        0.01 * (i - drift_start)
    )

    y_true[i] = 1

# ============================================================
# LEAKAGE INJECTION
# ============================================================

leak_start = int(N * 0.65)

leak_end = int(N * 0.80)

signal_anomaly[leak_start:leak_end] *= 0.96

y_true[leak_start:leak_end] = 1

# ============================================================
# NOISE BURST
# ============================================================

noise_start = int(N * 0.82)

noise_end = int(N * 0.90)

noise = np.random.normal(
    0,
    1.5,
    noise_end - noise_start
)

signal_anomaly[noise_start:noise_end] += noise

y_true[noise_start:noise_end] = 1

# ============================================================
# ПІДГОТОВКА ДАНИХ
# ============================================================

X = signal_anomaly.reshape(-1, 1)

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# ============================================================
# ============================================================
# MODEL 1 — ISOLATION FOREST
# ============================================================
# ============================================================

print("\nIsolation Forest...")

iforest = IsolationForest(
    contamination=0.15,
    random_state=42
)

iforest.fit(X_scaled)

scores_iforest = -iforest.decision_function(X_scaled)

pred_iforest = (
    iforest.predict(X_scaled) == -1
).astype(int)

# ============================================================
# ============================================================
# MODEL 2 — DBSCAN
# ============================================================
# ============================================================

print("DBSCAN...")

dbscan = DBSCAN(
    eps=0.6,
    min_samples=8
)

clusters = dbscan.fit_predict(X_scaled)

pred_dbscan = (
    clusters == -1
).astype(int)

scores_dbscan = pred_dbscan.astype(float)

# ============================================================
# ============================================================
# MODEL 3 — AUTOENCODER (MLP)
# ============================================================
# ============================================================

print("Autoencoder...")

autoencoder = MLPRegressor(
    hidden_layer_sizes=(16, 8, 16),
    max_iter=400,
    random_state=42
)

autoencoder.fit(X_scaled, X_scaled.ravel())

reconstructed = autoencoder.predict(X_scaled)

reconstruction_error = np.abs(
    X_scaled.ravel() - reconstructed
)

threshold_ae = np.percentile(
    reconstruction_error,
    85
)

pred_ae = (
    reconstruction_error > threshold_ae
).astype(int)

# ============================================================
# ============================================================
# MODEL 4 — KALMAN-LIKE
# ============================================================
# ============================================================

print("Kalman-like filter...")

rolling_mean = (
    pd.Series(signal_anomaly)
    .rolling(window=15)
    .mean()
    .bfill()
)

kalman_error = np.abs(
    signal_anomaly - rolling_mean
)

threshold_kalman = np.percentile(
    kalman_error,
    85
)

pred_kalman = (
    kalman_error > threshold_kalman
).astype(int)

# ============================================================
# ============================================================
# MODEL 5 — DOUBLE CONTROL
# ============================================================
# ============================================================

print("Double Control...")

gradient = np.gradient(signal_anomaly)

physical_balance = np.abs(gradient)

dc_score = (
    reconstruction_error
    +
    0.7 * physical_balance
)

threshold_dc = np.percentile(
    dc_score,
    85
)

pred_dc = (
    dc_score > threshold_dc
).astype(int)

# ============================================================
# ФУНКЦІЯ ОЦІНКИ
# ============================================================

def evaluate_model(
    name,
    y_true,
    y_pred,
    scores
):

    return {

        "Model": name,

        "ROC_AUC": roc_auc_score(
            y_true,
            scores
        ),

        "Precision": precision_score(
            y_true,
            y_pred,
            zero_division=0
        ),

        "Recall": recall_score(
            y_true,
            y_pred,
            zero_division=0
        ),

        "F1": f1_score(
            y_true,
            y_pred,
            zero_division=0
        )
    }

# ============================================================
# ФОРМУВАННЯ ТАБЛИЦІ
# ============================================================

results = []

results.append(
    evaluate_model(
        "Autoencoder",
        y_true,
        pred_ae,
        reconstruction_error
    )
)

results.append(
    evaluate_model(
        "DBSCAN",
        y_true,
        pred_dbscan,
        scores_dbscan
    )
)

results.append(
    evaluate_model(
        "IsolationForest",
        y_true,
        pred_iforest,
        scores_iforest
    )
)

results.append(
    evaluate_model(
        "Kalman",
        y_true,
        pred_kalman,
        kalman_error
    )
)

results.append(
    evaluate_model(
        "DoubleControl",
        y_true,
        pred_dc,
        dc_score
    )
)

# ============================================================
# DATAFRAME
# ============================================================

results_df = pd.DataFrame(results)

print("\n======================================")
print("РЕЗУЛЬТАТИ")
print("======================================")

print(results_df)

# ============================================================
# ЗБЕРЕЖЕННЯ ТАБЛИЦІ
# ============================================================

results_df.to_csv(
    "data/results/model_comparison.csv",
    index=False
)

# ============================================================
# ПОБУДОВА ROC-КРИВИХ
# ============================================================

print("\n======================================")
print("ПОБУДОВА ROC")
print("======================================")

plt.figure(figsize=(10, 8))

# ============================================================
# ROC FUNCTION
# ============================================================

def plot_roc(y_true, scores, label):

    fpr, tpr, _ = roc_curve(
        y_true,
        scores
    )

    auc = roc_auc_score(
        y_true,
        scores
    )

    plt.plot(
        fpr,
        tpr,
        linewidth=2,
        label=f"{label} AUC={auc:.3f}"
    )

# ============================================================
# ROC CURVES
# ============================================================

plot_roc(
    y_true,
    reconstruction_error,
    "Autoencoder"
)

plot_roc(
    y_true,
    scores_dbscan,
    "DBSCAN"
)

plot_roc(
    y_true,
    scores_iforest,
    "IsolationForest"
)

plot_roc(
    y_true,
    kalman_error,
    "Kalman"
)

plot_roc(
    y_true,
    dc_score,
    "DoubleControl"
)

# ============================================================
# ДІАГОНАЛЬ ВИПАДКОВОГО КЛАСИФІКАТОРА
# ============================================================

plt.plot(
    [0, 1],
    [0, 1],
    linestyle='--'
)

plt.xlabel("False Positive Rate")

plt.ylabel("True Positive Rate")

plt.title(
    "ROC-криві алгоритмів виявлення аномалій"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

# ============================================================
# ЗБЕРЕЖЕННЯ ROC
# ============================================================

plt.savefig(
    "data/plots/roc_curves.png",
    dpi=300
)

# ============================================================
# ГРАФІК СИГНАЛІВ
# ============================================================

plt.figure(figsize=(14, 6))

plt.plot(
    time_dense,
    signal_reconstructed,
    linewidth=2,
    label="Нормальний сигнал"
)

plt.plot(
    time_dense,
    signal_anomaly,
    linewidth=2,
    label="Сигнал з аномаліями"
)

plt.xlabel("Час")

plt.ylabel("Витрата газу")

plt.title(
    "Physics-informed anomaly injection"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

# ============================================================
# ЗБЕРЕЖЕННЯ SIGNAL PLOT
# ============================================================

plt.savefig(
    "data/plots/anomaly_signal.png",
    dpi=300
)

# ============================================================
# ЗБЕРЕЖЕННЯ DATASET
# ============================================================

dataset_df = pd.DataFrame({

    "time": time_dense,

    "signal_normal": signal_reconstructed,

    "signal_anomaly": signal_anomaly,

    "label": y_true
})

dataset_df.to_csv(
    "data/results/benchmark_dataset.csv",
    index=False
)

# ============================================================
# ФІНАЛ
# ============================================================

print("\n======================================")
print("РОБОТА ЗАВЕРШЕНА")
print("======================================")

print("\nФайли збережено:")

print(
    "\ndata/results/model_comparison.csv"
)

print(
    "data/results/benchmark_dataset.csv"
)

print(
    "data/plots/roc_curves.png"
)

print(
    "data/plots/anomaly_signal.png"
)

print("\n======================================")