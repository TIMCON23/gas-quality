import numpy as np


def inject_anomalies(signal):
    """Inject several types of physics-informed anomalies into a signal.
    Returns (signal_with_anomalies, labels)
    """
    s = signal.copy()
    N = len(s)
    labels = np.zeros(N, dtype=int)
    # drift
    ds = int(N * 0.30)
    de = int(N * 0.55)
    for i in range(ds, de):
        s[i] += 0.01 * (i - ds)
        labels[i] = 1
    # leakage
    ls = int(N * 0.65)
    le = int(N * 0.80)
    s[ls:le] *= 0.96
    labels[ls:le] = 1
    # noise burst
    ns = int(N * 0.82)
    ne = int(N * 0.90)
    s[ns:ne] += np.random.normal(0, 1.5, ne - ns)
    labels[ns:ne] = 1
    return s, labels
