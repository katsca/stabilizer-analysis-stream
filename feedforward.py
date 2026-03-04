import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

# DATA ROOT PATH

ROOT = "./data/feedforward_data/"


CH1_SCALE = 2.50      # V per division
CH2_SCALE = 0.100     # V per division (100 mV)
CH2_OFFSET = 264*10**(-3)

# Want to extract the data appropriately

# DATA IS OF FORMAT X | CH1 | CH2 in s | V | V


def load_units(path):
    df = pd.read_csv(path, nrows=1, skiprows=1)
    return df.iloc[0].to_dict()

def load_data(path):
    df = pd.read_csv(path, skiprows=[1])
    return df.apply(pd.to_numeric)

files = ["newFile0c1.csv"]

units = load_units(ROOT + files[0])

fig, axes = plt.subplots(len(files), 1, figsize=(10,8), sharex=True)

if len(files) == 1:
    axes = [axes]

for ax, file in zip(axes, files):
    
    df = load_data(ROOT + file)
    time = df["X"]
    df["CH1"] = df["CH1"] / CH1_SCALE
    df["CH2"] = (df["CH2"] + CH2_OFFSET) /  CH2_SCALE
    t = [-0.5531, 0.0]
    df_win = df[(df["X"] >= t[0]) & (df["X"] <= t[1])]


    
    # CH1 (reference phase)
    axes[0].plot(df_win["X"], df_win["CH1"], color="black")
    axes[0].set_ylabel("CH1")
    axes[0].grid(True)

    # CH2 (response)
    axes[1].plot(df_win["X"], df_win["CH2"], color="red")
    axes[1].set_ylabel("CH2")
    axes[1].set_xlabel("Time (s)")
    axes[1].grid(True)

plt.tight_layout()
plt.show()
