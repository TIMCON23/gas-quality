from .statistical import statistical_control
from .physical import physical_control

def double_control(signal, reconstructed, df=None, **kwargs):
    s_score = statistical_control(signal, reconstructed, **kwargs)
    p_score = physical_control(df, **kwargs) if df is not None else None
    return s_score, p_score
