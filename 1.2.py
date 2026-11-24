import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from pathlib import Path
# Resolve the data file relative to this script, independent of the terminal's
# current working directory.
mat_file = Path(__file__).resolve().parent / "MSD2026_Signals_for_CLSysID.mat"
data = scipy.io.loadmat(mat_file)
print(data.keys())
r = data['r'].ravel()
y = data['y'].ravel()

sample_tijd = 30e-6  
time = np.arange(r.size) * sample_tijd

print(r.shape)
plt.figure()
plt.plot(time, r, label='referentiesignaal')
plt.plot(time, y, label='uitgangssignaal')
plt.ylabel('amplitude')
plt.xlabel('tijd [s]')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure()
plt.plot(time, 5*r, label='referentiesignaal')
plt.plot(time, y, label='uitgangssignaal')
plt.ylabel('amplitude')
plt.xlabel('tijd [s]')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
