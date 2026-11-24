import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from pathlib import Path

# Resolve the data file relative to this script, independent of the terminal's
# current working directory.
mat_file = Path(__file__).resolve().parent / "MSD2026_Signals_for_CLSysID.mat"
data = scipy.io.loadmat(mat_file)
print(data.keys())
r= data['r']
y= data['y']
print(r.shape)
plt.figure()
plt.plot(r, label='refrence signaal') 
plt.plot(y, label='uitgangssignaal')
plt.ylabel('amplitude')
plt.xlabel('tijd')
plt.legend()
plt.show()