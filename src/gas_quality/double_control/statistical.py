import numpy as np


def statistical_control(signal, reconstructed, **kwargs):
    # simple reconstruction error based score
    recon_err = np.abs(reconstructed - signal[: len(reconstructed)])
    score = recon_err
    return score
