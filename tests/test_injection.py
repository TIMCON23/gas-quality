import numpy as np
from src.gas_quality.anomalies.injection import inject_anomalies


def test_injection_labels_length():
    s = np.ones(200)
    s2, labels = inject_anomalies(s)
    assert len(s2) == len(s)
    assert len(labels) == len(s)
    assert labels.sum() > 0
