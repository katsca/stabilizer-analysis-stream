import matplotlib.pyplot as plt
import pandas as pd
CH1_SCALE = 2.50      # V per division
CH2_SCALE = 0.100     # V per division (100 mV)
CH2_OFFSET = 264*10**(-3)

# Want to extract the data appropriately

# DATA IS OF FORMAT X | CH1 | CH2 in s | V | V
ROOT = "./data/feedforward_data/"

def load_units(path):
    df = pd.read_csv(path, nrows=1, skiprows=1)
    return df.iloc[0].to_dict()

def load_data(path):
    df = pd.read_csv(path, skiprows=[1])
    return df.apply(pd.to_numeric)
files = ["newFile0c1.csv"]

units = load_units(ROOT + files[0])
df = load_data(ROOT + files[0])
time = df["X"]
df["CH1"] = df["CH1"] / CH1_SCALE
df["CH2"] = (df["CH2"] + CH2_OFFSET) /  CH2_SCALE
t = [-0.5531, 0.0]
df_win = df[(df["X"] >= t[0]) & (df["X"] <= t[1])]


plt.figure(figsize=(6,6))
plt.plot(df_win["CH1"], df_win["CH2"])
plt.xlabel("CH1")
plt.ylabel("CH2")
plt.grid(True)
plt.show()