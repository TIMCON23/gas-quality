import pandas as pd
import numpy as np
from src.gas_quality.double_control.physical import physical_control


def test_physical_control_balance():
    df = pd.DataFrame({
        "Qin": [10, 10, 10],
        "Qout": [3, 3, 3],
        "Qcons": [4, 4, 4],
        "Qacc": [2, 2, 1],
    })
    res = physical_control(df)
    assert len(res) == 3
    assert (res >= 0).all()
