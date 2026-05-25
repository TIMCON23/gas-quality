import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline


def reconstruct_signal(time, signal, kp=0.15, kd=0.04, max_delta=0.8):
    time = np.array(time)
    signal = np.array(signal)
    # dense time
    t0 = int(np.min(time))
    t1 = int(np.max(time))
    time_dense = np.arange(t0, t1 + 1, 1)
    spline = CubicSpline(time, signal)
    signal_spline = spline(time_dense)

    # PID-inspired reconstruction
    recon = np.zeros_like(signal_spline)
    recon[0] = signal_spline[0]
    prev_error = 0
    for i in range(1, len(signal_spline)):
        target = signal_spline[i]
        current = recon[i - 1]
        error = target - current
        derivative = error - prev_error
        update = kp * error + kd * derivative
        recon[i] = current + update
        delta = recon[i] - recon[i - 1]
        if abs(delta) > max_delta:
            recon[i] = recon[i - 1] + np.sign(delta) * max_delta
        prev_error = error

    recon = pd.Series(recon).rolling(window=5, center=True).mean().bfill().ffill().values

    return time_dense, recon
