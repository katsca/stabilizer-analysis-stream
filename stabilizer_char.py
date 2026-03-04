import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import welch


def load_data(path):
    return pd.read_csv(path)

paths = ["data/adc_capture_10to5packets_noCS.csv", "data/adc_capture_10to5packets_CS_Voff036_noPSU.csv", "data/PI/adc_capture_10to5packets_CS_Voff077_PSU_KP0_KI0.csv", "data/PI/adc_capture_10to5packets_CS_Voff077_PSU_KP6_KI0.csv", "data/PI/adc_capture_10to5packets_CS_Voff077_PSU_KP1_KI0001.csv", "data/PI/adc_capture_10to5packets_CS_Voff077_PSU_KP12_KI20.csv"]
plt.figure(figsize=(8,5))
for path in paths:

    data = load_data(path)
    t = data["time"].values
    adc = data["adc"].values

    # ---- Sampling frequency ----
    dt = np.mean(np.diff(t))
    fs = 1.0 / dt
    print(f"Sampling rate: {fs:.2f} Hz")

    # ---- Remove DC offset ----
    adc = adc - np.mean(adc)

    # ---- Compute PSD using Welch ----
    f, Pxx = welch(
        adc,
        fs=fs,
        window="hann",
        nperseg= 2**18,
        scaling="density"
    )
    
    # ---- Convert to Amplitude Spectral Density ----
    ASD = np.sqrt(Pxx)
    ASD_dB = 20 * np.log10(ASD)
    plt.semilogx(f, ASD_dB)
    # ---- Plot ----
    #plt.loglog(f, ASD)
    

plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude Spectral Density (dBV / √Hz)")
plt.title("Noise Spectral Density")
plt.grid(True, which="both")
# plt.xlim((0,10**4))
plt.legend(["Noise Floor Stabilizer", "Noise Floor Stabilizer + Current Sense", "I=0.08A, no FB, Voff = 0.77V", "FB (Kp, Ki) = (6,0)", "FB (Kp, Ki) = (1,0.001)", "FB (Kp, Ki) = (12,20)"])
plt.show()