"""Generate synthetic but realistic metrological data for testing."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_metrological_data(days=7, output_dir="data/raw"):
    """Generate realistic gas meter data with balance sheet."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    timestamps = []
    flows = []
    pressures = []
    temps = []
    qins = []
    qouts = []
    qconss = []
    qaccs = []
    
    start_time = datetime(2026, 5, 1, 0, 0, 0)
    
    # 15-second intervals
    for minute in range(days * 24 * 60):
        ts = start_time + timedelta(minutes=minute)
        
        # Daily pattern + noise
        hour_of_day = ts.hour + ts.minute / 60.0
        base_flow = 100 + 30 * np.sin(2 * np.pi * hour_of_day / 24) + np.random.normal(0, 3)
        
        # Add anomaly windows
        minute_of_analysis = minute
        if 2000 <= minute_of_analysis <= 2500:  # drift
            base_flow += 0.01 * (minute_of_analysis - 2000)
        if 5000 <= minute_of_analysis <= 5500:  # leak
            base_flow *= 0.95
        if 7000 <= minute_of_analysis <= 7200:  # spike
            base_flow += np.random.choice([0, 25], p=[0.95, 0.05])
        
        # Correlated measurements
        pressure = 410 - 0.05 * base_flow + np.random.normal(0, 1)
        temp = 15 + 8 * np.sin(2 * np.pi * hour_of_day / 24) + np.random.normal(0, 0.5)
        
        # Balance components (illustrative)
        qin = base_flow
        qout = base_flow * 0.35 + np.random.normal(0, 2)
        qcons = base_flow * 0.35 + np.random.normal(0, 2)
        qacc = base_flow * 0.30 + np.random.normal(0, 1)
        
        timestamps.append(ts)
        flows.append(max(0, base_flow))
        pressures.append(max(300, pressure))
        temps.append(temp)
        qins.append(max(0, qin))
        qouts.append(max(0, qout))
        qconss.append(max(0, qcons))
        qaccs.append(max(0, qacc))
    
    df = pd.DataFrame({
        "timestamp": timestamps,
        "flow_m3h": flows,
        "pressure_kpa": pressures,
        "temp_c": temps,
        "Qin": qins,
        "Qout": qouts,
        "Qcons": qconss,
        "Qacc": qaccs,
    })
    
    # Save
    output_file = Path(output_dir) / "metrological_data.csv"
    df.to_csv(output_file, index=False)
    print(f"✓ Generated {len(df)} metrological records: {output_file}")
    
    return df


def generate_reconstruction_data(days=7, output_dir="data/raw"):
    """Generate reconstruction test data (15-second intervals)."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    times = []
    blacks = []
    grays = []
    
    t = 15
    for _ in range(days * 24 * 4 * 60):  # every 15 sec
        base = 2085 + 10 * np.sin(2 * np.pi * (t % 86400) / 86400) + np.random.normal(0, 1)
        times.append(t)
        blacks.append(base)
        grays.append(base + np.random.normal(0, 0.5))
        t += 15
    
    df = pd.DataFrame({"time": times, "black": blacks, "gray": grays})
    output_file = Path(output_dir) / "rec_date.csv"
    df.to_csv(output_file, index=False)
    print(f"✓ Generated {len(df)} reconstruction records: {output_file}")
    
    return df


if __name__ == "__main__":
    print("Generating synthetic metrological data...\n")
    generate_metrological_data()
    generate_reconstruction_data()
    print("\n✓ All data ready for analysis!")
