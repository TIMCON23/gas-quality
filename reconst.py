import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ==================== ЗАВАНТАЖЕННЯ ДАНИХ З CSV ====================
import os
os.makedirs('data/raw', exist_ok=True)
os.makedirs('data/plots', exist_ok=True)
df = pd.read_csv('data/raw/rec_date.csv')

time = df['time']
black = df['black']
gray = df['gray']

print(f"Дані завантажено успішно! Кількість точок: {len(time)}")

# ==================== ПОБУДОВА ГРАФІКА ====================
plt.figure(figsize=(16, 9))

plt.plot(time, black, 'k-', linewidth=2.7, label='Чорна лінія')
plt.plot(time, gray, color='#555555', linewidth=2.3, label='Сіра лінія')

plt.title('Витрата природного газу (м³/год) ', fontsize=14, pad=20)
plt.xlabel('Час, с', fontsize=12)
plt.ylabel('Витрата, м³/год', fontsize=12)

plt.grid(True, linestyle='--', alpha=0.8)
plt.minorticks_on()
plt.grid(which='minor', linestyle=':', alpha=0.5)

plt.legend(fontsize=11, loc='upper right')
plt.ylim(2060, 2130)
plt.xlim(12, 288)

plt.xticks(np.arange(15, 290, 15))
plt.yticks(np.arange(2060, 2135, 10))

plt.tight_layout()
plt.savefig('data/plots/reconstruction_preview.png', dpi=300)
plt.show()