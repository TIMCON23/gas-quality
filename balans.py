import pandas as pd
import matplotlib.pyplot as plt

# ============================================
# 1. Завантаження даних
# ============================================

# Вкажіть шлях до вашого CSV файлу
file_path = "data/raw/metrological_data.csv"

df = pd.read_csv(file_path)

# Якщо timestamp є текстом — перетворюємо
df["timestamp"] = pd.to_datetime(df["timestamp"])

# ============================================
# 2. Якщо balance_error ще не розрахований
# ============================================

# Формула:
# εB = Qin - (Qout + Qcons + ΔQacc)

if "balance_error" not in df.columns:
    df["balance_error"] = (
        df["Qin"]
        - (
            df["Qout"]
            + df["Qcons"]
            + df["Qacc"]
        )
    )

# ============================================
# 3. Поріг аномалії
# ============================================

threshold = df["balance_error"].mean() + 3 * df["balance_error"].std()

# ============================================
# 4. Побудова графіка
# ============================================

plt.figure(figsize=(14, 6))

plt.plot(
    df["timestamp"],
    df["balance_error"],
    label="Різниця балансів εB(t)"
)

plt.axhline(
    threshold,
    linestyle="--",
    label="Поріг аномалії"
)

plt.axhline(
    -threshold,
    linestyle="--"
)

plt.title("Аналіз сталості балансу вузла обліку газу")
plt.xlabel("Час")
plt.ylabel("εB(t)")
plt.legend()
plt.grid(True)

plt.tight_layout()

# Збереження
import os
os.makedirs('data/plots', exist_ok=True)
plt.savefig("data/plots/balance_error.png", dpi=300)

# Показ
plt.show()