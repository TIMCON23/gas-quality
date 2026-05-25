import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score


def plot_roc(y_true, scores, label):
    fpr, tpr, _ = roc_curve(y_true, scores)
    auc = roc_auc_score(y_true, scores)
    plt.plot(fpr, tpr, linewidth=2, label=f"{label} AUC={auc:.3f}")
