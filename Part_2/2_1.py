import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

#plant data
data = pd.read_csv("MSD2026_Plant_Coefficients.csv")

#numerator and denominator from plant coefficients
num = data["numerator"].to_numpy(dtype=float)
den = data["denominator"].to_numpy(dtype=float)

#Input delay and sample time extraction
Td = data["input_delay_s"].iloc[0]
Ts = data["sample_time_s"].iloc[0]

#transferfunction
P = signal.TransferFunction(num, den)

#Frequency response
# Frequency range in Hz
f = np.logspace(0, 4, 3000)

# Convert Hz to rad/s
w = 2 * np.pi * f

# Calculate frequency response without delay
w, H = signal.freqresp(P, w=w)

# Include the exact input delay
delay = np.exp(-1j * w * Td)
H_total = H * delay

# Calculate magnitude in dB
magnitude = 20 * np.log10(np.abs(H_total))

# Calculate phase in degrees
phase = np.unwrap(np.angle(H_total)) * 180 / np.pi


# ============================================================
# 4. PLOT BODE DIAGRAM
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    2, 1,
    figsize=(10, 8),
    sharex=True
)

# Magnitude
ax1.semilogx(f, magnitude, linewidth=1.5)
ax1.set_ylabel("Magnitude [dB]")
ax1.set_title("Bode Plot – Design Plant")
ax1.grid(True, which="both", linestyle="--", alpha=0.5)

# Phase
ax2.semilogx(f, phase, linewidth=1.5)
ax2.set_xlabel("Frequency [Hz]")
ax2.set_ylabel("Phase [degrees]")
ax2.grid(True, which="both", linestyle="--", alpha=0.5)

plt.tight_layout()

# Save figure
plt.savefig("Bode_Plant_Q2_1.png", dpi=300)

plt.show()