import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def main():
	data_file = Path(__file__).with_name("plant_response.csv")
	if not data_file.exists():
		raise FileNotFoundError(
			f"Missing {data_file.name}. Supply measured frequency_hz, magnitude_db, "
			"and phase_deg columns; a plant model or measurements are needed to plot its response."
		)

	with data_file.open(newline="", encoding="utf-8-sig") as file:
		rows = list(csv.DictReader(file))
	frequency = np.array([float(row["frequency_hz"]) for row in rows])
	magnitude = np.array([float(row["magnitude_db"]) for row in rows])
	phase = np.array([float(row["phase_deg"]) for row in rows])
	order = np.argsort(frequency)
	frequency, magnitude, phase = frequency[order], magnitude[order], phase[order]
	if len(frequency) < 2 or np.any(frequency <= 0):
		raise ValueError("Data must contain at least two positive frequency samples.")

	fig, (mag_ax, phase_ax) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
	mag_ax.semilogx(frequency, magnitude, "o-")
	mag_ax.set_ylabel("Magnitude (dB)")
	mag_ax.set_title("Plant frequency response")
	mag_ax.grid(True, which="both")
	phase_ax.semilogx(frequency, phase, "o-")
	phase_ax.set_xlabel("Frequency (Hz)")
	phase_ax.set_ylabel("Phase (degrees)")
	phase_ax.grid(True, which="both")
	fig.tight_layout()

	# Estimate the common low-pass bandwidth metric: the first -3 dB crossing.
	target = magnitude[0] - 3.0
	crossings = np.flatnonzero(magnitude[1:] <= target)
	if crossings.size:
		i = crossings[0] + 1
		fraction = (target - magnitude[i - 1]) / (magnitude[i] - magnitude[i - 1])
		bandwidth = frequency[i - 1] + fraction * (frequency[i] - frequency[i - 1])
		print(f"Approximate -3 dB bandwidth: {bandwidth:.4g} Hz")
		print("Gain roll-off and phase lag constrain usable bandwidth; avoid operating near strong resonances.")
	else:
		print("No -3 dB crossing is present in the measured range; bandwidth is not determined.")

	peaks = np.flatnonzero(
		(magnitude[1:-1] > magnitude[:-2]) & (magnitude[1:-1] >= magnitude[2:])
	) + 1
	if peaks.size:
		peak = peaks[np.argmax(magnitude[peaks])]
		print(f"Largest local peak: {frequency[peak]:.4g} Hz ({magnitude[peak]:.2f} dB).")
		print("A narrow peak with rapid phase change often suggests a lightly damped mechanical mode,"
			  " such as shaft/load flexibility or mounting resonance.")
	else:
		print("No distinct resonance peak is resolved in the data.")
	print("High-frequency roll-off/phase lag can arise from inertia and damping, actuator or electrical poles,"
		  " and sensor limits. Without the plant details, these causes cannot be distinguished from the plot alone.")
	plt.show()


if __name__ == "__main__":
	main()
