import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score, precision_score, recall_score, f1_score

# Завантаження
df = pd.read_csv("metrological_data.csv")

# Метрики
metrics = df.groupby("model").apply(lambda x: pd.Series({
    "ROC_AUC": roc_auc_score(x["y_true"], x["score"]),
    "Precision": precision_score(x["y_true"], x["pred"]),
    "Recall": recall_score(x["y_true"], x["pred"]),
    "F1": f1_score(x["y_true"], x["pred"])
}))

print(metrics)

# Таблиця
metrics.to_csv("comparison_table.csv")

# Графік
metrics["ROC_AUC"].sort_values().plot(kind="bar")
plt.ylabel("ROC-AUC")
plt.title("Порівняння моделей")
plt.tight_layout()
plt.savefig("roc_auc_comparison.png")
plt.show()