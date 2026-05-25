import numpy as np
from src.gas_quality.reconstruction import reconstruct_signal


def test_reconstruct_basic():
    time = np.array([0, 10, 20])
    signal = np.array([100.0, 110.0, 108.0])
    t_dense, recon = reconstruct_signal(time, signal)
    assert len(t_dense) == (int(t_dense[-1]) - int(t_dense[0]) + 1)
    assert recon.shape[0] == t_dense.shape[0]
    assert np.isfinite(recon).all()
